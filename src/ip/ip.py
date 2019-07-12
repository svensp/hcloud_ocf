from hetznercloud import ACTION_STATUS_SUCCESS

class Ip:
    def setRetriever(self, retriever):
        self.retriever = retriever

    def retrieve(self):
        self.retriever.retrieve()
        self.hetznerIp = self.retriever.getIp()
        return self

    def setTargetServer(self, server):
        self.server = server
        return self

    def assign(self):
        action = self.hetznerIp.assign_to_server(self.server.getId())
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)
        return self
