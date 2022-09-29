import socket
import threading
import json
import os

class Consumer(threading.Thread):
    def __init__(self, topic):
        threading.Thread.__init__(self) 
        self.topic = topic
        self.connAddress = ("localhost", 8001)

    def run(self):    
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.client.connect(self.connAddress)

        msg = {"topic": self.topic}
        self.client.send(str(msg).encode())
        #self.client.listen(1)

        # while True:
        #     clientsock = self.client.accept()
        #     msg = clientsock.recv(1024).decode()

        #     msg = eval(msg)
            
        #     msg = json.dumps(msg, indent = 4)
        #     msg = json.loads(msg)
            
        #     os.system("clear")
        #     print("Msg received")
        #     print(msg)