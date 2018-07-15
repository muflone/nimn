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

import argparse

from .constants import (
    VERBOSE_LEVEL_QUIET,
    VERBOSE_LEVEL_NORMAL,
    TOOLS_LIST,
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
)


class CommandLine(object):
    def __init__(self):
        """Parse command line arguments"""
        self.parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
        self.parser.set_defaults(verbose_level=VERBOSE_LEVEL_NORMAL)
        self.parser.add_argument('-I', '--interface',
                                 type=str,
                                 dest='interface',
                                 action='store',
                                 help='interface name to use')
        self.parser.add_argument('-n', '--count',
                                 type=int,
                                 default=1,
                                 dest='checks',
                                 action='store',
                                 help='max checks to do for each tool')
        self.parser.add_argument('-t', '--timeout',
                                 type=int,
                                 default=None,
                                 dest='timeout',
                                 action='store',
                                 help='max timeout in seconds for each request')
        self.parser.add_argument('-w', '--watch',
                                 type=int,
                                 default=None,
                                 dest='watch',
                                 action='store',
                                 help='watch mode (wait time in seconds)')
        self.parser.add_argument('-c', '--collect',
                                 default=None,
                                 dest='collect',
                                 action='store_true',
                                 help='collect data during watch mode')
        self.parser.add_argument('-W', '--workers',
                                 type=int,
                                 default=10,
                                 dest='workers',
                                 action='store',
                                 help='number of parallel workers')
        self.parser.add_argument('-C', '--configuration',
                                 dest='configuration',
                                 action='store_true',
                                 help='use saved configuration for network name')
        self.parser.add_argument('-V', '--version',
                                 dest='version',
                                 action='version',
                                 version='{app} {version}'.format(
                                     app=APP_NAME,
                                     version=APP_VERSION),
                                 help='show version number')
        self.parser.add_argument('-v', '--verbose', dest='verbose_level',
                                 action='count',
                                 help='show error and information messages')
        self.parser.add_argument('-q', '--quiet',
                                 dest='verbose_level',
                                 action='store_const',
                                 const=VERBOSE_LEVEL_QUIET,
                                 help='hide error and information messages')
        self.parser.add_argument('-T', '--timestamp',
                                 type=int,
                                 dest='timestamp',
                                 action='store',
                                 help='timestamp to compare')
        self.parser.add_argument('-O', '--changed',
                                 dest='changed',
                                 action='store_true',
                                 help='show only changed host during compare')
        self.parser.add_argument('network',
                                 type=str,
                                 nargs='*',
                                 action='store',
                                 help='network name or network range')
        self.parser.add_argument('-l', '--list-configurations',
                                 dest='list_configurations',
                                 action='store_true',
                                 help='list saved network configurations')
        self.parser.add_argument('--create-schema',
                                 dest='create_schema',
                                 action='store_true',
                                 help='create the database schema')
        self.arguments = self.parser.parse_args()
