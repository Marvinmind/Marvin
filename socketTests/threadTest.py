import threading
from queue import Queue
import time

class ThreadStuff(threading.Thread):
	def __init__(self, queue):
		super(ThreadStuff, self).__init__()
		self.queue = queue
		self.setDaemon(True)
	def run(self):
		while True:
			val = self.queue.get()
			if val is not None:
				print('Message received: '+val)

q = Queue()
myThread1 = ThreadStuff(q)
myThread1.start()
for i in range(5):
	q.put(str(i))
time.sleep(2)