import socket
import random
import threading
import string
import time
import sys

class Producer(threading.Thread):
    def __init__(self, topic, rate):
        threading.Thread.__init__(self)
        self.topic = topic
        self.rate = rate
        self.address = ("localhost", 8000)

    def getRandomMsg(self):
        msgLen = random.randint(1, 10)
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(msgLen))

    def sendMessage(self, msg):
        print("Sending...")
        print(f"Msg topic: {msg['topic']}")
        print(f"Msg body: {msg['body']}")

        size = str(sys.getsizeof(str(msg)))
        print(f"Lenght: {size}")

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(self.address)
            self.server.send(str(msg).encode())
        except Exception as err:
            print(f"Erro: {err}")
            return
        
    def run(self):
        while True:

            msg = ''
            msgBody = self.getRandomMsg()
            msg = {"topic": self.topic, "body": msgBody}

            try:
                self.sendMessage(msg)
                time.sleep(1/self.rate)
                input()
            except Exception as err:
                print(f"Erro: {err}")
                self.server.detach()
                return
            
if __name__=='__main__':

    topic = input("Informe o topico da mensagem para o produtor: ")
    rate = int(input("Informe a taxa de envio (msg/seg): "))

    prod1 = Producer(topic, rate)

    prod1.start()
    prod1.join()
