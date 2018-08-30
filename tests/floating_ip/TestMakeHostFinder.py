#!/usr/bin/python3
import sys
sys.path.append( '../..')
from floating_ip import hcloud 
import hetznercloud
import unittest
import mock

class TestMakeHostFinder(unittest.TestCase):

    def test_public_ip(self):
        finder = hcloud.makeHostFinder('public-ip')
        self.assertIsInstance(finder, hcloud.IpHostFinder)

    def test_hostname(self):
        finder = hcloud.makeHostFinder('hostname')
        self.assertIsInstance(finder, hcloud.HostnameHostFinder)

    def test_test(self):
        finder = hcloud.makeHostFinder('test')
        self.assertIsInstance(finder, hcloud.TestHostFinder)

if __name__ == '__main__':
    unittest.main()
