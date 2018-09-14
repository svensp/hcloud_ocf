#!/usr/bin/python3
import os
import sys
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) + '/../../stonith' )
import Base
import abc
import hetznercloud
import stonith
import stonith_agent
import time
import unittest
from unittest import mock
from mock import Mock
import stonith_agent

class TestBase(Base.TestBase):

    @abc.abstractmethod
    def serverAction(self, server):
        pass

    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_called(self, client, hostFinder):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        self.takeAction(agent)
        self.serverAction(server).assert_called_once()

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_repeatet_after_wait_on_action_server_error(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        self.serverAction(server).side_effect = [hetznercloud.HetznerInternalServerErrorException('502'), server]
        self.takeAction(agent)
        assert sleep.call_count == 1
        assert self.serverAction(server).call_count == 2

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_repeatet_after_wait_on_action_rate_limit_error(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        self.serverAction(server).side_effect = [hetznercloud.HetznerRateLimitExceeded('502'), server]
        self.takeAction(agent)
        assert sleep.call_count == 1
        assert self.serverAction(server).call_count == 2

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_repeatet_after_wait_on_action_action_error(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        self.serverAction(server).side_effect = [hetznercloud.HetznerActionException('502'), server]
        self.takeAction(agent)
        assert sleep.call_count == 1
        assert self.serverAction(server).call_count == 2

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_is_canceled_after_action_authentication_exception(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        self.serverAction(server).side_effect = [hetznercloud.HetznerAuthenticationException(), server]
        self.takeAction(agent)
        assert self.serverAction(server).call_count == 1

    @mock.patch('time.sleep')
    @mock.patch('shared.HostFinder')
    @mock.patch('hetznercloud.HetznerCloudClient')
    def test_action_returns_missconfigured_after_action_authentication_exception(self, client, hostFinder, sleep):
        server, hostFinder, agent = self.makeBase(client, hostFinder)
        agent.client = client
        self.serverAction(server).side_effect = [hetznercloud.HetznerAuthenticationException(), server]
        returnCode = self.takeAction(agent)
        assert returnCode == stonith.ReturnCodes.isMissconfigured
