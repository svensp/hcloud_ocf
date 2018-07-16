#!/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018 Sven Speckmaier

from hetznercloud import HetznerCloudClientConfiguration, HetznerCloudClient
from hetznercloud.servers import HetznerCloudServer
from lxml import etree as ET
from shared import Populater, Parameter, ParameterXmlBuilder
import sys
import os
import ocf

class ReturnCodes:
    success = 0
    error = 1
    notImplemented = 1
    invalidArguments = 1
    isMissconfigured = 1

class Api:
    def action(self):
        assert 1 < len(sys.argv)
        return sys.argv[1]
    def host(self):
        if len(sys.argv) <= 2:
            return ''
        return sys.argv[2]
    def variable(self, name):
        return os.environ.get(name)
    def meta(self, name):
        return Null

class StonithActionBuilder:
    def build(self, runner, resource):
        return {
            "gethosts": resource.getHosts,
            "on": getattr(resource, 'powerOn', runner.notImplemented),
            "off": getattr(resource, 'powerOff', runner.notImplemented),
            "reset": resource.powerReset,
            "status": resource.status,
            "getconfignames": lambda : runner.getConfigNames(resource),
            "getinfo-devid": resource.infoId,
            "getinfo-devname": resource.infoName,
            "getinfo-devdescr": resource.infoDescription,
            "getinfo-devurl": resource.infoUrl,
            "getinfo-xml": lambda : runner.metaData(resource),
        }


class Runner:
    def __init__(self, populater = Populater(Api()), actionBuilder = StonithActionBuilder,
        parameterBuilder = ParameterXmlBuilder()):
        self.populater = populater
        self.actionBuilder = actionBuilder
        self.parameterBuilder = parameterBuilder

    def notImplemented(self):
        return ReturnCodes.notImplemented

    def run(self, resource, action):
        self.populater.populate(resource)

        actions = self.actionBuilder.build(self, self, resource)

        try:
            actionMethod = actions[action]
        except KeyError:
            print("Action "+action+" not implemented.")
            return ReturnCodes.notImplemented

        return actionMethod()


    def metaData(self, resource):
        root = ET.Element('parameters')
        self.parameterBuilder.build(root, resource.getParameters() )
        tree = ET.ElementTree(root)
        print( ET.tostring(tree, encoding="UTF-8",
                     xml_declaration=True,
                     pretty_print=True,
                     doctype='<!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">'))
