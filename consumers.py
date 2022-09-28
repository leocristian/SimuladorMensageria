from consumer.src.main import Consumer

cons1 = Consumer("as")
cons2 = Consumer("cc")

cons1.start()
cons2.start()

cons1.join()
cons2.join()