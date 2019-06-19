from ocf.resource_agent import ResourceAgent
import ocf.printer

class DefaultResourceAgent(ResourceAgent):
    def __init__(self):
        super().__init__(printer=ocf.printer.BagPrinter())

    def start(self):
        pass

    def monitor(self):
        pass
