import abc
from abc import abstractmethod
import ocf.exception
import ocf.return_codes
import ocf.resource_agent_runner
import ocf.printer

class ResourceAgent(abc.ABC):
    def __init__(self, runner = ocf.resource_agent_runner.ResourceAgentRunner(), printer = ocf.printer.Printer() ):
        self.runner = runner
        self.printer = printer

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def monitor(self):
        pass

    def stop(self):
        pass

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
        return ocf.return_codes.Success()

    def run(self, action):
        return self.runner.setResourceAgent(self).setAction(action).run()
