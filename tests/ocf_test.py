import unittest
import ocf.resource_agent

class OcfTest(unittest.TestCase):
    def setUp(self):
        self.resourceAgent = ocf.resource_agent.ResourceAgent()

    def testOcfResourceAgentExists(self):
        self.assertSetUpRanWithoutError()

    def testOcfResourceAgentContainsDummyStop(self):
        self.resourceAgent.stop()

    def assertSetUpRanWithoutError(self):
        pass
