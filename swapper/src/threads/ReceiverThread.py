from http import client
import threading
import socket
import json
import time
from termcolor import colored
import os

class ReceiverThread(threading.Thread):
    def __init__(self, address, queueController, condition):
        self.address = address
        self.queueController = queueController
        self.condition = condition
        threading.Thread.__init__(self, name="Receiver")
        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.bind(self.address)

        self.conectedProds = []
    
    def messagesHandler(self, client, clientAddr):
        while True:

            try:
                msg = client.recv(1024).decode()

                # print(msg)
                msg = eval(msg)
                
                msg = json.dumps(msg, indent = 4)
                msg = json.loads(msg)

                self.condition.acquire()
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
                self.condition.release()

                os.system('clear')
                self.queueController.showQueueLen()
            except:
                self.conectedProds.remove(client)
                print(colored(f"Produtor ({clientAddr} desconectou-se!", "yellow"))
                client.close()
                break

    def run(self):
        
        self.swapper_server.listen(10)
        print(f'Thread receiver inicializada no endereço: ({self.address[0]}: {self.address[1]})...')
        
        try:
            while True:
                clientsock, clientAddr = self.swapper_server.accept()
                self.conectedProds.append(clientsock)

                print(colored(f"Novo produtor conectado ({clientAddr}.", "yellow"))

                thread = threading.Thread(target=self.messagesHandler, args=[clientsock, clientAddr])
                thread.start()
                
        except Exception as err:
            print(f"Erro: {err}")