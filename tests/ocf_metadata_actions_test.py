import unittest
from tests.ocf_metadata_testcase import TestCase
from lxml import etree, objectify

class OcfMetadataActionsTest(TestCase):

    def testXmlHasActions(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions')

    def testAddsStartActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action', {"name":"start"})

    def testAddsStopActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action', {"name":"stop"})

    def testAddsMonitorActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action', 
                {"name":"monitor"})

    def testAddsValidateallActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action', 
                {"name":"validate-all"})

    def testAddsMetaDataActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action',
                {"name":"meta-data"})

    def testAddsPromoteActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action',
                {"name":"promote"})

    def testAddsDemoteActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action',
                {"name":"demote"})

    def testAddsMigrateToActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action',
                {"name":"migrate_to"})

    def testAddsMigrateFromActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action',
                {"name":"migrate_from"})

    def testAddsNotifyActionByDefault(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/actions/action',
                {"name":"notify"})

    def testMetadataValidates(self):
        # deactivated until schema building is tested
        return
        self.loadSchema()
        self.loadXml()
        self.assertXmlValid()
