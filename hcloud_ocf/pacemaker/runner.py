class AbortWithError(Exception):
    def __init__(self, errorCode, errorMessage):
        self.errorCode = errorCode
        self.errorMessage = errorMessage

class ResourceAgent:
    def __init__(self, name, version, shortDescription, description):
        self.name = name
        self.version = version
        self.shortDescription = shortDescription
        self.description = description
        self.hints = {}

    def getName(self):
        return self.name
    def getVersion(self):
        return self.version
    def getShortDescription(self):
        return self.shortDescription
    def getDescription(self):
        return self.description
    def setHint(self, action, hint, value):
        try:
            self.hints[action].update({hint: value})
        except KeyError:
            self.hints[action] = {hint: value}
    def setHints(self, action, hints):
        try:
            self.hints[action].update(hints)
        except KeyError:
            self.hints[action] = hints
    def getHints(self, action):
        try:
            return self.hints[action]
        except KeyError:
            return {}
