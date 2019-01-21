#!/usr/bin/python3
import sys
import os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../..' )
from shared import Ipv4Validator
from common import Parameter 
import unittest
import mock

class TestTestHostFinder(unittest.TestCase):
    def test_validates_ipv4(self):
        ip = Parameter('ip')
        ip.set('192.168.1.1')
        validator = Ipv4Validator(ip)
        validator()

    def test_alerts_invalid_ipv4(self):
        ip = Parameter('ip')
        ip.set('192.168.1-1')
        validator = Ipv4Validator(ip)
        self.assertRaises(EnvironmentError, validator)

if __name__ == '__main__':
    unittest.main()
