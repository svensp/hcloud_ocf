import unittest
import unittest.mock
import ocf.default_resource_agent
import ocf.exception

class OcfDefaultResourceAgentTest(unittest.TestCase):

    def setUp(self):
        self.resourceAgent = ocf.default_resource_agent.DefaultResourceAgent()

    def testRunsMonitorOnMonitor(self):
        self.resourceAgent.monitor = unittest.mock.Mock()
        self.resourceAgent.run('monitor')
        self.resourceAgent.monitor.assert_called()

    def testRunsMonitorOnStatus(self):
        self.resourceAgent.monitor = unittest.mock.Mock()
        self.resourceAgent.run('status')
        self.resourceAgent.monitor.assert_called()

    def testRunsStart(self):
        self.resourceAgent.start = unittest.mock.Mock()
        self.resourceAgent.run('start')
        self.resourceAgent.start.assert_called()

    def testRunsStop(self):
        self.resourceAgent.stop = unittest.mock.Mock()
        self.resourceAgent.run('stop')
        self.resourceAgent.stop.assert_called()

    def testPromoteThrowsUnimplmented(self):
        with self.assertRaises(ocf.exception.Exception):
            self.resourceAgent.run('promote')

    def testDemoteThrowsUnimplmented(self):
        with self.assertRaises(ocf.exception.Exception):
            self.resourceAgent.run('demote')

    def testMigrateToThrowsUnimplmented(self):
        with self.assertRaises(ocf.exception.Exception):
            self.resourceAgent.run('migrate_to')

    def testMigrateFromThrowsUnimplmented(self):
        with self.assertRaises(ocf.exception.Exception):
            self.resourceAgent.run('migrate_from')
