from weatherapp.core.abstract import Command


class Providers(Command):
    """Print list of all providers.
    """

    name = 'providers'

    def run(self, argv):
        """Run command.
        """
        
        for name in self.app.providermanager._providers:
            print(name)
