from http import client
import threading
import socket
import json
import time
import os

class ReceiverThread(threading.Thread):
    def __init__(self, address, queueController, condition):
        self.address = address
        self.queueController = queueController
        self.condition = condition
        threading.Thread.__init__(self, name="Receiver")
        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind(self.address)

        self.conectedProds = []
    
    def messagesHandler(self, client, clientAddr):
        msg = client.recv(1024).decode()

        # print(msg)
        msg = eval(msg)
        
        msg = json.dumps(msg, indent = 4)
        msg = json.loads(msg)

        self.condition.acquire()
        # print(f"condition acquired by {self.name}")
        if self.queueController.isNewTopic(msg["topic"]) and msg['topic'] != 'fanout':
            self.queueController.createNewQueue(msg)
            print(f"fila do tópico {msg['topic']} foi criada pelo produtor {clientAddr}...")
            self.queueController.insertInCurrentQueue(msg)
        else:
            if msg['topic'] == 'fanout':
                if self.queueController.existsQueue():
                    print('Tópico fanout, mensagem inserida em todas as filas...')
                    self.queueController.insertAllQueues(msg)
                else:
                    self.queueController.createNewQueue(msg)
            else:
                print(f"produtor {clientAddr} adicionou uma mensagem na fila do tópico {msg['topic']}...")
                self.queueController.insertInCurrentQueue(msg)

        self.condition.notify()
        # print(f"condition notified by {self.name}")
        self.condition.release()
        # print(f"condition released by {self.name}")

        #os.system("clear")
        #print("Messages received-----------------------------------")
        self.queueController.showQueueLen()
            #print("-----------------------------------------------------")

    def run(self):
        
        self.swapper_server.listen(10)
        print(f'Receiver is started on address ({self.address[0]}: {self.address[1]})...')
        
        try:

            while True:
                clientsock, clientAddr = self.swapper_server.accept()
                print(f"Novo produtor conectado ({clientAddr}.")

                self.messagesHandler(clientsock, clientAddr)
                
        except Exception as err:
            print(f"Erro: {err}")