#!/usr/bin/python3
import sys
sys.path.append( '../..')
from floating_ip import hcloud 
from unittest.mock import patch

#
# Test Definitions Begin
#
class TestIpHostFinder(unittest.TestCase):

    def test_find_server1(self):
        ifAddr = ifaddr
        ifAddr.get_adapter = Mock(return=[
            Mock().ips = [ Mock().ip = '192.168.2.1' ]
        ])
        ipHostFinder = hcloud.IpHostFinder( IfAddr([
            '192.168.2.1'
        ]) )

#
# Init test objects
#

ipHostFinder = hcloud.IpHostFinder( IfAddr([
    '192.168.2.1'
]) )

#
# Init test objects end
#

#
# Tests
#
print("find server_1")
server = ipHostFinder.find( PseudoClient([
    '192.168.2.1',
    '', 
]) )
assert server.name == 'server_1'

print("find server_2")
server = ipHostFinder.find( PseudoClient([
    '', 
    '192.168.2.1',
]) )
assert server.name == 'server_2'

print("find not found")
try:
    server = ipHostFinder.find( PseudoClient([
    ]) )
except EnvironmentError:
    environmentErrorCought = True
    pass
assert environmentErrorCought

if __name__ == '__main__':
    unittest.main()
