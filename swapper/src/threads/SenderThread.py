import threading
import socket
import json
import time
from ..controllers.ConsumersController import ConsumersController
from termcolor import colored

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

        self.conectedCons = []


    def sendMessages(self, client, topic):

        for x in self.queueController.queues:
            if x['topic'] == topic:
                while len(x['queue']) > 0:
                    self.condition.acquire()
                    msg = x['queue'].pop()
                    client.send(str(msg).encode())
                    self.condition.wait()
                    self.condition.release()
                quit()

    def popFromQueue(self, topic):
        
        for x in self.queueController.queues:
            if len(x['queue']) == 0:
                print(f"lista com o tópico {x['topic']} está vazia")
                return ''
            if x['topic'] == topic:
                msg = x['queue'].pop()
        

        return msg

    def messagesHandler(self, client, clientAddr):

        try:
        
            msg = client.recv(1024).decode()
            msg = eval(msg)
        
            msg = json.dumps(msg, indent = 4)
            msg = json.loads(msg)

            print(f"Tópico recebido: {msg['topic']}")

            while True:
                
                if self.consumersController.isNewConsumer(msg['topic']):
                    self.consumersController.createConsumer(msg['topic'], clientAddr)
                    if self.queueController.isNewTopic(msg['topic']):
                        self.queueController.createNewQueue(msg)
                        print(f"fila com o tópico {msg['topic']} foi criada pelo cliente {clientAddr}...")
                    else:
                        print(f"fila com o tópico {msg['topic']} já existe...")
                        print("Enviando mensagens...")

                        self.sendMessages(client, msg['topic'])
                        # while True:

                        #     msgSend = self.popFromQueue(msg['topic'])
                        #     if msgSend != '':
                        #         print(f"Mensagem {msgSend} será enviada para o consumidor {clientAddr}")
                        #         client.send(str(msg).encode())
                        #     else:
                        #         quit()
                    
                        #     time.sleep(1)
        except:
            self.conectedProds.remove(client)
            print(colored(f"Consumidor ({clientAddr} desconectou-se!", "yellow"))
            client.close()

    def run(self):
        
        print(f'Thread sender inicializada no endereço: {self.address}')
        
        try:
            while True:
                clientsock, clientAddr = self.swapper_server.accept()
                self.conectedCons.append(clientsock)

                print(colored(f"Novo consumidor conectado ({clientAddr}.", "yellow"))

                thread = threading.Thread(target=self.messagesHandler, args=[clientsock, clientAddr])
                thread.start()
        except Exception as err:
            print(f"Erro: {err}")
