#!/usr/bin/python3
import sys
sys.path.append( '../../floating_ip')
import floating_ip
import shared
import ocf
import hetznercloud
import time
import unittest
import mock

class ExceptionTimes:
    def __init__(self, exception, return_value=False, times = 1):
        self.called = 0
        self.exception = exception
        self.times = times
        self.return_value = return_value

    def run(self, *args, **kwargs):
        if self.times <= self.called:
            return self.return_value
        self.called += 1
        raise self.exception

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
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerInternalServerErrorException(''), server)
        hostFinder.find = mock.Mock(side_effect=exceptionTimes.run)

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_ip_server_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerInternalServerErrorException(''), ip)
        floatingIp.ipFinder.find = mock.Mock(side_effect=exceptionTimes.run)

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_assign_server_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerInternalServerErrorException(''), ip)
        ip.assign_to_server = mock.Mock(side_effect=exceptionTimes.run)

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_host_ratelimit_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerRateLimitExceeded(''), ip)
        floatingIp.ipFinder.find = mock.Mock(side_effect=exceptionTimes.run)

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_ip_ratemlimit_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerRateLimitExceeded(''), ip)
        floatingIp.ipFinder.find = mock.Mock(side_effect=exceptionTimes.run)

        assert floatingIp.start() is ocf.ReturnCodes.success
        ip.assign_to_server.assert_called_once_with( server.id )
        sleep.assert_called_once()
        
    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_start_retries_on_assign_ratemlimit_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerRateLimitExceeded(''), ip)
        ip.assign_to_server = mock.Mock(side_effect=exceptionTimes.run)

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
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerActionException(''), ip)
        ip.assign_to_server = mock.Mock(side_effect=exceptionTimes.run)

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
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerRateLimitExceeded(''), server)
        hostFinder.find = mock.Mock(side_effect=exceptionTimes.run)

        assert floatingIp.monitor() is ocf.ReturnCodes.success

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_retries_on_server_server_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerInternalServerErrorException(''), server)
        hostFinder.find = mock.Mock(side_effect=exceptionTimes.run)

        assert floatingIp.monitor() is ocf.ReturnCodes.success

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_retries_on_ip_rate_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerRateLimitExceeded(''), ip)
        floatingIp.ipFinder.find = mock.Mock(side_effect=exceptionTimes.run)

        assert floatingIp.monitor() is ocf.ReturnCodes.success
        sleep.assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.makeHostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_monitor_retries_on_ip_server_error(self, client, makeHostFinder, sleep):

        server, hostFinder, ip, floatingIp = self.makeBase(client, makeHostFinder)
        ip.server = server.id
        exceptionTimes = ExceptionTimes(hetznercloud.HetznerInternalServerErrorException(''), ip)
        floatingIp.ipFinder.find = mock.Mock(side_effect=exceptionTimes.run)

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
