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
from gi.repository import Gtk, GLib, Gio
from constants import Constants


# Local Variables
path_trash_files = ""
path_trash = ""

def msg_path_not_found(widget):
    dialog = Gtk.MessageDialog(widget, 0, Gtk.MessageType.WARNING,
                               Gtk.ButtonsType.OK,
                               "¡Unable to analyze the recycle bin! Try manually to delete a file and empty the Recycle Bin.")
    dialog.set_title("Warning... Recycle Bin")
    dialog.show()
    dialog.destroy()

def msg_cmd_failed(widget):
    dialog = Gtk.MessageDialog(widget, 0, Gtk.MessageType.WARNING,
                               Gtk.ButtonsType.OK,
                               "¡The Recycle Bin could not be cleaned! Try again and verify your password.")
    dialog.set_title("Warning... Cleaning Recycling Bin")
    dialog.run()
    dialog.destroy()

def trash_get_params():
    home = Constants.USERHOMEDIR
    path_trash_files = home + "/.local/share/Trash/files/"
    gio_file = Gio.File.new_for_path(path_trash_files)

    if gio_file.query_exists():
        return path_trash_files
    else:
        try:
            GLib.spawn_command_line_sync("mkdir -p " + path_trash_files)
            return path_trash_files
        except Exception as err:
            print("ORG.GCLEANER.PLUGINS.TRASH: [COMMAND-ERROR: " + str(err) + "]")
            return "error"

def trash_clean(parent_window):
    home = Constants.USERHOMEDIR
    path_trash = home + "/.local/share/Trash/"
    cmd = "rm -Rf " + path_trash + "*"
    error = ""
    status = 0
    try:
        result, output, error, status = GLib.spawn_command_line_sync(cmd)
        if status != 0:
            # Show MsgBox with Error
            msg_cmd_failed(parent_window)
            return 1
        else:
            return 0
    except Exception as err:
        print("ORG.GCLEANER.PLUGIN-TRASH: [COMMAND-ERROR: " + str(err) + "]")
        print("ORG.GCLEANER.PLUGIN-TRASH: [ERROR: " + str(error) + "]")
        print("ORG.GCLEANER.PLUGIN-TRASH: [STATUS: " + str(status) + "%s]")
        return 1

