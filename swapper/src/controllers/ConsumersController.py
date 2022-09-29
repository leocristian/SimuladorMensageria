import os

class ConsumersController:
    def __init__(self):
        self.consumers = []
    
    def isNewConsumer(self, address):
        return (address not in self.consumers)
    
    def createConsumer(self, topic, address):
        self.consumers.append({"topic": topic, "address": address})
    
    def showConsumersQueue(self):
        os.system('cls')
        for i in self.consumers:
            print(i)