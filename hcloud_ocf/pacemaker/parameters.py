from lxml import etree as ET

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

