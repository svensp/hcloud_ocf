from lxml import etree

class Action():
    def __init__(self, name):
        self.name = name

    def setParentXml(self, parentXml):
        self.setParentXml = parentXml
        return self

    def appendToParentXml(self):
        element = etree.SubElement(self.setParentXml, 'action')
        element.set("name", self.name)
        return self

    def getName(self):
        return self.name
