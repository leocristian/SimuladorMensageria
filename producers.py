from producer.src.main import Producer
from consumer.src.main import Consumer

prod1 = Producer("aaa", 1)
prod2 = Producer("bbb", 1)
# prod3 = Producer("ccc", 2)

prod1.start()
prod2.start()
# prod3.start()

prod1.join()
prod2.join()
# prod3.join()