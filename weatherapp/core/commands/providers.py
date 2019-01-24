import sys

from weatherapp.core.abstract import Command


class Providers(Command):
    """Print list of all providers.
    """

    stdout = sys.stdout
    name = 'providers'

    def run(self, argv):
        """Run command.
        """
        
        for name in self.app.providermanager._providers:
            self.stdout.write(f'{name} \n')
