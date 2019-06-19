import os

class Environment:
    def __init__(self, environ = os.environ):
        self.environ = environ

    def get(self, name, defaultValue = None):
        if not self.environ.has_key(name):
            return defaultValue

        return self.environ.get('OCF_RESKEY_'+name)
