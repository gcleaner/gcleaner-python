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
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import GObject


class Result(GObject.GObject):
    concept = GObject.Property(type=str)
    size = GObject.Property(type=str)
    quantity = GObject.Property(type=str)

    def __init__(self, concept, size, quantity):
        super().__init__()
        self.concept = concept
        self.size = size
        self.quantity = quantity
