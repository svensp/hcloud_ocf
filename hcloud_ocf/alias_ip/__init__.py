#!/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

import sys
from ..pacemaker.ocf import AgentRunner
from ..pacemaker.ocf import Api
from ..pacemaker.ocf import ReturnCodes
from .alias_ip import AliasIp
import traceback

def main():
    application = AgentRunner()
    resourceAgent = AliasIp()
    api = Api()

    try:
        action = api.action()
    except AssertionError:
        print("Error: Missing action")
        sys.exit( ReturnCodes.invalidArguments )


    try:
        code = application.run(resourceAgent, api.action()) 
    except AssertionError as e:
        # Thanks to https://stackoverflow.com/questions/11587223/how-to-handle-assertionerror-in-python-and-find-out-which-line-or-statement-it-o?rq=1
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        tb_info = traceback.extract_tb(tb)
        filename, line, func, text = tb_info[-1]

        print('An error occurred on line {} in statement {}'.format(line, text))
        code = ReturnCodes.isMissconfigured
    sys.exit( code )


if __name__ == '__main__':
    main()
