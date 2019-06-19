import unittest
from unittest import mock
import ocf.environment

class OcfEnvironmentTest(unittest.TestCase):

    @mock.patch('os.environ')
    def setUp(self, environ):
        self.environ = environ
        self.environ.get = mock.Mock()
        self.ocfEnvironment = ocf.environment.Environment(environ)

    def testOcfConfigPrependsOcfReskey(self):
        self.ocfEnvironment.get('oink')
        self.environ.get.assert_called_with('OCF_RESKEY_oink')

    def testOcfConfigReturnsDefaultWhenNotSet(self):
        self.environ.has_key = mock.Mock(return_value=False)
        result = self.ocfEnvironment.get('test', 'abcdefg')
        self.assertEqual('abcdefg', result)
