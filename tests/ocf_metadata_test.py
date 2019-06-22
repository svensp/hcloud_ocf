import unittest
import ocf.metadata
import ocf.printer
import os
import re
from io import StringIO
from lxml import etree, objectify

class OcfMetadataTest(unittest.TestCase):
    def setUp(self):
        self.metadata = ocf.metadata.Metadata()
        self.printer = ocf.printer.BagPrinter()
        self.metadata.setPrinter(self.printer)

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
        self.loadXml()
        self.assertXmlHasXpath('/resource-agent/version')

    def testMetadataValidates(self):
        # deactivated until schema building is tested
        return
        self.loadSchema()
        self.loadXml()
        self.assertXmlValid()

    def loadSchema(self):
        self.findDTDPath()
        self.dtd = etree.DTD(open(self.dtdPath))

    def loadXml(self):
        self.metadata.print()
        self.xmlTreeObject = objectify.parse( StringIO(self.printer.log) )
        self.xmlTree = etree.fromstring(self.printer.log)

    def assertXmlValid(self):
        valid = self.dtd.validate(self.xmlTreeObject)
        self.assertTrue(valid, 'Metadata XML is not valid')

    def assertSetUpRuns(self):
        pass

    def assertXmlHasXpath(self, xpath, expectedElements=1):
        elements = self.xmlTree.xpath(xpath) 

        self.assertEqual(expectedElements, len(elements), "XML Element "+xpath+" not found in metadata" )
        if expectedElements == 1:
            return elements[0]

        return elements

    def findDTDPath(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        self.dtdPath = directory + "/resources/ra-api-1.dtd"

    def assertDoctypeMatches(self, regex):
        tree = etree.ElementTree(self.xmlTree)
        doctype = tree.docinfo.doctype
        self.assertTrue( re.search(regex, doctype), "Doctype "+doctype+" did not match" + regex )

    def assertElementAttribute(self, element, attribute, expectedValue):
        self.assertTrue(attribute in element.keys(), "Element does not have attribute " + attribute )
        self.assertEquals(expectedValue, element.get(attribute), "Element attribute "+attribute+" is not expected "+expectedValue)
