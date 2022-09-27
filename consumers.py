from consumer.src.main import Consumer

cons1 = Consumer("consumer 1", "aaa")
#cons2 = Consumer("consumer 2", "bbb")

cons1.start()
#cons2.start()

cons1.join()
#cons2.join()