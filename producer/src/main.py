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
        self.address = ("192.168.0.16", 8000)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
        self.server.connect(self.address)

    def getRandomMsg(self):
        msgLen = random.randint(1, 10)
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(msgLen))

    def sendMessage(self, msg):
        print("Sending...")
        print(f"Msg topic: {msg['topic']}")
        print(f"Msg body: {msg['body']}")

        size = str(sys.getsizeof(str(msg)))
        print(f"Lenght: {size}")

        self.server.send(str(msg).encode())
    
    def run(self):
        while True:

            msg = ''
            msgBody = self.getRandomMsg()
            msg = {"topic": self.topic, "body": msgBody}

            try:
                self.sendMessage(msg)
                time.sleep(1/self.rate)
                # input(f"({threading.get_ident()})Press ENTER to continue...")
            except Exception as err:
                print(f"Error: {err}")
                self.server.detach()
                break
            
if __name__=='__main__':

    topic = input("Informe o topico da mensagem para o produtor: ")
    rate = int(input("Informe a taxa de envio (msg/seg): "))

    prod1 = Producer(topic, rate)

    prod1.start()
    prod1.join()
