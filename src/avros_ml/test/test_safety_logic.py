# test/test_safety_logic.py
# Unit tests for the arbiter's decision rules (safety/*.py). The first two pass today;
# the rest are placeholders marking the behaviour to implement and verify next.

import math

import pytest

from avros_ml.safety.limiter import clamp, reject_nonfinite
from avros_ml.safety.hazard_distance import speed_limit_for_distance


def test_nan_becomes_stop():
    assert reject_nonfinite(float("nan"), 0.5) == (0.0, 0.0)


def test_speed_limit_zero_inside_stop_distance():
    assert speed_limit_for_distance(1.0, d_stop_m=1.5, brake_decel=1.0) == 0.0
    assert math.isclose(speed_limit_for_distance(3.5, 1.5, 1.0), 2.0)


def test_clamp():
    assert clamp(5.0, -5.0, 1.0, 1.0) == (1.0, -1.0)


@pytest.mark.skip(reason="TODO: implement slew_limit")
def test_decel_faster_than_accel():
    ...


@pytest.mark.skip(reason="TODO: implement state machine")
def test_autonomous_requires_models_ready():
    ...


@pytest.mark.skip(reason="TODO: implement hazard_distance")
def test_person_in_corridor_limits_speed():
    ...
