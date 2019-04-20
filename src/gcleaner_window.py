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
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, Gdk
from constants import Constants
from widgets.header_bar import HeaderBarOfWindow
from widgets.toolbar import ToolbarOfWindow
from widgets.sidebar import Sidebar


class GCleaner(Gtk.ApplicationWindow):

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Settings for save the GCleaner state
        self.__settings = Gio.Settings("org.gcleaner")

        """Boolean value that determines if use or not
        use HeaderBar according to the desktop environment"""
        self.__use_headerbar = False

        # MAIN WINDOW PROPERTIES
        self.move(self.__settings.get_int("opening-x"),
                  self.__settings.get_int("opening-y"))
        self.set_default_size(self.__settings.get_int("window-width"),
                              self.__settings.get_int("window-height"))
        self.set_title(Constants.PROGRAM_NAME)
        #self.set_application(self)

        # Application icon
        self.props.icon_name = "gcleaner"

        # BOXES
        # Box that will contain the rest of the boxes (this is adjusted to the window)
        self.__main_window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # Box containing the Sidebar, the separator and the remaining box info_action_box
        self.__content_box     = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # OWN WIDGETS
        self.__sidebar = Sidebar(self)
        self.__sidebar.get_style_context().add_class("Sidebar")

        """ This EventBox is created to color the
        background of the Box (Sidebar) in GTK+ <= 3.10 """
        self.__event_sidebar = Gtk.EventBox()
        self.__event_sidebar.add(self.__sidebar)
        self.__event_sidebar.get_style_context().add_class("SidebarEv")
        # The color is created in RGBA
        self.__colour = Gdk.RGBA()
        self.__colour.parse("103,103,103,1.0")
        """ OLD METHOD
        self.__colour.porps.red = 103.0
        self.__colour.porps.green = 103.0
        self.__colour.porps.blue = 103.0
        """
        # Transparency
        self.__colour.alpha = 1.0
        self.__event_sidebar.override_background_color(Gtk.StateFlags.NORMAL, self.__colour)

        # PACKAGING
        """
            TOOLBAR and HEADERBAR
            Here the magic of the dynamic
             -- Checking Desktop Environment to use Header Bars
        """
        # Create string variable to store the desktop environment
        self.__desktop_environment = ""
        # We keep the value of the CURRENT_DESKTOP variable
        self.__desktop_environment = os.popen("env | grep XDG_CURRENT_DESKTOP").readlines()
        self.__desktop_environment_parts = self.__desktop_environment[0].split('=')
        self.__desktop_environment = self.__desktop_environment_parts[1]
        self.__desktop_environment = self.__desktop_environment.replace("\n", "")
        self.__desktop_environment = self.__desktop_environment.upper()
        print("ORG.GCLEANER.APP: [DESKTOP: %s]" % (self.__desktop_environment))

        """If Desktop is Pantheon Desktop (elementary OS) or
        GNOME Desktop, or Ubuntu... then use HeaderBar."""
        if (self.__desktop_environment == "PANTHEON" or
            self.__desktop_environment == "GNOME" or
            self.__desktop_environment == "UBUNTU:GNOME"):
            self.__use_headerbar = True
        else:
            # Any other Desktop like Unity, XFCE, Mate, etc... use ToolBar
            self.__use_headerbar = False

        #  Use HeaderBar or ToolBar?
        if self.__use_headerbar:
            """HeaderBar:
                Create an instance of the HeaderBar (customized)"""
            self.__header_bar = HeaderBarOfWindow(app)
            self.__header_bar.get_style_context().add_class("csd")
            self.set_titlebar(self.__header_bar)
            self.__header_bar.set_name("header_bar")
        else:
            """ ToolBar:
                 Creates an instance of the Toolbar (customized)"""
            self.__toolbar = ToolbarOfWindow(app)
            self.__toolbar.get_style_context().add_class("Toolbar")
            self.__toolbar.set_name("Toolbar")

            # Add the Toolbar to the 'main window box'
            self.__main_window_box.pack_start(self.__toolbar, False, True, 0)

        # Content Box
        self.__content_box.pack_start(self.__event_sidebar, False, True, 0)

        # Final assembly
        self.__main_window_box.pack_start(self.__content_box, True, True, 0)

        # ************ TEMPORARY, then erase ******************* #
        self.__user_home = os.popen("env | grep 'HOME='").readlines()
        self.__user_home_parts = self.__user_home[0].split('=')
        self.__user_home = self.__user_home_parts[1]
        self.__user_home = self.__user_home.replace("\n", "")
        print("ORG.GCLEANER.APP: [USUARIO: %s]" % (self.__user_home))

        # Add the 'main window box' to the main window (Gtk.Window)
        self.connect("delete_event", self.on_delete_event)
        self.add(self.__main_window_box)
        self.show_all()

    def on_delete_event(self, action, param):
        self.__x = self.get_position()[0]
        self.__y = self.get_position()[1]
        self.__width = self.get_size()[0]
        self.__height = self.get_size()[1]

        # Save values into GSCHEMA
        self.__settings.set_int("opening-x", self.__x)
        self.__settings.set_int("opening-y", self.__y)
        self.__settings.set_int("window-width", self.__width)
        self.__settings.set_int("window-height", self.__height)

        self.__settings.set_boolean("analyzechrome", self.__sidebar.check_chrome.get_active())
        self.__settings.set_boolean("analyzepapelera", self.__sidebar.check_trash.get_active())

    def get_settings(self):
        return self.__settings

