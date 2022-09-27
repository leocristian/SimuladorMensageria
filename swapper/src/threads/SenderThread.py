import threading
import socket
from ..QueueController import QueueController

class SenderThread(threading.Thread):
    def __init__(self, address, queueController):
        self.address = address
        self.queueController = queueController
        threading.Thread.__init__(self)
    
    def sendMessage(self, msg, address):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
        self.server.connect(address)
        self.server.send(str(msg).encode())

    def run(self):
        print(f'Sender is started on address ({self.url}: {self.port})...')

        while not self.canClose:
            if self.queueController.isNewConsumer():
                self.queueController.createConsumer()
                #self.canClose = True
            else:
                print('Enviar mensagens...')
                self.sendMessage()