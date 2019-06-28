from io import StringIO
from lxml import etree
import ocf.parameter
import ocf.description
import ocf.action

class Metadata():

    def __init__(self):
        self.name = "default-name"
        self.version = "1.0"
        self.descriptions = ocf.description.DescriptionContainer()
        self.parameters = ocf.parameter.ParameterContainer()
        self.actions  = ocf.action.ActionContainer()
        self.__makeDefaultActions()
        self.__makeDefaultDescriptions()

    def __makeDefaultActions(self):
        self.actions.add( ocf.action.Action('start') )
        self.actions.add( ocf.action.Action('stop') )
        self.actions.add( ocf.action.Action('monitor') )
        self.actions.add( ocf.action.Action('validate-all') )
        self.actions.add( ocf.action.Action('meta-data') )
        self.actions.add( ocf.action.Action('promote') )
        self.actions.add( ocf.action.Action('demote') )
        self.actions.add( ocf.action.Action('migrate_to') )
        self.actions.add( ocf.action.Action('migrate_from') )
        self.actions.add( ocf.action.Action('notify') )

    def __makeDefaultDescriptions(self):
        self.setDescription('TODO: add short description', \
                'TODO: add long description')

    def setActionHint(self, actionName, hintName, hintValue):
        self.actions.setHint(actionName, hintName, hintValue)

    def disableAction(self, actionName):
        self.actions.remove(actionName)

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
        self.parameters.clear()

    def createParameter(self, name):
        createdParameter = ocf.parameter.Parameter(name)
        self.parameters.set(createdParameter)
        return createdParameter

    def print(self):
        self.__prepareXmlWithResourceAgentTag()
        self.__addName()
        self.__addVersion()
        self.__addDescriptions()
        self.__addParameters()
        self.__addActions()
        self.__xmlToString()
        self.__printFullXml()

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
        self.parameters.setParentXml(self.xmlRoot) \
                .appendToParentXml()

    def __addActions(self):
        self.actions.setParentXml(self.xmlRoot) \
                .appendToParentXml()

    def __xmlToString(self):
        self.xmlContent = etree.tostring(self.xmlTree, pretty_print=True).decode('utf-8')

    def __printFullXml(self):
        self.printer.print(self.xmlContent)
