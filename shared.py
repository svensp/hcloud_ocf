import ifaddr
import socket
import os
from hetznercloud.servers import HetznerCloudServer

#
# Validators
#
class IpvAnyValidator:
    def __init__(self, parameter):
        self.parameter = parameter
        self.ipv4 = Ipv4Validator(parameter);
        self.ipv6 = Ipv6Validator(parameter);

    def __call__(self):
        try:
            self.ipv4()
            return
        except EnvironmentError:
            pass

        try:
            self.ipv6()
            return
        except EnvironmentError:
            pass

        raise EnvironmentError(0, "Parameter "+self.parameter.name+" is neither a valid ipv4 nor ipv6 address")


#
# Validators
#
class Ipv4Validator:
    def __init__(self, parameter):
        self.parameter = parameter

    def __call__(self):
        try:
            socket.inet_aton( self.parameter.get() )
        except socket.error:
            raise EnvironmentError(0, "Parameter "+self.parameter.name+" is not a valid ipv4 address")

#
# Validators
#
class Ipv6Validator:
    def __init__(self, parameter):
        self.parameter = parameter

    def __call__(self):
        try:
            socket.inet_pton(socket.AF_INET6, self.parameter.get() )
        except socket.error:
            raise EnvironmentError(0, "Parameter "+self.parameter.name+" is not a valid ipv6 address")

class StringLengthValidator:
    def __init__(self, parameter, length):
        self.parameter = parameter
        self.length = length

    def __call__(self):
        if len( self.parameter.get() ) == self.length:
            return

        raise EnvironmentError(0, "Parameter "+self.parameter.name+" does not have the length of a hetzner cloud token("+str(self.length)+" characters)")
            


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
class HostFinder:
    def find(self, client) -> HetznerCloudServer:
        pass

class IpHostFinder(HostFinder):
    def find(self, client) -> HetznerCloudServer:
        my_ips = []
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            for ip in adapter.ips:
                my_ips.append(ip.ip)
        servers = client.servers().get_all()
        for server in servers:
            if server.public_net_ipv4 in  my_ips:
                return server
        raise EnvironmentError('Host not found in hcloud api.')

class HostnameHostFinder(HostFinder):
    def __init__(self, hostname):
        self.hostname = hostname

    def find(self, client) -> HetznerCloudServer:
        success = False
        while not success:
            servers = list(client.servers().get_all(name=self.hostname))
            success = True
        if len(servers) < 1:
            raise EnvironmentError('Host '+self.hostname+' not found in hcloud api.')
        return servers[0]

class TestHostFinder(HostFinder):
    def find(self, client) -> HetznerCloudServer:
        name = os.environ.get('TESTHOST')
        servers = list( client.servers().get_all(name=name) )
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

