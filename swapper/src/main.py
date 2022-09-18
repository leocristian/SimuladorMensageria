from os import system
import socket
import threading
import json
from QueueController import QueueController

class Swapper:
    def __init__(self):
        addres = ("localhost", 8000) #host and port
        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind(addres)

        self.queueProducerController = QueueController()
        self.queueConsumerController = QueueController()

        # Criação de thread para receber mensagens dos produtores e armazenar nas filas
        self.recvMessagesThread = threading.Thread(target=self.receiveMessages())
        
        # Criação de thread para enviar mensagens para os consumidores corretos de acordo com o rótulo
        self.distribMessagesThread = threading.Thread(target=self.distributeMessages())
        
    def run(self):
        self.recvMessagesThread.start()
        self.recvMessagesThread.join()

        self.distribMessagesThread.start()
        self.distribMessagesThread.join()

    def receiveMessages(self):
        self.swapper_server.listen(10)
        print('swapper is receiving...')
        
        while True:
        
            clientsock, clientAddr = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()

            msg = eval(msg)
            
            msg = json.dumps(msg, indent = 4)
            msg = json.loads(msg)

            if self.queueProducerController.isNewClient(msg["producerID"]):
                self.queueProducerController.createNewQueue(msg)
            else:
                self.queueProducerController.insertInCurrentQueue(msg)
            
            system("clear")
            print("Producers queues------------------------------------")
            self.queueProducerController.showAllQueues()
            print("-----------------------------------------------------")
 
    def distributeMessages(self):
        print('swapper is sending...')

        pass    

if __name__=='__main__':
    swapper = Swapper()
    #swapper.run()