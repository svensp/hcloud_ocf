import ocf.return_codes

class Exception(Exception):
    def __init__(self, returnCode = ocf.return_codes.GenericError()):
        self.returnCode = returnCode

    def getReturnCode(self):
        return self.returnCode
