import socket
import threading
import json

class Swapper:
    def __init__(self):
        addres = ("localhost", 8000) #host and port
        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind(addres)

        self.producers = []
        self.queues = []

    def receiveMessages(self):
        self.swapper_server.listen(10)
        print('swapper is receiving...')
        
        while True:
        
            clientsock, clientAddr = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()

            msg = eval(msg)
            
            msg = json.dumps(msg, indent = 4)
            msg = json.loads(msg)

            if msg["producerID"] not in self.producers:
                self.producers.append(msg["producerID"])
                self.queues.append({"producerID": msg["producerID"], "queue": []})
            else:
                for i in self.queues:
                    if i["producerID"] == msg["producerID"]:
                        i["queue"].append({"topic": msg["topic"], "body": msg["body"]})
        

            print("Message Received...")
            print(self.queues)
    
    def distributeMessages(self):
        print('swapper is sending...')

        pass

if __name__=='__main__':
    swapper = Swapper()
    swapper.receiveMessages()