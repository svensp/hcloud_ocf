#!/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

from hetznercloud import HetznerCloudClientConfiguration, HetznerCloudClient
from hetznercloud.servers import HetznerCloudServer
from hetznercloud.floating_ips import HetznerCloudFloatingIp
import ocf
import socket
import ifaddr

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
class MyHostFinder:
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

class IpFinder:
     def find(self, client, address) -> HetznerCloudFloatingIp:
         for floatingIp in client.floating_ips().get_all():
             if floatingIp.ip == address:
                 return floatingIp
         raise EnvironmentError('Floating ip not found.')

class FloatingIp(ocf.ResourceAgent):
    def __init__(self):
        self.hostFinder = MyHostFinder()
        self.ipFinder = IpFinder()

        ocf.ResourceAgent.__init__(self, 'floating_ip', '0.1.0', 'Manage Hetzner Cloud Floating Ips',
                '''
                This resource agent uses the hetzner cloud api and to manage a floating ip address.

                IMPORTANT: This resource agent assumes that the hostname of the target cluster member
                is the same as its name in the cloud api.

                It does NOT manage adding the ip address to the network interface. You should either
                add it permanently to your network adapter by setting it in /etc/network/interfaces,
                /etc/netplan/* or in NetworkManager OR you could use a second resource of type IPAddr2
                with the address and set at least two constraints:
                colocation ip address with floating ip
                order start ip address after floating ip
                ''')

        self.floatingIp = ocf.Parameter('floating_ip', shortDescription='Hetner Cloud Ip-Address x.x.x.x' ,
                description='''
                The Hetzner Cloud Floating Ip Address which this resource should manage.
                Note that this does not mean the Id of the Ip-Address but the Address
                itself.
                ''',
                required=True, unique=True)
        self.apiToken = ocf.Parameter('htoken', shortDescription='Hetner Cloud api token' ,
                description='''
                The Hetzner Cloud api token with which the ip address can be managed.

                You can create this in the Hetner Cloud Console. Select the project
                which contains your Ip-Address, then select `Access` on the leftside menu
                Activate the second tab `Api Tokens` and create a new token.
                ''',
                required=True, unique=False)
        self.parameters = [
                self.floatingIp,
                self.apiToken
        ]
        self.setHint('start', 'timeout', '10')

    def getParameters(self):
        return self.parameters

    def populated(self):
        configuration = HetznerCloudClientConfiguration().with_api_key( self.apiToken.get() ).with_api_version(1)
        self.client = HetznerCloudClient(configuration)

    def start(self):
        server = self.hostFinder.find(self.client)
        ip = self.ipFinder.find(self.client)
        print('Start!')

    def stop(self):
        return ocf.ReturnCodes.success

    def monitor(self):
        server = self.hostFinder.find(self.client)
        ip = self.ipFinder.find(self.client)
