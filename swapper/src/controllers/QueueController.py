class QueueController:
    def __init__(self):
        self.queues = []
        self.clients = []
        self.consumers = []
    
    def isNewTopic(self, topic):
        return (topic not in self.clients)

    def createConsumer(self, topic, address):
        self.clients.append({"topic":topic, "address":address})
 
    def createEmptyQueue(self, topic): 
        self.queues.append({"topic": topic, "queue": []})
    
    def createNewQueue(self, msg):
        self.clients.append(msg["topic"])
        self.queues.append({"topic": msg["topic"], "queue": []})
        # self.insertInCurrentQueue(msg)
    
    def insertInCurrentQueue(self, msg):
        for i in self.queues:
            if i["topic"] == msg["topic"]:
                 i["queue"].append({"body": msg["body"]})
    
    def removeFromQueue(self, topic):
        for i in self.queues:
            if i["topic"] == topic:
                i["queue"].pop()

    def showAllQueues(self):
        for i in self.queues:
            print(f"topic: {i['topic']}----------------")
            for j in i["queue"]:
                print(j)
    
    def showQueueLen(self):
        for i in self.queues:
            print(f"{len(i['queue'])} mensagens recebidas com o tópico: {i['topic']} ")
                
    def showClientQueue(self, topic):
        for i in self.queues:
            if i["topic"] == topic:
                for j in i["queue"]:
                    print(j)