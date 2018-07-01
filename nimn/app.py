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

from .constants import TOOLS_LIST, TOOL_PING, TOOL_ARPING, TOOL_HOSTNAME
from .settings import Settings
from .dbhosts import DBHosts, MAC_ADDRESS, HOSTNAME
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
            tools[tool].timeout = self.arguments.timeout
        # Cycle over all the network addresses
        for address in network.range():
            # Cycle over all the available tools
            for tool in TOOLS_LIST:
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
                # Get results for the tool
                data[tool] = tools[tool].results[address]
            results[address] = data
        # Save detections
        for ip in results:
            self.dbhosts.add_detection(ip=ip,
                                       mac=results[ip][TOOL_ARPING],
                                       hostname=results[ip][TOOL_HOSTNAME])
        # Compare data or print results
        if self.arguments.timestamp is not None:
            compare = self.dbhosts.get_detections(self.arguments.timestamp)
        print('S IP Address          MAC address         Hostname'
              '                      Message')
        print('-' * 120)
        for ip in results:
            detail_msg = ''
            host_mac = results[ip][TOOL_ARPING]
            if host_mac is None:
                host_mac = '-'
            host_hostname = results[ip][TOOL_HOSTNAME]
            host_ping = results[ip][TOOL_PING]
            if self.arguments.timestamp is None:
                # No compare
                host_symbol = '>'
            else:
                # Compare results
                if ip not in compare and (host_mac != '-'
                                          or host_hostname
                                          or host_ping):
                    # New host but no information, skipped
                    continue
                elif ip not in compare:
                    # New host
                    host_symbol = '+'
                    detail_msg = 'New host added'
                elif not host_mac and compare[ip][MAC_ADDRESS]:
                    host_symbol = '-'
                    detail_msg = ('MAC address lost: {mac}').format(
                                      mac=compare[ip][MAC_ADDRESS])
                elif compare[ip][MAC_ADDRESS] != results[ip][TOOL_ARPING]:
                    host_symbol = '~'
                    detail_msg = ('MAC address changed: old {mac}').format(
                                      mac=compare[ip][MAC_ADDRESS])
                elif compare[ip][HOSTNAME] != results[ip][TOOL_HOSTNAME]:
                    host_symbol = 'h'
                    detail_msg = ('Hostname changed: old {old}').format(
                                      old=compare[ip][HOSTNAME])
                else:
                    host_symbol = ' '
            if host_symbol != ' ' or not self.arguments.changed:
                print('{symbol} {ip:20}{mac:20}{hostname:30}{message}'.format(
                    symbol=host_symbol,
                    ip=ip,
                    mac=host_mac,
                    hostname=host_hostname,
                    ping=host_ping,
                    message=detail_msg
                ))
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
