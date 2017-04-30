from .. import State
from rospy import Publisher
from std_msgs.msg import Bool

class StateControl(State):
    def __init__(self, name, fsm, topic):
        super(StateControl, self).__init__(name, fsm)

        if topic == None or topic == "":
            self.logfatal("topic not set")
        self.__pub = Publisher(topic, Bool, queue_size=2, latch=True)

    ### Method Overrides ###

    def start(self):
        self.__pub.publish(True)
        self.logdebug("started")

    def stop(self):
        self.__pub.publish(False)
        self.logdebug("stopped")

    ###  / Method Overrides ###
