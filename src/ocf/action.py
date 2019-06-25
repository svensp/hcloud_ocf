from lxml import etree

class Action():
    def __init__(self, name):
        self.name = name
        self.hints = {}
        self.setDefaultTimeout()

    def setHint(self, hintName, hintValue):
        self.hints[hintName] = hintValue

    def setDefaultTimeout(self):
        self.setHint("timeout", 10)

    def setParentXml(self, parentXml):
        self.setParentXml = parentXml
        return self

    def appendToParentXml(self):
        element = etree.SubElement(self.setParentXml, 'action')
        element.set("name", self.name)
        for hintName in self.hints:
            hintValue = self.hints[hintName]
            element.set(hintName, str(hintValue) )
        return self

    def getName(self):
        return self.name
