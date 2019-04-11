import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
from constants import Constants
from widgets.header_bar  import  HeaderBarOfWindow
from widgets.toolbar import ToolbarOfWindow


class HeaderBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(800, 600)

        """hb = HeaderBarOfWindow(self)
        self.set_titlebar(hb)"""

        main_window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        tb = ToolbarOfWindow(self)
        tb.get_style_context().add_class("Toolbar")
        tb.set_name("Toolbar")
        self.set_title(Constants.PROGRAM_NAME)

        css_file = "/usr/share/gcleaner/gtk-widgets-gcleaner.css"
        css_provider = Gtk.CssProvider()

        try:
            css_provider.load_from_path(css_file)
            Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER);
        except Exception as err:
            print("ORG.GCLEANER.APP: [ERROR CARGANDO ESTILOS CSS [" + str(err) + "]");
            print(">>> Check path: /usr/share/gcleaner/gtk-widgets-gcleaner.css");

        main_window_box.pack_start(tb, False, True, 0)
        main_window_box.pack_start(Gtk.TextView(), True, True, 0)

        self.add(main_window_box)

win = HeaderBarWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

# print("GCleaner Version: ", Constants.VERSION)

