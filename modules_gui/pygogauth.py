import os
import sys
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2
from urllib.parse import urlparse
import gettext

from gogapi.token import Token, get_auth_url

from modules.set_nebula_dir import set_nebula_dir

nebula_dir = set_nebula_dir()

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

CONFIG_PATH = os.getenv('HOME') + '/.config/games_nebula/'

class PyGogAuth(Gtk.Dialog):

    def __init__(self):

        super(PyGogAuth, self).__init__()

        if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)

        self.token_path = CONFIG_PATH + '/token.json'

        self.connect('delete-event', self.cancel)

        app_icon = GdkPixbuf.Pixbuf.new_from_file(nebula_dir + '/images/icon.png')
        self.set_icon(app_icon)
        self.set_title("Games Nebula")

        content_area = self.get_content_area()
        content_area.set_property('orientation', Gtk.Orientation.HORIZONTAL)

        content_manager = self.new_content_manager()
        self.webpage = WebKit2.WebView(user_content_manager=content_manager)
        self.webpage.connect('load_changed', self.webpage_loaded)

        self.webpage.set_size_request(390, 496)

        self.webpage_color = Gdk.RGBA(
            red = 0.149019,
            green = 0.149019,
            blue = 0.149019,
            alpha = 1.0,
        )
        self.webpage.set_background_color(self.webpage_color)

        auth_url = get_auth_url()
        self.webpage.load_uri(auth_url)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(390, 496)

        self.scrolled_window.add(self.webpage)
        content_area.add(self.scrolled_window)
        self.show_all()

    def new_content_manager(self):

        css = """
        .icn--close {
            visibility: hidden;
        }
        button#continue_offline {
            visibility: hidden;
        }
        """
        content_injected_frames = WebKit2.UserContentInjectedFrames(0)
        user_style_level = WebKit2.UserStyleLevel(0)
        style_sheet = WebKit2.UserStyleSheet(css, content_injected_frames, user_style_level, None, None)

        content_manager = WebKit2.UserContentManager()
        content_manager.add_style_sheet(style_sheet)

        return content_manager

    def cancel(self, window, event):

        self.response(1)
        self.destroy()

    def webpage_loaded(self, webview, event):

        if event == WebKit2.LoadEvent.FINISHED:

            js_set_color = 'document.body.style.backgroundColor = "#262626"'
            webview.run_javascript(js_set_color, None, None, None)

        elif event == WebKit2.LoadEvent.REDIRECTED:

            url = webview.get_uri()
            url_path = urlparse(url).path
            url_query = urlparse(url).query

            if not url_path.startswith("/on_login_success"):
                return

            query_match = re.compile(r"code=([\w\-]+)").search(url_query)

            if query_match is not None:
                login_code = query_match.group(1)
                token = Token.from_code(login_code)
                token.save(self.token_path)
                print("Authorization successful!")
                self.response(0)
                self.destroy()
            else:

                message_dialog = Gtk.MessageDialog(
                    None,
                    0,
                    Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK,
                    _("Error")
                )
                message_dialog.format_secondary_text(_("Could not parse code from query: %s") % url_query)

                content_area = message_dialog.get_content_area()
                content_area.set_property('margin-left', 10)
                content_area.set_property('margin-right', 10)
                content_area.set_property('margin-top', 10)
                content_area.set_property('margin-bottom', 10)

                message_dialog.run()
                message_dialog.destroy()
                print("Authorization failed")
                self.response(1)
                self.destroy()
