#!/usr/bin/python3
import os
import sys
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../../stonith' )
import abc
import hetznercloud
import stonith
import stonith_agent
import time
import unittest
from unittest import mock
from mock import Mock, MagicMock
import stonith_agent

class TestBase(abc.ABC):

    @abc.abstractmethod
    def takeAction(self, agent):
        pass

    def makeBase(self, client, hostFinder):
        server = hetznercloud.servers.HetznerCloudServer([])
        server.id = 51
        server.power_on = Mock(return_value=MagicMock())
        server.power_off = Mock(return_value=MagicMock())
        server.reset = Mock(return_value=MagicMock())
        hostFinder.find = Mock(return_value=server)
        agent = stonith_agent.Stonith()
        agent.hostFinder = hostFinder
        return [server, hostFinder, agent]

    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_returns_success(self, client, hostFinder):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        returnCode = self.takeAction(agent)
        assert returnCode == stonith.ReturnCodes.success

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_repeatet_after_wait_on_host_find_environment_error(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        hostFinder.find = Mock(side_effect=[EnvironmentError("Host not found"), server])
        self.takeAction(agent)
        assert sleep.call_count == 1
        assert hostFinder.find.call_count == 2
        try:
            self.serverAction(server).assert_called_once()
        except AttributeError:
            pass

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_on_host_find_environment_error_if_fail_is_set(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        hostFinder.find = Mock(side_effect=[EnvironmentError("Host not found"), server])
        agent.failOnHostfindFailure.set('true')
        self.assertRaises(EnvironmentError, self.takeAction, agent)
        assert hostFinder.find.call_count is 1
        try:
            assert self.serverAction(server).assert_call_count is 0
        except AttributeError:
            pass

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_repeatet_after_wait_on_host_find_server_error(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        hostFinder.find = Mock(side_effect=[hetznercloud.HetznerInternalServerErrorException('502'), server])
        self.takeAction(agent)
        assert sleep.call_count == 1
        assert hostFinder.find.call_count == 2
        try:
            self.serverAction(server).assert_called_once()
        except AttributeError:
            pass

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_repeatet_after_wait_on_host_find_rate_limit_error(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        hostFinder.find.side_effect = [hetznercloud.HetznerRateLimitExceeded('502'), server]
        self.takeAction(agent)
        assert sleep.call_count == 1
        assert hostFinder.find.call_count == 2
        try:
            self.serverAction(server).assert_called_once()
        except AttributeError:
            pass

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_repeatet_after_wait_on_host_find_json_decode_error(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        hostFinder.find.side_effect = [ValueError('json decode error'), server]
        self.takeAction(agent)
        assert sleep.call_count == 1
        assert hostFinder.find.call_count == 2
        try:
            self.serverAction(server).assert_called_once()
        except AttributeError:
            pass

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_canceled_after_host_find_authentication_exception(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        hostFinder.find.side_effect = [hetznercloud.HetznerAuthenticationException(), server]
        self.takeAction(agent)
        assert hostFinder.find.call_count == 1
        try:
            assert self.serverAction(server).call_count == 0
        except AttributeError:
            pass

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_returns_missconfigured_after_host_find_authentication_exception(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        hostFinder.find.side_effect = [hetznercloud.HetznerAuthenticationException(), server]
        returnCode = self.takeAction(agent)
        assert returnCode == stonith.ReturnCodes.isMissconfigured

