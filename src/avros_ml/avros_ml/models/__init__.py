# models/__init__.py
# The plug-and-play model layer. Nodes only talk to the Detector / Policy interfaces in
# base.py; which concrete model is used is chosen by a ROS parameter via registry.py.
# Importing the built-in backends here makes them register themselves by name.

from . import registry  # noqa: F401
from .builtin import dummy_detector, dummy_policy  # noqa: F401  (registers "dummy")
from . import torchscript_backend, tensorrt_backend  # noqa: F401  (register "torchscript", "tensorrt")
