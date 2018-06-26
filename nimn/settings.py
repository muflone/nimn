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
import argparse
import time
import sys

if sys.version_info.major == 3:
    import configparser
else:
    import ConfigParser as configparser

from .functions import *
from .constants import *

SECTION_MAINWIN = 'main window'
SECTION_APPLICATION = 'application'

class Settings(object):
    def __init__(self):
        # Command line options and arguments
        parser = argparse.ArgumentParser(description='Find new devices in my network')
        parser.set_defaults(verbose_level=VERBOSE_LEVEL_NORMAL,
                            tools=TOOLS_DEFAULT)
        parser.add_argument('-I', '--interface',
                            type=str,
                            dest='interface',
                            action='store',
                            help='interface name to use')
        parser.add_argument('-t', '--tools',
                            type=str,
                            dest='tools',
                            action='store',
                            nargs='+',
                            choices=TOOLS_LIST,
                            help='tools to use for checks')
        parser.add_argument('-a', '--all',
                            dest='all_tools',
                            action='store_true',
                            help='show all tools in response')
        parser.add_argument('-C', '--configuration',
                            dest='configuration',
                            action='store_true',
                            help='use saved configuration for network name')
        parser.add_argument('-V', '--version',
                            dest='version',
                            action='version',
                            version='{app} {version}'.format(
                                app=APP_NAME,
                                version=APP_VERSION),
                            help='show version number')
        parser.add_argument('-v', '--verbose', dest='verbose_level',
                            action='store_const', const=VERBOSE_LEVEL_MAX,
                            help='show error and information messages')
        parser.add_argument('-q', '--quiet', dest='verbose_level',
                            action='store_const', const=VERBOSE_LEVEL_QUIET,
                            help='hide error and information messages')
        parser.add_argument('network',
                            type=str,
                            action='store',
                            help='network name or network range')
        self.arguments = parser.parse_args()

        # Parse settings from the configuration file
        self.config = configparser.RawConfigParser()
        # Determine which filename to use for settings
        self.filename = FILE_SETTINGS
        if self.filename:
            self.logText('Loading settings from %s' % self.filename,
                         VERBOSE_LEVEL_MAX)
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
        self.logText('Saving settings to %s' % self.filename,
                     VERBOSE_LEVEL_MAX)
        self.config.write(file_settings)
        file_settings.close()

    def logText(self, text, verbose_level=VERBOSE_LEVEL_NORMAL):
        """Print a text with current date and time based on verbose level"""
        if verbose_level <= self.arguments.verbose_level:
            print('[%s] %s' % (time.strftime('%Y/%m/%d %H:%M:%S'), text))
