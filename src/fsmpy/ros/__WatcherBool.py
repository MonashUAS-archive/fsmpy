from .. import Watcher
from rospy import Subscriber
from std_msgs.msg import Bool

'''
A subclass of Watcher for receiving messages of type Bool on a ROS topic.
'''
class WatcherBool(Watcher):
    '''
	name:		the name of the Watcher used in logging
    topic:		the ROS topic to be used
	value=True:	WatcherBool waits for Bool data on topic to equal value
	'''
    def __init__(self, name, topic, value=True):
        super(WatcherBool, self).__init__(name)

        if topic == None or topic == "":
            self.logfatal("topic not set")
        self.__topic = topic
        self.__value = value

        self.__sub = None

    ### Method Overrides ###

    def start(self):
		super(WatcherTrigger, self).start()
        self.__sub = Subscriber(self.__topic, Bool, self.handler)

    def stop(self):
		super(WatcherTrigger, self).stop()
        self.__sub.unregister()

    ###  / Method Overrides ###
    ### Overridable methods ###

	'''
	Handles messages received on the ros topic.
	By default, if the data value is equal to value, then the watcher is triggered.
	'''
    def handler(self, data):
        if data.data == self.__value:
            with self.event.get_lock():
                self.event.value = True

    ### / Overridable methods ###
