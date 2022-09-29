from producer.src.main import Producer
from consumer.src.main import Consumer

prod1 = Producer("1", "aaa", 1)
prod2 = Producer("2", "bbb", 1)
prod3 = Producer("3", "ccc", 2)

prod1.start()
prod2.start()
prod3.start()

prod1.join()
prod2.join()
prod3.join()