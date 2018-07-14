import argparse

from .constants import (
    VERBOSE_LEVEL_QUIET,
    VERBOSE_LEVEL_NORMAL,
    TOOLS_LIST,
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
)


class CommandLine(object):
    def __init__(self):
        """Parse command line arguments"""
        self.parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
        self.parser.set_defaults(verbose_level=VERBOSE_LEVEL_NORMAL)
        self.parser.add_argument('-I', '--interface',
                                 type=str,
                                 dest='interface',
                                 action='store',
                                 help='interface name to use')
        self.parser.add_argument('-n', '--count',
                                 type=int,
                                 default=1,
                                 dest='checks',
                                 action='store',
                                 help='max checks to do for each tool')
        self.parser.add_argument('-t', '--timeout',
                                 type=int,
                                 default=None,
                                 dest='timeout',
                                 action='store',
                                 help='max timeout in seconds for each request')
        self.parser.add_argument('-w', '--watch',
                                 type=int,
                                 default=None,
                                 dest='watch',
                                 action='store',
                                 help='watch mode (wait time in seconds)')
        self.parser.add_argument('-c', '--collect',
                                 default=None,
                                 dest='collect',
                                 action='store_true',
                                 help='collect data during watch mode')
        self.parser.add_argument('-C', '--configuration',
                                 dest='configuration',
                                 action='store_true',
                                 help='use saved configuration for network name')
        self.parser.add_argument('-V', '--version',
                                 dest='version',
                                 action='version',
                                 version='{app} {version}'.format(
                                     app=APP_NAME,
                                     version=APP_VERSION),
                                 help='show version number')
        self.parser.add_argument('-v', '--verbose', dest='verbose_level',
                                 action='count',
                                 help='show error and information messages')
        self.parser.add_argument('-q', '--quiet',
                                 dest='verbose_level',
                                 action='store_const',
                                 const=VERBOSE_LEVEL_QUIET,
                                 help='hide error and information messages')
        self.parser.add_argument('-T', '--timestamp',
                                 type=int,
                                 dest='timestamp',
                                 action='store',
                                 help='timestamp to compare')
        self.parser.add_argument('-O', '--changed',
                                 dest='changed',
                                 action='store_true',
                                 help='show only changed host during compare')
        self.parser.add_argument('network',
                                 type=str,
                                 nargs='*',
                                 action='store',
                                 help='network name or network range')
        self.parser.add_argument('-l', '--list-configurations',
                                 dest='list_configurations',
                                 action='store_true',
                                 help='list saved network configurations')
        self.arguments = self.parser.parse_args()
