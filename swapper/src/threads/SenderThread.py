import threading
import socket
import json
import time
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
        # self.server.connect(address)

        self.server.send(str(msg).encode())

    def popFromQueue(self, topic):
        for x in self.queueController.queues:
            if x['topic'] == topic:
                msg = x['queue'].pop()

        return msg['body']

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
                    msgSend = self.popFromQueue(msg['topic'])
                    print(f"Mensagem {msgSend} será enviada para o consumidor {clientAddr}")
                    self.sendMessage(msgSend, clientAddr)
                # self.consumersController.showConsumersQueue()
            else:
                print('Enviar mensagens...')  
                time.sleep(2)