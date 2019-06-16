#!/usr/bin/python3
import sys
import os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../..' )
from shared import IpvAnyValidator
from common import Parameter 
import unittest
import mock

class TestTestHostFinder(unittest.TestCase):
    def test_validates_ipv4(self):
        ip = Parameter('ip')
        ip.set('192.168.1.1')
        validator = IpvAnyValidator(ip)
        validator()

    def test_validates_ipv6(self):
        ip = Parameter('ip')
        ip.set('2001:db8::2:1')
        validator = IpvAnyValidator(ip)
        validator()

    def test_alerts_invalid_ipv6(self):
        ip = Parameter('ip')
        ip.set('2001:db8::2:q1')
        validator = IpvAnyValidator(ip)
        self.assertRaises(EnvironmentError, validator)

if __name__ == '__main__':
    unittest.main()
