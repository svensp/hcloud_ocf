class Builder:
    def setTarget(self, floatingIp):
        self.floatingIp = floatingIp
        return self

    def buildPreValidation(self):
        #self.floatingIp.validators.append()
        return self

    def build(self):
        return self
