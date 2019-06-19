import unittest
from unittest import mock
import ocf.exception

class OcfExceptionTest(unittest.TestCase):
    def setUp(self):
        self.exception = ocf.exception.Exception()

    def testExceptionIsException(self):
        self.assertIsInstance(self.exception, Exception)

    def testHasReturnCode(self):
        returnCode = self.exception.getReturnCode()

    def testReturnCodeIsReturnCode(self):
        returnCode = self.exception.getReturnCode()

        self.assertIsInstance(returnCode, ocf.return_codes.ReturnCode)

    def testDefaultReturnCodeIsGenericError(self):
        returnCode = self.exception.getReturnCode()

        self.assertIsInstance(returnCode, ocf.return_codes.GenericError)

    def testCanSetReturnCode(self):
        exception = ocf.exception.Exception( ocf.return_codes.Success() )
        returnCode = exception.getReturnCode()

        self.assertIsInstance(returnCode, ocf.return_codes.Success)
