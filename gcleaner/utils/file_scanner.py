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
import os

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("GLib", "2.0")
gi.require_version("Gio", "2.0")
gi.require_version("Polkit", "1.0")
from gi.repository import Gio, GLib, Polkit


class FileScanner():
    """
    Scans a directory to count the number of files that will be cleaned
    and calculates the total disk space occupied by the directory.

    This class traverses a given directory and its subdirectories, counting
    the number of files and summing their sizes. It can be used to estimate
    the amount of storage that could be freed if the files were deleted.

    Attributes:
        file_count (int): The number of files found in the directory.
        total_size (int): The total size of the files in bytes.

    Methods:
        scan_directory(dir, space="", cancellable=None, inventory=None):
            Recursively scans a directory and returns the number of files and
            their total size.

        get_directory_data(path, inventory):
            Initiates the scanning process for a given directory path, handling
            errors and returning the count of files and total size.
    """

    def __init__(self):
        """
        Initializes the Scanner object with default values.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.file_count = 0
        self.total_size = 0

    def request_permission(self):
        authority = Polkit.Authority.get_sync(None)
        subject = Polkit.UnixProcess.new_for_owner(os.getpid(), 0, -1)
        action_id = "com.gcleaner.list_directory"
        flags = Polkit.CheckAuthorizationFlags.ALLOW_USER_INTERACTION

        result = authority.check_authorization_sync(
            subject, action_id, None, flags, None
        )

        return result.get_is_authorized()

    def scan_directory(
        self, dir: Gio.File, space: str = "",
        cancellable: Gio.Cancellable = None, inventory=None
    ) -> tuple[int, int]:
        """
        Recursively scans a directory to count files and calculate total size.

        Args:
            dir (Gio.File): The directory to scan.
            space (str, optional): Formatting space for display purposes.
            Defaults to "".
            cancellable (Gio.Cancellable, optional): A cancellable operation.
            Defaults to None.
            inventory (optional): A collection to store file paths.
            Defaults to None.

        Returns:
            list: A list containing [file_count, total_size].
        """
        try:
            enumerator = dir.enumerate_children(
                "standard::*", Gio.FileQueryInfoFlags.NOFOLLOW_SYMLINKS,
                cancellable
            )
        except GLib.Error as e:
            self.logger.warning(
                f"Unable to access '{dir.get_path()}' ({e.message})"
            )
            return None, None

        while True:
            try:
                info = enumerator.next_file(cancellable)
                if info is None:
                    break
            except GLib.Error:
                break  # Error during iteration

            if info.get_file_type() == Gio.FileType.DIRECTORY:
                subdir = dir.get_child(info.get_name())
                self.scan_directory(
                    subdir, space + " ", cancellable, inventory
                )
            else:
                self.file_count += 1
                self.total_size += info.get_size()
                if inventory is not None:
                    inventory.add(f"{dir.get_path()}/{info.get_name()}")

        return self.file_count, self.total_size

    def get_directory_data(self, path: str, inventory) -> tuple[int, int]:
        """
        Initiates the directory scanning process to count files and calculate
        total size.

        Args:
            path (str): The directory path to scan.
            inventory: A collection to store file paths.

        Returns:
            list: A list containing [file_count, total_size] or None if an
            error occurs.
        """
        if not path:
            self.logger.warning(f"Invalid directory path > {path}")
            return None, None

        self.file_count = 0
        self.total_size = 0

        start_directory = Gio.File.new_for_path(path)

        try:
            return self.scan_directory(
                start_directory, "", Gio.Cancellable(), inventory
            )
        except GLib.Error as e:
            self.logger.error(f"{e.message}")
            self.logger.error(f"Check path > {path}")

        return None, None
