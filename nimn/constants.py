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

import sys
import os.path
from xdg import BaseDirectory

# Application constants
APP_NAME = 'New in my Net'
APP_VERSION = '0.2.0'
APP_DESCRIPTION = 'Find new devices in my network'
APP_ID = 'nimn.muflone.com'
APP_URL = 'http://www.muflone.com/nimn/'
APP_AUTHOR = 'Fabio Castelli'
APP_AUTHOR_EMAIL = 'muflone@vbsimple.net'
APP_COPYRIGHT = 'Copyright 2018 %s' % APP_AUTHOR
# Other constants
DOMAIN_NAME = 'nimn'
VERBOSE_LEVEL_QUIET = 0
VERBOSE_LEVEL_NORMAL = 1
VERBOSE_LEVEL_HIGH = 2
VERBOSE_LEVEL_MAX = 3
VERBOSE_LEVEL_DEBUG = 4
# Tools
TOOL_PING = 'ping'
TOOL_ARPING = 'arping'
TOOL_HOSTNAME = 'hostname'
TOOLS_LIST = (TOOL_PING, TOOL_ARPING, TOOL_HOSTNAME)

# Paths constants
# If there's a file data/nimn.png then the shared data are searched
# in relative paths, else the standard paths are used
if os.path.isfile(os.path.join('data', 'nimn.png')):
    DIR_PREFIX = '.'
    DIR_LOCALE = os.path.join(DIR_PREFIX, 'locale')
    DIR_DOCS = os.path.join(DIR_PREFIX, 'doc')
else:
    DIR_PREFIX = os.path.join(sys.prefix, 'share', 'nimn')
    DIR_LOCALE = os.path.join(sys.prefix, 'share', 'locale')
    DIR_DOCS = os.path.join(sys.prefix, 'share', 'doc', 'nimn')
# Set the paths for the folders
DIR_DATA = os.path.join(DIR_PREFIX, 'data')
DIR_SETTINGS = BaseDirectory.save_config_path(DOMAIN_NAME)
# Set the paths for the data files
FILE_ICON = os.path.join(DIR_DATA, 'nimn.png')
FILE_CONTRIBUTORS = os.path.join(DIR_DOCS, 'contributors')
FILE_TRANSLATORS = os.path.join(DIR_DOCS, 'translators')
FILE_LICENSE = os.path.join(DIR_DOCS, 'license')
FILE_RESOURCES = os.path.join(DIR_DOCS, 'resources')
# Set the paths for configuration files
FILE_HOSTS = os.path.join(DIR_SETTINGS, 'hosts.db')
FILE_SETTINGS = os.path.join(DIR_SETTINGS, 'settings.conf')
