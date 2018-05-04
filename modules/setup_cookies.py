import os
import gi
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2

CONFIG_PATH = os.getenv('HOME') + '/.config/games_nebula/'

def setup_cookies():

    cookiejar_path = CONFIG_PATH + '/cookies.txt'
    cookies_dir = os.path.dirname(cookiejar_path)

    if not os.path.exists(cookies_dir):
        os.makedirs(cookies_dir)

    context = WebKit2.WebContext.get_default()
    cookie_manager = context.get_cookie_manager();
    cookie_manager.set_persistent_storage(cookiejar_path, WebKit2.CookiePersistentStorage.TEXT);
