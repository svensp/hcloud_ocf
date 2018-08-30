#!/usr/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

from hetznercloud import HetznerCloudClientConfiguration, HetznerCloudClient
from hetznercloud.servers import HetznerCloudServer
from hetznercloud.floating_ips import HetznerCloudFloatingIp
from hetznercloud.exceptions import HetznerAuthenticationException, HetznerInternalServerErrorException, HetznerActionException, HetznerRateLimitExceeded
import ocf
import socket
import ifaddr
import os
import time
import stonith

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
class IpHostFinder:
    def __init__(self, ipApi = ifaddr):
        self.ipApi = ipApi

    def find(self, client) -> HetznerCloudServer:
        my_ips = []
        adapters = self.ipApi.get_adapters()
        for adapter in adapters:
            for ip in adapter.ips:
                my_ips.append(ip.ip)
        servers = client.servers().get_all()
        for server in servers:
            if server.public_net_ipv4 in  my_ips:
                return server
        raise EnvironmentError('Host not found in hcloud api.')

class HostnameHostFinder():
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

class TestHostFinder():
    def find(self, client) -> HetznerCloudServer:
        name = os.environ.get('TESTHOST')
        servers = client.servers().get_all(name=name)
        if len(servers) < 1:
            raise EnvironmentError('Host '+name+' not found in hcloud api.')
        return servers[0]

def makeHostFinder(type):
    if type == 'public-ip':
        return IpHostFinder()
    if type == 'hostname':
        hostname = socket.gethostname()
        return HostnameHostFinder(hostname)
    if type == 'test':
        return TestHostFinder()
    raise KeyError('Unkown host finder type')

class IpFinder:
     def find(self, client, address) -> HetznerCloudFloatingIp:
         for floatingIp in client.floating_ips().get_all():
             if floatingIp.ip == address:
                 return floatingIp
         raise EnvironmentError('Floating ip not found.')

class FloatingIp(ocf.ResourceAgent):
    def __init__(self):
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
        self.apiToken = ocf.Parameter('api_token', shortDescription='Hetner Cloud api token' ,
                description='''
                The Hetzner Cloud api token with which the ip address can be managed.

                You can create this in the Hetner Cloud Console. Select the project
                which contains your Ip-Address, then select `Access` on the leftside menu
                Activate the second tab `Api Tokens` and create a new token.
                ''',
                required=True, unique=False)
        self.finderType = ocf.Parameter('host_finder', default='public-ip', shortDescription='Host finder' ,
                description='''
                Implementation to use for matching the host this agent is running on to the host in the api

                Available implementations:
                - public-ip: The public ipv4 address listed in the api is present on any adapter on the host
                - hostname: The hosts `hostname` matches the server name in the api
                - test: 
                ''',
                required=False, unique=False)
        self.sleep = ocf.Parameter('sleep', default='2', shortDescription='Sleep duration when an api request fails' ,
                description='''
                The number of seconds to wait before trying again when an api request fails from something other than
                a insufficient permissions
                ''',
                required=False, unique=False)
        self.parameters = [
                self.floatingIp,
                self.apiToken,
                self.finderType,
                self.sleep
        ]
        self.setHint('start', 'timeout', '10')

    def getParameters(self):
        return self.parameters

    def populated(self):
        if not self.apiToken.get():
            return
        configuration = HetznerCloudClientConfiguration().with_api_key( self.apiToken.get() ).with_api_version(1)
        self.client = HetznerCloudClient(configuration)
        self.wait = int( self.sleep.get() )
        self.rateLimitWait = int( self.sleep.get() ) * 5 

    def start(self):
        success = False
        hostFinder = makeHostFinder( self.finderType.get() )
        while not success:
            try:
                server = self.hostFinder.find( self.client )
            except HetznerActionException:
                time.sleep( self.wait )
            except HetznerInternalServerErrorException:
                time.sleep( self.wait )
            except HetznerRateLimitExceeded:
                time.sleep( self.rateLimitWait )

        success = False
        try:
            while not success:
                try:
                    ip = self.ipFinder.find( self.client )
                    ip.assign_to_server( server.id )
                    success = True
                except HetznerActionException:
                    time.sleep( self.wait )
                except HetznerInternalServerErrorException:
                    time.sleep( self.wait )
                except HetznerRateLimitExceeded:
                    time.sleep( self.rateLimitWait )
        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            return ocf.ReturnCodes.isMissconfigured

    def stop(self):
        return ocf.ReturnCodes.success

    def monitor(self):
        isActive = False

        try:
            hostFinder = makeHostFinder( self.finderType.get() )
            success = False
            while not success:
                try:
                    server = self.hostFinder.find( self.client )
                except HetznerActionException:
                    time.sleep( self.wait )
                except HetznerInternalServerErrorException:
                    time.sleep( self.wait )
                except HetznerRateLimitExceeded:
                    time.sleep( self.rateLimitWait )

            success = False
            while not success:
                try:
                    ip = self.ipFinder.find( self.client )
                    if ip.server == server.id:
                        isActive = True
                    success = True
                except HetznerInternalServerErrorException:
                    time.sleep( self.wait )
                except HetznerActionException:
                    time.sleep( self.wait )
                except HetznerRateLimitExceeded:
                    time.sleep( self.rateLimitWait )
        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            return ocf.ReturnCodes.isMissconfigured
        return isActive

class Stonith():
    def __init__(self):
        self.sleep = ocf.Parameter('sleep', default="2", shortDescription='Time in seconds to sleep on failed api requests' ,
                description='''
                If a request to the hetzner api fails then the device will retry the request after the number of
                seconds specified here, or 1 second by default.

                Exceptions to this are:
                Requests which failed due to the rate limit will sleep for 5 times the time set here

                Requests which failed due to insufficient permissions will not be retried and will
                cause the device to error out.
                This is because as of the time writing this there are not scopes for api tokens. If
                a request is denied by the api the token was most likely deleted
                ''',
                required=False, unique=False)
        self.apiToken = ocf.Parameter('api_token', shortDescription='Hetner Cloud api token' ,
                description='''
                The Hetzner Cloud api token with which the ip address can be managed.

                You can create this in the Hetner Cloud Console. Select the project
                which contains your Ip-Address, then select `Access` on the leftside menu
                Activate the second tab `Api Tokens` and create a new token.
                ''',
                required=True, unique=False)
        self.hostnameToApi = ocf.Parameter('hostname_to_api', shortDescription='hostname:apiname - only match the given hostname, reset the server with the given api name' ,
                description='''
                When this parameter is given then the stonith device switches to a different mode.
                Format: hostname:apiname[,hostname2:apiname2]

                Default Mode:
                The names of all servers present in the api project are reported as managed.
                Finding the api server to manage is done by looking for an api server with 'hostname' as its name.
                -> The hostnames MUST match the servers name in the api

                hostname_to_api Mode:
                Only the give 'hostnames' are reported as managed
                Finding  the api server to manage is done by looking for an api server with the matching 'apiname' as its name
                -> hostnames can be mapped to server names in the api
                ''',
                required=False, unique=False)

        self.parameters = [
                self.apiToken,
                self.hostnameToApi,
                self.sleep,
        ]

    def getParameters(self):
        return self.parameters
    
    def setHost(self, host):
        if self.hostnameToApi.get():
            hostlist = self.hostnameToApi.get().split(',')
            for hostToApi in hostlist:
                hostname, apiname = hostToApi.split(':')
                if hostname == host:
                    self.hostFinder = HostnameHostFinder(apiname)
                    return
            raise KeyError
            return
        self.hostFinder = HostnameHostFinder(host)
            

    def populated(self):
        if not self.apiToken.get():
            return
        configuration = HetznerCloudClientConfiguration().with_api_key( self.apiToken.get() ).with_api_version(1)
        self.client = HetznerCloudClient(configuration)
        self.wait = int( self.sleep.get() )
        self.rateLimitWait = int( self.sleep.get() ) * 5 

    def getHosts(self):
        if self.hostnameToApi.get():
            hostnames = []
            hostlist = self.hostnameToApi.get().split(',')
            for host in hostlist:
                host.split(':')
                hostnames.append(host[0])
            print( ' '.join(hostnames) )
            return stonith.ReturnCodes.success
                
            
        success = False
        while not success:
            try:
                hosts = list(self.client.servers().get_all())
                success = True
            except HetznerAuthenticationException:
                print('Error: Cloud Api returned Authentication error. Token deleted?')
                return stonith.ReturnCodes.isMissconfigured
            except HetznerInternalServerErrorException:
                time.sleep( self.wait )
            except HetznerRateLimitExceeded:
                time.sleep( self.rateLimitWait )

        hostnames = []
        for host in hosts:
            hostnames.append(host.name)
            

        print( ' '.join(hostnames) )
            
        return stonith.ReturnCodes.success

    def powerOn(self):
        host = self.hostFinder.find(self.client)
        host.power_on()

    def powerOff(self):
        host = self.hostFinder.find(self.client)
        host.power_off()

    def powerReset(self):
        host = self.hostFinder.find(self.client)
        host.reset()

    def status(self):
        try:
            success = False
            while not success:
                try:
                    list( self.client.servers().get_all() )
                    success = True
                except HetznerInternalServerErrorException:
                    time.sleep(self.wait)
                except HetznerRateLimitExceeded:
                    time.sleep(self.rateLimitWait)

        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            return stonith.ReturnCodes.isMissconfigured
        return stonith.ReturnCodes.success

    def infoId(self):
        print ("hetzner_cloud")
        return stonith.ReturnCodes.success

    def infoName(self):
        print ("hetzner_cloud")
        return stonith.ReturnCodes.success

    def infoUrl(self):
        print ("https://github.com/svensp/hcloud_ocf")
        return stonith.ReturnCodes.success

    def infoDescription(self):
        print ('''
        Use the hetzner cloud api as stonith device for your cluster.
        
        If your hostnames match your server names in the api then only an api token
        is required. Otherwise you can set a list of hostnames to apinames with the
        hostname_to_api paramter.
        Format: hostname:apiname[,hostname2:apiname2]
        ''')
        return stonith.ReturnCodes.success
