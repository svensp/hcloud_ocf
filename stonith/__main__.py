#!/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

import stonith
import hcloud
import sys

if __name__ == '__main__':
    application = stonith.Runner()
    resourceAgent = hcloud.Stonith()
    api = stonith.Api()

    try:
        action = api.action()
    except AssertionError:
        print("Error: Missing action")
        sys.exit( stonith.ReturnCodes.invalidArguments )


    try:
        code = application.run( resourceAgent, api.action() )
    except AssertionError:
        code = stonith.ReturnCodes.isMissconfigured
    sys.exit( code )
