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


# ***************** USER HOME DIRECTORY ***************** #
user_home_dir = os.popen("env | grep 'HOME='").readlines()
user_home_parts = user_home_dir[0].split('=')
user_home_dir = user_home_parts[1]
user_home_dir = user_home_dir.replace("\n", "")


# Here are declared the CONSTANTS
class Constants:

    INSTALL_PREFIX = "/usr"
    DATADIR        = "/usr/share"
    PKGDATADIR     = "/usr/share/gcleaner"
    USERHOMEDIR    = user_home_dir
    PROGRAM_NAME   = "GCleaner"
    RELEASE_NAME   = "Bosch Aerotwin"
    VERSION        = "0.02.139"
    VERSION_INFO   = "Initial Release of GCleaner."
    EXEC_NAME      = "gcleaner"
    APP_LAUNCHER   = "gcleaner.desktop"

	# About GCleaner
    AUTHORS        = ["Juan Pablo Lozano <lozanotux@gmail.com>"
					 ,"Andres Segovia <his@mail.com>"]

    ARTISTS        = ["Juan Pablo Lozano <lozanotux@gmail.com>"
                     ,"Ivan Matias Suarez <ivan.msuar@gmail.com>"]

    DOCUMENTERS    =["Juan Pablo Lozano <lozanotux@gmail.com>"
                    ,"Andres Segovia <his@mail.com>"]

