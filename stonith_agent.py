#!/usr/bin/python3
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

import time
import stonith
import shared
from hetznercloud import HetznerCloudClientConfiguration, HetznerCloudClient, \
        ACTION_STATUS_SUCCESS
from hetznercloud.servers import HetznerCloudServer, SERVER_STATUS_OFF
from hetznercloud.floating_ips import HetznerCloudFloatingIp
from hetznercloud.exceptions import HetznerAuthenticationException, \
        HetznerInternalServerErrorException, HetznerActionException, \
        HetznerRateLimitExceeded, HetznerWaitAttemptsExceededException

class FindHostException(Exception):
    def __init__(self, code):
        self.code = code

class Stonith():
    def __init__(self):
        self.sleep = stonith.Parameter('sleep', default="5", shortDescription='Time in seconds to sleep on failed api requests' ,
                description='''
                If a request to the hetzner api fails then the device will retry the request after the number of
                seconds specified here, or 5 second by default.

                Exceptions to this are:
                Requests which failed due to the rate limit will sleep for 5 times the time set here

                Requests which failed due to insufficient permissions will not be retried and will
                cause the device to error out.
                This is because as of the time writing this there are not scopes for api tokens. If
                a request is denied by the api the token was most likely deleted
                ''',
                required=False, unique=False)
        self.apiToken = stonith.Parameter('api_token', shortDescription='Hetner Cloud api token' ,
                description='''
                The Hetzner Cloud api token with which the ip address can be managed.

                You can create this in the Hetner Cloud Console. Select the project
                which contains your Ip-Address, then select `Access` on the leftside menu
                Activate the second tab `Api Tokens` and create a new token.
                ''',
                required=True, unique=False)
        self.hostnameToApi = stonith.Parameter('hostname_to_api', shortDescription='hostname:apiname - only match the given hostname, reset the server with the given api name' ,
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
        self.failOnHostfindFailure = stonith.Parameter('fail_on_host_find_failure', shortDescription='Exit with misconfigured if the host was not found' ,
                description='''
                If this is set to true then failing to find a host will cause the agent to exit
                with a Missconfigured error - usually a fatal exit code preventing the resource
                from being started again without user interventaion
                ''',
                required=False, unique=False)
        self.wait = 5
        self.rateLimitWait = 5

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
                    self.hostFinder = shared.HostnameHostFinder(apiname)
                    return
            raise KeyError
            return
        self.hostFinder = shared.HostnameHostFinder(host)

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
            except ValueError: # JSONDecodeError
                time.sleep( self.wait )

        hostnames = []
        for host in hosts:
            hostnames.append(host.name)
            

        print( ' '.join(hostnames) )
            
        return stonith.ReturnCodes.success

    def powerOn(self):
        try: 
            host = self.findServer()
        except FindHostException as e:
            return e.code

        try:
            success = False
            while not success:
                try:
                    powerOnAction = host.power_on()
                    powerOnAction.wait_until_status_is(ACTION_STATUS_SUCCESS, \
                           attempts=5, wait_seconds=self.wait)
                    success = True
                except HetznerWaitAttemptsExceededException:
                    time.sleep(self.wait)
                except HetznerInternalServerErrorException:
                    time.sleep(self.wait)
                except HetznerRateLimitExceeded:
                    time.sleep(self.rateLimitWait)
                except HetznerActionException:
                    time.sleep(self.wait)
                except ValueError: # JSONDecodeError
                    time.sleep( self.wait )

        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            return stonith.ReturnCodes.isMissconfigured

        return stonith.ReturnCodes.success

    def powerOff(self):
        try:
            success = False
            while not success:
                try:
                    host = self.findServer()
                    if host.status == SERVER_STATUS_OFF:
                        return stonith.ReturnCodes.success

                    powerOffAction = host.power_off()
                    powerOffAction.wait_until_status_is(ACTION_STATUS_SUCCESS, \
                           attempts=5, wait_seconds=self.wait)
                    success = True
                except FindHostException as e:
                    return e.code
                except HetznerWaitAttemptsExceededException:
                    time.sleep(self.wait)
                except HetznerInternalServerErrorException:
                    time.sleep(self.wait)
                except HetznerRateLimitExceeded:
                    time.sleep(self.rateLimitWait)
                except HetznerActionException:
                    time.sleep(self.wait)
                except ValueError: # JSONDecodeError
                    time.sleep( self.wait )

        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            return stonith.ReturnCodes.isMissconfigured

        return stonith.ReturnCodes.success

    def powerReset(self):
        try:
            success = False
            while not success:
                try:
                    host = self.findServer()
                    if host.status == SERVER_STATUS_OFF:
                        return stonith.ReturnCodes.success

                    resetAction  = host.reset()
                    resetAction.wait_until_status_is(ACTION_STATUS_SUCCESS, \
                           attempts=5, wait_seconds=self.wait)
                    success = True
                except FindHostException as e:
                    return e.code
                except HetznerWaitAttemptsExceededException:
                    time.sleep(self.wait)
                except HetznerInternalServerErrorException:
                    time.sleep(self.wait)
                except HetznerActionException:
                    time.sleep(self.wait)
                except HetznerRateLimitExceeded:
                    time.sleep(self.rateLimitWait)
                except ValueError: # JSONDecodeError
                    time.sleep(self.wait)

        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            return stonith.ReturnCodes.isMissconfigured

        return stonith.ReturnCodes.success

    def status(self):
        try: 
            host = self.findServer()
        except FindHostException as e:
            return e.code
        return stonith.ReturnCodes.success

    
    def findServer(self):
        try:
            success = False
            while not success:
                try:
                    host = self.hostFinder.find(self.client)
                    success = True
                except HetznerInternalServerErrorException:
                    time.sleep(self.wait)
                except HetznerRateLimitExceeded:
                    time.sleep(self.rateLimitWait)
                except EnvironmentError as e: # Host not found
                    if self.failOnHostfindFailure.get() is 'true':
                        raise e
                    time.sleep(self.wait)
                except ValueError: # JSONDecodeError
                    time.sleep(self.wait)

        except HetznerAuthenticationException:
            print('Error: Cloud Api returned Authentication error. Token deleted?')
            raise FindHostException(stonith.ReturnCodes.isMissconfigured)

        return host

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
