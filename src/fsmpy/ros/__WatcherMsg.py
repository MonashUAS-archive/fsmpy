from .. import Watcher
from rospy import Subscriber

'''
A generic subclass of Watcher for receiving messages on a ROS topic.
'''
class WatcherMsg(Watcher):
	'''
	name:	the name of the Watcher used in logging
	topic:	the ROS topic to be used
	type:	the type of the ROS message that will be sent
	'''
	def __init__(self, name, topic, type):
		super(WatcherMsg, self).__init__(name)

		if topic == None or topic == "":
			self.logfatal("topic not set")
		self.__topic = topic

		if topic == None:
			self.logfatal("type not set")
		self.__type = type

		self.__sub = None

	### Method Overrides ###

	def start(self):
		super(WatcherMsg, self).start()
		self.__sub = Subscriber(self.__topic, self.__type, self.handler)

	def stop(self):
		super(WatcherMsg, self).stop()
		self.__sub.unregister()

	###  / Method Overrides ###
	### Overridable methods ###

	'''
	Handles messages received on the ros topic.
	By default, it does nothing.
	'''
	def handler(self, data):
		pass

	### / Overridable methods ###
