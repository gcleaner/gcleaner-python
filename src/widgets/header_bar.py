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
from library.specs import Specs


class HeaderBarOfWindow(Gtk.HeaderBar):

    def __init__(self, app):
        super().__init__() # Initialize is required for Gtk.HeaderBar class

        # Class Variables
        self.__app = app
        self.__complete_system_specs = ""

        # Render GCleaner Icon for HeaderBar
        self.__icon = Gtk.Image()

        try:
            self.__icon_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                                    "/usr/share/icons/hicolor/32x32/apps/gcleaner.svg",
                                    40,
                                    40,
                                    False)
            self.__icon.set_from_pixbuf(self.__icon_pixbuf)
        except Exception as err:
            print("ORG.GCLEANER.APP.HEADERBAR: [GDK::ERROR CREATING PIXBUF ICON]")
            print(">>> Check path: /usr/share/icons/hicolor/32x32/apps/gcleaner.svg")
            print(">>> Error Message: ", str(err))

        self.__complete_system_specs = (Specs().get_processor() + "  •  "
                                      + Specs().get_ram_memory() + " RAM  •  "
                                      + Specs().get_graphics())

        # LABELS WITH PANGO MARKUP
        self.__app_title = Gtk.Label("")
        self.__app_title.set_markup("<b>GCleaner</b>")

        self.__app_version = Gtk.Label("")
        self.__app_version.set_markup("<small>v" + Constants.VERSION + "</small>")

        self.__os_information = Gtk.Label("")
        #font_size='small' by default
        self.__os_information.set_markup("<span>" + Specs().get_os_information() + "</span>")

        self.__system_specs = Gtk.Label("")
        self.__system_specs.set_markup("<span font_size='small'>" + self.__complete_system_specs + "</span>")

        """
        Here, first we create an Image and then add
        this image to MenuButton and resize it.
        """
        self.__appmenu_button = Gtk.MenuButton()
        self.__gear_icon = Gtk.Image()
        self.__gear_icon.set_from_icon_name("open-menu", Gtk.IconSize.LARGE_TOOLBAR)
        self.__appmenu_button.set_image(self.__gear_icon)
        self.__appmenu_button.get_style_context().add_class("about_btn")

        """
        Here define an Menu Model and
        add it to appmenu Button.
        """
        self.__menu_model = Gio.Menu()
        self.__menu_model.append("About...", "app.about")
        self.__appmenu_button.set_menu_model(self.__menu_model)

        # Here we define the Actions
        self.__about_action = Gio.SimpleAction.new("about", None)
        self.__about_action.connect("activate", self.__app.about_callback)
        self.__app.add_action(self.__about_action)

        # BOXES
        # to assemble the header
        self.__container_box    = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.__name_version_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__specs_os_box     = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # boxes for elements
        self.__icon_box     = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__app_name_box	= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__version_box  = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__os_box       = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__specs_box    = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # PACKAGING
        # Packaging widgets
        self.__icon_box.pack_start(self.__icon, True, True, 0)
        self.__app_name_box.pack_start(self.__app_title, False, True, 0)
        self.__version_box.pack_start(self.__app_version, False, True, 0)
        self.__os_box.pack_start(self.__os_information, False, True, 0)
        self.__specs_box.pack_start(self.__system_specs, False, True, 0)

        # Packaging boxes
        self.__name_version_box.pack_start(self.__app_name_box, True, True, 0)
        self.__name_version_box.pack_start(self.__version_box, True, True, 0)
        self.__specs_os_box.pack_start(self.__os_box, True, True, 0)
        self.__specs_os_box.pack_start(self.__specs_box, True, True, 0)
        self.__container_box.pack_start(self.__icon_box, False, True, 6)
        self.__container_box.pack_start(self.__name_version_box, False, True, 6)
        self.__container_box.pack_start(self.__specs_os_box, False, True, 6)

        # Configure Vertical Align of Certain Boxes
        self.__specs_os_box.set_valign(Gtk.Align.FILL)
        self.__name_version_box.set_valign(Gtk.Align.FILL)
        self.__container_box.set_valign(Gtk.Align.FILL)

        self.__item = Gtk.ToolItem()
        self.__item.add(self.__container_box)

        # HeaderBar properties
        self.pack_start(self.__item)
        self.pack_end(self.__appmenu_button)
        self.set_show_close_button(True)

