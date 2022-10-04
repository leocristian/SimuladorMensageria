import socket
import threading
import json
import time
from termcolor import colored

class Consumer(threading.Thread):
    def __init__(self, topic):
        threading.Thread.__init__(self) 
        self.topic = topic
        self.connAddress = ("localhost", 8001)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        tries = 0
        while tries < 3:
            try:
                self.client_socket.connect(self.connAddress)
                break
            except Exception as err:
                print(colored("Erro ao conectar-se com o trocador, tentando novamente...", "yellow"))
                tries += 1
                time.sleep(2)
            
            if tries == 2:
                print(colored("Não foi possível se conectar ao trocador!", "red"))
                quit()


    def sendTopic(self):
        msg = {"topic": self.topic}

        try:
            self.client_socket.send(str(msg).encode())
        finally:
            print(colored("Tópico enviado com sucesso!", "green"))
    
    def receiveMsg(self):
        print("Aguardando mensagem...")
        while True:
            msgRecvd = self.client_socket.recv(1024).decode()

            # msgRecvd = eval(msgRecvd)
            msgRecvd = json.dumps(msgRecvd, indent=4)
            msgRecvd = json.loads(msgRecvd)
            
            print(f"Mensagem recebida: {msgRecvd}")
            input()
    
    def run(self):    
        self.sendTopic()
        self.receiveMsg()

if __name__ == '__main__':

    topic = input("Informe o tópico da mensagem para o consumidor: ")
    cons1 = Consumer(topic)

    cons1.start()
    cons1.join()