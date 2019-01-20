#!/usr/bin/env python


"""Main application module
"""

import sys
import logging
from argparse import ArgumentParser

from weatherapp.core import config
from weatherapp.core.commandmanager import CommandManager
from weatherapp.core.providermanager import ProviderManager


class App:
    """  Weather agregator application.
    """

    logger = logging.getLogger(__name__)
    LOG_LEVEL_MAP = {0: logging.WARNING,
                     1: logging.INFO,
                     2: logging.DEBUG}

    def __init__(self):
        self.arg_parser = self._arg_parse()
        self.providermanager = ProviderManager()
        self.commandmanager = CommandManager()


    def _arg_parse(self):
        """Initialize argument parser
        """
        
        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('command', help="Command", nargs='?')
        arg_parser.add_argument('--refresh', help="Bypass caches",
                                action='store_true')
        arg_parser.add_argument('--debug',
                                action='store_true',
                                default=False,
                                help="Bypass catching errors")
        arg_parser.add_argument('-v', '--verbose',
                                action='count',
                                dest='verbose_level',
                                default=config.DEFAULT_VERBOSE_LEVEL,
                                help='Increase verbosity of output.')
        return arg_parser

    def configure_logging(self):
        """Create logging handlers for any log output.
        """
        
        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        console_level = self.LOG_LEVEL_MAP.get(self.options.verbose_level,
                                               logging.WARNING)
        console.setLevel(console_level)
        formatter = logging.Formatter(config.DEFAULT_MESSAGE_FORMAT)
        console.setFormatter(formatter)
        root_logger.addHandler(console)
        
    def produce_output(self, title, location, info):
        """Print results.
        """
        print(f'{title}:')
        print("#"*10, end="\n\n")
        
        print(f'{location}')
        print('_'*20)
        
        for key, value in info.items():
            print(f'{key}: {value}')
        print("="*40, end="\n\n")


    def run(self, argv):
        """Run application.

        :parm argv: list of passed arguments
        """
        self.options, remaining_args = self.arg_parser.parse_known_args(argv)
        self.configure_logging()
        self.logger.debug('Got the following args %s', argv)
        command_name = self.options.command

        if command_name in self.commandmanager:
            command_factory = self.commandmanager.get(command_name)
            try:
                return command_factory(self).run(remaining_args)
            except Exception:
                msg = "Error during command: %s run"
                if self.options.debug:
                    self.logger.exception(msg, command_name)
                else:
                    self.logger.error(msg, command_name)

        if not command_name:
            # run all weather providers by default
            for name, provider in self.providermanager._providers.items():
                self.produce_output(provider.title,
                               provider(self).location,
                               provider(self).run(remaining_args))
            
        elif command_name in self.providermanager:
            # run specified provider
            provider = self.providermanager[command_name](self)
            self.produce_output(provider.title,
                           provider.location,
                           provider.run(remaining_args))
            
def main(argv=sys.argv[1:]):
    """Main entry point
    """
#    if argv and argv[0]=='--debug':
    return App().run(argv)
#    else:
#        try:
#            return App().run(argv)
#        except:
#            print("An error ocured. Programm stopped running. "
#                  "Please contact developer.")

if __name__ == '__main__':
    main(sys.argv[1:])

#end
