##
#     Project: New in my net
# Description: Find new devices in my network
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2018 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import os
import os.path
import time
import sys

if sys.version_info.major == 3:
    import configparser
else:
    import ConfigParser as configparser

from .printf import printf
from .constants import (
  VERBOSE_LEVEL_NORMAL,
  VERBOSE_LEVEL_HIGH,
  VERBOSE_LEVEL_MAX,
  VERBOSE_LEVEL_DEBUG,
  FILE_SETTINGS,
)

SECTION_APPLICATION = 'application'


class Settings(object):
    def __init__(self, command_line):
        self.command_line = command_line
        # Parse settings from the configuration file
        self.config = configparser.RawConfigParser()
        self.filename = FILE_SETTINGS
        self.log_verbose('Loading settings from %s' % self.filename)
        self.config.read(self.filename)

    def get(self, section, option, default=None):
        """Get an option from a specific section"""
        if self.config.has_section(section) and \
                self.config.has_option(section, option):
            return self.config.get(section, option)
        else:
            return default

    def set(self, section, option, value):
        """Save an option in a specific section"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def get_boolean(self, section, option, default=None):
        """Get a boolean option from a specific section"""
        return self.get(section, option, default) == '1'

    def set_boolean(self, section, option, value):
        """Save a boolean option in a specific section"""
        self.set(section, option, '1' if value else '0')

    def get_int(self, section, option, default=0):
        """Get an integer option from a specific section"""
        return int(self.get(section, option, default))

    def set_int(self, section, option, value):
        """Set an integer option from a specific section"""
        self.set(section, option, int(value))

    def get_setting(self, setting, default=None):
        """Get the specified setting with a fallback value"""
        section, option, option_type = setting
        if option_type is int:
            return self.get_int(section, option, default and default or 0)
        elif option_type is bool:
            return self.get_boolean(section, option, default if True else False)
        else:
            return self.get(section, option, default)

    def set_setting(self, setting, value):
        """Set the specified setting"""
        section, option, option_type = setting
        if option_type is int:
            return self.set_int(section, option, value)
        elif option_type is bool:
            return self.set_boolean(section, option, value)
        else:
            return self.set(section, option, value)

    def save(self):
        """Save the whole configuration"""
        file_settings = open(self.filename, mode='w')
        self.log_verbose('Saving settings to %s' % self.filename)
        self.config.write(file_settings)
        file_settings.close()

    def log_text(self, text):
        """Print a text with current date and time"""
        printf(objects='[%s] %s' % (time.strftime('%Y/%m/%d %H:%M:%S'), text),
               file=sys.stderr)

    def log_normal(self, text, verbose_level=VERBOSE_LEVEL_NORMAL):
        """Print a text with current date and time based on verbose level"""
        if self.command_line.arguments.verbose_level >= VERBOSE_LEVEL_NORMAL:
            self.log_text(text)

    def log_verbose(self, text):
        """Print a text with current date and time based on verbose level"""
        if self.command_line.arguments.verbose_level >= VERBOSE_LEVEL_HIGH:
            self.log_text(text)

    def log_verbose_max(self, text):
        """Print a text with current date and time based on verbose level"""
        if self.command_line.arguments.verbose_level >= VERBOSE_LEVEL_MAX:
            self.log_text(text)

    def log_verbose_debug(self, text):
        """Print a text with current date and time based on verbose level"""
        if self.command_line.arguments.verbose_level >= VERBOSE_LEVEL_DEBUG:
            self.log_text(text)
