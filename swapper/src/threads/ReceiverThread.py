import threading
import socket
import json
from os import system
from ..QueueController import QueueController

class ReceiverThread(threading.Thread):
    def __init__(self, name, url, port):
        self.url = url
        self.port = port
        threading.Thread.__init__(self)
        self.name = name
        self.queueProducerController = QueueController()
    
    def run(self):
        addres = (self.url, self.port) #host and port
        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind(addres)
        self.swapper_server.listen(10)

        print(f'Receiver is started on address ({self.url}: {self.port})...')
        
        while True:
        
            clientsock, clientAddr = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()

            msg = eval(msg)
            
            msg = json.dumps(msg, indent = 4)
            msg = json.loads(msg)

            if self.queueProducerController.isNewClient(msg["clientID"]):
                self.queueProducerController.createNewQueue(msg)
                print(f"Client {msg['clientID']} is connected.")
            else:
                self.queueProducerController.insertInCurrentQueue(msg)
            
            system("cls")
            print("Messages received-----------------------------------")
            self.queueProducerController.showAllQueues()
            print("-----------------------------------------------------")