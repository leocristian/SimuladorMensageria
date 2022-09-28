from consumer.src.main import Consumer
from producer.src.main import Producer
from consumer.src.main import Consumer

cons1 = Consumer("aaa")
cons2 = Consumer("bbb")
prod1 = Producer("1", "aaa", 1)

cons1.start()
cons2.start()
prod1.start()

cons1.join()
cons2.join()

prod1.join()
