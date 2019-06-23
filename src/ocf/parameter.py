from lxml import etree

class Parameter():
    def __init__(self, name):
        self.setName(name)

    def setName(self, name):
        self.name = name
        return self

    def setParentXml(self, parentXml):
        self.parentXml = parentXml
        return self

    def addXmlToParent(self):
        self.xmlElement = etree.SubElement(self.parentXml, "parameter")
        self.__addName()

    def __addName(self):
        self.xmlElement.set("name", self.name)
