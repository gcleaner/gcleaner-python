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
import configparser
from pathlib import Path
from constants import Constants
from entities.plugin import Plugin


class FirefoxPlugin(Plugin):
    """GCleaner Plugin to clean up the temporary files of Firefox."""

    def __init__(self):
        super().__init__()
        self.profiles = self.get_profiles()

    def get_profiles(self) -> list:
        """
        Auto-discovers full Firefox profiles paths on a GNU/Linux system
        """
        profiles = []

        # Default Firefox profile locations
        config_dir = f"{Constants.USERHOMEDIR}/.mozilla/firefox"
        profiles_ini = f"{config_dir}/profiles.ini"

        # Check if the file profiles.ini exists
        if Path(profiles_ini).exists():
            config = configparser.ConfigParser()
            config.read(profiles_ini)
            profile_id = config.get('General', 'StartWithLastProfile')
            for section in config.sections():
                if section.startswith('Profile'):
                    relative_id = config.get(section, 'IsRelative')
                    if relative_id == profile_id:
                        full_profile_path = (
                            f"{config_dir}/{config.get(section, 'Path')}"
                        )

                        # Only add full profile directories
                        if Path(full_profile_path).exists():
                            profiles.append(str(full_profile_path))

        return profiles

    def scan(self) -> list:
        pass

    def clean(self) -> None:
        pass
