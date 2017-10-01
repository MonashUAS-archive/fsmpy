from . import WatcherMsg
from std_msgs.msg import Bool

'''
A subclass of Watcher for receiving messages of type Bool on a ROS topic.
'''
class WatcherBool(WatcherMsg):
	'''
	name:		the name of the Watcher used in logging
	topic:		the ROS topic to be used
	value=True:	WatcherBool waits for Bool data on topic to equal value
	'''
	def __init__(self, name, topic, value=True):
		super(WatcherBool, self).__init__(name, topic, Bool)
		self.__value = value

	### Method Overrides ###

	# If the data value is equal to value, then the watcher is triggered.
	def handler(self, data):
		if data.data == self.__value:
			with self.event.get_lock():
				self.event.value = True

	###  / Method Overrides ###
