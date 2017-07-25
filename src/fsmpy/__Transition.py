from . import Watcher, State, FSM
from .base import Base

'''
The base Transition class.
'''
class Transition(Base):
	'''
	name:		the name of the Transition used in logging
	fsm:		the FSM object the Transition is associated with
	watcher:	the Watcher for this Transition
	next_state:	the State to be transitioned too if 'watcher' triggers. May be FSM.previous_state
	'''
	def __init__(self, name, fsm, watcher, next_state):
		super(Transition, self).__init__("Transition", name)

		if fsm == None:
			self.logfatal("fsm is not set")
		if not isinstance(watcher, Watcher):
			self.logfatal("watcher is not an instance or subclass of Watcher")
		if not isinstance(next_state, State):
			self.logfatal("next_state is not an instance or subclass of State")
		self.__fsm = fsm
		self.__watcher = watcher
		self.__next_state = next_state

	def __load(self):
		self.__watcher._Watcher__load()

	def __unload(self):
		self.__watcher._Watcher__unload()

	def __loop(self):
		self.__watcher.loop()
		if self.__watcher._Watcher__check():
			self.__watcher.reset()
			return self.__next_state
		return None
