#!/usr/bin/python3
import sys
sys.path.append( '../..')
import shared
import unittest
import ifaddr
from unittest import mock
from mock import patch
from mock import Mock

#
# Test Definitions Begin
#
class TestIpHostFinder(unittest.TestCase):

    def makeAdapter(self, get_adapters, ip):
        mockIp = Mock()
        mockIp.ip = ip
        mockAdapter = Mock()
        mockAdapter.ips = [ mockIp ]
        mockAdapters = [ mockAdapter ]
        get_adapters.return_value = mockAdapters
    

    def makeServers(self, server_ips):
        servers = []
        index = 0
        for ip in server_ips:
            server = Mock()
            server.index = index
            server.public_net_ipv4 = ip
            servers.append(server)
            index += 1
            
        return servers


    @mock.patch('ifaddr.get_adapters')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_find_first(self, client, get_adapters):
        self.makeAdapter(get_adapters, '192.168.2.1')
        servers = self.makeServers(['192.168.2.1', '192.168.2.5'])
        client.servers = Mock(return_value=client)
        client.get_all = Mock(return_value=servers)
        ipHostFinder = shared.IpHostFinder( )
        server = ipHostFinder.find(client)
        assert server.public_net_ipv4 == '192.168.2.1'
        assert server.index == 0

    @mock.patch('ifaddr.get_adapters')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_find_middle(self, client, get_adapters):
        self.makeAdapter(get_adapters, '192.168.2.1')
        servers = self.makeServers(['192.168.2.5', '192.168.2.1', '192.168.2.4'])
        client.servers = Mock(return_value=client)
        client.get_all = Mock(return_value=servers)
        ipHostFinder = shared.IpHostFinder( )
        server = ipHostFinder.find(client)
        assert server.public_net_ipv4 == '192.168.2.1'
        assert server.index == 1

    @mock.patch('ifaddr.get_adapters')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_find_last(self, client, get_adapters):
        self.makeAdapter(get_adapters, '192.168.2.1')
        servers = self.makeServers(['192.168.2.5', '192.168.2.4', '192.168.2.1'])
        client.servers = Mock(return_value=client)
        client.get_all = Mock(return_value=servers)
        ipHostFinder = shared.IpHostFinder( )
        server = ipHostFinder.find(client)
        assert server.public_net_ipv4 == '192.168.2.1'
        assert server.index == 2

    @mock.patch('ifaddr.get_adapters')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_find_not_found(self, client, get_adapters):
        self.makeAdapter(get_adapters, '192.168.2.1')
        servers = self.makeServers(['192.168.2.5', '192.168.2.6'])
        client.servers = Mock(return_value=client)
        client.get_all = Mock(return_value=servers)
        ipHostFinder = shared.IpHostFinder( )
        self.assertRaises(EnvironmentError, ipHostFinder.find, client)

if __name__ == '__main__':
    unittest.main()
