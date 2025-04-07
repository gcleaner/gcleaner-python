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
from gi.repository import Gtk, Gio, Gdk
from widgets.main_window import MainWindow
from widgets.about import About


logging.basicConfig(
    format="[%(levelname)s] %(name)s.%(funcName)s: %(message)s",
    encoding='utf-8', level=logging.WARNING
)


class GCleaner(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.gcleaner")
        self.window = None

    def do_activate(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('data/application.css')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        if not self.window:
            self.window = MainWindow(self)

        self.window.present()

    def about_callback(self, simple: Gio.SimpleAction, parameter=None):
        about = About(self.window)
        about.present()


if __name__ == "__main__":
    app = GCleaner()
    app.run()
