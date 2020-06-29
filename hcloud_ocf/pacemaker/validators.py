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
            
