import unittest
import unittest.mock
import ocf.default_resource_agent
import ocf.exception
import ocf.return_codes
import ocf.printer
from unittest.mock import Mock
import xml.etree.ElementTree as ET

class OcfDefaultResourceAgentTest(unittest.TestCase):

    def setUp(self):
        self.resourceAgent = ocf.default_resource_agent.DefaultResourceAgent()
        self.actions = [
                'monitor',
                'start',
                'stop',
                'promote',
                'demote',
                'migrate_to',
                'migrate_from',
                'usage',
                'help',
                ]

    def testOcfExceptionReturnsCodeOnAnyAction(self):
        returnCode = ocf.return_codes.UnimplementedError()
        self.resourceAgent.monitor = Mock(side_effect=ocf.exception.Exception(returnCode))
        self.resourceAgent.start = Mock(side_effect=ocf.exception.Exception(returnCode))
        self.resourceAgent.stop = Mock(side_effect=ocf.exception.Exception(returnCode))
        self.resourceAgent.promote = Mock(side_effect=ocf.exception.Exception(returnCode))
        self.resourceAgent.demote = Mock(side_effect=ocf.exception.Exception(returnCode))
        self.resourceAgent.migrateTo = Mock(side_effect=ocf.exception.Exception(returnCode))
        self.resourceAgent.migrateFrom = Mock(side_effect=ocf.exception.Exception(returnCode))
        self.resourceAgent.help = Mock(side_effect=ocf.exception.Exception(returnCode))
        for action in self.actions:
            result = self.resourceAgent.run(action)
            self.assertEqual(3, result)

    def testRunsPreBuildOnAnyAction(self):
        for action in self.actions:
            self.resourceAgent.buildPreValidation = unittest.mock.Mock(name="buildPreValidation "+action)
            self.resourceAgent.run(action)
            self.resourceAgent.buildPreValidation.assert_called()

    def testRunsBuildOnAnyAction(self):
        for action in self.actions:
            self.resourceAgent.build = unittest.mock.Mock(name="build "+action)
            self.resourceAgent.run(action)
            self.resourceAgent.build.assert_called()

    def testValidateOnValidatedActions(self):
        self.resourceAgent.isValidated = Mock(return_value=True)
        for action in self.actions:
            self.resourceAgent.validate = unittest.mock.Mock(name="validate "+action)
            self.resourceAgent.run(action)
            self.resourceAgent.validate.assert_called()

    def testDoesNotValidateOnNonValidatedActions(self):
        self.resourceAgent.isValidated = Mock(return_value=False)
        for action in self.actions:
            self.resourceAgent.validate = unittest.mock.Mock(name="validate "+action)
            self.resourceAgent.run(action)
            self.resourceAgent.validate.assert_not_called()

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

    def testReturnsUnimplemented(self):
        result = self.resourceAgent.run('promote')
        self.assertEqual(3, result)

    def testDemoteReturnsUnimplmented(self):
        result = self.resourceAgent.run('demote')
        self.assertEqual(3, result)

    def testMigrateToReturnsUnimplmented(self):
        result = self.resourceAgent.run('migrate_to')
        self.assertEqual(3, result)

    def testMigrateFromReturnsUnimplmented(self):
        result = self.resourceAgent.run('migrate_from')
        self.assertEqual(3, result)

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
