import unittest
from unittest.mock import Mock, patch
import ocf.return_codes
from ip.agent import FloatingIp
from ip.server import Server
from ip.ip import Ip

class FloatingIpStartTest(unittest.TestCase):

    def setUp(self):
        self.floatingIp = FloatingIp()
        self.setUpMocks()

    @patch('hetznercloud.HetznerCloudClientConfiguration')
    @patch('hetznercloud.HetznerCloudClient')
    def testNoSettingsFailsValidation(self, client, clientConfig):
        #self.returnCode = self.agent.run('start')
        #self.assertValidationFailed()

    def assertValidationFailed(self):
        self.assertEquals(self.returnCode, ocf.return_codes.ConfigurationError().getValue())

    def setUpMocks(self):
        self.agent = FloatingIp()
