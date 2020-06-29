#!/usr/bin/python3

import ifaddr
import os
import socket

#
# The HostFinder searches for the hetzner cloud api server which manages the
# machine this script is running on
#
# Implementation:
#   An api server is matched if the ipv4 address listed in the api is present
#   on this machine
#  
# Possible alternatives:
# Match hostname to servername
#
#

from hcloud.servers.client import BoundServer

class HostFinder:
    def find(self, client) -> BoundServer:
        pass

class IpHostFinder(HostFinder):
    def find(self, client) -> BoundServer:
        my_ips = []
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            for ip in adapter.ips:
                my_ips.append(ip.ip)
        servers = client.servers.get_all()
        for server in servers:
            if server.public_net.ipv4.ip in  my_ips:
                return server
        raise EnvironmentError('Host not found in hcloud api.')

class HostnameHostFinder(HostFinder):
    def __init__(self, hostname):
        self.hostname = hostname

    def find(self, client) -> BoundServer:
        servers = list(client.servers.get_all(name=self.hostname))
        if len(servers) < 1:
            raise EnvironmentError('Host '+self.hostname+' not found in hcloud api.')
        return servers[0]

class TestHostFinder(HostFinder):
    def find(self, client) -> BoundServer:
        name = os.environ.get('TESTHOST')
        servers = list( client.servers.get_all(name=name) )
        if len( servers ) < 1:
            raise EnvironmentError('Host '+name+' not found in hcloud api.')
        return servers[0]

def makeHostFinder(type) -> HostFinder:
    if type == 'public-ip':
        return IpHostFinder()
    if type == 'hostname':
        hostname = socket.gethostname()
        return HostnameHostFinder(hostname)
    if type == 'test':
        return TestHostFinder()
    raise KeyError('Unkown host finder type')

