#!/usr/bin/python3
import sys
import os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../..' )
import shared
import hetznercloud
import unittest
import mock

class TestMakeHostFinder(unittest.TestCase):

    def test_public_ip(self):
        finder = shared.makeHostFinder('public-ip')
        self.assertIsInstance(finder, shared.IpHostFinder)

    def test_hostname(self):
        finder = shared.makeHostFinder('hostname')
        self.assertIsInstance(finder, shared.HostnameHostFinder)

    def test_test(self):
        finder = shared.makeHostFinder('test')
        self.assertIsInstance(finder, shared.TestHostFinder)

if __name__ == '__main__':
    unittest.main()
