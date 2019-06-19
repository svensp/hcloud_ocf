class ResourceAgentRunner:

    def setResourceAgent(self, resourceAgent):
        self.resourceAgent = resourceAgent
        return self

    def setAction(self, action):
        self.action = action
        return self
    
    def run(self):
        actionSwitcher = {
            "start": self.resourceAgent.start,
            "stop": self.resourceAgent.stop,
            "monitor": self.resourceAgent.monitor,
            "status": self.resourceAgent.monitor,
            "promote": self.resourceAgent.promote,
            "demote": self.resourceAgent.demote,
            "migrate_to": self.resourceAgent.migrateTo,
            "migrate_from": self.resourceAgent.migrateFrom,
        }
        func = actionSwitcher.get(self.action, lambda: ocf.return_codes.GenericError())
        returnCode = func()
        return returnCode.getValue()
