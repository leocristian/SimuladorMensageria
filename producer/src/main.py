from cgi import print_exception
import socket
import random
import threading
import string
import time
import sys
from termcolor import colored


class Producer(threading.Thread):
    def __init__(self, topic, rate):
        threading.Thread.__init__(self)
        self.topic = topic
        self.rate = rate
        self.address = ("localhost", 8000)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tries = 0
        while tries < 3:
            try:
                self.server.connect(self.address)
                break
            except:
                print(colored("Erro ao conectar-se com o trocador, tentando novamente...", "yellow"))
                tries += 1
                time.sleep(2)
            
            if tries == 2:
                print(colored("Não foi possível se conectar ao trocador!", "red"))
                quit()

    def getRandomMsg(self):
        msgLen = random.randint(1, 100)
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(msgLen))

    def sendMessage(self, msg):
        size = str(sys.getsizeof(str(msg)))
        try:
            self.server.send(str(msg).encode())
            print(f"Mensagem enviada com sucesso ({size} bytes)...")
        except Exception as err:
            print("Erro ao enviar mensagem, trocador desconectado.")
            quit()
        
    def run(self):
        while True:

            msg = ''
            msgBody = self.getRandomMsg()
            msg = {"topic": self.topic, "body": msgBody}

            try:
                self.sendMessage(msg)
                time.sleep(1/self.rate)
            except Exception as err:
                print(f"Erro: {err}")
                self.server.detach()
                return
            
if __name__=='__main__':

    topic = input("Informe o topico da mensagem para o produtor: ")

    while True:
        try:
            rate = int(input("Informe a taxa de envio (msg/seg): "))
            break
        except:
            print("Informe uma taxa válida!")

    prod1 = Producer(topic, rate)

    try:
        prod1.start()
        prod1.join()
    except KeyboardInterrupt:
        print(colored("Produtor finalizado com sucesso!", "red"))
