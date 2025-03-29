"""
Copyright 2025 Juan Pablo Lozano

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
import logging
import gi
gi.require_version('Gtk', '4.0')
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gio
from constants import Constants


class Sidebar(Gtk.Box):

    # CHECK BUTTONS
    check_firefox = Gtk.CheckButton()
    check_trash = Gtk.CheckButton()

    def __init__(self, window):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.get_style_context().add_class("sidebar")

        # Constructor Variables
        self.app_main_window = window  # Needed to acces GLib settings

        # BOXES
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.apps_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.system_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        """
        Gtk.Fixed is a container (a kind of Gtk.Box) which can place other
        children Widgets in fixed positions and size in pixels.
        """
        self.fixed_box = Gtk.Fixed()
        self.fixed_box.put (self.main_box, 0, 0)
        self.fixed_box.set_vexpand(True)

        self.append(self.fixed_box)

        # LABELS
        self.category_apps_label = Gtk.Label()
        self.category_apps_label.set_markup("<b>APPLICATIONS</b>")

        self.category_system_label = Gtk.Label()
        self.category_system_label.set_markup("<b>SYSTEM</b>")

        # SEPARATORS
        self.category_separator = Gtk.Label.new("  ")

        # APPLICATIONS CHECKBOXS
        """           Firefox           """
        firefox_icon = Gtk.Image()
        firefox_icon.set_from_icon_name("firefox")
        firefox_icon.set_icon_size(Gtk.IconSize.NORMAL)
        firefox_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        firefox_label = Gtk.Label.new("Firefox")
        firefox_box.append(firefox_icon)
        firefox_box.append(firefox_label)
        self.check_firefox.set_child(firefox_box)

        # SYSTEM CHECKBOXS
        """           Trash           """
        trash_icon = Gtk.Image()
        trash_icon.set_from_icon_name("user-trash")
        trash_icon.set_icon_size(Gtk.IconSize.NORMAL)
        trash_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        trash_label = Gtk.Label.new("Trash")
        trash_box.append(trash_icon)
        trash_box.append(trash_label)
        self.check_trash.set_child(trash_box)

        # PACKAGING CHECKBOX
        self.apps_box.append(self.category_apps_label)
        self.system_box.append(self.category_system_label)

        self.main_box.append(self.apps_box)

        """ CHECK IF FIREFOX EXISTS AND ADD ITS CHECKBOX """
        self.firefox_file = Gio.File.new_for_path("/usr/bin/firefox")
        if self.firefox_file.query_exists():
            self.main_box.append(self.check_firefox)
            self.check_firefox.set_active(self.app_main_window.get_settings().get_boolean("scan-firefox"))

        self.main_box.append(self.category_separator)

        self.main_box.append(self.system_box)
        self.main_box.append(self.check_trash)

        # ACTIVATE REMAINING CHECKBOX
        self.check_trash.set_active(self.app_main_window.get_settings().get_boolean("scan-trash"))
