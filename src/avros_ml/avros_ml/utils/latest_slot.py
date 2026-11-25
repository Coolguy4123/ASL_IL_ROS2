# utils/latest_slot.py
#
# A "mailbox with room for one letter". The ROS subscription callback drops the newest
# message in; a worker thread picks it up. If the worker is busy and a newer message
# arrives, the old one is simply replaced.
#
# Why: neural-network inference can be slower than the camera. A normal queue would
# fill with stale frames and make the robot react to the past. With this slot the model
# always works on the most recent frame and old ones are dropped (and counted).

import threading


class LatestSlot:
    def __init__(self):
        self._value = None
        self._cond = threading.Condition()
        self.dropped = 0  # how many messages were overwritten before anyone read them

    def put(self, value):
        """Called from the ROS callback. Must stay fast and never block."""
        with self._cond:
            if self._value is not None:
                self.dropped += 1
            self._value = value
            self._cond.notify()

    def get(self, timeout=0.1):
        """Called from the worker thread. Returns the newest value, or None on timeout."""
        with self._cond:
            if self._value is None:
                self._cond.wait(timeout)
            value, self._value = self._value, None
            return value
