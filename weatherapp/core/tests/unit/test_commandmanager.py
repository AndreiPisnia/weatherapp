import unittest

from weatherapp.core.commandmanager import CommandManager


class DummyCommand:
    pass


class CommandManagerTestCase(unittest.TestCase):

    """Unit test case for command manager
    """

    def setUp(self):
        self.command_manager = CommandManager()

    def test_add(self):
        """Test "add" method for command manager.
        """
        print('test is running')
        self.command_manager.add('dummy', DummyCommand)
        
        self.assertTrue('dummy' in self.command_manager.commands)
        self.assertEqual(self.command_manager.get('dummy'), DummyCommand)
        
        for key, value in self.command_manager.commands.items():
            print(key)
            print(value)

    def test_get(self):
        """Test "get" method for command manager.
        """

        self.command_manager.add('dummy', DummyCommand)

        self.assertEqual(self.command_manager.get('dummy'), DummyCommand)
        self.assertIsNone(self.command_manager.get('bar'))

    def test_containes(self):
        """Test "__containes__" method for command manager
        """
        
        self.command_manager.add('dummy', DummyCommand)

        self.assertTrue('dummy' in self.command_manager)
        self.assertFalse('bar' in self.command_manager)


if __name__ == '__main__':
    unittest.main()
