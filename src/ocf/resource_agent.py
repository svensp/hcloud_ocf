import abc
from abc import abstractmethod
import ocf.exception
import ocf.return_codes
import ocf.resource_agent_runner
import ocf.printer
import ocf.metadata

class ResourceAgent(abc.ABC):
    def __init__(self,
            runner = ocf.resource_agent_runner.ResourceAgentRunner(),
            printer = ocf.printer.Printer(),
            meta= ocf.metadata.Metadata() ):
        self.runner = runner
        self.printer = printer
        self.meta = meta
        self.validatedActions = [
                'start',
                'stop',
                'monitor',
                'status',
                'promote',
                'demote',
                'migrate_to',
                'migrate_from',
                ]

    def buildPreValidation(self):
        pass

    def isValidated(self, action):
        return action in self.validatedActions

    def build(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def monitor(self):
        pass

    def stop(self):
        return ocf.return_codes.Success()

    def promote(self):
        raise ocf.exception.Exception( ocf.return_codes.UnimplementedError() )

    def demote(self):
        raise ocf.exception.Exception( ocf.return_codes.UnimplementedError() )

    def migrateTo(self):
        raise ocf.exception.Exception( ocf.return_codes.UnimplementedError() )

    def migrateFrom(self):
        raise ocf.exception.Exception( ocf.return_codes.UnimplementedError() )

    def help(self):
        return ocf.return_codes.Success()

    def validate(self):
        return ocf.return_codes.Success()

    def metaData(self):
        self.printer.print("<xml></xml>")
        self.meta.setPrinter(self.printer).print()

        return ocf.return_codes.Success()

    def run(self, action):
        return self.runner.setResourceAgent(self).setAction(action).run()
