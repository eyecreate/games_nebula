#!/usr/bin/env python
# -*- coding: utf-8; -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2
#~ import webbrowser

class TabGogCom:

    def create(self):

        self.webkit = WebKit2
        #~ self.webbrowser = webbrowser

        self.webpage = self.webkit.WebView()
        self.webpage.load_uri('https://www.gog.com')

        self.scrolled_window = Gtk.ScrolledWindow(
            name = 'gogcom_tab'
            )

        self.scrolled_window.add(self.webpage)
        #~ self.check_gogcom_tab()

        return self.scrolled_window
