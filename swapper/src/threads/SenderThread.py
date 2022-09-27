import threading
from ..QueueController import QueueController

class SenderThread(threading.Thread):
    def __init__(self, name, url, port):
        self.url = url
        self.port = port
        threading.Thread.__init__(self)
        self.name = name
        self.queueConsumerController = QueueController()
        self.canClose = True
    
    def run(self):
        print(f'Sender is started on address ({self.url}: {self.port})...')

        while not self.canClose:
            print(self.queueConsumerController.clients.__len__)
            if self.queueConsumerController.clients.__len__ == 0:
                print("No clients...aborting...")
                self.canClose = False
            else:
                print('aa')  