# safety/state_machine.py
#
# The arbiter's mode logic: which source of commands is allowed to drive the robot.
#
#   MANUAL      - operator (joystick) commands pass through, with limits.
#   AUTONOMOUS  - the IL policy drives, with the safety filter applied.
#   SAFE_STOP   - output is zero. Latched: needs an explicit operator reset.
#
# Rules it will enforce:
#   * AUTONOMOUS can only be entered if the model nodes reported ready (/avros/ready).
#   * Any e-stop, NaN output, or repeated stale-input fault drops to SAFE_STOP.
#   * Leaving SAFE_STOP requires a deliberate reset request, never happens automatically.

from enum import Enum, auto


class Mode(Enum):
    MANUAL = auto()
    AUTONOMOUS = auto()
    SAFE_STOP = auto()


def next_mode(current, request, models_ready, estop, fault):
    """Return the next Mode. TODO: implement transition table described above."""
    raise NotImplementedError
