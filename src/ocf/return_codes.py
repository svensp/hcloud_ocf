import abc

class ReturnCode(abc.ABC):
    @abc.abstractmethod
    def getValue(self):
        pass

    @abc.abstractmethod
    def getAlias(self):
        pass

    @abc.abstractmethod
    def getDescription(self):
        pass

    @abc.abstractmethod
    def getSeverity(self):
        pass

class Success(ReturnCode):
    def getValue(self):
        return 0

    def getAlias(self):
        return "OCF_SUCCESS"

    def getDescription(self):
        return "Success. The command completed successfully. This is the expected result for all start, stop, promote and demote commands."

    def getSeverity(self):
        return "soft"

class GenericError(ReturnCode):
    def getValue(self):
        return 1

    def getAlias(self):
        return "OCF_ERR_GENERIC"

    def getDescription(self):
        return "Generic \"there was a problem\" error code."

    def getSeverity(self):
        return "soft"

class ArgumentsError(ReturnCode):
    def getValue(self):
        return 2

    def getAlias(self):
        return "OCF_ERR_ARGS"

    def getDescription(self):
        return "The resource’s configuration is not valid on this machine. E.g. it refers to a location not found on the node."

    def getSeverity(self):
        return "hard"

class UnimplementedError(ReturnCode):
    def getValue(self):
        return 3

    def getAlias(self):
        return "OCF_ERR_UNIMPLEMENTED"

    def getDescription(self):
        return "The requested action is not implemented."

    def getSeverity(self):
        return "hard"

class PermissionError(ReturnCode):
    def getValue(self):
        return 4

    def getAlias(self):
        return "OCF_ERR_PERM"

    def getDescription(self):
        return "The resource agent does not have sufficient privileges to complete the task."

    def getSeverity(self):
        return "hard"

class InstallationError(ReturnCode):
    def getValue(self):
        return 5

    def getAlias(self):
        return "OCF_ERR_INSTALLED"

    def getDescription(self):
        return "The tools required by the resource are not installed on this machine."

    def getSeverity(self):
        return "hard"

class ConfigurationError(ReturnCode):
    def getValue(self):
        return 6

    def getAlias(self):
        return "OCF_ERR_CONFIGURED"

    def getDescription(self):
        return "The resource’s configuration is invalid. E.g. required parameters are missing."

    def getSeverity(self):
        return "fatal"

class NotRunning(ReturnCode):
    def getValue(self):
        return 7

    def getAlias(self):
        return "OCF_NOT_RUNNING"

    def getDescription(self):
        return "The resource is safely stopped. The cluster will not attempt to stop a resource that returns this for any action."

    def getSeverity(self):
        return "Not applicable"

class RunningMaster(ReturnCode):
    def getValue(self):
        return 8

    def getAlias(self):
        return "OCF_RUNNING_MASTER"

    def getDescription(self):
        return "The resource is running in master mode."

    def getSeverity(self):
        return "soft"

class MasterFailed(ReturnCode):
    def getValue(self):
        return 9

    def getAlias(self):
        return "OCF_FAILED_MASTER"

    def getDescription(self):
        return "The resource is in master mode but has failed. The resource will be demoted, stopped and then started (and possibly promoted) again."

    def getSeverity(self):
        return "soft"
