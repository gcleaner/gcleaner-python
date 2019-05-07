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


def to_human_format(bytes):
    size = 0.0
    size_format = ""

    size = bytes / 1000
    if size < 1000:
        size = round(size, 2)
        size_format = str(size) + " KB"
    else:
        size = size / 1000
        if size < 1000:
            size = round(size, 2)
            size_format = str(size) + " MB"
        else:
            size = size / 1000;
            if size < 1000:
                size = round(size, 2)
                size_format = str(size) + " GB"

    return size_format


class Scanner():

    def __init__(self):
        # Global Scanned Values
        self.files = 0
        self.scanned_size = 0

    """ Function to search for files and folder size
    """
    def scan_folder(self, start_folder):
        data = []
        if start_folder == "":
            print("ORG.GCLEANER.LIB.SCANNER [INVALID DIRECTORY: " + str(start_folder) + "]")
            data.append(0)
            data.append(0)
        else:
            # Current Folder Values
            folder_size = 0
            folder_files = 0
            for dirpath, dirnames, filenames in os.walk(start_folder):
                for f in filenames:
                    file_path = os.path.join(dirpath, f)
                    self.scanned_size += os.path.getsize(file_path)
                    folder_size += os.path.getsize(file_path)
                    folder_files += 1
                    self.files += 1
            data.append(folder_files)
            data.append(folder_size)
        return data

    def get_files(self):
        return self.files

    def get_scanned_size(self):
        return self.scanned_size

