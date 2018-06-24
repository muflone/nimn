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

from .constants import FILE_HOSTS
from .network import Network

import sqlite3
import os.path


class DBHosts(object):
    def __init__(self):
        if not os.path.exists(FILE_HOSTS):
            self.create_schema()
        self.connection = sqlite3.connect(FILE_HOSTS)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def close(self):
        """Close the database connection"""
        self.cursor.close()
        self.connection.close()

    def create_schema(self):
        """Create the database schema"""
        # TODO: create schema
        pass

    def list_networks(self):
        results = {}
        self.cursor.execute('SELECT * FROM networks')
        for row in self.cursor.fetchall():
            results[row['name']] = Network(row['name'],
                                           row['ip_starting'],
                                           row['ip_ending'],
                                           row['mac_lookup'],
                                           row['hostname_lookup'],
                                           row['ping'],
                                          )
        return results
