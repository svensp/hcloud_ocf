#!/usr/bin/python3
import sys
import os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../..' )
import shared
import hetznercloud
import unittest
import mock

class TestTestHostFinder(unittest.TestCase):
    @mock.patch('os.environ')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_searches_for_environment_hostname(self, cloudClient, environ):
        finder = shared.TestHostFinder()
        environ.get = mock.Mock(return_value='test_server')
        cloudClient.servers = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(return_value=[ 'serverobject' ])
        server = finder.find(cloudClient);
        
        cloudClient.get_all.assert_called_once_with(name='test_server')
        assert server == 'serverobject'

    @mock.patch('os.environ')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_throws_on_empty_list(self, cloudClient, environ):
        finder = shared.TestHostFinder()
        environ.get = mock.Mock(return_value='test_server')
        cloudClient.servers = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(return_value=[])
        self.assertRaises(EnvironmentError, finder.find, cloudClient)
        
            

if __name__ == '__main__':
    unittest.main()
