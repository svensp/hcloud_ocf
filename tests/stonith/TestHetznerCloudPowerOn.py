#!/usr/bin/python3
import sys
import os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../../stonith' )
import unittest
import CallsBase

class TestHetznerCloud(CallsBase.TestBase, unittest.TestCase):

    def takeAction(self, agent):
        return agent.powerOn()

    def serverAction(self, server):
        return server.power_on


if __name__ == '__main__':
    unittest.main()
