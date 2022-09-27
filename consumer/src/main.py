import socket
import threading
import json
import os

class Consumer(threading.Thread):
    def __init__(self, name, topic):
        threading.Thread.__init__(self, name=name)
        self.addres = ("localhost", 8000)
        self.topic = topic

    def run(self):    
        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind()
        self.swapper_server.listen(10)

        while True:
            clientsock = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()

            msg = eval(msg)
            
            msg = json.dumps(msg, indent = 4)
            msg = json.loads(msg)
            
            os.system("clear")
            print("Msg received")
            print(msg)