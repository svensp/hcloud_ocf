import abc
from abc import abstractmethod
import ocf.exception
import ocf.return_codes

class ResourceAgent(abc.ABC):
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

    def run(self, action):
        actionSwitcher = {
            "start": self.start,
            "stop": self.stop,
            "monitor": self.monitor,
            "status": self.monitor,
            "promote": self.promote,
            "demote": self.demote,
            "migrate_to": self.migrateTo,
            "migrate_from": self.migrateFrom,
        }
        func = actionSwitcher.get(action, lambda: ocf.return_codes.GenericError())
        returnCode = func()
        return returnCode.getValue()
