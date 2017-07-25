from multiprocessing import Process
from .base import Base

'''
The base State class.

Code running in a State may be stopped at anytime.
'''
class State(Base):
	'''
	name:	the name of the State used in logging
	fsm:	the FSM object the State is associated with
	'''
	def __init__(self, name, fsm, add_to_fsm=True):
		super(State, self).__init__("State", name)

		if fsm == None:
			self.logfatal("fsm is not set")
		self.__fsm = fsm

		self.__transitions = set()

		if add_to_fsm:
			fsm._FSM__add_state(self)

	# Defines the link between a Transition the State. The State may have may Transitions.
	def add_transition(self, transition):
		if transition._Transition__fsm != self.__fsm:
			self.logfatal("transition is for a different fsm")
		for t in self.__transitions:
			if t._Transition__watcher == transition._Transition__watcher:
				self.logfatal("watcher already used in this state")
		self.__transitions.add(transition)

	### Overridable methods ###

	'''
	Code to be run when the State is started.
	Use this function for initialisation.
	It is recommended to include 'self.logdebug("started")'.
	'''
	def start(self):
		self.logdebug("started")

	'''
	Code to be run when the State is stopped.
	It is recommended to include 'self.logdebug("stopped")'.
	'''
	def stop(self):
		self.logdebug("stopped")

	'''
	Code to be run on an itteration of the FSM's main loop.
	Similar to MAVProxy's 'idle_task' function in a module.
	'''
	def loop(self):
		pass

	### / Overridable methods ###

	def __load_transistions(self):
		for t in self.__transitions:
			t._Transition__load()

	def __unload_transistions(self):
		for t in self.__transitions:
			t._Transition__unload()

	def __loop(self):
		self.loop()
		next_state = None
		for t in self.__transitions:
			res = t._Transition__loop()
			if res != None:
				next_state = res
		return next_state

'''
A subclass of State for applications requring asynchronous execution.
Code running in a StateAsync may be stopped at anytime.
'''
class StateAsync(State):
	'''
	name:	the name of the State used in logging
	fsm:	the FSM object the State is associated with
	target:	the function to be called asynchronously. No arguments are passes to 'target' on execution.
	'''
	def __init__(self, name, fsm, target):
		super(StateAsync, self).__init__(name, fsm)

		if not callable(target):
			self.logfatal("target is not callable")
		self.__target = target

		self.__process = None

	### Method Overrides ###

	def start(self):
		self.__process = Process(target=self.__target)
		self.__process.start()
		self.logdebug("started")

	def stop(self):
		self.__process.terminate()
		self.__process.join(None)
		self.__process = None
		self.logdebug("stopped")

	### / Method Overrides ###
