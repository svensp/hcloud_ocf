#!/usr/bin/python3
import os
import sys
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../../stonith' )
import Base
import unittest

class TestHetznerCloudStatus(Base.TestBase,unittest.TestCase):

    def takeAction(self, agent):
        return agent.status()
