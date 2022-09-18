class QueueController:
    def __init__(self):
        self.queues = []
        self.clients = []

    def isNewClient(self, clientID):
        return (clientID not in self.clients)
    
    def createNewQueue(self, msg):
        self.clients.append(msg["clientID"])
        self.queues.append({"clientID": msg["clientID"], "queue": []})
        self.insertInCurrentQueue(msg)
    
    def insertInCurrentQueue(self, msg):
        for i in self.queues:
            if i["clientID"] == msg["clientID"]:
                 i["queue"].append({"topic": msg["topic"], "body": msg["body"]})
    
    def removeFromQueue(self, clientID):
        for i in self.queues:
            if i["clientID"] == clientID:
                i["queue"].pop()

    def showAllQueues(self):
        for i in self.queues:
            print(f"Client: {i['clientID']}----------------")
            for j in i["queue"]:
                print(j)
