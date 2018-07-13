#!/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

import os
import sys
from lxml import etree as ET

class ReturnCodes:
    success = 0
    genericError = 1
    invalidArguments = 2
    isNotImplemented = 3
    hasInsufficientPermissions = 4
    isMissingRequiredComponent = 5
    isMissconfigured = 6
    isNotRunning = 7
    isRunningMaster = 8
    isFailedMaster = 9

class Api:
    def action(self):
        assert 1 < len(sys.argv)
        return sys.argv[1]
    def variable(self, name):
        return os.environ.get('OCF_RESKEY_'+name)
    def meta(self, name):
        converted_name = name.replace('-','_')
        return os.environ.get('OCF_RESKEY_CRM_meta_'+converted_name)

class Populater:
    def __init__(self):
        self.api = Api()

    def populate(self, resource):
        for parameter in resource.getParameters():
            value = self.api.variable( parameter.getName() )
            if parameter.isRequired():
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
            resource.populated()
        except AttributeError:
            pass

class Agent:
    def __init__(self, name, version):
        self.name = name
        self.version  = version
        self.parameters = []
        self.languages = []

class Parameter:
    def __init__(self, name, shortDescription='', description='', default='', type='string', unique=False, required=False):
        self.name = name
        self.default = default
        self.shortDescription = shortDescription
        self.description = description
        self.unique = unique
        self.required = required
        self.type = type

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

class AgentRunner:
    def __init__(self):
        self.populater = Populater()

    def notImplemented(self):
        return OCfErrors.notImplemented

    def metaData(self, resource):
        root = ET.Element('resource-agent')
        root.set('name', resource.getName())
        root.set('version', resource.getVersion())
        version = ET.SubElement(root, 'version')
        version.text = resource.getVersion()
        shortdesc = ET.SubElement(root, 'shortdesc')
        shortdesc.text = resource.getShortDescription()
        shortdesc.set('lang', 'en')
        longdesc = ET.SubElement(root, 'longdesc')
        longdesc.text = resource.getDescription()
        longdesc.set('lang', 'en')
            
        parametersNode = ET.SubElement(root, 'parameters')
        for parameter in resource.getParameters():
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

        actions = ['start', 'stop', 'monitor', 'meta-data', 'validate-all'
                'reload', 'migrate_to', 'migrate_from', 'promote', 'demote']
        actionsNode = ET.SubElement(root, 'actions')
        for action in actions:
            try:
                getattr(resource,action)
                actionNode = ET.SubElement(actionsNode, 'action')
                actionNode.set('name', action)
                hints = resource.getHints(action)
                for k in hints:
                    actionNode.set(k, str(hints[k]) )
            except AttributeError:
                pass

        tree = ET.ElementTree(root)
        print( ET.tostring(tree, encoding="UTF-8",
                     xml_declaration=True,
                     pretty_print=True,
                     doctype='<!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">'))

    def validate(self, resource):
        self.populater.populate(resource)

        for item in resource.getParameters():
            item.validate()
            
        try:
            resource.validate()
        except AttributeError:
            pass

        return 0 

    def run(self, resource, action):
        self.populater.populate(resource)

        actions = {}
        try:
            actions.update({"start": resource.start})
        except AttributeError:
            pass

        try:
            actions.update({"stop": resource.stop})
        except AttributeError:
            pass

        try:
            actions.update({"monitor": resource.monitor})
            actions.update({"status": resource.monitor})
        except AttributeError:
            pass

        actions.update({
            "promote": getattr(resource, 'promote', self.notImplemented),
            "demote": getattr(resource, 'demote', self.notImplemented),
            "migrate_to": getattr(resource, 'migrateTo', self.notImplemented),
            "migrate_from": getattr(resource, 'migrateFrom', self.notImplemented),
            "meta-data": lambda : self.metaData(resource),
            "validate-all": lambda : self.validate(resource),
        })

        try:
            actionMethod = actions[action]
            return actionMethod()
        except KeyError:
            return OCfReturnCodes.isNotImplemented

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
