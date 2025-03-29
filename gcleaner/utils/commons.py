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


def to_human_format(bytes: int) -> str:
    """
    Converts a size in bytes to a readable human format (KB, MB, GB).
    GNU/Linux uses a format of 1000 instead of 1024 to transform measurements. 
    """
    size = bytes / 1000
    if size < 1000:
        return f"{round(size, 2)} KB"
    size /= 1000
    if size < 1000:
        return f"{round(size, 2)} MB"
    size /= 1000
    return f"{round(size, 2)} GB"