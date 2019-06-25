import ocf.printer
import ocf.metadata
import os
import re
import unittest
from lxml import etree, objectify
from io import StringIO

class TestCase(unittest.TestCase):
    def setUp(self):
        self.metadata = ocf.metadata.Metadata()
        self.printer = ocf.printer.BagPrinter()
        self.metadata.setPrinter(self.printer)

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
