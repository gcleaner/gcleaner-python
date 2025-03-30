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
from abc import ABC, abstractmethod


class Plugin(ABC):
    """Abstract Base Class for cleaning plugins."""

    @abstractmethod
    def scan(self) -> list:
        """
        Retrieve a list the files be cleaned and the disk space to free up.
        """
        pass

    @abstractmethod
    def clean(self) -> None:
        """Perform the cleaning operation."""
        pass
