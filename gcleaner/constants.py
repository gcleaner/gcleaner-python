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
import os


class Constants:
    INSTALL_PREFIX = "/usr"
    DATADIR = "/usr/share"
    PKGDATADIR = "/usr/share/gcleaner"
    USERHOMEDIR = os.getenv("HOME")
    APP_NAME = "GCleaner"
    RELEASE_NAME = "Bosch Aerotwin"
    VERSION = "0.0.1"
    VERSION_INFO = "Initial Release of GCleaner."
    COMMENTS = "Clean your GNU/Linux system"
    WEBSITE = "https://gcleaner.github.io/"
    EXEC_NAME = "gcleaner"
    APP_LAUNCHER = "gcleaner.desktop"
    COPYRIGHT = "© 2025 Juan Pablo Lozano"
    AUTHORS = ["Juan Pablo Lozano"]
