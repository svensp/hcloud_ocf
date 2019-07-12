class Retriever:
    def setClient(self, client):
        self.client = client

class ByIdRetriever(Retriever):
    def setId(self, id):
        self.id = id
    
    def retrieve():
        return self.client.floating_ips().get(self.id)
