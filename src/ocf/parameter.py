from lxml import etree
import ocf.description

class Parameter():
    CONTENT_TYPE_BOOL = 'boolean'
    CONTENT_TYPE_STRING = 'string'
    CONTENT_TYPE_INTEGER = 'integer'

    def __init__(self, name):
        self.name = name
        self.unique = False
        self.required = False
        self.descriptions = ocf.description.DescriptionContainer()
        self.contentType = self.CONTENT_TYPE_BOOL
        self.defaultValue = None
        self.__setDefaultDescription()

    def __setDefaultDescription(self):
        self.setDescription('TODO: short description', 'TODO: long description')

    def setContentType(self, contentType):
        self.contentType = contentType
        return self

    def setDefaultValue(self, defaultValue):
        self.defaultValue = defaultValue

    def setName(self, name):
        self.name = name
        return self

    def setUnique(self, unique):
        self.unique = unique

    def setRequired(self, required):
        self.required = required

    def setDescription(self, shortDescription, longDescription, language='en'):
        newDescription = ocf.description.Description(shortDescription, longDescription, language)
        self.descriptions.addDescription(newDescription)

    def setParentXml(self, parentXml):
        self.parentXml = parentXml
        return self

    def addXmlToParent(self):
        self.xmlElement = etree.SubElement(self.parentXml, "parameter")
        self.__addName()
        self.__addUnique()
        self.__addRequired()
        self.__addDescriptions()
        self.__addContent()

    def __addName(self):
        self.xmlElement.set("name", self.name)

    def __addUnique(self):
        if self.unique:
            self.xmlElement.set("unique", "1")
            return
        self.xmlElement.set("unique", "0")

    def __addRequired(self):
        if self.required:
            self.xmlElement.set("required", "1")
            return
        self.xmlElement.set("required", "0")

    def __addDescriptions(self):
        self.descriptions.setParentXml(self.xmlElement) \
                .appendToParentXml()

    def __addContent(self):
        self.contentElement = etree.SubElement(self.xmlElement, "content")
        self.__addContentType()
        self.__addDefaultValue()

    def __addContentType(self):
        self.contentElement.set("type", self.contentType)

    def __addDefaultValue(self):
        if self.defaultValue is None:
            return

        self.contentElement.set("default", str(self.defaultValue) )
