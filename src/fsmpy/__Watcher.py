from multiprocessing import Lock, Process, Value
from .base import Base

'''
The base Watcher class.

Code running in a Watcher may be stopped at anytime.

To trigger this Watcher run:
with self.event.get_lock():
	self.event.value = True
'''
class Watcher(Base):
	'''
	name:	the name of the Watcher used in logging
	'''
	def __init__(self, name):
		super(Watcher, self).__init__("Watcher", name)

		self.event = Value('B', False)

		# these properties are protected by this mutex
		self.__mutex = Lock()
		self.__transitions = 0

	### Overridable methods ###

	'''
	Code to be run when the Watcher is started.
	Use this function for initialisation.
	It is recommended to include 'self.logdebug("started")'.
	'''
	def start(self):
		self.logdebug("started")

	'''
	Code to be run when the Watcher is stopped.
	It is recommended to include 'self.logdebug("stopped")'.
	'''
	def stop(self):
		self.logdebug("stopped")

	'''
	Code to be run when the Watcher is reset.
	A reset occurs when the Watcher triggers and a FSM registers it.
	It is recommended to include 'self.logdebug("reset")'.
	'''
	def reset(self):
		self.logdebug("reset")
		with self.event.get_lock():
			self.event.value = False

	'''
	Code to be run on an itteration of the FSM's main loop.
	Similar to MAVProxy's 'idle_task' function in a module.
	'''
	def loop(self):
		pass

	### / Overridable methods ###

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

'''
A subclass of Watcher for applications requring asynchronous execution.

Code running in a WatcherAsync may be stopped at anytime.

To trigger this Watcher run:
with self.event.get_lock():
	self.event.value = True
'''
class WatcherAsync(Watcher):
	'''
	name:	the name of the Watcher used in logging
	target:	the function to be called asynchronously. 'self.event' is passed as a single argument on execution
	'''
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
