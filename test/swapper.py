import socket
import threading
import json

class Swapper:
    def __init__(self):
        addres = ("localhost", 8000) #host and port
        self.swapper_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swapper_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.swapper_server.bind(addres)

        self.producers = []

    def start(self):
        self.swapper_server.listen(10)
        print('swapper is started')
        
        while True:
        
            clientsock, clientAddr = self.swapper_server.accept()
            msg = clientsock.recv(1024).decode()

            msg = eval(msg)
            
            if msg['producer_id'] not in self.producers:
                print('new producer added: ' + msg['producer_id'] )
                self.producers.append(msg['producer_id'])

            msg = json.dumps(msg, indent = 4)

            print('\n' + msg)
    
    def to_distribute(self, msg: dict):
        pass

if __name__=='__main__':
    swapper = Swapper()
    swapper.start()