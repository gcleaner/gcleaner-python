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


class About(Gtk.AboutDialog):

    def __init__(self):
        super().__init__()

        # Constructor Variables
        self.props.license = "This program is released under the terms of the GPL (General Public License) as published by the Free Software Foundation, is an application that will be useful, but WITHOUT ANY WARRANTY; for details, visit: http://www.gnu.org/licenses/gpl.html"
        self.set_wrap_license(True)

        try:
            self.__logo = GdkPixbuf.Pixbuf.new_from_file_at_size(
                "/usr/share/icons/hicolor/128x128/apps/gcleaner.svg", 128, 128)
            self.set_logo(self.__logo)
            self.__logo = None
        except Exception as err:
            print("ORG.GCLEANER.APP.ABOUT: [GLIB::ERROR CREATING Pixbuf ICON]")
            print(">>> Check path: /usr/share/icons/hicolor/128x128/apps/gcleaner.svg")

        self.props.program_name = Constants.PROGRAM_NAME
        self.props.version      = Constants.VERSION
        self.props.comments     = "Clean your System GNU/Linux"
        self.props.copyright	= ("Copyright © 2015-" +
                                   str(GLib.DateTime.new_now_local().get_year()) +
                                   " Juan Pablo Lozano")
        self.props.website      = "https://gcleaner.github.io/"

        self.connect("response", self.on_response)

        # Application icon
        try:
            self.props.icon = GdkPixbuf.Pixbuf.new_from_file(
                "/usr/share/icons/hicolor/128x128/apps/gcleaner.svg")
        except Exception as err:
            print("ORG.GCLEANER.APP.ABOUT: [GLIB::ERROR LOADING ICON")
            print(">>> " + str(err))

    def on_response(self, action, parameter):
        action.destroy()

