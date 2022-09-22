import socket
import threading
import json
import os

class Consumer:
    def __init__(self):
        addres = ("localhost", 8000)

        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind(addres)

        self.recvMessagesThread = threading.Thread(target=self.receiveMessages())

    def run(self):    
        self.recvMessagesThread.start()
        self.recvMessagesThread.join()

    def receiveMessages(self):
        self.swapper_server.listen(10)
        print('swapper is receiving...')
        
        while True:
        
            clientsock, clientAddr = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()

            msg = eval(msg)
            
            msg = json.dumps(msg, indent = 4)
            msg = json.loads(msg)
            
            os.system("clear")
            print("Msg received")
            print(msg)