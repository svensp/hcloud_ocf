import unittest
import unittest.mock
import ocf.config

class OcfConfigTest(unittest.TestCase):

    def testGetReturnsOcfReskeyValue(self):
        self.buildConfig({
            "OCF_RESKEY_kekse":"a"
            })
        self.assertEqual( 'a', self.config.get('kekse') )

    @unittest.mock.patch('os.environ')
    def testWorksWithEnviron(self, environ):
        pass

    def buildConfig(self, values):
        self.config = ocf.config.Config(values)
