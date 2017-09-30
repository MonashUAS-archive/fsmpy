from .. import Watcher
from rospy import Service
from std_srvs.srv import Trigger, TriggerResponse

'''
A subclass of Watcher for receiving service requests of type Trigger.
WatcherTrigger can be inherited to implement behaviour where the Watcher responds with False if needed.
'''
class WatcherTrigger(Watcher):
	'''
	name:		  the name of the Watcher used in logging
	service_name: the name of the service to be used
	'''
	def __init__(self, name, service_name):
		super(WatcherTrigger, self).__init__(name)

		if service_name == None or service_name == "":
			self.logfatal("service_name not set")
		self.__service_name = service_name

		self.__service = None

	### Method Overrides ###

	def start(self):
		super(WatcherTrigger, self).start()
		self.__service = Service(self.__service_name, Trigger, self.handler)

	def stop(self):
		super(WatcherTrigger, self).stop()
		self.__service.shutdown()

	###  / Method Overrides ###
	### Overridable methods ###

	'''
	Handles incoming service requests.
	By default, the watcher is triggered and True is returned.
	'''
	def handler(self, req):
		with self.event.get_lock():
			self.event.value = True
		return TriggerResponse(True, "")

	### / Overridable methods ###
