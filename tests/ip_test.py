from hetznercloud import HetznerCloudClientConfiguration, HetznerCloudClient, ACTION_STATUS_SUCCESS
import unittest
from unittest.mock import Mock, MagicMock
from ip.ip import Ip
from ip.server import Server
from ip.retriever import ByIdRetriever

class IpTest(unittest.TestCase):
    def setUp(self):
        self.setUpMocks()
        self.ip = Ip()
        self.ip.setRetriever(self.retriever)

    def testRetrievesFromRetriever(self):
        self.ip.retrieve()
        self.assertWasRetrieved()
        pass

    def testAssignsToServer(self):
        self.ip.retrieve().setTargetServer(self.server).assign()
        self.assertWasAssigned()

    def testWaitsForActionSuccess(self):
        self.ip.retrieve().setTargetServer(self.server).assign()
        self.assertWaitsForActionDone()

    def assertWasRetrieved(self):
        self.retriever.retrieve.assert_called()

    def assertWasAssigned(self):
        self.hetznerIp.assign_to_server.assert_called_with(5)

    def assertWaitsForActionDone(self):
        self.action.wait_until_status_is.assert_called_with(ACTION_STATUS_SUCCESS)

    def setUpMocks(self):
        self.action = MagicMock()

        self.hetznerIp = MagicMock()
        self.hetznerIp.assign_to_server = Mock(name='hetznerIp.assign_to_server', return_value=self.action)

        self.retriever = MagicMock()
        self.client = MagicMock()
        self.retriever.getIp = Mock(name='retriever.getIp',
                return_value=self.hetznerIp)

        self.server = Server()
        self.server.getId = Mock(name='server.getId', return_value=5)
