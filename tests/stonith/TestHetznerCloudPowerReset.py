#!/usr/bin/python3
import sys
import os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../../stonith' )
import unittest
import Base

class TestHetznerCloud(Base.TestBase, unittest.TestCase):

    def takeAction(self, agent):
        return agent.powerReset()

    def serverAction(self, server):
        return server.reset

if __name__ == '__main__':
    unittest.main()
