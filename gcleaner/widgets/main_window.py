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
from gi.repository import Gtk, Gdk, Gio
from widgets.toolbar import ToolBar
from widgets.sidebar import Sidebar
from entities.result import Result
from constants import Constants


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app, *args, **kwargs):
        super().__init__(application=app, *args, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)

        self.set_title(Constants.APP_NAME)
        self.props.icon_name = "gcleaner"

        # Settings for save the GCleaner state
        self.settings = Gio.Settings("org.gcleaner")
        self.set_default_size(
            self.settings.get_int("window-width"),
            self.settings.get_int("window-height")
        )
        
        # BOXES
        # Box that will contain the rest of the boxes (this is adjusted to the window)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # Box containing the ToolBar, the separator and the remaining box info_action_box
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # Box containing the spinner, the progress bar and the % of the progress
        self.progress_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # Box that will hold the buttons to scan and clean
        self.buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # Box containing the progress_box, result_box and buttons_box
        self.info_action_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # Box containing the Gtk.Spinner, and Gtk.Images of Status Notifications
        self.status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # BUTTONS
        self.scan_button = Gtk.Button.new_with_label(" Scan ")
        self.clean_button = Gtk.Button.new_with_label(" Clean ")
        """
        Initial state of the buttons (Scan painted blue
        and clear disabled)
        """
        # Paint the Button of blue (depends of the Gtk Theme used)
        self.scan_button.get_style_context().add_class("suggested-action")
        # Disable clean button
        self.clean_button.set_sensitive(False)

        # Status Images
        self.info_img = Gtk.Image()
        self.info_img.set_from_icon_name("dialog-information")
        self.info_img.set_icon_size(Gtk.IconSize.NORMAL)
        self.success_img = Gtk.Image()
        self.success_img.set_from_icon_name("dialog-ok")
        self.success_img.set_icon_size(Gtk.IconSize.NORMAL)

        # LABELS
        self.progress = 0
        self.percentage_progress = Gtk.Label()
        self.percentage_progress.set_markup(f"<b>{self.progress:.2f}%</b>")

        # SEPARATORS
        self.content_separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.buttons_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.buttons_separator.set_opacity(0)  # not draw
        self.buttons_separator.set_hexpand(True)
        self.result_separator_top = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.result_separator_bottom = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        """ Creates an instance of a customized Toolbar """
        self.toolbar = ToolBar(app)
        self.toolbar.set_name("Toolbar")
        # Add the Toolbar to the 'main window box'
        self.main_box.append(self.toolbar)

        # SIDEBAR
        self.sidebar = Sidebar(self)

        # OTHERS WIDGETS
        # Widgets for status_box
        self.scanning_spin = Gtk.Spinner()
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_hexpand(True)
        self.progress_bar.get_style_context().add_class("progress-bar")
        self.progress_bar.set_margin_top(2)
        self.progress_bar.set_margin_bottom(2)
        self.progress_bar.set_margin_start(4)
        self.progress_bar.set_margin_end(4)
        self.progress_bar.set_fraction(0.8)

        # LIST STORE - SCAN/CLEANING INFORMATION
        self.result_store = Gio.ListStore.new(Result)
        selection = Gtk.SingleSelection.new(self.result_store)

        concept_factory = Gtk.SignalListItemFactory()
        concept_factory.connect("setup", self.setup_label)
        concept_factory.connect("bind", self.bind_label, "Concept")

        size_factory = Gtk.SignalListItemFactory()
        size_factory.connect("setup", self.setup_label)
        size_factory.connect("bind", self.bind_label, "Size")

        quantity_factory = Gtk.SignalListItemFactory()
        quantity_factory.connect("setup", self.setup_label)
        quantity_factory.connect("bind", self.bind_label, "Quantity")

        column_view = Gtk.ColumnView.new(selection)
        column_view.set_hexpand(True)
        column_view.set_vexpand(True)

        concept_column = Gtk.ColumnViewColumn(title="Concept", factory=concept_factory)
        size_column = Gtk.ColumnViewColumn(title="Size", factory=size_factory)
        quantity_column = Gtk.ColumnViewColumn(title="Quantity", factory=quantity_factory)

        for col in (concept_column, size_column, quantity_column):
            col.set_expand(True)

        column_view.append_column(concept_column)
        column_view.append_column(size_column)
        column_view.append_column(quantity_column)

        self.result_window = Gtk.ScrolledWindow()
        self.result_window.set_child(column_view)
        self.result_window.set_hexpand(True)
        self.result_window.set_vexpand(True)

        # Progress Bar & Spinner
        self.status_box.append(self.scanning_spin)
        self.progress_box.append(self.status_box)
        self.progress_box.append(self.progress_bar)
        self.progress_box.append(self.percentage_progress)

        # Buttons
        self.buttons_box.append(self.scan_button)
        self.buttons_box.append(self.buttons_separator)
        self.buttons_box.append(self.clean_button)
        self.buttons_box.set_margin_top(4)
        self.buttons_box.set_margin_bottom(4)
        self.buttons_box.set_margin_start(4)
        self.buttons_box.set_margin_end(4)

        # Information, Results and Actions
        self.info_action_box.append(self.progress_box)
        self.info_action_box.append(self.result_separator_top)
        self.info_action_box.append(self.result_window)
        # Separador entre la botonera y los resultados
        self.info_action_box.append(self.result_separator_bottom)
        self.info_action_box.append(self.buttons_box)

        # Content Box
        self.content_box.append(self.sidebar)
        # Visible Gtk.Separator beetwen Sidebar and info_action_box
        self.content_box.append(self.content_separator)
        """"
        Package the info_action_box (that contents the progress bar,"
        result information and buttons)"
        """
        self.content_box.append(self.info_action_box)

        # Final assembly
        self.main_box.append(self.content_box)

        # User that execute the application
        print(f"[INFO] MainWindow.__init__: User > {Constants.USERHOMEDIR}")

        # Add the 'main window box' to the main window (Gtk.Window)
        self.connect("close_request", self.on_delete_event)
        self.set_child(self.main_box)
    
    def get_settings(self):
        return self.settings
    
    def on_delete_event(self, param):
        self.width = self.get_size(Gtk.Orientation.HORIZONTAL)
        self.height = self.get_size(Gtk.Orientation.VERTICAL)

        # Save values into GSCHEMA
        self.settings.set_int("window-width", self.width)
        self.settings.set_int("window-height", self.height)

        self.settings.set_boolean("scan-firefox", self.sidebar.check_firefox.get_active())
        self.settings.set_boolean("scan-trash", self.sidebar.check_trash.get_active())

    def setup_label(self, factory, list_item):
        label = Gtk.Label(xalign=0)
        list_item.set_child(label)

    def bind_label(self, factory, list_item, property_name):
        item = list_item.get_item()
        label = list_item.get_child()
        value = getattr(item, property_name)
        label.set_text(str(value))
