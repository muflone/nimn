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

from .constants import TOOLS_LIST
from .settings import Settings
from .dbhosts import DBHosts
from .command_line import CommandLine
from .network import Network, network_range, network_cidr
from .tools import tools

class Application(object):
    def __init__(self):
        """Create the application object"""
        self.command_line = CommandLine()
        self.arguments = self.command_line.arguments
        self.dbhosts = DBHosts()
        self.check_command_line()
        self.settings = Settings(self.command_line)

    def startup(self):
        """Configure the application during the startup"""
        pass

    def run(self):
        """Execute the application"""
        if self.arguments.configuration:
            # Use a saved configuration for network
            networks_list = self.dbhosts.list_networks()
            network = networks_list[self.arguments.network[0]]
        else:
            # Use the command line arguments for network
            if '-' in self.arguments.network[0]:
                # Network IP range
                (ip1, ip2) = network_range(self.arguments.network[0])
            elif '/' in self.arguments.network:
                # Network CIDR
                (ip1, ip2) = network_cidr(self.arguments.network[0])
            else:
                # Single IP address
                ip1 = self.arguments.network[0]
                ip2 = ip1
            network = Network(name='-',
                              ip1=ip1,
                              ip2=ip2)
        # Set tools parameters
        for tool in TOOLS_LIST:
            tools[tool].interface = self.arguments.interface
            tools[tool].checks = self.arguments.checks
        # Cycle over all the network addresses
        for address in network.range():
            # Cycle over all the available tools
            for tool in TOOLS_LIST:
                # If the tool was enabled then execute the checks
                if tool in self.arguments.tools:
                    # Check the host using the tool
                    tools[tool].execute(address)
        # Start the tools threads
        for tool in TOOLS_LIST:
            tools[tool].start()
        # Awaits the tools to complete
        for tool in TOOLS_LIST:
            tools[tool].process()
        # Sort data and print results
        results = OrderedDict()
        for address in network.range():
            data = {}
            for tool in TOOLS_LIST:
                if self.arguments.all_tools:
                    # Print results for all the tools, not only the enabled
                    data[tool] = (tools[tool].results[address]
                                  if tool in self.arguments.tools
                                  else None)
                elif tool in self.arguments.tools:
                    # Print results only for the enabled tools
                    data[tool] = tools[tool].results[address]
            results[address] = data
        # Print results
        for data in results:
            print('{ip:20}{results}'.format(ip=data,
                                            results=results[data]))
        return results

    def check_command_line(self):
        """Check command line arguments"""
        if self.arguments.list_configurations:
            # List networks list
            print('Network configurations list:')
            for network in self.dbhosts.list_networks():
                print('  {network}'.format(network=network))
            self.command_line.parser.exit(1)
        elif not self.arguments.network:
            # Missing both networks list and network name
            self.command_line.parser.error('Network must be provided')
