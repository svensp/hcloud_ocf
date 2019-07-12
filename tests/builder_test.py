import unittest
from unittest.mock import Mock

class BuilderTest(unittest.TestCase):
    def setUp(self):
        self.setUpMocks()

    def setUpMocks(self):
        self.floatingIp = FloatingIp()
