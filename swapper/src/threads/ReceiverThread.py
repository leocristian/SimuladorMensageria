import threading
import socket
import json
from os import system
import readchar

class ReceiverThread(threading.Thread):
    def __init__(self, address, queueController):
        self.address = address
        self.queueController = queueController
        threading.Thread.__init__(self)
    
    def run(self):
        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind(self.address)
        self.swapper_server.listen(10)

        print(f'Receiver is started on address ({self.address[0]}: {self.address[1]})...')
        
        while True:
        
            clientsock, clientAddr = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()

            msg = eval(msg)
            
            msg = json.dumps(msg, indent = 4)
            msg = json.loads(msg)

            print(f'endereço: {clientAddr}')

            if self.queueController.isNewClient(msg["topic"]):
                self.queueController.createNewQueue(msg)
                print(f"Client {msg['topic']} is connected.")
            else:
                print(f"fila com o tópico {msg['topic']} já existe")
                self.queueController.insertInCurrentQueue(msg)
            
            system("cls")
            print("Messages received-----------------------------------")
            self.queueController.showQueueLen()
            print("-----------------------------------------------------")