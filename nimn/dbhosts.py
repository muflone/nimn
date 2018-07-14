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

MAC_ADDRESS = 'MAC'
HOSTNAME = 'HOSTNAME'

from .constants import FILE_HOSTS
from .network import Network

import sqlite3
import time


class DBHosts(object):
    def __init__(self, settings):
        self.connection = sqlite3.connect(FILE_HOSTS)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.settings = settings

    def close(self):
        """Close the database connection"""
        self.cursor.close()
        self.connection.close()

    def create_schema(self):
        """Create the database schema"""
        self.settings.log_verbose('Creating database schema')
        self.settings.log_verbose_max('Creating table detections')
        self.cursor.execute('CREATE TABLE "detections" ('
                            '  "timestamp" INTEGER NOT NULL,'
                            '  "ip" TEXT NOT NULL,'
                            '  "mac" TEXT NULL,'
                            '  "hostname" TEXT NOT NULL,'
                            '  PRIMARY KEY (timestamp, ip)'
                            ')'
                           )
        self.settings.log_verbose_max('Creating table networks')
        self.cursor.execute('CREATE TABLE "networks" ('
                            '  "name" TEXT NOT NULL,'
                            '  "ip_starting" TEXT NOT NULL,'
                            '  "ip_ending" TEXT NOT NULL,'
                            '  PRIMARY KEY (name)'
                            ')'
                           )
        self.settings.log_verbose_max('Saving schema')
        self.connection.commit()
        self.settings.log_verbose_max('Database schema created')

    def list_networks(self):
        results = {}
        self.cursor.execute('SELECT * FROM networks')
        for row in self.cursor.fetchall():
            results[row['name']] = Network(row['name'],
                                           row['ip_starting'],
                                           row['ip_ending'],
                                          )
        return results

    def add_detection(self, ip, mac, hostname):
        """Add a new detection record for the ip address"""
        timestamp = time.time()
        self.cursor.execute('INSERT INTO detections '
                            '(timestamp, ip, mac, hostname) '
                            'VALUES(?, ?, ?, ?)',
                            (int(timestamp), ip, mac, hostname)
                           )
        self.connection.commit()

    def get_detections(self, timestamp):
        """Get detections for the specified timestamp"""
        results = {}
        self.cursor.execute('SELECT * FROM detections '
                            'WHERE timestamp=?',
                            (timestamp, ))
        for row in self.cursor.fetchall():
            response = {}
            response[MAC_ADDRESS] = row['mac']
            response[HOSTNAME] = row['hostname']
            results[row['ip']] = response
        return results
