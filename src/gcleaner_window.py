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
import os, time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, Gdk
from constants import Constants
from widgets.header_bar import HeaderBarOfWindow
from widgets.toolbar import ToolbarOfWindow
from widgets.sidebar import Sidebar


class GCleaner(Gtk.ApplicationWindow):

    # Global Variables
    """ Set to 0 Counter Files and Accumulator Size
        Of All Items checked in SideBar
    """
    counter = 0
    accumulator = 0


    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # VARS
        # Settings for save the GCleaner state
        self.__settings = Gio.Settings("org.gcleaner")
        """Boolean value that determines if use or not
        use HeaderBar according to the desktop environment"""
        self.__use_headerbar = False
        self.__success_icon = 0

        # MAIN WINDOW PROPERTIES
        self.move(self.__settings.get_int("opening-x"),
                  self.__settings.get_int("opening-y"))
        self.set_default_size(self.__settings.get_int("window-width"),
                              self.__settings.get_int("window-height"))
        self.set_title(Constants.PROGRAM_NAME)

        # Application icon
        self.props.icon_name = "gcleaner"

        # BOXES
        # Box that will contain the rest of the boxes (this is adjusted to the window)
        self.__main_window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # Box containing the Sidebar, the separator and the remaining box info_action_box
        self.__content_box     = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # Box containing the spinner, the progress bar and the % of the progress
        self.__progress_box    = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # Box containing the Gtk.ScrolledWindow of Results
        self.__result_box      = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # Box that will hold the buttons to scan and clean
        self.__buttons_box     = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # Box containing the __progress_box, __result_box and __buttons_box
        self.__info_action_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # Box containing the Gtk.Spinner, and Gtk.Images of Status Notifications
        self.__status_box      = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # BUTTONS
        self.__scan_button  = Gtk.Button.new_with_label(" Scan ")
        self.__clean_button = Gtk.Button.new_with_label(" Clean ")
        """ Initial state of the buttons
        (Scan painted blue and clear disabled)
        """
        # Paint the Button of blue (With Adwaita theme, depends of the Gtk Theme used)
        self.__scan_button.get_style_context().add_class("suggested-action")
        # Disable clean button
        self.__clean_button.set_sensitive(False)

        # LABELS
        self.__percentage_progress = Gtk.Label("")
        self.__percentage_progress.set_markup("<b>0%</b>")

        # SEPARATORS
        self.__content_separator       = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.__result_separator_left   = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.__result_separator_right  = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.__result_separator_top	   = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.__result_separator_bottom = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        # IMAGES
        self.__info_img = Gtk.Image()
        self.__info_img.set_from_icon_name("dialog-information", Gtk.IconSize.MENU)
        self.__success_img = Gtk.Image()
        self.__success_img.set_from_icon_name("dialog-ok", Gtk.IconSize.MENU)

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

        # OTHERS WIDGETS
        # Widgets for __status_box
        self.__scanning_spin = Gtk.Spinner()
        self.__progress_bar  = Gtk.ProgressBar()

        # LIST STORE - SCAN/CLEANING INFORMATION
        self.__result_list = Gtk.ListStore(str, str, str)
        self.__result_view = Gtk.TreeView.new_with_model(self.__result_list)
        self.__result_window = Gtk.ScrolledWindow(None, None)
        self.__result_window.add(self.__result_view)
        """ Results Columns ----------------------------------------------------
        """
        self.__concept_rendr = Gtk.CellRendererText()
        self.__concept_col   = Gtk.TreeViewColumn("Concept", self.__concept_rendr, text=0)
        self.__result_view.append_column(self.__concept_col)

        self.__size_rendr = Gtk.CellRendererText()
        self.__size_col   = Gtk.TreeViewColumn("Size", self.__size_rendr, text=1)
        self.__result_view.append_column(self.__size_col)

        self.__quantity_rendr = Gtk.CellRendererText()
        self.__quantity_col   = Gtk.TreeViewColumn("Quantity", self.__quantity_rendr, text=2)
        self.__result_view.append_column(self.__quantity_col)

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

        # PROGRESS_BAR and SPINNER
        self.__status_box.pack_start(self.__scanning_spin, True, True, 0)
        self.__progress_box.pack_start(self.__status_box, False, True, 8)
        self.__progress_box.pack_start(self.__progress_bar, True, True, 8)
        self.__progress_box.pack_start(self.__percentage_progress, False, True, 8)

        # Scanning and Cleaning RESULTS
        self.__result_box.pack_start(self.__result_separator_left, False, True, 0)
        self.__result_box.pack_start(self.__result_window, True, True, 0)
        self.__result_box.pack_start(self.__result_separator_right, False, True, 0)

        # Buttons
        self.__buttons_box.pack_start(self.__scan_button, False, False, 0)
        self.__buttons_box.pack_end(self.__clean_button, False, False, 0)

        # Information, Results and Actions
        self.__info_action_box.pack_start(self.__progress_box, False, True, 8)
        self.__info_action_box.pack_start(self.__result_separator_top, False, True, 0)
        self.__info_action_box.pack_start(self.__result_box, True, True, 0)
        # Separador entre la botonera y los resultados
        self.__info_action_box.pack_start(self.__result_separator_bottom, False, True, 0)
        self.__info_action_box.pack_start(self.__buttons_box, False, True, 8)

        # Content Box
        self.__content_box.pack_start(self.__event_sidebar, False, True, 0)
        # Visible Gtk.Separator beetwen Sidebar and __info_action_box
        self.__content_box.pack_start(self.__content_separator, False, True, 0)
        # Packaging the box with progress bar, result information and buttons
        self.__content_box.pack_start(self.__info_action_box, True, True, 8)

        # Final assembly
        self.__main_window_box.pack_start(self.__content_box, True, True, 0)

        # ************ TEMPORARY, then erase ******************* #
        print("ORG.GCLEANER.APP: [USUARIO: %s]" % (Constants.USERHOMEDIR))

        """ Here the GLib.MainLoop is a Loop for draw the GUI.
            With this Class we avoid freezing the user interface.
        """
        self.__loop = GLib.MainLoop()

        # Setting up the values for progress_bar and percentage label
        self.__progress_fraction = 0.0
        self.__progress_number = 0.0

        """ Scan button actions and Logic
        """
        self.__scan_button.connect("clicked", self.on_clicked_scan)

        """ Clean button actions and Logic
        """
        self.__clean_button.connect("clicked", self.on_clicked_clean)

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

    def on_clicked_scan(self, button):
        # Clean the results list
        self.__result_list.clear()
        # Remove the blue color of the button
        self.__scan_button.get_style_context().remove_class("suggested-action")
        # Disable the scan button
        self.__scan_button.set_sensitive(False)
        """ Function to show childrens of GtkBox:
        childrens = self.__status_box.get_children()
        for children in childrens:
            print("Children: " + str(children.get_name()))
        """
        self.__status_box.remove(self.__success_img)
        if self.__success_icon == 1:
            self.__status_box.add(self.__scanning_spin)
            self.__success_icon = 0
        self.__scanning_spin.props.active = True
        # --------------> 0%
        self.__progress_bar.set_fraction(0)
        self.__progress_fraction = 0
        self.__progress_number = 0
        # Set to 0 both for each scan process
        counter = 0
        accumulator = 0
        self.__progress_fraction += 0.1428571
        self.__progress_number += 14.28571
        self.__progress_bar.set_fraction(self.__progress_fraction)
        self.__percentage_progress.set_markup("<b>" + str(round(self.__progress_number)) + "%</b>")
        time.sleep(2)
        self.__progress_fraction += 0.1428571
        self.__progress_number += 14.28571
        self.__progress_bar.set_fraction(self.__progress_fraction)
        self.__percentage_progress.set_markup("<b>" + str(round(self.__progress_number)) + "%</b>")
        time.sleep(2)
        self.__progress_fraction = 1.0
        self.__progress_number = 100.0
        self.__progress_bar.set_fraction(self.__progress_fraction)
        self.__percentage_progress.set_markup("<b>" + str(round(self.__progress_number)) + "%</b>")
        # Quit GtkMainLoop
        self.__loop.quit()

    def on_clicked_clean(self, button):
        print("Clean Button Clicked!")

