#!/usr/bin/python3
import sys
import os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../..' )
import floating_ip
import hetznercloud
import unittest
import mock

class TestIpFinder(unittest.TestCase):
    @mock.patch('hetznercloud.floating_ips.HetznerCloudFloatingIp')
    @mock.patch('hetznercloud.floating_ips.HetznerCloudFloatingIp')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_finds_ip(self, cloudClient, expectedIp, wrongIp):
        cloudClient.floating_ips = mock.Mock(return_value=cloudClient)
        expectedIp.ip = '127.0.0.1';
        wrongIp.ip = '10.42.0.1';
        cloudClient.get_all = mock.Mock(return_value=[ 
            wrongIp,
            expectedIp
        ])

        ipFinder = floating_ip.IpFinder();
        ip = ipFinder.find(cloudClient, '127.0.0.1')
        assert ip.ip == '127.0.0.1'

    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_no_ips_causes_exception(self, cloudClient):
        cloudClient.floating_ips = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(return_value=[ ])

        ipFinder = floating_ip.IpFinder();
        self.assertRaises(EnvironmentError, ipFinder.find, cloudClient, '127.0.0.1')

    @mock.patch('hetznercloud.floating_ips.HetznerCloudFloatingIp')
    @mock.patch('hetznercloud.floating_ips.HetznerCloudFloatingIp')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_only_unmatching_ips_causes_exception(self, cloudClient, wrongIp1,
            wrongIp2):
        wrongIp1.ip = '127.1.0.1'
        wrongIp2.ip = '127.2.0.1'
        cloudClient.floating_ips = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(return_value=[ 
            wrongIp1,
            wrongIp2
        ])

        ipFinder = floating_ip.IpFinder();
        self.assertRaises(EnvironmentError, ipFinder.find, cloudClient, '127.0.0.1')

if __name__ == '__main__':
    unittest.main()
