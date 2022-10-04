import threading
from .threads.ReceiverThread import ReceiverThread
from .threads.SenderThread import SenderThread
from .controllers.QueueController import QueueController
import socket
from termcolor import colored

class Swapper:
    def __init__(self):
        self.queueController = QueueController()
        self.condition = threading.Condition()

        host = "localhost"
        recvAddr = (host, 8000)
        senderAddr = (host, 8001)
        
        # Criação de thread para receber mensagens dos produtores e armazenar nas filas
        self.recvThread = ReceiverThread(recvAddr, self.queueController, self.condition)
        # Criação de thread para enviar mensagens para os consumidores corretos de acordo com o rótulo
        self.senderThread = SenderThread(senderAddr, self.queueController, self.condition)

    def run(self):
        try:
            self.recvThread.start()
            self.senderThread.start()

            self.recvThread.join()
            self.senderThread.join()
        except KeyboardInterrupt:
            print(colored("Trocador finalizado com sucesso!", "red"))