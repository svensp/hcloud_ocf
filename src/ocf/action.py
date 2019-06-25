from lxml import etree

class ActionContainer():
    def __init__(self):
        self.actions  = {}

    def add(self, action):
        self.actions[action.getName()] = action

    def setHint(self, actionName, hintName, hintValue):
        self.actions[actionName].setHint(hintName, hintValue)

    def setParentXml(self, parentXml):
        self.parentXml = parentXml
        return self
    
    def appendToParentXml(self):
        actionsElement = etree.SubElement(self.parentXml, 'actions')
        for actionKey in self.actions:
            action = self.actions[actionKey]
            action.setParentXml(actionsElement) \
                    .appendToParentXml()

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
