#!/usr/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

from ..pacemaker.ocf import ReturnCodes
from ..pacemaker.ocf import AbortWithError
from ..pacemaker.ocf import ResourceAgent
from ..pacemaker.ocf import Parameter
from ..pacemaker.validators import IpvAnyValidator, StringLengthValidator
import time
from . hostfinder import makeHostFinder
from hcloud import Client

class AliasIp(ResourceAgent):
    def __init__(self):

        ResourceAgent.__init__(self, 'alias_ip', '0.1.0', 'Manage Hetzner Cloud Private Network Alias Ips',
                '''
                This resource agent uses the hetzner cloud api and to manage an alias ip address.

                By default matching the host to a server entry in the api is done by matching its
                default ipv4 address to those listed in the api servers.
                This can be chaned using the host_finder parameter

                This resource does NOT manage adding the ip address to the network interface. You should either
                add it permanently to your network adapter by setting it in /etc/network/interfaces,
                /etc/netplan/* or in NetworkManager OR you could use a second resource of type IPAddr2
                with the address and set at least two constraints:
                colocation ip address with alias ip
                order start ip address after alias ip
                ''')

        self.aliasIp = Parameter('ip', shortDescription='Hetner Cloud Ip-Address x.x.x.x' ,
                description='''
                The Hetzner Cloud Floating Ip Address which this resource should manage.
                Note that this does not mean the Id of the Ip-Address but the Address
                itself.
                ''',
                required=True, unique=True)
        self.aliasIp.validate = IpvAnyValidator(self.aliasIp)
        self.apiToken = Parameter('api_token', shortDescription='Hetner Cloud api token' ,
                description='''
                The Hetzner Cloud api token with which the ip address can be managed.

                You can create this in the Hetner Cloud Console. Select the project
                which contains your Ip-Address, then select `Access` on the leftside menu
                Activate the second tab `Api Tokens` and create a new token.
                ''',
                required=True, unique=False)
        self.apiToken.validate = StringLengthValidator(self.apiToken, 64)
        self.finderType = Parameter('host_finder', default='public-ip', shortDescription='Host finder' ,
                description='''
                Implementation to use for matching the host this agent is running on to the host in the api

                Available implementations:
                - public-ip: The public ipv4 address listed in the api is present on any adapter on the host
                - hostname: The hosts `hostname` matches the server name in the api
                ''',
                required=False, unique=False)
        self.parameters = [
                self.aliasIp,
                self.apiToken,
                self.finderType
        ]
        self.setHint('start', 'timeout', '60')
        self.setHint('monitor', 'timeout', '60')

    def getParameters(self):
        return self.parameters

    def populated(self):
        if not self.apiToken.get():
            return
        self.client = Client(token=self.apiToken.get(), poll_interval=3)

    def findServer(self):
        hostFinder = makeHostFinder( self.finderType.get() )
        return hostFinder.find( self.client )

    def start(self):
        try:
            server = self.findServer()
            network = self.findNetwork(server)

            managedAliasIp = self.aliasIp.get()  
            aliasIps = network.alias_ips
            # Ip already assigned, no action required
            if managedAliasIp in aliasIps:
                return ReturnCodes.success
                
            aliasIps.append( managedAliasIp )
            self.client.servers.change_alias_ips(server, network, aliasIps).wait_until_finished()

        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            return ReturnCodes.isMissconfigured
        return ReturnCodes.success

    def stop(self):
        try:
            server = self.findServer()
            network = self.findNetwork(server)

            managedAliasIp = self.aliasIp.get()  
            aliasIps = network.alias_ips
            # Ip already assigned, no action required
            if managedAliasIp not in aliasIps:
                return ReturnCodes.success
                
            aliasIps.remove( managedAliasIp )
            self.client.servers.change_alias_ips(server, network, aliasIps).wait_until_finished()

        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            return ReturnCodes.isMissconfigured
        return ReturnCodes.success

    def monitor(self):
        isActive = False

        try:
            server = self.findServer()
            network = self.findNetwork(server)
            
            managedAliasIp = self.aliasIp.get()  
            aliasIps = network.alias_ips

            if managedAliasIp in aliasIps:
                isActive = True
                
        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            return ReturnCodes.isMissconfigured

        if not isActive:
            return ReturnCodes.isNotRunning
            
        return ReturnCodes.success
