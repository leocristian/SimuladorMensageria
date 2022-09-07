import socket
import threading
import json

class Swapper:
    def __init__(self):
        addres = ("localhost", 8000) #host and port

        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind(addres)

    def start(self):
        self.swapper_server.listen(10)
        print('swapper is started')
        
        while True:
        
            clientsock, clientAddr = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()

            print(msg)
            
    
    def to_distribute(self, msg: dict):
        pass

if __name__=='__main__':

    swapper = Swapper()

    swapper.start()