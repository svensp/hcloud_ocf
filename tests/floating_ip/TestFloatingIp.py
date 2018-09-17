#!/usr/bin/python3
import sys
import os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../../floating_ip' )
import floating_ip
import shared
import ocf
import hetznercloud
import time
import unittest
import mock

class TestFloatingIp(unittest.TestCase):

    def makeBase(self, client, makeHostFinder):
        # mock HostFinder to return a generic server object
        server = hetznercloud.servers.HetznerCloudServer([])
        server.id = 51
        hostFinder = shared.HostFinder()
        hostFinder.find = mock.Mock(return_value=server)
        makeHostFinder.return_value = hostFinder

        # mock IpFinder to return a generic floating ip object
        ip = hetznercloud.floating_ips.HetznerCloudFloatingIp([])
        floatingIp = floating_ip.FloatingIp()
        floatingIp.client = client
        floatingIp.ipFinder.find = mock.Mock(return_value=ip)

        # mock client
        ip.assign_to_server = mock.Mock()
        return [server, hostFinder, ip, floatingIp]

    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_returns_success(self, client, makeHostFinder):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)

        assert floatingIp.start() is ocf.ReturnCodes.success

    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_assigns_ip(self, client, makeHostFinder):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_returns_missconfigured_on_not_found(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        hostFinder.find = mock.Mock(side_effect=EnvironmentError('host not found'))

        assert floatingIp.start() is ocf.ReturnCodes.isMissconfigured

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_host_server_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        hostFinder.find = mock.Mock(side_effect=[hetznercloud.HetznerInternalServerErrorException(''), server])

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_ip_server_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        floatingIp.ipFinder.find = mock.Mock(side_effect=[hetznercloud.HetznerInternalServerErrorException(''), ip])

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_assign_server_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.assign_to_server = mock.Mock(side_effect=[hetznercloud.HetznerInternalServerErrorException(''), ip])

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_host_ratelimit_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        floatingIp.ipFinder.find = mock.Mock(side_effect=[hetznercloud.HetznerRateLimitExceeded(''), ip])

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_host_json_decode_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        floatingIp.ipFinder.find = mock.Mock(side_effect=[ValueError('json decode error'), ip])

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_ip_ratemlimit_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        floatingIp.ipFinder.find = mock.Mock(side_effect=[hetznercloud.HetznerRateLimitExceeded(''), ip])

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )
        sleep.assert_called_once()
        
    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_assign_ratemlimit_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.assign_to_server = mock.Mock(side_effect=[hetznercloud.HetznerRateLimitExceeded(''), ip])

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_assign_ratemlimit_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.assign_to_server = mock.Mock(side_effect=[ValueError('json decode error'), ip])

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_with( server.id )
        sleep.assert_called_once()

    def test_stop_returns_success(self):
        floatingIp = floating_ip.FloatingIp()
        assert floatingIp.stop() is ocf.ReturnCodes.success
        
    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_assign_action_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.assign_to_server = mock.Mock(side_effect=[hetznercloud.HetznerActionException(''), ip])

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_returns_success_if_assigned_to_server(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id

        assert floatingIp.monitor() is ocf.ReturnCodes.success

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_returns_not_running_if_not_assigned_to_server(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id + 5

        assert floatingIp.monitor() is ocf.ReturnCodes.isNotRunning


    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_retries_on_server_rate_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        hostFinder.find = mock.Mock(side_effect=[hetznercloud.HetznerRateLimitExceeded(''), server])

        assert floatingIp.monitor() is ocf.ReturnCodes.success

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_retries_on_server_server_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        hostFinder.find = mock.Mock(side_effect=[hetznercloud.HetznerInternalServerErrorException(''), server])

        assert floatingIp.monitor() is ocf.ReturnCodes.success

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_retries_on_server_json_decode_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        hostFinder.find = mock.Mock(side_effect=[ValueError('Json decode error'), server])

        assert floatingIp.monitor() is ocf.ReturnCodes.success

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_retries_on_ip_rate_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        floatingIp.ipFinder.find = mock.Mock(side_effect=[hetznercloud.HetznerRateLimitExceeded(''), ip])

        assert floatingIp.monitor() is ocf.ReturnCodes.success
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_retries_on_ip_server_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        floatingIp.ipFinder.find = mock.Mock(side_effect=[hetznercloud.HetznerInternalServerErrorException(''), ip])

        assert floatingIp.monitor() is ocf.ReturnCodes.success
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_retries_on_ip_json_decode_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        floatingIp.ipFinder.find = mock.Mock(side_effect=[ValueError('Json decode error'), ip])

        assert floatingIp.monitor() is ocf.ReturnCodes.success
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_returns_missconfigured_on_not_found(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        hostFinder.find = mock.Mock(side_effect=EnvironmentError('host not found'))

        assert floatingIp.monitor() is ocf.ReturnCodes.isMissconfigured

    def test_stop_returns_success(self):
        floatingIp = floating_ip.FloatingIp()
        assert floatingIp.stop() is ocf.ReturnCodes.success

if __name__ == '__main__':
    unittest.main()
