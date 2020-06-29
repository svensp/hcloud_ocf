#!/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018 Sven Speckmaier

import os
import sys
from lxml import etree as ET
from .runner import AbortWithError, ResourceAgent
from .parameters import Populater, Parameter, ParameterXmlBuilder

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

class AgentActionBuilder:
    def build(self, runner, resource):
        return {
            "start": resource.start,
            "stop": resource.stop,
            "monitor": resource.monitor,
            "status": resource.monitor,
            "promote": getattr(resource, 'promote', runner.notImplemented),
            "demote": getattr(resource, 'demote', runner.notImplemented),
            "migrate_to": getattr(resource, 'migrateTo', runner.notImplemented),
            "migrate_from": getattr(resource, 'migrateFrom', runner.notImplemented),
            "meta-data": lambda : runner.metaData(resource),
            "validate-all": lambda : runner.validate(resource),
        }

class AgentRunner:
    def __init__( self, populater = Populater(Api()), actionBuilder = AgentActionBuilder(),
            parameterBuilder = ParameterXmlBuilder()):
        self.populater = populater
        self.actionBuilder = actionBuilder
        self.parameterBuilder = parameterBuilder

    def notImplemented(self):
        return ReturnCodes.isNotImplemented

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
        self.parameterBuilder.build(parametersNode, resource.parameters)

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
        xml =  ET.tostring(tree, encoding='UTF-8',
                     xml_declaration=True,
                     pretty_print=True,
                     doctype='<!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">').decode('UTF-8')
        xmlWithoutEncoding = xml.replace("encoding='UTF-8'", '')
        print(xmlWithoutEncoding)

    def validate(self, resource):
        self.populater.populate(resource)

        try:
            for item in resource.getParameters():
                item.validate()
        except EnvironmentError as e:
            print( e.strerror )
            return ReturnCodes.isMissconfigured
            
        try:
            resource.validate()
        except AttributeError:
            pass

        return 0 

    def run(self, resource, action):
        validate = ( action != 'meta-data' )
        self.populater.populate(resource, validate)

        actions = self.actionBuilder.build(self, resource)

        try:
            actionMethod = actions[action]
            return actionMethod()
        except AbortWithError as e:
            print(e.errorMessage)
            return e.errorCode
        except KeyError:
            return ReturnCodes.isNotImplemented
