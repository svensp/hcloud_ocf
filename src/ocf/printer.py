class Printer:
    def print(message):
        print(message)

class BagPrinter(Printer):
    def __init__(self):
        self.log = ""

    def print(self, message):
        self.log += message

