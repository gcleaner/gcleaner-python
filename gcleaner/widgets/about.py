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
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from constants import Constants


class About(Gtk.AboutDialog):
    def __init__(self, parent):
        super().__init__()

        # Constructor Variables
        self.set_transient_for(parent)  # associates dialog to main window
        self.set_modal(True)  # makes dialog modal
        self.set_program_name(Constants.APP_NAME)
        self.set_version(Constants.VERSION)
        self.set_comments(Constants.COMMENTS)
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_wrap_license(True)
        self.set_website(Constants.WEBSITE)
        self.set_authors(Constants.AUTHORS)
        self.set_copyright(Constants.COPYRIGHT)
        self.set_logo_icon_name("gcleaner")

        # Apply dark mode to the About dialog
        self.get_style_context().add_class("dark")

    def on_response(self, action, parameter):
        action.destroy()
