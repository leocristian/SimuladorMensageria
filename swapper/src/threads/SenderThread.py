import threading
import socket
import json
import time
from ..controllers.ConsumersController import ConsumersController


class SenderThread(threading.Thread):
    def __init__(self, address, queueController, condition):
        self.address = address
        self.condition = condition
        self.consumersController = ConsumersController() 
        self.queueController = queueController
        threading.Thread.__init__(self, name="Sender")
        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.bind(self.address)
        self.swapper_server.listen(10)


    def sendMessage(self, msg, address):
        self.swapper_server.sendto(str(msg).encode(), address)

    def popFromQueue(self, topic):
        for x in self.queueController.queues:
            if len(x['queue']) == 0:
                print(f"lista com o tópico {x['topic']} está vazia")
                return ''
            if x['topic'] == topic:
                msg = x['queue'].pop()

        return msg

    def run(self):
        
        print(f'sender started on address {self.address}')

        clientsock, clientAddr = self.swapper_server.accept()
        msg = clientsock.recv(1024).decode()
        msg = eval(msg)
        
        msg = json.dumps(msg, indent = 4)
        msg = json.loads(msg)

        while True:

            if self.consumersController.isNewConsumer(msg['topic']):
                self.consumersController.createConsumer(msg['topic'], clientAddr)
                if self.queueController.isNewTopic(msg['topic']):
                    self.queueController.createNewQueue(msg)
                    print(f"fila com o tópico {msg['topic']} foi criada pelo cliente {clientAddr}...")
                else:
                    print(f"fila com o tópico {msg['topic']} já existe...")
                    msgSend = self.popFromQueue(msg['topic'])
                    if msgSend != '':
                        print(f"Mensagem {msgSend} será enviada para o consumidor {clientAddr}")
                        self.sendMessage(msgSend, clientAddr)
                    
                    input()
                # self.consumersController.showConsumersQueue()
            else:
                print('Enviar mensagens...')  
