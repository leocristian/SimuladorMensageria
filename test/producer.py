import socket
from sqlite3 import adapt
import threading
import random
import time

class Producer:
            
    def getRandomMsg(self) -> str:

        messages = [
            "Mais vale um bebadis conhecidiss, que um alcoolatra anonimis.",
            "Atirei o pau no gatis, per gatis num morreus.",
            "Interagi no mé, cursus quis, vehicula ac nisi.",
            "Si num tem leite então bota uma pinga aí cumpadi!",
            "Cevadis im ampola pa arma uma pindureta.",
            "Sed non consequat odio.",
            "Vide electram sadipscing et per.",
            "Aenean aliquam molestie leo, vitae iaculis nisl.",
            "Detraxit consequat et quo num tendi nada.Sapien in monti palavris qui num significa nadis i pareci latim.",
            "eu conheço uma cachacis que pode alegrar sua vidis.",
        ]
        
        return messages[random.randint(0, (len(messages) -1) )]
    
    def getRadomLabels(self):

        labels = [
            "audio",
            "video",
            "pdf",
            "image",
            "executable"
        ]
        
        return labels[random.randint(0, (len(labels) -1) )]

    def start(self):
        print('producer is started')
        addres = ("localhost", 8000) #host and port
        
        while True:
            self.producer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.producer_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
            self.producer_server.connect(addres)

            message = self.getRandomMsg();
            print(f'send message: {message}')

            data = { self.getRadomLabels() : message}
            print(data)

            self.producer_server.send(str(data).encode())
           
            time.sleep(1)
            

if __name__=='__main__':
    
    producer = Producer()
    producer.start()
