from .. import Watcher
from rospy import Service
from std_srvs.srv import Trigger, TriggerResponse

class WatcherTrigger(Watcher):
    def __init__(self, name, service_name):
        super(WatcherTrigger, self).__init__(name)

        if service_name == None or service_name == "":
            self.logfatal("service_name not set")
        self.__service_name = service_name

        self.__service = None

    ### Method Overrides ###

    def start(self):
        self.__service = Service(self.__service_name, Trigger, self.handler)
        self.logdebug("started")

    def stop(self):
        self.__service.shutdown()
    	self.logdebug("stopped")

    ###  / Method Overrides ###
    ### Overridable methods ###

    def handler(self, req):
        with self.event.get_lock():
            self.event.value = True
        return TriggerResponse(True, "")

    ### / Overridable methods ###
