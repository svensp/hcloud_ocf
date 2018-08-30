#!/usr/bin/python3
import sys
sys.path.append( '../..')
from floating_ip import hcloud 
import hetznercloud
import unittest
import mock

class TestHostnameHostFinder(unittest.TestCase):
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_searches_for_passed_hostname(self, cloudClient):
        finder = hcloud.HostnameHostFinder( 'server_1' )
        cloudClient.servers = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(return_value=[ 'serverobject' ])
        server = finder.find(cloudClient);
        
        cloudClient.get_all.assert_called_once_with(name='server_1')
        assert server == 'serverobject'

    rated = False
    def rateLimitOnce(self, name):
        if not self.rated:
            self.rated = True
            raise hetznercloud.HetznerRateLimitExceeded()
        return [ 'server' ]
            

    @mock.patch('time.sleep')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_retries_on_ratelimit(self, cloudClient, sleep):
        finder = hcloud.HostnameHostFinder( 'server_1' )
        finder.rateLimitWait = 10
        cloudClient.servers = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(side_effect=self.rateLimitOnce)
        server = finder.find(cloudClient);
        sleep.assert_called_once_with(10)

    errored = False
    def serverErrorOnce(self, name):
        if not self.errored:
            self.errored = True
            raise hetznercloud.HetznerInternalServerErrorException('test')
        return [ 'server' ]

    @mock.patch('time.sleep')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_retries_on_server_error(self, cloudClient, sleep):
        finder = hcloud.HostnameHostFinder( 'server_1' )
        finder.serverErrorWait = 15
        cloudClient.servers = mock.Mock(return_value=cloudClient)
        cloudClient.get_all = mock.Mock(side_effect=self.serverErrorOnce)
        server = finder.find(cloudClient);
        sleep.assert_called_once_with(15)


if __name__ == '__main__':
    unittest.main()
