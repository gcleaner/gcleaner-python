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
from abc import ABC, abstractmethod
from pathlib import Path
from utils.file_scanner import FileScanner
from utils.inventory import PathsInventory


class Plugin(ABC):
    """Abstract Base Class for cleaning plugins."""

    def __init__(self):
        super().__init__()
        self.name = f"{self.__class__.__name__}"
        self.logger = logging.getLogger(self.__class__.__name__)
        self.summary = f"{self.__class__.__name__} Summary"
        self.scanner = FileScanner()
        self.inventory = PathsInventory()

    @abstractmethod
    def scan(self) -> tuple[int, int]:
        """
        Retrieve a list the files be cleaned and the disk space to free up.
        tuple[files, size]
        """
        pass

    def clean(self) -> None:
        """Perform the cleaning operation."""
        for path in self.inventory.paths:
            try:
                Path(path).unlink()
            except IsADirectoryError:
                Path(path).rmdir()
            except Exception as e:
                self.logger.warning(f"Error deleting {path} > {e}")
