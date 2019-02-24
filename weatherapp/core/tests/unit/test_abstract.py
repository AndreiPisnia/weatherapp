import abc
import unittest
import unittest.mock

from weatherapp.core.abstract import Command
from weatherapp.core.abstract import Formatter
from weatherapp.core.abstract import Manager
from weatherapp.core.abstract import WeatherProvider

class AbstractTestCase(unittest.TestCase):
    """Test abstract class creation.
    """
   
    @unittest.mock.patch.multiple(Command, __abstractmethods__=set())
    def test_command_instance(self):
        """ Test formatter instance creation.
        """    
        self.instance = Command('app')
        self.assertIsInstance(self.instance, Command)
        
        print('test abstract formatter complete')


    @unittest.mock.patch.multiple(Formatter, __abstractmethods__=set())
    def test_formatter_instance(self):
        """ Test formatter instance creation.
        """    
        self.instance = Formatter()
        self.assertIsInstance(self.instance, Formatter)
        
        print('test abstract formatter complete')

    @unittest.mock.patch.multiple(Manager, __abstractmethods__=set())
    def test_manager_instance(self):
        """ Test manager instance creation.
        """    
        self.instance_manager = Manager()
        self.assertIsInstance(self.instance_manager, Manager)
        
        print('test abstract manager complete')

    @unittest.mock.patch.multiple(WeatherProvider, __abstractmethods__=set())
    def test_provider_instance(self):
        """ Test provider class instance creation.
        """    
        self.instance_provider = WeatherProvider('app')
        self.assertIsInstance(self.instance_provider, WeatherProvider)
        
        print('test abstract class provider complete')



if __name__ == '__main__':
    unittest.main()
    
