import unittest
from tests.ocf_metadata_testcase import TestCase
from lxml import etree, objectify

class OcfMetadataStructureTest(TestCase):
    def testMetadataExists(self):
        self.assertSetUpRuns()

    def testMetadataIsXml(self):
        self.loadXml()

    def testMetadataHasDoctype(self):
        self.loadXml()
        self.assertDoctypeMatches(r'DOCTYPE\s+\bresource-agent\b')
        self.assertDoctypeMatches(r'\bSYSTEM\b')
        self.assertDoctypeMatches(r'"ra-api-1.dtd"')

    def testMetadataHasResourceAgent(self):
        self.loadXml()
        element = self.assertXmlHasXpath('/resource-agent')

    def testResourceAgentHasNameAttribute(self):
        self.metadata.setName('gday')
        self.loadXml()
        element = self.assertXmlHasXpath('/resource-agent')
        self.assertElementAttribute(element, "name", 'gday')

    def testResourceAgentHasVersionAttribute(self):
        self.metadata.setVersion('1.0.0')
        self.loadXml()
        element = self.assertXmlHasXpath('/resource-agent')
        self.assertElementAttribute(element, "version", '1.0.0')

    def testMetadataHasVersion(self):
        self.metadata.setVersion('1.0.0')
        self.loadXml()
        self.assertXmlHasElementText('/resource-agent/version', '1.0.0')

    def testMetadataHasDefaultLongDescription(self):
        self.loadXml()
        self.assertXmlHasElementText('/resource-agent/longdesc', 'TODO: add long description')

    def testMetadataHasDefaultShortDescription(self):
        self.loadXml()
        self.assertXmlHasElementText('/resource-agent/shortdesc', 'TODO: add short description')

    def testMetadataHasLongDescription(self):
        self.metadata.setDescription('short description', 'long description', 'en')
        self.loadXml()
        self.assertXmlHasElementText('/resource-agent/longdesc', 'long description')

    def testMetadataHasShortDescription(self):
        self.metadata.setDescription('short description', 'long description', 'en')
        self.loadXml()
        self.assertXmlHasElementText('/resource-agent/shortdesc', 'short description')

    def testSameLanguageOverridesDescriptions(self):
        self.metadata.setDescription('short description', 'long descripiton', 'en')
        self.metadata.setDescription('overridden short description', 'overridden long description', 'en')

        self.loadXml()

        self.assertXmlHasElementText('/resource-agent/longdesc', 'overridden long description')
        self.assertXmlHasElementText('/resource-agent/shortdesc', 'overridden short description')

    def testDifferentLanguagesAreAddedSeparatly(self):
        self.metadata.setDescription('short description en', 'long description en', 'en')
        self.metadata.setDescription('short description de', 'long description de', 'de')

        self.loadXml()

        self.assertXmlHasElementText('/resource-agent/longdesc', 'long description en', {"lang":"en"})
        self.assertXmlHasElementText('/resource-agent/shortdesc', 'short description en', {"lang":"en"})
        self.assertXmlHasElementText('/resource-agent/longdesc', 'long description de', {"lang":"de"})
        self.assertXmlHasElementText('/resource-agent/shortdesc', 'short description de', {"lang":"de"})

    def testMetadataValidates(self):
        # deactivated until schema building is tested
        self.loadSchema()
        self.metadata.createParameter('test')
        self.loadXml()
        print(self.printer.log)
        self.assertXmlValid()
