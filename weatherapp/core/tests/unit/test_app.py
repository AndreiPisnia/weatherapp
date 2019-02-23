import unittest
import argparse

from weatherapp.core.app import App

class AppTestCase(unittest.TestCase):
    """Test application class method.
    """
   

    def setUp(self):
        self.parser = App._arg_parse(self)

    def test_arg_parse(self):
        """ Test application argument parser creation.
        """    

        self.assertIsInstance(self.parser, argparse.ArgumentParser)
        
        print('test 1 complete')

    def test_arg_parser_default_values(self):
        """Test application argument parser default values.
        """

        parsed_args = self.parser.parse_args([])
        self.assertIsNone(parsed_args.command)
        self.assertEqual(parsed_args.formatter, 'table')
        self.assertFalse(parsed_args.debug)
        
    def test_arg_parser_arg(self):
        """Test application argument parser.
        """

        parsed_args = self.parser.parse_args(['accu', '--debug',
                                              '--refresh', '-v'])
        self.assertEqual(parsed_args.command, 'accu')
        self.assertEqual(parsed_args.formatter, 'table')
        self.assertTrue(parsed_args.debug)
        self.assertTrue(parsed_args.refresh)    
        self.assertEqual(parsed_args.verbose_level, 1)


if __name__ == '__main__':
    unittest.main()
    
