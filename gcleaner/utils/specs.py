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
import re
import subprocess


class Specs():

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_processor(self):
        """
        Retrieves the processor model name from /proc/cpuinfo
        and cleans unnecessary details.

        Returns:
            str: The cleaned processor model name or "Generic" if it cannot
            be retrieved
        """
        processor = "Generic"
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    match = re.match(r"^model name\s*:\s*(.*)", line)
                    if match:
                        processor = match.group(1)
                        break

            processor = processor.replace("(R)", "®").replace("(TM)", "™")
            processor = re.sub(
                r"\s+with\s+.*", "",
                processor, flags=re.IGNORECASE
            )
            processor = re.sub(r"\s+CPU.*", "", processor, flags=re.IGNORECASE)

        except FileNotFoundError:
            self.logger.warning("Processor info not found")
        except PermissionError:
            self.logger.warning("Permission denied accessing processor info")
        return processor

    def get_ram_memory(self):
        """
        Retrieves the total RAM memory from /proc/meminfo and formats it into
        a human-readable string.

        Returns:
            str: The total RAM size in a human-readable format.
        """
        try:
            result = subprocess.run(
                ["pkexec", "dmidecode", "-t", "memory"],
                capture_output=True,
                text=True,
                check=True
            )

            total_ram = 0
            for line in result.stdout.split("\n"):
                if (
                    line.startswith("\tSize:")
                    and "No Module Installed" not in line
                    and "None" not in line
                ):
                    total_ram += int(line.split(":")[1].strip().split(" ")[0])

            return f"{total_ram} GB"

        except (FileNotFoundError, PermissionError, ValueError) as err:
            self.logger.warning(f"RAM Memory Not found ({err})")
            return "0 B"

    def get_graphics(self):
        """
        Retrieves the installed graphics card(s) using `lspci`.

        Returns:
            str: A formatted string describing the detected graphics card(s).
        """
        try:
            result = subprocess.run(
                ["lspci"], capture_output=True, text=True, check=True
            )
            graphics_list = []

            gpu_regex = re.compile(r".*VGA|.*3D", re.IGNORECASE)

            for line in result.stdout.split("\n"):
                if gpu_regex.search(line):
                    gpu_name = line.split(": ", 1)[-1].strip()

                    if "Intel" in gpu_name:
                        graphics_list.append("Intel Graphics")
                    elif "NVIDIA" in gpu_name:
                        graphics_list.append("NVIDIA Graphics")
                    elif "AMD" in gpu_name or "Radeon" in gpu_name:
                        graphics_list.append("AMD Radeon Graphics")
                    elif "VMware" in gpu_name:
                        graphics_list.append("VMware Graphics")
                    else:
                        graphics_list.append(f"Unknown Graphics ({gpu_name})")

            return (
                " + ".join(graphics_list)
                if graphics_list else "Unknown Graphics"
            )

        except subprocess.CalledProcessError as err:
            self.logger.warning(f"Graphics Detection Failed ({err})")
            return "Unknown Graphics"

    def get_os_architecture(self):
        """
        Retrieves the system's architecture using `uname` utility.

        Returns:
            str: The architecture of the operating system
        """
        try:
            result = subprocess.run(
                ["uname", "-m"], capture_output=True, text=True, check=True
            )
            architecture = result.stdout.strip()

            if architecture == "x86_64":
                return "64-bit"
            elif "arm" in architecture:
                return "ARM"
            elif re.match(r"^i[3456789]86$", architecture):
                return "32-bit"
            else:
                return "Unknown Architecture"

        except subprocess.CalledProcessError as err:
            self.logger.warning(f"Architecture Detection Failed ({err})")
            return "Unknown Architecture"

    def get_os_information(self):
        """
        Retrieves the system's OS information by reading the /etc/os-release
        file and the system architecture.

        Returns:
            str: A string containing the full OS. For instance:
            <name, version, codename, and architecture>
        """
        os_info = {"os": "Unknown", "version": "X", "codename": "X"}

        try:
            with open("/etc/os-release", "r") as file:
                for line in file:
                    line = line.strip().replace('"', '')

                    if line.startswith("NAME="):
                        os_info["os"] = line.split("=", 1)[1]
                    elif line.startswith("VERSION_ID="):
                        os_info["version"] = line.split("=", 1)[1]
                    elif line.startswith("VERSION_CODENAME="):
                        os_info["codename"] = line.split("=", 1)[1]
                    elif (
                        not os_info["codename"]
                        and line.startswith("VARIANT_ID=")
                    ):
                        os_info["codename"] = line.split("=", 1)[1]

            os_info["codename"] = os_info["codename"].capitalize()

        except FileNotFoundError:
            self.logger.warning("/etc/os-release file not found")

        architecture = Specs.get_os_architecture(self)

        os_complete = (
            f"{os_info['os']} {os_info['version']} ({os_info['codename']})"
            f" {architecture}"
        )

        return os_complete
