from .threads.ReceiverThread import ReceiverThread
from .threads.SenderThread import SenderThread
import multiprocessing

class Swapper:
    def __init__(self):
        
        # Criação de thread para receber mensagens dos produtores e armazenar nas filas
        self.recvThread = ReceiverThread("receiver 1", "localhost", 8000)
        # Criação de thread para enviar mensagens para os consumidores corretos de acordo com o rótulo
        self.senderThread = SenderThread("sender 1", "localhost", 8081)

    def run(self):
        self.recvThread.start()
        ##self.senderThread.start()

        self.recvThread.join()
        #self.senderThread.join()
