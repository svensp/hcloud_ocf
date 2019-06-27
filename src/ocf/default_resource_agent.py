from ocf.resource_agent import ResourceAgent
import ocf.printer
import ocf.return_codes

class DefaultResourceAgent(ResourceAgent):
    def __init__(self):
        super().__init__(printer=ocf.printer.BagPrinter())

    def start(self):
        return ocf.return_codes.Success()

    def monitor(self):
        return ocf.return_codes.Success()
