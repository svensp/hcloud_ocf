import unittest
from unittest.mock import Mock
from ip.agent import FloatingIp
from ip.server import Server
from ip.ip import Ip

class FloatingIpMonitorTest(unittest.TestCase):

    def setUp(self):
        self.floatingIp = FloatingIp()
        self.setUpMocks()

    def testExists(self):
        self.assertSetUpPassed()

    def testRetrievesServer(self):
        self.floatingIp.monitor()

        self.assertServerIsRetrieved();

    def testRetrievesIp(self):
        self.floatingIp.monitor()

        self.assertIpIsRetrieved();

    def testIpAssignedToServer(self):
        self.floatingIp.monitor()

        self.assertIpIsAssertedToPointToServer();

    def assertSetUpPassed(self):
        pass

    def assertServerIsRetrieved(self):
        self.server.retrieve.assert_called()

    def assertIpIsRetrieved(self):
        self.ip.retrieve.assert_called()

    def assertIpIsAssertedToPointToServer(self):
        self.ip.setTargetServer.assert_called_with(self.server)
        self.ip.assertAssigned.assert_called_with()

    def setUpMocks(self):
        self.server = Server()
        self.server.retrieve = Mock(name='server.retrieve', return_value=self.server)

        self.floatingIp.server = self.server

        self.ip = Ip()
        self.ip.setTargetServer = Mock(name='setTargetServer', return_value=self.ip)
        self.ip.retrieve = Mock(name='ip.retrieve', return_value=self.ip)
        self.ip.assertAssigned = Mock(name='assertAssigned')

        self.floatingIp.ip = self.ip
