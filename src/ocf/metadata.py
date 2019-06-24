from io import StringIO
from lxml import etree
import ocf.parameter
import ocf.description

class Metadata():

    def __init__(self):
        self.name = "default-name"
        self.version = "1.0"
        self.descriptions = ocf.description.DescriptionContainer()
        self.parameters = {}

    def setDescription(self, shortDescription, longDescription, language = 'en'):
        newDescription = ocf.description.Description(shortDescription, longDescription, language)
        self.descriptions.addDescription(newDescription)

    def setName(self, name):
        self.name = name

    def setVersion(self, version):
        self.version = version

    def setPrinter(self, printer):
        self.printer = printer
        return self

    def clearParameters(self):
        self.parameters = {}

    def createParameter(self, name):
        createdParameter = ocf.parameter.Parameter(name)
        self.parameters[name] = createdParameter
        return createdParameter

    def print(self):
        self.__prepareXmlWithResourceAgentTag()
        self.__addName()
        self.__addVersion()
        self.__addDescriptions()
        self.__addParameters()
        self.__xmlToString()
        self.__printFullXml()
        #self.printExampleXml()

    def __prepareXmlWithResourceAgentTag(self):
        self.xmlTree = etree.parse(StringIO('''<?xml version="1.0"?>

        <!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">
        <resource-agent />'''))
        self.xmlRoot = self.xmlTree.getroot()

    def __addName(self):
        self.xmlRoot.set("name", self.name)

    def __addVersion(self):
        self.xmlRoot.set("version", self.version)
        self.versionElement = etree.SubElement(self.xmlRoot, "version")
        self.versionElement.text = self.version

    def __addDescriptions(self):
        self.descriptions.setParentXml(self.xmlRoot) \
                .appendToParentXml()
    
    def __addParameters(self):
        parametersElement = etree.SubElement(self.xmlRoot, "parameters")
        for key in self.parameters:
            parameter = self.parameters[key]
            parameter.setParentXml(parametersElement) \
                .addXmlToParent()

    def __xmlToString(self):
        self.xmlContent = etree.tostring(self.xmlTree, pretty_print=True).decode('utf-8')

    def __printFullXml(self):
        print(self.xmlContent)
        self.printer.print(self.xmlContent)

    def printExampleXml(self):
        self.printer.print('''<?xml version="1.0"?>

<!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">

<resource-agent name="gday" version="0.1">

  <version>0.1</version>

  <longdesc lang="en">

This is a fictitious example resource agent written for the

OCF Resource Agent Developers Guide.

  </longdesc>

  <shortdesc lang="en">Example resource agent

  for budding OCF RA developers</shortdesc>

  <parameters>

    <parameter name="eggs" unique="0" required="1">

      <longdesc lang="en">

      Number of eggs, an example numeric parameter

      </longdesc>

      <shortdesc lang="en">Number of eggs</shortdesc>

      <content type="integer"/>

    </parameter>

    <parameter name="superfrobnicate" unique="0" required="0">

      <longdesc lang="en">

      Enable superfrobnication, an example boolean parameter

      </longdesc>

      <shortdesc lang="en">Enable superfrobnication</shortdesc>

      <content type="boolean" default="false"/>

    </parameter>

    <parameter name="datadir" unique="0" required="1">

      <longdesc lang="en">

      Data directory, an example string parameter

      </longdesc>

      <shortdesc lang="en">Data directory</shortdesc>

      <content type="string"/>

    </parameter>

  </parameters>

  <actions>

    <action name="start"        timeout="20" />

    <action name="stop"         timeout="20" />

    <action name="monitor"      timeout="20"

                                interval="10" depth="0" />

    <action name="reload"       timeout="20" />

    <action name="migrate_to"   timeout="20" />

    <action name="migrate_from" timeout="20" />

    <action name="meta-data"    timeout="5" />

    <action name="validate-all"   timeout="20" />

  </actions>

</resource-agent>
        ''')
