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
from gi.repository import Gtk, Gio, GdkPixbuf
from constants import Constants
from utils.specs import Specs


class ToolBar(Gtk.Box):
    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.get_style_context().add_class("toolbar")

        # LABELS
        # APP NAME AND VERSION
        """
        PANGO MARKUP FONT SIZEs:
            - xx-small
            - x-small
            - small
            - medium
            - large
            - x-large
            - xx-large
        More information in:
            https://developer.gnome.org/pango/stable/PangoMarkupFormat.html
        """
        self.title = Gtk.Label()
        self.title.set_markup(
            f"<span font_size='large'><b>{Constants.APP_NAME}</b></span>"
        )

        self.app_version = Gtk.Label()
        self.app_version.set_markup(
            f"<span font_size='small'> v{Constants.VERSION}</span>"
        )

        # Information of Operating System, RAM and Video
        self.information = Gtk.Label()
        self.information.set_markup(
            f"<span font_size='small'>{Specs().get_os_information()}</span>"
        )

        self.machine_specs = (
            f"{Specs().get_processor()}  •  "
            f"{Specs().get_ram_memory()} RAM  •  "
            f"{Specs().get_graphics()}"
        )

        self.specs = Gtk.Label()
        self.specs.set_markup(
            f"<span font_size='small'>{self.machine_specs}</span>"
        )

        # Filling spaces to visually accommodate some elements
        self.help_fill_1 = Gtk.Label()
        self.help_fill_2 = Gtk.Label()
        self.icon_fill = Gtk.Label()
        self.specs_fill = Gtk.Label()
        self.title_fill = Gtk.Label()
        self.help_fill_1.set_markup("<span font_size='large'>  </span>")
        self.help_fill_2.set_markup(" ")
        self.icon_fill.set_markup("<span font_size='xx-small'>  </span>")
        self.title_fill.set_markup("<span font_size='large'>  </span>")
        self.specs_fill.set_markup("<span font_size='x-large'>  </span>")

        # Menu
        # Option 1 (doesn't recognize dark mode)
        # self.menu_button = Gtk.MenuButton()
        # self.menu_button.set_icon_name("applications-system")
        # self.menu_button.set_size_request(32, 32)
        # Option 2
        self.menu_button = Gtk.MenuButton()
        self.gear_icon = Gtk.Image()
        try:
            self.gear_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                "data/media/settings-menu.svg", 32, 32, False
            )
            self.gear_icon.set_from_pixbuf(self.gear_pixbuf)
        except Exception as err:
            self.logger.warning("Error creating settings menu icon pixbuf")
        self.menu_button.set_child(self.gear_icon)
        self.menu_button.set_size_request(32, 32)

        self.menu_button.get_style_context().add_class("about-btn")

        # Here we define a Menu Model and add it to the appmenu Button
        self.menu_model = Gio.Menu()
        self.menu_model.append("About...", "app.about")
        self.menu_button.set_menu_model(self.menu_model)

        # Here we define the Actions
        self.about_action = Gio.SimpleAction.new("about", None)
        self.about_action.connect("activate", app.about_callback)
        app.add_action(self.about_action)

        # BOXES
        # For Icon
        self.icon_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.sub_icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # Name and Version
        self.app_name_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.app_title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app_version_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.sub_name_app_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # Operating System and System specs
        self.os_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.system_properties_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.specs_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.sub_specs_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # Help
        self.help_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.about_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # OTHERS TOOLITEMS
        """Separator (Expander), to go expanding the blank space"""
        self.expander = Gtk.Separator()
        self.expander.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.expander.set_opacity(0)  # not draw
        self.expander.set_hexpand(True)  # and YES, expand

        # GCleaner icon for Toolbar
        self.icon = Gtk.Image.new_from_icon_name("gcleaner")
        self.icon.set_pixel_size(56)
        self.icon.get_style_context().add_class("toolbar-icon")

        # PACKAGING
        # Icon
        self.icon_box.append(self.icon_fill)
        self.icon_box.append(self.icon)
        self.sub_icon_box.append(self.icon_box)

        # Name and Version
        self.app_title_box.append(self.title)
        self.app_version_box.append(self.app_version)
        self.app_name_box.append(self.title_fill)
        self.app_name_box.append(self.app_title_box)
        self.app_name_box.append(self.app_version_box)
        self.sub_name_app_box.append(self.app_name_box)

        # Operating System and System Specs
        self.os_box.append(self.information)
        self.system_properties_box.append(self.specs)
        self.specs_box.append(self.specs_fill)
        self.specs_box.append(self.os_box)
        self.specs_box.append(self.system_properties_box)
        self.sub_specs_box.append(self.specs_box)

        # Help ToolButton
        self.about_box.append(self.menu_button)
        self.help_box.append(self.help_fill_1)
        self.help_box.append(self.about_box)
        self.help_box.append(self.help_fill_2)

        # ToolBar*
        self.append(self.sub_icon_box)
        self.append(self.sub_name_app_box)
        self.append(self.sub_specs_box)
        self.append(self.expander)
        self.append(self.help_box)
