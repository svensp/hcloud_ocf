#!/usr/bin/python3
import sys
sys.path.append( '../..')
from floating_ip import hcloud 
import hetznercloud
import unittest
import mock

class TestFloatingIp(unittest.TestCase):
    @mock.patch('hcloud.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def start_assigns_ip(self, cloudClient, makeHostFinder):
        hostFinder = HostFinder()
        hostFinder.find = Mock(return_value)
        makeHostFinder = Mock( return_value=mockHostFinder )
        floatingIp = hcloud.FloatingIp()

        cloudClient.servers = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(return_value=[ 'serverobject' ])

    def stop_does_nothing(self):
        floatingIp = hcloud.FloatingIp()

if __name__ == '__main__':
    unittest.main()
