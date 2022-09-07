import socket
from sqlite3 import adapt
import threading
import random
import time
import uuid
import sys

#by joão carlos

import datetime

class Producer:

    def __init__(self) -> None:
        self._id = str(uuid.uuid4())
            
    def getRandomMsg(self) -> str:

        messages = [
            "Mais vale um bebadis conhecidiss, que um alcoolatra anonimis.",
            "Atirei o pau no gatis, per gatis num morreus.",
            "Interagi no me, cursus quis, vehicula ac nisi.",
            "Si num tem leite entao bota uma pinga ai cumpadi!",
            "Cevadis im ampola pa arma uma pindureta.",
            "Sed non consequat odio.",
            "Vide electram sadipscing et per.",
            "Aenean aliquam molestie leo, vitae iaculis nisl.",
            "Detraxit consequat et quo num tendi nada.Sapien in monti palavris qui num significa nadis i pareci latim.",
            "eu conheso uma cachacis que pode alegrar sua vidis.",
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

    def start(self, label:str, total_messages_per_minute:int):

        print('producer is started')
        addres = ("localhost", 8000) #host and port
        
        while True:
            try:
                print('sending...')
                self.producer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.producer_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
                self.producer_server.connect(addres)

                message = self.getRandomMsg();

                date_info = str(datetime.datetime.now())

                data = {'received_datetime': date_info,'producer_id': self._id, 'label':  label, 'message': message}
                
                self.producer_server.send(str(data).encode())

                time.sleep( 60 / total_messages_per_minute )

            except:
                print('swapper is not alive')
                print('trying to connect again')
                time.sleep(1)
            

if __name__=='__main__':

    if (len(sys.argv) - 1) > 4:
        print("argumentos invalidos")
    
    label = sys.argv[2]
    mensage_per_minute = int(sys.argv[4])

    producer = Producer()

    producer.start(label, mensage_per_minute)
    

