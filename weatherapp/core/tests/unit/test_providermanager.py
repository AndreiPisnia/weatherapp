import unittest

from weatherapp.core.providermanager import ProviderManager


class DummyProvider:
    pass


class ProviderManagerTestCase(unittest.TestCase):

    """Unit test case for provider manager
    """

    def setUp(self):
        self.provider_manager = ProviderManager()

    def test_add(self):
        """Test "add" method for provider manager.
        """

        self.provider_manager.add('dummy', DummyProvider)
        
        self.assertTrue('dummy' in self.provider_manager._providers)
        self.assertEqual(self.provider_manager.get('dummy'), DummyProvider)
        
        for key, value in self.provider_manager._providers.items():
            print(key)
            print(value)

    def test_get(self):
        """Test "get" method for provider manager.
        """

        self.provider_manager.add('dummy', DummyProvider)

        self.assertEqual(self.provider_manager.get('dummy'), DummyProvider)
        self.assertIsNone(self.provider_manager.get('any'))

    def test_containes(self):
        """Test "__containes__" method for provider manager
        """
        
        self.provider_manager.add('dummy', DummyProvider)

        self.assertTrue('dummy' in self.provider_manager)
        self.assertTrue('accu' in self.provider_manager)
        self.assertFalse('any' in self.provider_manager)


if __name__ == '__main__':
    unittest.main()
