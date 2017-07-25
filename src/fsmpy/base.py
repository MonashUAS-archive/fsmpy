import logging

logger = ""

'''
Base class for all FSM elements.
Implements name and logging features that can be used on all FSM elements.
'''
class Base(object):
	def __init__(self, typ, name):
		if typ == None or typ == "":
			raise Exception("no type set for class")
		self.__type = typ

		if name == None or name == "":
			raise Exception("no name set for %s"%(self.__type))
		self.__name = name

		self.__logger = logging.getLogger(logger)

	def __format(self, msg):
		return "%s (%s): %s"%(self.__type, self.name, msg)

	# Returns the name of the FSM element.
	@property
	def name(self):
		return self.__name

	### ROS logging methods ###

	def logdebug(self, msg, *args, **kw):
		self.__logger.debug(self.__format(msg), *args, **kw)

	def loginfo(self, msg, *args, **kw):
		self.__logger.info(self.__format(msg), *args, **kw)

	def logwarn(self, msg, *args, **kw):
		self.__logger.warning(self.__format(msg), *args, **kw)

	def logerr(self, msg, *args, **kw):
		self.__logger.error(self.__format(msg), *args, **kw)

	def logfatal(self, msg, *args, **kw):
		msg_fmt = self.__format(msg)
		self.__logger.critical(msg_fmt, *args, **kw)
		raise Exception(msg_fmt)

	###  / ROS logging methods ###
