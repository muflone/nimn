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

from collections import OrderedDict

from .constants import *
from .settings import Settings
from .dbhosts import DBHosts


class Application(object):
    def __init__(self):
        """Create the application object"""
        self.settings = Settings()
        self.dbhosts = DBHosts()

    def startup(self):
        """Configure the application during the startup"""
        pass

    def run(self):
        """Execute the application"""
        if self.settings.arguments.configuration:
            # Use a saved configuration for network
            networks_list = self.dbhosts.list_networks()
            network = networks_list[self.settings.arguments.network]
        network.tool_ping.interface = self.settings.arguments.interface
        network.tool_arping.interface = self.settings.arguments.interface
        network.tool_hostname.interface = self.settings.arguments.interface
        for address in network.range():
            if network.check_ping:
                # Check the host using PING
                network.tool_ping.execute(address)
            if network.check_arping:
                # Check the host using ARPING
                network.tool_arping.execute(address)
            if network.check_host:
                # Get hostname from the address
                network.tool_hostname.execute(address)
        # Start the tools threads
        network.tool_ping.start()
        network.tool_arping.start()
        network.tool_hostname.start()
        # Awaits the tools to complete
        network.tool_ping.process()
        network.tool_arping.process()
        network.tool_hostname.process()
        # Sort data and print results
        results = OrderedDict()
        for address in network.range():
            data = {}
            data['ping'] = (network.tool_ping.results[address]
                            if network.check_ping else None)
            data['arping'] = (network.tool_arping.results[address]
                              if network.check_arping else None)
            data['hostname'] = (network.tool_hostname.results[address]
                                if network.check_host else None)
            results[address] = data
        for data in results:
            print(data, results[data])
        return results
