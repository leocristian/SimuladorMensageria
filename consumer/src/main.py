import socket
import threading
import json
import os

class Consumer(threading.Thread):
    def __init__(self, topic):
        threading.Thread.__init__(self) 
        self.topic = topic
        self.connAddress = ("localhost", 8001)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect(self.connAddress)

    def sendTopic(self):
        msg = {"topic": self.topic}

        try:
            self.client_socket.send(str(msg).encode())
        finally:
            print("Tópico enviado com sucesso!")
    
    def receiveMsg(self):
        print("Aguardando mensagens...")
        while True:
            msgRecvd = self.client_socket.recv(1024).decode()

            msgRecvd = eval(msgRecvd)
            msgRecvd = json.dumps(msgRecvd, indent=4)
            msgRecvd = json.loads(msgRecvd)
            
            print(f"Mensagem recebida: {msgRecvd}")
    
    def run(self):    
        self.sendTopic()
        self.receiveMsg()
        
        #clientsock, clientAddr = self.client.accept()
        #msg = clientsock.recv(1024).decode()
        
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

if __name__ == '__main__':

    topic = input("Informe o tópico da mensagem para o consumidor: ")
    cons1 = Consumer(topic)

    cons1.start()
    cons1.join()