from os.path import isfile
from time import sleep
from . import State
from .base import Base

'''
The base Finite State Machine class.

Properties
previous_state:	A special instance of the State class than when used in a Transition causes the FSM to revert to the previous state.
delay_duraton:	Time between itterations of the main loop.
'''
class FSM(Base):
	'''
	name:			the name of the FSM used in logging
	save_file=None:	path to a file to be used for storing the current state stack
	'''
	def __init__(self, name, save_file=None):
		super(FSM, self).__init__("FSM", name)

		if save_file != None:
			if not isfile(save_file):
				self.logfatal("save_file is not a file")
		self.__save_file = save_file

		self.delay_duraton = 0.01	# 10ms

		self.__states = set()
		self.__process = None
		self.__stack = []

		self.previous_state = State("Previous State for FSM '%s'"%(self.name), self, add_to_fsm=False)

	# Gets the reset State for the FSM. AttributeError is raised if one has not been set.
	@property
	def reset_state(self):
		return self.__reset_state

	# Sets the reset State for the FSM. A reset State is requried for the FSM to start.
	@reset_state.setter
	def reset_state(self, state):
		if not state in self.__states:
			self.logfatal("reset state not in fsm")
		for transition in state._State__transitions:
			if transition._Transition__next_state == self.previous_state:
				self.logfatal("reset state can't have a transition to previous_state")
		self.__reset_state = state

	# Starts the FSM. Will block until an Exception is raised.
	def start(self):
		if self.__save_file != None:
			self.__read_save_file()

		if len(self.__stack) == 0:
			try:
				self.__set_state(self.reset_state)
			except AttributeError:
				self.logfatal("no reset state set")

		self.logdebug("started")
		self.__current_state()._State__load_transistions()
		while True:
			self.on_transition(self.__current_state())

			next_state = None
			self.__current_state().start()

			# Wait for next state
			while next_state == None:
				self.delay()
				next_state = self.__current_state()._State__loop()

			self.__current_state().stop()

			previous_state = self.__current_state()
			self.__set_state(next_state)

			# Load Watchers for next current state before unloading the previous state's
			# Watchers so that any Watchers that are shared between states are kept loaded.
			self.__current_state()._State__load_transistions()
			previous_state._State__unload_transistions()

	### Overridable methods ###

	# Called when the FSM transitions to a new State.
	def on_transition(self, next_state):
		pass

	# Function used to delay itterations of the main loop.
	def delay(self):
		sleep(self.delay_duraton)

	### / Overridable methods ###

	def __add_state(self, state):
		if state._State__fsm != self:
			self.logfatal("state is for a different fsm")
		if state == self.previous_state:
			self.logfatal("can't add previous state as a state")
		for s in self.__states:
			if state.name == s.name:
				self.logfatal("state's name already used by different state")
		self.__states.add(state)

	def __set_state(self, state):
		if state == self.previous_state:
			if len(self.__stack) < 2:
				self.logerr("no previous state available")
			else:
				self.__stack.pop()
		else:
			self.__stack.append(state)

		if self.__save_file != None:
			self.__write_save_file()

	def __current_state(self):
		if len(self.__stack) < 1:
			self.logerr("stack is empty")
			return None
		return self.__stack[-1]

	def __read_save_file(self):
		for line in open(self.__save_file):
			line = line.rstrip()
			if line == "":
				continue
			state = self.__find_state_by_name(line)
			if state == None:
				self.logfatal("state '%s' is not in FSM"%(line))
			self.__stack.append(state)

	def __write_save_file(self):
		with open(self.__save_file, 'w') as f:
			f.write("\n".join([state.name for state in self.__stack]))

	def __find_state_by_name(self, name):
		for state in self.__states:
			if name == state.name:
				return state
		return None
