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
from pathlib import Path
from constants import Constants
from entities.plugin import Plugin


class TrashPlugin(Plugin):
    """GCleaner Plugin to clean up the trash files of the system."""

    def __init__(self):
        super().__init__()
        self.summary = "Recycle Bin"
    
    def scan(self) -> tuple[int, int]:
        trash_path = f"{Constants.USERHOMEDIR}/.local/share/Trash/files/"
        files = 0
        size = 0

        if Path(trash_path).exists():
            files, size = self.scanner.get_directory_data(
                trash_path, self.inventory
            )
        
        return files, size
