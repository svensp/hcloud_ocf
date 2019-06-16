#!/usr/bin/python3
import sys
import os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../..' )
import shared
import hetznercloud
import unittest
import mock

class TestHostnameHostFinder(unittest.TestCase):
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_searches_for_passed_hostname(self, cloudClient):
        finder = shared.HostnameHostFinder( 'server_1' )
        cloudClient.servers = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(return_value=[ 'serverobject' ])
        server = finder.find(cloudClient);
        
        cloudClient.get_all.assert_called_once_with(name='server_1')
        assert server == 'serverobject'

    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_throws_on_empty_list(self, cloudClient):
        finder = shared.HostnameHostFinder( 'server_1' )
        cloudClient.servers = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(return_value=[])
        self.assertRaises(EnvironmentError, finder.find, cloudClient)
        
            

if __name__ == '__main__':
    unittest.main()
