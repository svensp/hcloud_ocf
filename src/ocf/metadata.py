from io import StringIO
from lxml import etree

class Metadata():

    def __init__(self):
        self.name = "default-name"
        self.version = "1.0"
        self.descriptions = {}

    def setDescription(self, shortDescription, longDescription, language = 'en'):
        self.descriptions[language] = {
            "long": longDescription,
            "short": shortDescription
        }

    def setName(self, name):
        self.name = name

    def setVersion(self, version):
        self.version = version

    def setPrinter(self, printer):
        self.printer = printer
        return self

    def print(self):
        self.prepareXmlWithResourceAgentTag()
        self.addName()
        self.addVersion()
        self.addDescriptions()
        self.xmlToString()
        self.printFullXml()
        #self.printExampleXml()

    def prepareXmlWithResourceAgentTag(self):
        self.xmlTree = etree.parse(StringIO('''<?xml version="1.0"?>

        <!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">
        <resource-agent />'''))
        self.xmlRoot = self.xmlTree.getroot()

    def addName(self):
        self.xmlRoot.set("name", self.name)

    def addVersion(self):
        self.xmlRoot.set("version", self.version)
        self.versionElement = etree.SubElement(self.xmlRoot, "version")
        self.versionElement.text = self.version

    def addDescriptions(self):
        for languageKey in self.descriptions:
            shortDescriptionElement = etree.SubElement(self.xmlRoot, "shortdesc")
            shortDescriptionElement.set('lang', languageKey)
            shortDescriptionElement.text = self.descriptions[languageKey]["short"]
            longDescriptionElement = etree.SubElement(self.xmlRoot, "longdesc")
            longDescriptionElement.set('lang', languageKey)
            longDescriptionElement.text = self.descriptions[languageKey]["long"]

    def xmlToString(self):
        self.xmlContent = etree.tostring(self.xmlTree, pretty_print=True).decode('utf-8')

    def printFullXml(self):
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
