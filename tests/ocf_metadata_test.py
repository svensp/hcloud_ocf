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
        self.metadata.setVersion('1.0.0')
        self.loadXml()
        self.assertXmlHasElementText('/resource-agent/version', '1.0.0')

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

    def testHasParameter(self):
        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters')

    def testParametersAreAddedAsElement(self):
        self.metadata.createParameter("test-parameter")

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter',
                { "name":"test-parameter" })

    def testMultipleParametersAreAddedAsElement(self):
        self.metadata.createParameter("test-parameter")
        self.metadata.createParameter("test-parameter2")

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter',
                { "name":"test-parameter" })
        self.assertXmlHasXpath('/resource-agent/parameters/parameter',
                { "name":"test-parameter2" })

    def testParametersUniqueTrueIsAddedAsAttribute(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setUnique(True)

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter',
                { "name":"test-parameter",
                    "unique":"1" })

    def testParametersUniqueFalseIsAddedAsAttribute(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setUnique(False)

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter',
                { "name":"test-parameter",
                    "unique":"0" })

    def testParametersRequiredTrueIsAddedAsAttribute(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setRequired(True)

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter',
                { "name":"test-parameter",
                    "required":"1" })

    def testParametersRequiredFalseIsAddedAsAttribute(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setRequired(False)

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter',
                { "name":"test-parameter",
                    "required":"0" })

    def testParametersRequiredFalseIsAddedAsAttribute(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setRequired(False)

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter',
                { "name":"test-parameter",
                    "required":"0" })

    def testParametersDescriptionsAreAddedAsElement(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setDescription("short description", "long description", "en")

        self.loadXml()

        self.assertXmlHasElementText('/resource-agent/parameters/parameter/shortdesc',
                "short description",
                { "lang":"en" })
        self.assertXmlHasElementText('/resource-agent/parameters/parameter/longdesc',
                "long description",
                { "lang":"en" })

    def testParametersDescriptionsSameLanguageOverrides(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setDescription("short description", "long description", "en")
        parameter.setDescription("overridden short description", "overridden long description", "en")

        self.loadXml()

        self.assertXmlHasElementText('/resource-agent/parameters/parameter/shortdesc',
                "overridden short description",
                { "lang":"en" })
        self.assertXmlHasElementText('/resource-agent/parameters/parameter/longdesc',
                "overridden long description",
                { "lang":"en" })

    def testParametersDescriptionsDifferentLanguageAddsBoth(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setDescription("short en", "long en", "en")
        parameter.setDescription("short de", "long de", "de")

        self.loadXml()

        self.assertXmlHasElementText('/resource-agent/parameters/parameter/shortdesc',
                "short en",
                { "lang":"en" })
        self.assertXmlHasElementText('/resource-agent/parameters/parameter/longdesc',
                "long en",
                { "lang":"en" })
        self.assertXmlHasElementText('/resource-agent/parameters/parameter/shortdesc',
                "short de",
                { "lang":"de" })
        self.assertXmlHasElementText('/resource-agent/parameters/parameter/longdesc',
                "long de",
                { "lang":"de" })

    def testParameterContentTypeIsAddedAsElement(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setContentType(parameter.CONTENT_TYPE_BOOL)

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter/content',
                { "type":"boolean" })

    def testParameterContentTypeIsAddedAsElement(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setContentType(parameter.CONTENT_TYPE_BOOL)

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter/content',
                { "type":"boolean" })

    def testParameterDefaultValueIsAddedAsElement(self):
        parameter = self.metadata.createParameter("test-parameter")
        parameter.setDefaultValue(False)

        self.loadXml()

        self.assertXmlHasXpath('/resource-agent/parameters/parameter/content',
                { "default":"False" })

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

    def assertXmlHasXpath(self, xpath, requiredAttributes = {}, expectedElements=1):
        elements = self.xmlTree.xpath(xpath) 

        filteredElements = self.filterElementsWithAttributes(elements, requiredAttributes)

        self.assertEqual(expectedElements, len(filteredElements), "XML Element "+xpath+" with "+str(requiredAttributes)+" not found in metadata" )
        if expectedElements == 1:
            return elements[0]

        return elements

    def assertXmlHasElementText(self, xpath, expectedText, requiredAttributes = {}):
        foundElements = self.findElementsWithText(xpath, expectedText)
        self.assertTrue( len(foundElements) > 0, "No elements found for xpath "+xpath )

        filteredElements = self.filterElementsWithAttributes(foundElements, requiredAttributes)
        self.assertTrue( len(filteredElements) > 0, "No elements found for xpath "+xpath+" and required attributes "+str(requiredAttributes) )

        numFoundElements = len(filteredElements)
        self.assertTrue(numFoundElements > 0, "Text "+expectedText+" not found in "+str(numFoundElements)+" elements of xpath "+xpath)

    def findElementsWithText(self, xpath, expectedText):
        elements = self.xmlTree.xpath(xpath) 
        foundElements = []
        for element in elements:
            if(element.text == expectedText):
                foundElements.append( element )
        return foundElements

    def filterElementsWithAttributes(self, elements, requiredAttributes):
        matchingElements = []

        for element in elements:
            allFound = True
            for attributeName in requiredAttributes:
                elementValue = element.get(attributeName)
                requiredValue = requiredAttributes[attributeName]
                if elementValue != requiredValue:
                    allFound = False

            if allFound:
                matchingElements.append( element )
                
        return matchingElements

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
