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

if sys.version_info.major == 3:
    import queue
else:
    import Queue as queue

import threading


class ManagedQueue(object):
    def __init__(self, cb_function, workers):
        self.cb_function = cb_function
        # Queue for requests and responses
        self.queue_incoming = queue.Queue()
        self.queue_results = queue.Queue()
        self.results = {}
        # Setup running worker threads
        self.workers = []
        for _ in range(workers):
            worker_thread = threading.Thread(target=self.consumer)
            self.workers.append(worker_thread)

    def execute(self, data):
        """Add new data to the queue"""
        # print('add new data %s to queue %s' % (data, self.__class__.__name__))
        self.queue_incoming.put(data)

    def consumer(self):
        """Extract data from the queue and process it"""
        try:
            while True:
                # Get the next data
                data = self.queue_incoming.get_nowait()
                # print('get data %s from queue %s' % (data, self.__class__.__name__))
                self.queue_results.put((data, self.cb_function(data)))
        except queue.Empty:
            # No more data to process
            pass
        finally:
            # Work done, thread can terminate
            pass
            # self.queue_results.put(None)

    def start(self):
        """Execute the running threads"""
        for worker in self.workers:
            worker.daemon = True
            worker.start()

    def process(self):
        """Awaits the running threads for completion"""
        for worker in self.workers:
            worker.join()
        # Get results from queue
        for data in self.queue_results.queue:
            self.results[data[0]] = data[1]
        return self.results
