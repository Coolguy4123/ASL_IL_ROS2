# models/builtin/dummy_policy.py
#
# A pretend imitation-learning policy for testing. It ignores the image and simply
# drives forward slowly in a gentle curve. Lets you test the arbiter, the actuator and
# the launch files without a trained TCN.

from ..base import OdomState, Policy
from ..registry import register


@register("policy", "dummy")
class DummyPolicy(Policy):
    def load(self, weights, device, spec):
        pass

    def __call__(self, rgbt, odom: OdomState):
        return 0.3, 0.1  # m/s forward, rad/s turn
