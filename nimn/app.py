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

import os.path
import time
from collections import OrderedDict

from .constants import (
    FILE_HOSTS,
    TOOLS_LIST,
    TOOL_PING,
    TOOL_ARPING,
    TOOL_HOSTNAME,
    VERBOSE_LEVEL_QUIET,
    VERBOSE_LEVEL_HIGH,
    VERBOSE_LEVEL_MAX
)
from .settings import Settings
from .dbhosts import DBHosts, MAC_ADDRESS, HOSTNAME
from .command_line import CommandLine
from .network import Network, network_range, network_cidr
from .tools import tools
from .printf import printf

class Application(object):
    def __init__(self):
        """Create the application object"""
        self.command_line = CommandLine()
        self.arguments = self.command_line.arguments
        self.settings = Settings(self.command_line)
        self.dbhosts = DBHosts(self.settings)
        self.check_command_line()

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
        results = OrderedDict()
        while True:
            scan_results = self.do_scan(network)
            # Prints command, output and errors
            is_verbose = (self.command_line.arguments.verbose_level >=
                          VERBOSE_LEVEL_HIGH)
            for ip in scan_results:
                for tool in TOOLS_LIST:
                    if is_verbose or scan_results[ip][tool].error:
                        self.settings.log_normal(
                            'IP: {ip} TOOL: {tool}'.format(ip=ip, tool=tool))
                    self.settings.log_verbose(
                        'Command line for IP {ip} [{tool}]: {data}'.format(
                            ip=ip,
                            tool=tool,
                            data=scan_results[ip][tool].command))
                    self.settings.log_verbose_max(
                        'Output: {output}'.format(
                            output=scan_results[ip][tool].output))
                    if is_verbose or scan_results[ip][tool].error:
                        self.settings.log_normal(
                            'Error: {error}'.format(
                                error=scan_results[ip][tool].error))
            # Sum results in collect option
            if self.arguments.collect:
                for ip in scan_results:
                    # Add missing host
                    if ip not in results:
                        results[ip] = scan_results[ip]
                    # Merge results
                    if scan_results[ip][TOOL_ARPING].data is not None:
                        results[ip][TOOL_ARPING].data = (
                            scan_results[ip][TOOL_ARPING].data)
                    if scan_results[ip][TOOL_HOSTNAME].data != ip:
                        results[ip][TOOL_HOSTNAME].data = (
                            scan_results[ip][TOOL_HOSTNAME].data)
            else:
                results = scan_results
            # Compare data or print results
            if self.arguments.timestamp is not None:
                compare = self.dbhosts.get_detections(self.arguments.timestamp)
            printf('S IP Address          MAC address         Hostname'
                   '                      Message')
            printf('-' * 120)
            for ip in results:
                detail_msg = ''
                host_mac = results[ip][TOOL_ARPING].data
                if host_mac is None:
                    host_mac = '-'
                host_hostname = results[ip][TOOL_HOSTNAME].data
                host_ping = results[ip][TOOL_PING].data
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
                    elif host_mac == '-' and compare[ip][MAC_ADDRESS].data:
                        host_symbol = '-'
                        detail_msg = ('MAC address lost: {mac}').format(
                                          mac=compare[ip][MAC_ADDRESS].data)
                    elif (compare[ip][MAC_ADDRESS].data !=
                            results[ip][TOOL_ARPING].data):
                        host_symbol = 'M'
                        detail_msg = ('MAC address changed: old {mac}').format(
                                          mac=compare[ip][MAC_ADDRESS].data)
                    elif (compare[ip][HOSTNAME].data !=
                            results[ip][TOOL_HOSTNAME].data):
                        host_symbol = 'h'
                        detail_msg = ('Hostname changed: old {old}').format(
                                          old=compare[ip][HOSTNAME].data)
                    else:
                        host_symbol = ' '
                if host_symbol != ' ' or not self.arguments.changed:
                    printf('{symbol} {ip:20}{mac:20}{hostname:30}{message}'.format(
                           symbol=host_symbol,
                           ip=ip,
                           mac=host_mac,
                           hostname=host_hostname,
                           ping=host_ping,
                           message=detail_msg
                          ))
            # Exit from loop
            if not self.arguments.watch:
                break
            else:
                # Loop for watch mode
                printf('')
                printf('Watch mode, sleeping for {wait} seconds...'.format(
                           wait=self.arguments.watch), end='', flush=True)
                time.sleep(self.arguments.watch)
                printf(' scanning now')
        return results

    def check_command_line(self):
        """Check command line arguments"""
        self.arguments.verbose_level = min(max(self.arguments.verbose_level,
                                               VERBOSE_LEVEL_QUIET),
                                           VERBOSE_LEVEL_MAX)
        # If no database exists create it
        if not os.path.getsize(FILE_HOSTS) or self.arguments.create_schema:
            self.dbhosts.close()
            os.unlink(FILE_HOSTS)
        if not os.path.exists(FILE_HOSTS):
            self.dbhosts = DBHosts(self.settings)
            self.dbhosts.create_schema()
        # Check command line arguments
        if self.arguments.list_configurations:
            # List networks list
            printf('Network configurations list:')
            for network in self.dbhosts.list_networks():
                printf('  {network}'.format(network=network))
            self.command_line.parser.exit(1)
        elif self.arguments.collect and not self.arguments.watch:
            # Check collect option
            self.command_line.parser.error(
                'The collect (--collect) option requires watch (--watch) mode')
        elif not self.arguments.network:
            # Missing both networks list and network name
            self.command_line.parser.error('Network must be provided')

    def do_scan(self, network):
        for tool in TOOLS_LIST:
            # Prepare the workers
            tools[tool].prepare()
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
                                       mac=results[ip][TOOL_ARPING].data,
                                       hostname=results[ip][TOOL_HOSTNAME].data
                                      )
        return results
