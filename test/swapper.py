import socket
import threading

class Swapper:
    def __init__(self):
        addres = ("localhost", 8000) #host and port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addres)

    def start(self):
        self.server.listen(1)
        print('swapper is started')

        while True:
            clientsock, clientAddr = self.server.accept()
            comand = clientsock.recv(2048).decode()
            self.to_distribute(comand)
    
    def to_distribute(self, comand: dict):
        pass

if __name__=='__main__':

    swapper = Swapper()

    swapper.start()