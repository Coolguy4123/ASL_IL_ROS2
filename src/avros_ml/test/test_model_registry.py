# test/test_model_registry.py
# Checks the plug-and-play mechanism: models are found by name, can be loaded from a
# "module:Class" path, and unknown names fail with a clear error.

import pytest

import avros_ml.models  # noqa: F401  (registers built-ins)
from avros_ml.models.base import OdomState
from avros_ml.models.registry import build_detector, build_policy


def test_dummy_models_by_name():
    det = build_detector("dummy", weights="person_ahead")
    import numpy as np
    assert det(np.zeros((480, 640, 4), np.uint8))[0].cls == "person"
    assert build_policy("dummy")(None, OdomState(0.0, 0.0)) == (0.3, 0.1)


def test_load_by_module_path():
    det = build_detector("avros_ml.models.builtin.dummy_detector:DummyDetector")
    assert det is not None


def test_unknown_name_raises():
    with pytest.raises(KeyError):
        build_detector("does_not_exist")
