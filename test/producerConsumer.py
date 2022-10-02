import threading
import time

class Producer(threading.Thread):
    def __init__(self, integers, condition):
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition
    
    def run(self):
        for x in range(10):
            integer = x
            self.condition.acquire()
            print(f'condição adquirida por: {self.name}')
            self.integers.append(integer)
            print(f'{self.name} adicionou {integer} na lista')
            self.condition.notify()
            print(f'condição notificada por: {self.name}')
            self.condition.release()
            print(f'condição liberada por: {self.name}')
            time.sleep(10)


class Consumer(threading.Thread):
    def __init__(self, integers, condition):
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition
    
    def run(self):
        while True:
            self.condition.acquire()
            print(f'condição adquirida por: {self.name}')
            while True:
                if self.integers:
                    integer = self.integers.pop()
                    print(f'{self.name} removeu {integer} na lista')
                    break
                self.condition.wait()
                print(f'condição esperada por: {self.name}')
            self.condition.release()
            print(f'condição liberada por: {self.name}')

def main():
    integers = []
    condition = threading.Condition()

    p1 = Producer(integers, condition)
    c1 = Consumer(integers, condition)

    p1.start()
    c1.start()

    p1.join()
    c1.join()

if __name__ == '__main__':
    main()
