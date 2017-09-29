from .. import State
from rospy import Publisher
from std_msgs.msg import Bool

'''
A subclass of State for controlling a ROS node with a topic of type Bool.

When the state is started a message is published on the supplied topic with value True.
When the state is stopped a message is published on the supplied topic with value False.
'''
class StateControl(State):
    '''
    name:	the name of the State used in logging
	fsm:	the FSM object the State is associated with
    topic:  the ROS topic to be used
    '''
    def __init__(self, name, fsm, topic):
        super(StateControl, self).__init__(name, fsm)

        if topic == None or topic == "":
            self.logfatal("topic not set")
        self.__pub = Publisher(topic, Bool, queue_size=2, latch=True)

    ### Method Overrides ###

    def start(self):
		super(StateControl, self).start()
        self.__pub.publish(True)

    def stop(self):
		super(StateControl, self).stop()
        self.__pub.publish(False)

    ###  / Method Overrides ###
