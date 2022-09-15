
class QueueController:
    def __init__(self):
        self.queues = []
        self.producers = []

    def isNewProducer(self, producerID):
        return (producerID not in self.producers)
    
    def createNewQueue(self, producerID):
        self.producers.append(producerID)
        self.queues.append({"producerID": producerID, "queue": []})
    
    def insertInCurrentQueue(self, msg):
        for i in self.queues:
            if i["producerID"] == msg["producerID"]:
                 i["queue"].append({"topic": msg["topic"], "body": msg["body"]})

    def showAllQueues(self):
        for i in self.queues:
            print(f"producer: {i['producerID']} | queue: {i['queue']}")
