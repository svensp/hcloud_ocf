import unittest
import ocf.return_codes

class ReturnCodesTest(unittest.TestCase):

    def testHasSuccessReturnCode(self):
        success = ocf.return_codes.Success()
        self.assertEqual( 0, success.getValue() )
        self.assertEqual( "OCF_SUCCESS", success.getAlias() )
        self.assertEqual( "Success. The command completed successfully. This is the expected result for all start, stop, promote and demote commands.", success.getDescription() )
        self.assertEqual( "soft", success.getSeverity() )

    def testHasGenericErrorReturnCode(self):
        genericError = ocf.return_codes.GenericError()
        self.assertEqual( 1, genericError.getValue() )
        self.assertEqual( "OCF_ERR_GENERIC", genericError.getAlias() )
        self.assertEqual( "Generic \"there was a problem\" error code.", genericError.getDescription() )
        self.assertEqual( "soft", genericError.getSeverity() )

    def testHasArgumentsErrorReturnCode(self):
        genericError = ocf.return_codes.ArgumentsError()
        self.assertEqual( 2, genericError.getValue() )
        self.assertEqual( "OCF_ERR_ARGS", genericError.getAlias() )
        self.assertEqual( "The resource’s configuration is not valid on this machine. E.g. it refers to a location not found on the node.", genericError.getDescription() )
        self.assertEqual( "hard", genericError.getSeverity() )

    def testHasUnimplementedErrorReturnCode(self):
        unimplementedError = ocf.return_codes.UnimplementedError()
        self.assertEqual( 3, unimplementedError.getValue() )
        self.assertEqual( "OCF_ERR_UNIMPLEMENTED", unimplementedError.getAlias() )
        self.assertEqual( "The requested action is not implemented.", unimplementedError.getDescription() )
        self.assertEqual( "hard", unimplementedError.getSeverity() )

    def testHasPermissionErrorReturnCode(self):
        permissionError = ocf.return_codes.PermissionError()
        self.assertEqual( 4, permissionError.getValue() )
        self.assertEqual( "OCF_ERR_PERM", permissionError.getAlias() )
        self.assertEqual( "The resource agent does not have sufficient privileges to complete the task.", permissionError.getDescription() )
        self.assertEqual( "hard", permissionError.getSeverity() )

    def testHasInstallationErrorReturnCode(self):
        permissionError = ocf.return_codes.InstallationError()
        self.assertEqual( 5, permissionError.getValue() )
        self.assertEqual( "OCF_ERR_INSTALLED", permissionError.getAlias() )
        self.assertEqual( "The tools required by the resource are not installed on this machine.", permissionError.getDescription() )
        self.assertEqual( "hard", permissionError.getSeverity() )

    def testHasConfigurationErrorReturnCode(self):
        configurationError = ocf.return_codes.ConfigurationError()
        self.assertEqual( 6, configurationError.getValue() )
        self.assertEqual( "OCF_ERR_CONFIGURED", configurationError.getAlias() )
        self.assertEqual( "The resource’s configuration is invalid. E.g. required parameters are missing.", configurationError.getDescription() )
        self.assertEqual( "fatal", configurationError.getSeverity() )

    def testHasNotRunningReturnCode(self):
        notRunning = ocf.return_codes.NotRunning()
        self.assertEqual( 7, notRunning.getValue() )
        self.assertEqual( "OCF_NOT_RUNNING", notRunning.getAlias() )
        self.assertEqual( "The resource is safely stopped. The cluster will not attempt to stop a resource that returns this for any action.", notRunning.getDescription() )
        self.assertEqual( "Not applicable", notRunning.getSeverity() )

    def testHasRunningMasterReturnCode(self):
        runningMaster = ocf.return_codes.RunningMaster()
        self.assertEqual( 8, runningMaster.getValue() )
        self.assertEqual( "OCF_RUNNING_MASTER", runningMaster.getAlias() )
        self.assertEqual( "The resource is running in master mode.", runningMaster.getDescription() )
        self.assertEqual( "soft", runningMaster.getSeverity() )

    def testHasMasterFailedReturnCode(self):
        masterFailed = ocf.return_codes.MasterFailed()
        self.assertEqual( 9, masterFailed.getValue() )
        self.assertEqual( "OCF_FAILED_MASTER", masterFailed.getAlias() )
        self.assertEqual( "The resource is in master mode but has failed. The resource will be demoted, stopped and then started (and possibly promoted) again.", masterFailed.getDescription() )
        self.assertEqual( "soft", masterFailed.getSeverity() )
