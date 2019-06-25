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
        self.parameters = {}
        self.actions  = {}
        self.__makeDefaultActions()
        self.__makeDefaultDescriptions()

    def __makeDefaultActions(self):
        self.__addAction( ocf.action.Action('start') )
        self.__addAction( ocf.action.Action('stop') )
        self.__addAction( ocf.action.Action('monitor') )
        self.__addAction( ocf.action.Action('validate-all') )
        self.__addAction( ocf.action.Action('meta-data') )
        self.__addAction( ocf.action.Action('promote') )
        self.__addAction( ocf.action.Action('demote') )
        self.__addAction( ocf.action.Action('migrate_to') )
        self.__addAction( ocf.action.Action('migrate_from') )
        self.__addAction( ocf.action.Action('notify') )

    def __makeDefaultDescriptions(self):
        self.setDescription('TODO: add short description', \
                'TODO: add long description')

    def __addAction(self, action):
        self.actions[action.getName()] = action

    def setActionHint(self, actionName, hintName, hintValue):
        self.actions[actionName].setHint(hintName, hintValue)

    def disableAction(self, actionName):
        del self.action[actionName]

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
        parametersElement = etree.SubElement(self.xmlRoot, "parameters")
        for key in self.parameters:
            parameter = self.parameters[key]
            parameter.setParentXml(parametersElement) \
                .addXmlToParent()

    def __addActions(self):
        actionsElement = etree.SubElement(self.xmlRoot, 'actions')
        for actionKey in self.actions:
            action = self.actions[actionKey]
            action.setParentXml(actionsElement) \
                    .appendToParentXml()
            

    def __xmlToString(self):
        self.xmlContent = etree.tostring(self.xmlTree, pretty_print=True).decode('utf-8')

    def __printFullXml(self):
        self.printer.print(self.xmlContent)
