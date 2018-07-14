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

import subprocess
import platform

from .managed_queue import ManagedQueue
from .tool_results import ToolResults

NUM_WORKERS = 20


class Ping(ManagedQueue):
    def __init__(self):
        ManagedQueue.__init__(self, self.do_process, NUM_WORKERS)

    def do_process(self, address):
        command = ['ping',
                   '-n' if platform.system().lower() == 'windows' else '-c',
                   str(self.checks)]
        # If provided, add interface name
        if self.interface:
            command.append('-I')
            command.append(self.interface)
        # If provided, add timeout
        if self.timeout:
            command.append('-w')
            command.append(str(self.timeout))
        # Add destination address
        command.append(address)
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        (stdout, stderr) = process.communicate()
        return ToolResults(process.poll() == 0, command, stdout, stderr)
