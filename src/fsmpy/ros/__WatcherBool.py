from .. import Watcher
from rospy import Subscriber
from std_msgs.msg import Bool

class WatcherBool(Watcher):
    def __init__(self, name, topic, value=True):
        super(WatcherBool, self).__init__(name)

        if topic == None or topic == "":
            self.logfatal("topic not set")
        self.__topic = topic
        self.__value = value

        self.__sub = None

    ### Method Overrides ###

    def start(self):
        self.__sub = Subscriber(self.__topic, Bool, self.__handler)
        self.logdebug("started")

    def stop(self):
        self.__sub.unregister()
    	self.logdebug("stopped")

    ###  / Method Overrides ###
    ### Overridable methods ###

    def handler(self, data):
        if data.data == self.__value:
            with self.event.get_lock():
                self.event.value = True

    ### / Overridable methods ###
