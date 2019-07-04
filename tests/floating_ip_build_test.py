import unittest
from unittest.mock import Mock
from ip.agent import FloatingIp
from ip.server import Server
from ip.builder import Builder
from ip.ip import Ip

class FloatingIpBuildTest(unittest.TestCase):

    def setUp(self):
        self.setUpMocks()
        self.floatingIp = FloatingIp(self.server, self.ip, self.builder)

    def testExists(self):
        self.assertSetUpPassed()

    def testBuildPreValidation(self):
        self.floatingIp.buildPreValidation()
        self.assertBuilderOperatesOnIp();
        self.assertBuilderReceivesPreValidation();

    def testBuild(self):
        self.floatingIp.build()
        self.assertBuilderOperatesOnIp();
        self.assertBuilderReceivesBuild();

    def assertSetUpPassed(self):
        pass

    def assertBuilderOperatesOnIp(self):
        self.builder.setTarget.assert_called_with(self.floatingIp)

    def assertBuilderReceivesPreValidation(self):
        self.builder.buildPreValidation.assert_called()

    def assertBuilderReceivesBuild(self):
        self.builder.build.assert_called()

    def setUpMocks(self):
        self.builder = Builder()
        self.builder.setTarget = Mock(name='builder.setTarget', \
                return_value=self.builder)
        self.builder.buildPreValidation = Mock(name='builder.buildPreValidation')
        self.builder.build = Mock(name='builder.build')

        self.server = Server()
        self.ip = Ip()
