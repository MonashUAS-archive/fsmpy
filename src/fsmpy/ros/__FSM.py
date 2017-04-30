from .. import FSM as FSMBase
from .. import set_logger
import rospy

class FSM(FSMBase):
	def __init__(self, name, *args, **kw):
		save_file = kw.pop('save_file')
		rospy.init_node(*args, **kw)
		set_logger("rosout")
		super(FSM, self).__init__(name, save_file=save_file)

	### Method Overrides ###

	def on_transition(self, next_state):
		self.loginfo("Transitioned to State '%s'"%(next_state.name()))

	def delay(self):
		rospy.sleep(self.delay_duraton)
		if rospy.is_shutdown():
			self.logfatal("ROS shutdown")

	### / Method Overrides ###
