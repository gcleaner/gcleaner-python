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


class ToolbarOfWindow(Gtk.Toolbar):

    def __init__(self, app):
        super().__init__()

        # Constructor Variables
        self.__app = app
        self.__complete_system_specs = ""

        """Class property to give ToolBar aspect of Ubuntu
        (consecutive to the edge of the window)"""
        self.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

        # LABELS
        # NAME APP AND VERSION
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
        self.__app_title = Gtk.Label("")
        self.__app_title.set_markup("<span font_size='large'><b>GCleaner</b></span>")

        self.__app_version = Gtk.Label("")
        self.__app_version.set_markup ("<span font_size='small'> v" + Constants.VERSION + "</span>")

        # Information of Operating System, RAM and Video
        self.__os_information = Gtk.Label("")
        self.__os_information.set_markup("<span font_size='small'>" + Specs().get_os_information() + "</span>")

        self.__complete_system_specs = (Specs().get_processor() + "  •  "
                                      + Specs().get_ram_memory() + " RAM  •  "
                                      + Specs().get_graphics())

        self.__system_specs = Gtk.Label("")
        self.__system_specs.set_markup("<span font_size='small'>" + self.__complete_system_specs + "</span>")

        # Fillings
        self.__help_fill_1       = Gtk.Label("")
        self.__help_fill_2       = Gtk.Label(" ")
        self.__icon_fill         = Gtk.Label("")
        self.__system_specs_fill = Gtk.Label("")
        self.__app_name_fill     = Gtk.Label("")
        self.__help_fill_1.set_markup("<span font_size='large'>  </span>")
        self.__icon_fill.set_markup("<span font_size='xx-small'>  </span>")
        self.__app_name_fill.set_markup("<span font_size='large'>  </span>")
        self.__system_specs_fill.set_markup("<span font_size='x-large'>  </span>")

        """Here, first we create an Image and then add
		this image to MenuButton and resize it."""
        self.__appmenu_button = Gtk.MenuButton()
        self.__gear_icon = Gtk.Image()
        self.__gear_icon.set_from_icon_name("open-menu", Gtk.IconSize.LARGE_TOOLBAR)
        self.__appmenu_button.set_image(self.__gear_icon)
        self.__appmenu_button.set_size_request(32, 32)
        self.__appmenu_button.get_style_context().add_class("about_btn")

        """Here define an Menu Model and
		add it to appmenu Button"""
        self.__menumodel = Gio.Menu()
        self.__menumodel.append("About...", "app.about")
        self.__appmenu_button.set_menu_model(self.__menumodel)

        # Here we define the Actions
        self.__about_action = Gio.SimpleAction.new("about", None)
        self.__about_action.connect("activate", self.__app.about_callback)
        self.__app.add_action(self.__about_action)

        # BOXES
        # For Icon
        self.__icon_box 	= Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # Engloba para separar con pixels los ToolItem
        self.__sub_icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # Name and Version
        self.__app_name_box     = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__app_title_box    = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__app_version_box  = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # Engloba para separar con pixels los ToolItem
        self.__sub_name_app_box	= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # Operating System and System specs
        self.__os_box                = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__system_properties_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__specs_box             = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # Engloba para separar con pixels los ToolItem
        self.__sub_specs_box         = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # Help
        self.__help_box  = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__about_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # TOOLITEMS
        self.__item_icon = Gtk.ToolItem()
        self.__item_name = Gtk.ToolItem()
        self.__item_spec = Gtk.ToolItem()
        self.__item_help = Gtk.ToolItem()

        # OTHERS TOOLITEMS
        """Separator (Expander), to go expanding the blank space"""
        self.__expander = Gtk.SeparatorToolItem()
        self.__expander.set_draw(False) # not draw
        self.__expander.set_expand(True) # and YES, expand

        # GCleaner icon for Toolbar
        self.__icon = Gtk.Image()
        try:
            self.__icon_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                                           "/usr/share/icons/hicolor/64x64/apps/gcleaner.svg",
                                           56,
                                           56,
                                           False)
            self.__icon.set_from_pixbuf(self.__icon_pixbuf)
        except Exception as err:
            print("ORG.GCLEANER.APP.TOOLBAR: [GLIB::ERROR CREATING PIXBUF ICON]")
            print(">>> Check path: /usr/share/icons/hicolor/64x64/apps/gcleaner.svg")
            print(">>> Error Message: ", str(err))

        # PACKAGING
        """ box_name.pack_start(widget, expand, fill, padding) """
        # Icon
        self.__icon_box.pack_start(self.__icon_fill, False, True, 0)
        self.__icon_box.pack_start(self.__icon, False, True, 2)
        self.__sub_icon_box.pack_start(self.__icon_box, False, True, 6)

        # Name and Version
        self.__app_title_box.pack_start(self.__app_title, False, True, 0)
        self.__app_version_box.pack_start(self.__app_version, False, True, 0)
        self.__app_name_box.pack_start(self.__app_name_fill, False, True, 0)
        self.__app_name_box.pack_start(self.__app_title_box, False, True, 0)
        self.__app_name_box.pack_start(self.__app_version_box, False, True, 0)
        self.__sub_name_app_box.pack_start(self.__app_name_box, False, True, 6)

        # Operating System and System Specs
        self.__os_box.pack_start(self.__os_information, False, True, 0)
        self.__system_properties_box.pack_start(self.__system_specs, False, True, 0)
        self.__specs_box.pack_start(self.__system_specs_fill, False, True, 0)
        self.__specs_box.pack_start(self.__os_box, False, True, 0)
        self.__specs_box.pack_start(self.__system_properties_box, False, True, 0)
        self.__sub_specs_box.pack_start(self.__specs_box, False, True, 6)

        # Help ToolButton
        self.__about_box.pack_start(self.__appmenu_button, False, True, 6)
        self.__help_box.pack_start(self.__help_fill_1, False, True, 1)
        self.__help_box.pack_start(self.__about_box, False, True, 0)
        self.__help_box.pack_start(self.__help_fill_2, False, True, 0)

        # ToolItems
        self.__item_icon.add(self.__sub_icon_box)
        self.__item_name.add(self.__sub_name_app_box)
        self.__item_spec.add(self.__sub_specs_box)
        self.__item_help.add(self.__help_box)

        # ToolBar*
        self.add(self.__item_icon)
        self.add(self.__item_name)
        self.add(self.__item_spec)
        self.add(self.__expander)
        self.add(self.__item_help)

    # ACTIONS CALLBACKS HERE
    def about_callback(simple: Gio.SimpleAction, parameter=None):
            #self.__about = new GCleaner.Widgets.About()
            #self.__about.run()
            pass

