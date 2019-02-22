import unittest
import argparse

from weatherapp.core.app import App

class AppTestCase(unittest.TestCase):
    """Test application class method.
    """
   

    def setUp(self):
        self.parser = App._arg_parse(self)

    def test_arg_parser(self):
        """ Test application argument parser creation.
        """    

        self.assertIsInstance(self.parser, argparse.ArgumentParser)
        
        print('test complete')

    def test_arg_parser_default_values(self):

        parsed_args = self.parser.parse_args([])
        self.assertIsNone(parsed_args.command)
        self.assertFalse(parsed_args.debug)
