#!/usr/bin/env python


"""Main application module
"""

import sys
from argparse import ArgumentParser

from commandmanager import CommandManager
from providermanager import ProviderManager


class App:
    """  Weather agregator application.
    """

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
        return arg_parser


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
        command_name = self.options.command

        if command_name in self.commandmanager:
            command_factory = self.commandmanager.get(command_name)
            return command_factory(self).run(remaining_args)

        if not command_name:
            # run all weather providers by default
            for name, provider in self.providermanager._providers.items():
#                provider_obj = provider(self)
                self.produce_output(provider.title,
                               provider(self).location,
                               provider(self).run(remaining_args))

#                self.produce_output(provider_obj.title,
#                               provider_obj.location,
#                               provider_obj.run(remaining_args))
            
        elif command_name in self.providermanager:
            # run specified provider
            provider = self.providermanager[command_name](self)
#            provider_obj = provider(self)
            self.produce_output(provider.title,
                           provider.location,
                           provider.run(remaining_args))
            
def main(argv=sys.argv[1:]):
    """Main entry point
    """
    try:
        return App().run(argv)
    except:
        print("An error ocured. Programm stopped running. "
              "Please contact developer.")


if __name__ == '__main__':
    main(sys.argv[1:])
