from lxml import etree as ET
import socket

class Ipv4Validator:
    def __init__(self, parameter):
        self.parameter = parameter

    def __call__(self):
        try:
            socket.inet_aton( self.parameter.get() )
        except socket.error:
            raise EnvironmentError(0, "Parameter "+self.parameter.name+" is not a valid ipv4 address")

class StringLengthValidator:
    def __init__(self, parameter, length):
        self.parameter = parameter
        self.length = length

    def __call__(self):
        if len( self.parameter.get() ) == self.length:
            return

        raise EnvironmentError(0, "Parameter "+self.parameter.name+" does not have the length of a hetzner cloud token("+str(self.length)+" characters)")
            

class ParameterXmlBuilder:
    def build(self, parametersNode, parameters):
        for parameter in parameters:
            parameterNode = ET.SubElement(parametersNode, 'parameter')
            parameterNode.set('name', parameter.getName())
            content = ET.SubElement(parameterNode, 'content')
            content.set('type', parameter.getType())

            longDesc = ET.SubElement(parameterNode, 'longdesc')
            longDesc.text = parameter.getDescription()
            longDesc.set('lang', 'en')
            shortDesc = ET.SubElement(parameterNode, 'shortdesc')
            shortDesc.text = parameter.getShortDescription()
            shortDesc.set('lang', 'en')

            parameterNode.set('unique', '0')
            if parameter.isUnique():
                parameterNode.set('unique', '1')

            parameterNode.set('required', '0')
            if parameter.isRequired():
                parameterNode.set('required', '1')

class Populater:
    def __init__(self, api):
        self.api = api

    def populate(self, resource, validate = True):
        for parameter in resource.getParameters():
            value = self.api.variable( parameter.getName() )
            if validate and parameter.isRequired():
                try:
                    assert not value == None
                    assert not value == ''
                except AssertionError:
                    print( "Error: Missing parameter "+parameter.getName() )
                    raise
            if not value:
                value = parameter.getDefault()

            parameter.set(value)
        try:
            resource.setHost( self.api.host() )
        except AttributeError:
            pass

        try:
            resource.populated()
        except AttributeError:
            pass

class Parameter:
    def __init__(self, name, shortDescription='', description='', default='', type='string', unique=False, required=False):
        self.name = name
        self.default = default
        self.shortDescription = shortDescription
        self.description = description
        self.unique = unique
        self.required = required
        self.type = type
        self.value = False
        self.validate = lambda : True

    def set(self, value):
        self.value = value
    def get(self):
        return self.value
    def getName(self):
        return self.name
    def getDefault(self):
        return self.default
    def isRequired(self):
        return self.required
    def isUnique(self):
        return self.unique
    def getShortDescription(self):
        return self.shortDescription
    def getDescription(self):
        return self.description
    def getType(self):
        return self.type

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
