"""
Copyright 2019 Juan Pablo Lozano

This file is part of GCleaner.

GCleaner is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

GCleaner is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with GCleaner. If not, see http://www.gnu.org/licenses/.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, Gio
from constants import Constants


class Sidebar(Gtk.Box):

    # CHECKBUTTONS
    check_trash = Gtk.CheckButton()
    check_chrome = Gtk.CheckButton()

    def __init__(self, app_win):
        super().__init__()

        # Constructor Variables
        self.__app_win = app_win

        # BOXES
        self.__sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__apps_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__system_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        """ Fixed is a container (a kind of BOX) which can place other
        Widgets children in fixed positions and size in pixels. """
        self.__fixed_box = Gtk.Fixed()
        self.__fixed_box.add (self.__sidebar_box)

        # Value specified in the HIG (Human Interface Guidelines) of Elementary OS
        self.__sidebar_box.set_border_width(12)
        # Only the Box is added where the Fixed (fixed_box) is adapted to the Box
        self.add(self.__fixed_box)

        # LABELS
        self.__category_apps_label = Gtk.Label("")
        self.__category_apps_label.set_markup("<b>APPLICATIONS</b>")

        self.__category_system_label = Gtk.Label("")
        self.__category_system_label.set_markup("<b>SYSTEM</b>")

        # SEPARATORS
        self.__category_separator = Gtk.Label("  ")

        # APPLICATIONS CHECKBOXS
        """ ******************** Google Chrome ******************** """
        chrome_icon = Gtk.Image()
        chrome_icon.set_from_icon_name("google-chrome", Gtk.IconSize.MENU)
        chrome_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        chrome_label = Gtk.Label("Google Chrome")
        chrome_box.pack_start(chrome_icon, False, False, 4)
        chrome_box.pack_start(chrome_label, False, False, 0)
        self.check_chrome.add(chrome_box)

        # SYSTEM CHECKBOXS
        """ ******************** Trash ******************** """
        trash_icon = Gtk.Image()
        trash_icon.set_from_icon_name("user-trash", Gtk.IconSize.MENU)
        trash_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        trash_label = Gtk.Label("Trash")
        trash_box.pack_start(trash_icon, False, False, 4)
        trash_box.pack_start(trash_label, False, False, 0)
        self.check_trash.add(trash_box)

        # PACKAGING CHECKBOX
        self.__apps_box.pack_start(self.__category_apps_label, False, True, 0)
        self.__system_box.pack_start(self.__category_system_label, False, True, 0)

        self.__sidebar_box.pack_start(self.__apps_box, False, True, 2)

        """ CHECK IF GOOGLE CHROME EXISTS AND ADD ITS CHECKBOX """
        self.__chrome_file = Gio.File.new_for_path("/usr/bin/google-chrome-stable")
        self.__chrome_file_alt = Gio.File.new_for_path("/usr/bin/google-chrome")
        if self.__chrome_file.query_exists() or self.__chrome_file_alt.query_exists():
            self.__sidebar_box.pack_start(self.check_chrome, True, True, 2)
            self.check_chrome.set_active(self.__app_win.get_settings().get_boolean("analyzechrome"))
        else:
            self.check_chrome.set_active(False)

        self.__sidebar_box.pack_start(self.__category_separator, True, True, 2)

        self.__sidebar_box.pack_start(self.__system_box, False, True, 2)
        self.__sidebar_box.pack_start(self.check_trash, True, True, 2)

        # ******************** ACTIVATE REMAINING CHECKBOX ********************
        self.check_trash.set_active(self.__app_win.get_settings().get_boolean("analyzepapelera"))

        # AND SHOW ALL CONTENT
        self.__sidebar_box.show_all()

