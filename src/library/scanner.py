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
from gi.repository import GLib, Gio


def to_file_size_format(bytes):
    size = 0.0
    size_format = ""

    size = bytes / 1000
    if size < 1000:
        size = round((size * 100) / 100)
        size_format = str(size) + " KB"
    else:
        size = size / 1000
        if size < 1000:
            size = round((size * 100) / 100)
            size_format = str(size) + " MB"
        else:
            size = size / 1000;
            if size < 1000:
                size = round((size * 100) / 100)
                size_format = str(size) + " GB"

    return size_format


class Scanner():

    # Local Variables
    files = 0
    scanned_size = 0

    def __init__(self):
        files = 0
        scanned_size = 0

    """ Function to search for files and folder size
    """
    def list_folder_content(self, folder, space = "", cancellable = None, inventory = None):
        print("__ITERATION__")
        data = []
        enumerator = Gio.FileEnumerator()

        try:
            print("__WITHIN TRY__")
            enumerator = folder.enumerate_children(
                                    'standard::*',
                                    Gio.FileQueryInfoFlags.NOFOLLOW_SYMLINKS,
                                    cancellable)
            print("__AFTER ENUM__")
        except Exception as err:
            print("ORG.GCLEANER.LIB.SCANNER: [WARNING: Unable to access to the path "
                   + str(folder.get_path()))
            print(">>> " + str(err))
            data.append(0)
            data.append(0)
            return data
        print("__BEFORE WHILE__")
        info = enumerator.next_file(cancellable)
        while cancellable.is_cancelled() == False and info != None:
            if info.get_file_type() == Gio.FileType.DIRECTORY:
                subdir = folder.resolve_relative_path(info.get_name())
                list_folder_content(subdir, space + " ", cancellable, inventory)
                # Here we can count folders
            else:
                # Count Files
                files = files + 1
                scanned_size = scanned_size + info.get_size()
                inventory.add(folder.get_uri() + "/" + info.get_name())
            info = enumerator.next_file(cancellable)

        if cancellable.is_cancelled():
            raise Exception("ORG.GCLEANER.LIB.SCANNER: [Operation was cancelled]")

        data.append(files)
        data.append(scanned_size)
        return data

    def scan_folder(self, folder_path, inventory = None):
        data = None

        # Set Local Variables
        files = 0
        scanned_size = 0
        if folder_path == "":
            print("ORG.GCLEANER.LIB.SCANNER [INVALID DIRECTORY: " + str(folder_path) + "]")
        else:
            folder_to_scan = Gio.File.new_for_path(folder_path)
            try:
                data = self.list_folder_content(folder_to_scan, "", Gio.Cancellable(), inventory)
            except Exception as err:
                print("ORG.GCLEANER.LIB.SCANNER [Error: " + str(err) + "]")
                print(">>> Check path: " + str(folder_path))

        return data

