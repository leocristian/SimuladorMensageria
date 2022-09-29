from queue import Queue
from .threads.ReceiverThread import ReceiverThread
from .threads.SenderThread import SenderThread
from .controllers.QueueController import QueueController

class Swapper:
    def __init__(self):
        self.queueController = QueueController()

        recvAddr = ("localhost", 8000)
        senderAddr = ("localhost", 8001)
        
        # Criação de thread para receber mensagens dos produtores e armazenar nas filas
        self.recvThread = ReceiverThread(recvAddr, self.queueController)
        # Criação de thread para enviar mensagens para os consumidores corretos de acordo com o rótulo
        self.senderThread = SenderThread(senderAddr, self.queueController)

    def run(self):
        self.recvThread.start()
        self.senderThread.start()

        self.recvThread.join()
        self.senderThread.join()