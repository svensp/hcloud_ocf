import unittest
from tests.ocf_metadata_testcase import TestCase
from lxml import etree, objectify

class OcfMetadataTest(TestCase):
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

    def testParametersHaveDefaultDescription(self):
        parameter = self.metadata.createParameter("test-parameter")

        self.loadXml()

        self.assertXmlHasElementText('/resource-agent/parameters/parameter/shortdesc',
                "TODO: short description",
                { "lang":"en" })
        self.assertXmlHasElementText('/resource-agent/parameters/parameter/longdesc',
                "TODO: long description",
                { "lang":"en" })

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
