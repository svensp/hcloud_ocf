#!/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

import ocf
import hcloud
import sys

if __name__ == '__main__':
    application = ocf.AgentRunner()
    resourceAgent = hcloud.FloatingIp()
    api = ocf.Api()

    try:
        action = api.action()
    except AssertionError:
        print("Error: Missing action")
        sys.exit( ocf.ReturnCodes.invalidArguments )


    try:
        code = application.run(resourceAgent, api.action()) 
    except AssertionError:
        code = ocf.ReturnCodes.isMissconfigured
    sys.exit( code )
