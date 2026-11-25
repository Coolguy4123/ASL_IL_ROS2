# safety/limiter.py
#
# Last line of defence on every velocity command before it reaches the wheels:
#   * reject_nonfinite(): a NaN/inf from a model becomes a stop, never a wild motion.
#   * clamp(): enforce maximum linear and angular speed.
#   * slew_limit(): limit how fast the command may change (acceleration limits).
#     Deceleration is allowed to be faster than acceleration, so stopping is quick
#     but starting is smooth.

import math


def reject_nonfinite(v, w):
    return (0.0, 0.0) if not (math.isfinite(v) and math.isfinite(w)) else (v, w)


def clamp(v, w, v_max, w_max):
    return max(-v_max, min(v_max, v)), max(-w_max, min(w_max, w))


def slew_limit(v, w, prev_v, prev_w, a_acc, a_dec, dt):
    """Return (v, w) moved no further from (prev_v, prev_w) than the accel/decel limits allow.

    TODO: implement asymmetric rate limiting.
    """
    raise NotImplementedError
