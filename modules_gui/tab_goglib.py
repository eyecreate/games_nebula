#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; -*-

import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository.GdkPixbuf import InterpType
import gettext

from modules.set_nebula_dir import set_nebula_dir
from modules.pygogdownloader import Pygogdownloader
from modules.gamesdb import GamesDB

nebula_dir = set_nebula_dir()

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

image_path_global = nebula_dir + '/images/goglib/'

# TODO Change to correct path
image_path_user = os.getenv('HOME') + '/.games_nebula/images/goglib/'

# TODO Move to config file
banners_scale = 0.5
DOWNLOAD_DIR = '/media/Hitachi/Distrib/Games/GOG/'

class TabGogLib:

    def create(self):

        self.pygogdownloader = Pygogdownloader()
        self.pygogdownloader.activate_gogapi()

        games_dict = self.pygogdownloader.get_games_data()
        games_list = sorted(games_dict)
        
        box_goglib = Gtk.Box(
                orientation = Gtk.Orientation.VERTICAL,
                homogeneous = False,
                name = 'tab_goglib',
        )
        
################################################################################

        box_filters = Gtk.Box(
                orientation = Gtk.Orientation.HORIZONTAL,
                homogeneous = False,
                margin_left = 10,
                margin_right = 10,
                margin_top = 10,
                margin_bottom = 10,
                spacing = 10
        )
        
        search_entry = Gtk.SearchEntry(
                placeholder_text = _("Search"),
                halign = Gtk.Align.FILL,
                sensitive = False # FIX
        )
        #~ search_entry.connect('search-changed', self.search_filter)
        
        combobox_filter_status = Gtk.ComboBoxText(
                tooltip_text = _("Status filter"),
                name = 'combobox_goglib_status',
                sensitive = False # FIX
        )

        status_list = [_("No filter"), _("Installed"), _("Unavailable")]

        for i in range(len(status_list)):
            combobox_filter_status.append_text(status_list[i])
            #~ if status_list[i] == self.status_filter:
                #~ combobox_filter_status.set_active(i)
        #~ combobox_filter_status.connect('changed', self.cb_combobox_filter_status)
        #~ combobox_filter_status.connect('button-press-event', self.cb2_comboboxes_filters)
        combobox_filter_status.set_active(0) # TODO Temp
        
        combobox_filter_tags1 = Gtk.ComboBoxText(
                tooltip_text = _("Tags filter 1"),
                name = 'combobox_filter_tags1',
                sensitive = False # FIX
        )
        combobox_filter_tags1.append_text(_("No filter"))
        combobox_filter_tags1.append_text(_("No tags"))
        combobox_filter_tags1.set_active(0) # TODO Temp
        
        img_add = Gtk.Image.new_from_icon_name("list-add", Gtk.IconSize.SMALL_TOOLBAR)
        button_filter_add = Gtk.Button(
                name = 'add',
                image = img_add,
                #~ no_show_all = True,
                tooltip_text = _("Add tags filter"),
                sensitive = False # FIX
        )
        #~ button_filter_add.connect('clicked', self.tag_filters_number_changed)
        
        #~ adjustment_scale_banner = Gtk.Adjustment(self.scale_level, 0.4, 1, 0.1, 0.3)
        adjustment_scale_banner = Gtk.Adjustment(banners_scale, 0.4, 1, 0.1, 0.3)
        #~ adjustment_scale_banner.connect('value-changed', self.cb_adjustment_scale_banner)
        adjustment_scale_banner.set_value(banners_scale)
        scale_banner = Gtk.Scale(
                tooltip_text = _("Scale"),
                orientation = Gtk.Orientation.HORIZONTAL,
                halign = Gtk.Align.END,
                valign = Gtk.Align.CENTER,
                width_request = 150,
                draw_value = False,
                show_fill_level = True,
                adjustment = adjustment_scale_banner,
                sensitive = False # FIX
        )
        
        box_filters.pack_start(search_entry, True, True, 0)
        box_filters.pack_start(combobox_filter_status, False, False, 0)
        box_filters.pack_start(combobox_filter_tags1, False, False, 0)
        box_filters.pack_start(button_filter_add, False, False, 0)
        box_filters.pack_start(scale_banner, False, False, 0)
        
################################################################################
        
        scrolled_window = Gtk.ScrolledWindow()

        flowbox = Gtk.FlowBox(
                max_children_per_line = 42,
                selection_mode = Gtk.SelectionMode.NONE,
                row_spacing = 20,
                column_spacing = 20,
                margin_left = 20,
                margin_right = 20,
                margin_top = 20,
                margin_bottom = 20
        )

        for game_name in games_list:

            game_grid = Gtk.Grid(
                    can_focus=False,
                    column_homogeneous = True
            )

            image_path_0 = image_path_global + game_name + '.jpg'
            image_path_1 = image_path_user + game_name + '.jpg'
            if os.path.exists(image_path_1):
                image_path = image_path_1
            elif os.path.exists(image_path_0):
                image_path = image_path_0
            else:
                # Download or create image
                pass

            pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)

            pixbuf = pixbuf.scale_simple(518 * banners_scale,
                                        240 * banners_scale,
                                        InterpType.BILINEAR
            )

            game_image = Gtk.Image(
                    name = game_name,
                    tooltip_text = games_dict[game_name][1],
                    pixbuf = pixbuf
            )

            button_setup = Gtk.Button(
                    name = game_name,
                    label = "Install"
            )
            button_setup.connect('clicked', self.button_setup_clicked)

            button_play = Gtk.Button(
                    name = game_name,
                    label = "Play",
                    sensitive = False
            )

            game_grid.attach(game_image, 0, 0, 2, 1)
            game_grid.attach(button_setup, 0, 1, 1, 1)
            game_grid.attach(button_play, 1, 1, 1, 1)

            flowbox_child = Gtk.FlowBoxChild(halign=Gtk.Align.CENTER)
            flowbox_child.add(game_grid)
            flowbox.add(flowbox_child)
            
################################################################################
        
        scrolled_window.add(flowbox)
        
        box_goglib.pack_start(box_filters, False, False, 0)
        box_goglib.pack_start(scrolled_window, True, True, 0)

        return box_goglib

    def button_setup_clicked(self, button):

        button.set_label("Installing")
        button.set_sensitive(False)
        game_name = button.get_name()
        print(game_name)

        #~ self.pygogdownloader.download(game_name, 'en', DOWNLOAD_DIR)
