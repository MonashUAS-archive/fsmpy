from multiprocessing import Lock, Process, Value
from .base import Base

class Watcher(Base):
	def __init__(self, name):
		super(Watcher, self).__init__("Watcher", name)

		self.event = Value('B', False)

		# these properties are protected by this mutex
		self.__mutex = Lock()
		self.__transitions = 0

	def __load(self):
		self.__mutex.acquire()
		if self.__transitions == 0:
			self.start()
		self.__transitions += 1
		self.__mutex.release()

	def __unload(self):
		self.__mutex.acquire()
		self.__transitions -= 1
		if self.__transitions == 0:
			self.stop()
		self.__mutex.release()

	def __check(self):
		value = None
		with self.event.get_lock():
			value = self.event.value
		return value

	### Overridable methods ###

	def start(self):
		self.logdebug("started")

	def stop(self):
		self.logdebug("stopped")

	def reset(self):
		self.logdebug("reset")
		with self.event.get_lock():
			self.event.value = False

	def loop(self):
		pass

	### / Overridable methods ###

class WatcherAsync(Watcher):
	def __init__(self, name, target):
		super(WatcherAsync, self).__init__(name)

		if not callable(target):
			self.logfatal("target is not callable")
		self.__target = target

		self.__process = None

	### Method Overrides ###

	def start(self):
		with self.event.get_lock():
			if self.__process != None:
				self.logerr("__process is still here!")
			self.__process = Process(target=self.__target, args=(self.event,))
			self.__process.start()
			self.logdebug("started")

	def stop(self):
		with self.event.get_lock():
			if self.__process == None:
				self.logerr("__process is gone!")
			self.__process.terminate()
			self.__process.join(None)
			self.__process = None
			self.logdebug("stopped")

	###  / Method Overrides ###
