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

import ipaddress

from .tools.ping import Ping
from .tools.hostname import Hostname


class Network(object):
    def __init__(self, name, ip1, ip2, check_mac, check_host, check_ping):
        self.name = name
        self.ip1 = ip1
        self.ip2 = ip2
        self.check_mac = check_mac
        self.check_host = check_host
        self.check_ping = check_ping
        self.tool_ping = Ping()

    def __repr__(self):
        return '<nimn.Network: %s>' % (self.name, )

    def range(self):
        """Get the list of all the IPs in the network"""
        ip1 = ipaddress.IPv4Address(self.ip1)
        ip2 = ipaddress.IPv4Address(self.ip2)
        results = []
        while ip1 <= ip2:
            results.append(str(ip1))
            ip1 += 1
        return results
