import unittest
import unittest.mock
import ocf.config

class OcfConfigTest(unittest.TestCase):

    @unittest.mock.patch('os.environ')
    def setUp(self, environ):
        self.ocfConfig = ocf.config.Config(environ)

    def testOcfConfigExists(self):
        pass
