# Sets the logger for fsmpy. Must be called before instantiating any states.
def set_logger(log):
    import base
    base.logger = log
    del base

from .__State import State, StateAsync
from .__FSM import FSM
from .__Watcher import Watcher, WatcherAsync
from .__Transition import Transition
import ros
