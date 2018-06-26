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
import ipaddress

from .tools.ping import Ping
from .tools.arping import ARPing
from .tools.hostname import Hostname

if sys.version_info.major == 3:
    unicode = str


class Network(object):
    def __init__(self, name, ip1, ip2, check_host, check_ping, check_arping):
        self.name = name
        self.ip1 = ip1
        self.ip2 = ip2
        self.check_host = check_host
        self.check_ping = check_ping
        self.check_arping = check_arping
        self.tool_ping = Ping()
        self.tool_arping = ARPing()
        self.tool_hostname = Hostname()

    def __repr__(self):
        return '<nimn.Network: %s>' % (self.name, )

    def range(self):
        """Get the list of all the IPs in the network"""
        ip1 = ipaddress.IPv4Address(unicode(self.ip1))
        ip2 = ipaddress.IPv4Address(unicode(self.ip2))
        results = []
        while ip1 <= ip2:
            results.append(str(ip1))
            ip1 += 1
        return results


def network_range(ip_range):
    """
    Return the first host and the last host of a network segment in the form of
    x.x.x.x-y.y.y.y.y (e.g. 192.168.1.10-192.168.1.50)
    """
    hosts = ip_range.split('-', 1)
    return (hosts[0], hosts[1])


def network_cidr(cidr):
    """
    Return the first host and the last host of a network CIDR in the form of
    x.x.x.x/n (e.g. 192.168.1.8/24)
    """
    hosts = list(ipaddress.ip_network(unicode(cidr)).hosts())
    return (hosts[0], hosts[-1])
