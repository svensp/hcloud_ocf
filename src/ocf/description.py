from lxml import etree

class DescriptionContainer():
    def __init__(self):
        self.descriptions = {}

    def addDescription(self, description):
        self.descriptions[description.language] = description

    def setParentXml(self, parentXml):
        self.parentXml = parentXml
        return self
    
    def appendToParentXml(self):
        for languageKey in self.descriptions:
            description = self.descriptions[languageKey]
            description.setParentXml(self.parentXml) \
                    .appendToParentXml()
            

class Description():
    def __init__(self, shortDescription, longDescription, language='en'):
        self.shortDescription = shortDescription
        self.longDescription = longDescription
        self.language = language
    
    def setParentXml(self, parentXml):
        self.parentXml = parentXml
        return self

    def appendToParentXml(self):
        longDescriptionElement = etree.SubElement(self.parentXml, "longdesc")
        longDescriptionElement.set('lang', self.language)
        longDescriptionElement.text = self.longDescription
        shortDescriptionElement = etree.SubElement(self.parentXml, "shortdesc")
        shortDescriptionElement.set('lang', self.language)
        shortDescriptionElement.text = self.shortDescription
