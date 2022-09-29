import threading
import socket
import json
from ..controllers.ConsumersController import ConsumersController


class SenderThread(threading.Thread):
    def __init__(self, address, queueController):
        self.address = address
        self.consumersController = ConsumersController() 
        self.queueController = queueController
        threading.Thread.__init__(self)

    def sendMessage(self, msg, address):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
        self.server.connect(address)
        self.server.send(str(msg).encode())

    def run(self):
        
        print(f'sender started on address {self.address}')

        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind(self.address)
        self.swapper_server.listen(10)

        while True:
            clientsock, clientAddr = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()
            msg = eval(msg)
            
            msg = json.dumps(msg, indent = 4)
            msg = json.loads(msg)

            if self.consumersController.isNewConsumer(msg['topic']):
                self.consumersController.createConsumer(msg['topic'], clientAddr)
                if self.queueController.isNewTopic(msg['topic']):
                    self.queueController.createNewQueue(msg)
                    print(f"fila com o tópico {msg['topic']} foi criada pelo cliente {clientAddr}...")
                else:
                    print(f"fila com o tópico {msg['topic']} já existe...")
                # self.consumersController.showConsumersQueue()
            else:
                print('Enviar mensagens...')
                #self.sendMessage()