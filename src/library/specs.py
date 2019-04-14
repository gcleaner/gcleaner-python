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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib


class Specs(object):

    def __init__(self):
        super().__init__()

    def get_processor(self):
        self.__processor_title = ""
        try:
            self.__processor = os.popen("sed -n 's/^model name[ \t]*: *//p' /proc/cpuinfo").readlines()
            self.__cores = 0

            for line in self.__processor:
                self.__cores += 1

            if self.__cores > 0:
                self.__processor_title = str(self.__processor[0].replace("\n",""))
                self.__processor_title = self.__processor_title.replace("(R)", "®")
                self.__processor_title = self.__processor_title.replace("(TM)", "™")
        except Exception as err:
            print("ORG.GCLEANER.APP.SPECS: [ERROR::Proccesor Not found [ " + str(err) + " ]]")
            self.__processor_title = "Unkown Processor"

        return self.__processor_title

    def  get_ram_memory(self):
        self.__ram_memory = ""
        try:
            self.__memory = os.popen("sed -n 's/^MemTotal[ \t]*: *//p' /proc/meminfo").readlines()

            self.__ram_memory = str(self.__memory[0].replace(" kB",""))
        except Exception as err:
            print("ORG.GCLEANER.APP.SPECS: [ERROR::RAM Memory Not found [ " + str(err) + " ]]")
            self.__ram_memory = "0"

        self.__memory = GLib.format_size((int(self.__ram_memory) * 1024));
        return self.__memory

    def get_graphics(self):
        self.__graphics = ""
        try:
            self.__video = os.popen("lspci").readlines()
            for line in self.__video:
                if "VGA" in str(line) or "3D" in str(line):
                    self.__graphics = line

            self.__parts = self.__graphics.split(':')
            self.__result = self.__graphics

            if len(self.__parts) == 3:
                self.__result = self.__parts[2]
            elif len(self.__parts) > 3:
                self.__result = self.__parts[2]
                for i in range(2, len(self.__parts)):
                    self.__result += self.__parts[i]
            else:
                print("ORG.GCLEANER.APP.SPECS: [ERROR::Unknown LSPCI format: "
                                                   + str(self.__parts[0])
                                                   + str(self.__parts[1]) + "]")
                self.__result = "Unknown"

            if "Intel" in self.__result:
                self.__graphics = "Video Intel"
            elif "NVIDIA" in self.__result:
                self.__graphics = "Video NVIDIA"
            elif "AMD" in self.__result:
                self.__graphics = "Video AMD"
            elif "Radeon" in self.__result:
                self.__graphics = "Video AMD Radeon"
            elif "VMware" in self.__result:
                self.__graphics = "Video VMware"
            else:
                self.__graphics = "Video Generic"

        except Exception as err:
            print("ORG.GCLEANER.APP.SPECS: [ERROR:: Video: ", str(err) + "]")
            self.__graphics = "VIDEO DESCONOCIDO"

        return self.__graphics

    def get_os_architecture(self):
        self.__architecture = ""
        try:
            self.__arch = os.popen("uname -m").readlines()
            self.__arch = self.__arch[0].replace("\n","")
            if self.__arch == "x86_64":
                self.__architecture = "64-bit"
            elif "arm" in self.__arch:
                self.__architecture = "ARM"
            else:
                self.__architecture = "32-bit"

        except Exception as err:
            print("ORG.GCLEANER.APP.SPECS: [ERROR:: ARCHITECTURE: ", str(err) + "]")
            self.__architecture = "NO ARCH"

        return self.__architecture

    def get_os_information(self):
        # System Operating Information
        self.__os = ""
        self.__version = ""
        self.__codename = ""
        try:
            # Dump the contents of 'file' to 'distribution' to process information
            self.__distribution = open("/etc/os-release", "r")
            self.__line = ""

            # Read line by line
            for self.__line in self.__distribution.readlines():
                # If find the Distribution Name clean in a variable the value of the same
                if "NAME=" in self.__line and self.__os == "":
                    self.__os = self.__line.replace("NAME=", "")
                    self.__os = self.__os.replace("\n", "")
                    if "\"" in self.__os:
                        self.__os = self.__os.replace("\"", "")
                elif "VERSION_ID=" in self.__line:
                    self.__version = self.__line.replace("VERSION_ID=", "")
                    self.__version = self.__version.replace("\n", "")
                    if "\"" in self.__version:
                        self.__version = self.__version.replace("\"", "")
                elif "VERSION_CODENAME=" in self.__line:
                    self.__codename = self.__line.replace ("VERSION_CODENAME=", "");
                    self.__codename = self.__codename.replace("\n", "")
                    self.__codename = self.__codename.capitalize()
                elif self.__codename == "" and "VARIANT_ID=" in self.__line:
                    self.__codename = self.__line.replace ("VARIANT_ID=", "");
                    self.__codename = self.__codename.replace("\n", "")
                    self.__codename = self.__codename.capitalize()
                    if "\"" in self.__codename:
                        self.__codename = self.__codename.replace("\"", "")

        except Exception as err:
            print("ORG.GCLEANER.APP.SPECS: [ERROR:: OS: /etc/os-release file not found]")
            print(">>> Error: " + str(err))
            self.__os = "Unknown"
            self.__version = "X"
            self.__codename = "X"

        # The architecture is obtained to build the entire chain of the operating system
        self.__architecture = self.get_os_architecture()
        self.__os_completo = self.__os + " " + self.__version + " (" + self.__codename + ") " + self.__architecture

        return self.__os_completo
