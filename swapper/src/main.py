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

        self.queueController = QueueController()

        # Criação de thread para receber mensagens dos produtores e armazenar nas filas
        self.recvMessagesThread = threading.Thread(target=self.receiveMessages())
        self.recvMessagesThread.start()
        
        # Criação de thread para enviar mensagens para os consumidores corretos de acordo com o rótulo
        self.distribMessagesThread = threading.Thread(target=self.distributeMessages())
        self.distribMessagesTgread.Start()

    def receiveMessages(self):
        self.swapper_server.listen(10)
        print('swapper is receiving...')
        
        while True:
        
            clientsock, clientAddr = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()

            msg = eval(msg)
            
            msg = json.dumps(msg, indent = 4)
            msg = json.loads(msg)

            
            if self.queueController.isNewProducer(msg["producerID"]):
                self.queueController.createNewQueue(msg["producerID"])
            else:
                self.queueController.insertInCurrentQueue(msg)

            print("Message Received...")
            self.queueController.showAllQueues()
 
    def distributeMessages(self):
        print('swapper is sending...')

        pass

if __name__=='__main__':
    swapper = Swapper()
    swapper.receiveMessages()