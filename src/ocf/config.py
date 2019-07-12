class Config:
    def __init__(self, environ):
        self.environ = environ

    def get(self, key):
        return self.environ['OCF_RESKEY_'+key]
