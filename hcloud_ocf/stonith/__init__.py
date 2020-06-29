#!/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

import sys
import stonith
from .stonith_agent import Stonith

def main():
    application = stonith.Runner()
    resourceAgent = Stonith()
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

if __name__ == '__main__':
    main()
