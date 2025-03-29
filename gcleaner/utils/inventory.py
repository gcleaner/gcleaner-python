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
class PathsInventory():
    """
    A class to store an inventory of all file paths to be cleaned.
    """

    def __init__(self):
        """
        Initializes an empty list to store file paths.
        """
        self.paths = []

    def add(self, file_path: str):
        """
        Adds a file path to the inventory.
        
        :param file_path: The file path to be added.
        """
        self.paths.append(file_path)