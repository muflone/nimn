import argparse

from .constants import (
  VERBOSE_LEVEL_QUIET,
  VERBOSE_LEVEL_NORMAL,
  VERBOSE_LEVEL_MAX,
  TOOLS_DEFAULT,
  TOOLS_LIST,
  APP_NAME,
  APP_VERSION,
  APP_DESCRIPTION,
)


class CommandLine(object):
    def __init__(self):
        """Parse command line arguments"""
        self.parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
        self.parser.set_defaults(verbose_level=VERBOSE_LEVEL_NORMAL,
                                    tools=TOOLS_DEFAULT)
        self.parser.add_argument('-I', '--interface',
                                    type=str,
                                    dest='interface',
                                    action='store',
                            help='interface name to use')
        self.parser.add_argument('-t', '--tools',
                                 type=str,
                                 dest='tools',
                                 action='store',
                                 nargs='+',
                                 choices=TOOLS_LIST,
                                 help='tools to use for checks')
        self.parser.add_argument('-a', '--all',
                                 dest='all_tools',
                                 action='store_true',
                                 help='show all tools in response')
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
                                 action='store_const',
                                 const=VERBOSE_LEVEL_MAX,
                                 help='show error and information messages')
        self.parser.add_argument('-q', '--quiet',
                                 dest='verbose_level',
                                 action='store_const',
                                 const=VERBOSE_LEVEL_QUIET,
                                 help='hide error and information messages')
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
