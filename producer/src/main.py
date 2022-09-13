import socket
import random
import threading
import string
import time
import sys

class Producer:
    def __init__(self, topic, rate):
        self.topic = topic
        self.rate = rate

        self.thread = threading.Thread(target=self.startService())
        self.thread.start()

    def getRandomMsg(self):
        msgLen = random.randint(1, 1000)
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(msgLen))

    def sendMessage(self, msg, address):
        print("Sending...")
        print(f"Msg topic: {msg['topic']}")
        print(f"Msg body: {msg['body']}")

        size = str(sys.getsizeof(str(msg)))
        print(f"Lenght: {size}")

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
        self.server.connect(address)
        self.server.send(str(msg).encode())

    def startService(self):

        print(f"Thread: {threading.get_ident()} is running.")
        while True:
            
            address = ("localhost", 8000)

            msgBody = self.getRandomMsg()
            msg = {"producerID": threading.get_ident(), "topic": self.topic, "body": msgBody}

            try:
                self.sendMessage(msg, address)
                time.sleep(1/self.rate)
            except Exception as err:
                print(f"Error: {err}")
                break

    def run(self):
        self.thread.join()

if __name__ == "__main__":
    
    producer1 = Producer("fanout", 1)
    # producer1.run()