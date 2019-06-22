import unittest
import unittest.mock
import ocf.default_resource_agent
import ocf.exception
import ocf.printer
import xml.etree.ElementTree as ET

class OcfDefaultResourceAgentTest(unittest.TestCase):

    def setUp(self):
        self.resourceAgent = ocf.default_resource_agent.DefaultResourceAgent()

    def testRunsMonitorOnMonitor(self):
        self.resourceAgent.monitor = unittest.mock.Mock(name="monitor")
        self.resourceAgent.run('monitor')
        self.resourceAgent.monitor.assert_called()

    def testRunsMonitorOnStatus(self):
        self.resourceAgent.monitor = unittest.mock.Mock(name="monitor")
        self.resourceAgent.run('status')
        self.resourceAgent.monitor.assert_called()

    def testRunsStart(self):
        self.resourceAgent.start = unittest.mock.Mock(name="start")
        self.resourceAgent.run('start')
        self.resourceAgent.start.assert_called()

    def testRunsStop(self):
        self.resourceAgent.stop = unittest.mock.Mock("stop")
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

    def testUsageRunsHelp(self):
        self.resourceAgent.help = unittest.mock.Mock(name="help")
        self.resourceAgent.run('usage')
        self.resourceAgent.help.assert_called()

    def testHelpRunsHelp(self):
        self.resourceAgent.help = unittest.mock.Mock(name="help")
        self.resourceAgent.run('help')
        self.resourceAgent.help.assert_called()

    def testHelpReturnsSuccess(self):
        returnCode = self.resourceAgent.help()
        self.assertIsInstance(returnCode, ocf.return_codes.Success)

    def testNoActionRunsHelp(self):
        self.resourceAgent.help = unittest.mock.Mock(name="help")
        self.resourceAgent.run('')
        self.resourceAgent.help.assert_called()

    def testNoActionRunsHelp(self):
        self.resourceAgent.help = unittest.mock.Mock(name="help")
        self.resourceAgent.run(None)
        self.resourceAgent.help.assert_called()

    def testValidateAllRunsValidate(self):
        self.resourceAgent.validate = unittest.mock.Mock(name="validate")
        self.resourceAgent.run('validate-all')
        self.resourceAgent.validate.assert_called()

    def testValidateReturnsSuccess(self):
        returnCode = self.resourceAgent.validate()
        self.assertIsInstance(returnCode, ocf.return_codes.Success)

    def testMetaDataRunMetaData(self):
        self.resourceAgent.metaData = unittest.mock.Mock(name="metaData")
        self.resourceAgent.run('meta-data')
        self.resourceAgent.metaData.assert_called()

    def testMetaDataReturnsSuccess(self):
        returnCode = self.resourceAgent.metaData()
        self.assertIsInstance(returnCode, ocf.return_codes.Success)

    def testMetaDataUsesMetadataPrinter(self):
        self.resourceAgent.meta.print = unittest.mock.Mock(name="meta.print")
        self.resourceAgent.run('meta-data')
        self.resourceAgent.meta.print.assert_called()
