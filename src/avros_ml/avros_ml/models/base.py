# models/base.py
#
# The CONTRACT every model must follow. A node never knows whether it is running a YOLO
# TensorRT engine, a TorchScript TCN, or a fake test model: it only calls these methods.
#
#   Detector: RGB-T frame            -> list of detections
#   Policy:   RGB-T frame + odometry -> (linear velocity, angular velocity)
#
# To plug in a new model: subclass one of these, register it in registry.py (or point the
# ROS parameter `model` at "my_package.my_file:MyClass"), and ship a model.yaml next to the
# weights describing input size, normalisation and outputs (see model_spec.py).

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Det:
    """One detected object, in pixel coordinates of the RGB-T image."""
    cls: str
    score: float
    cx: float
    cy: float
    w: float
    h: float


@dataclass
class OdomState:
    """The few robot-state numbers a policy is allowed to see (velocities, not pose)."""
    vx: float
    wz: float


class Detector(ABC):
    @abstractmethod
    def load(self, weights: str, device: str, spec) -> None:
        """Read weights/engine from disk and move them to the device. Slow; runs once."""

    def warmup(self, n: int = 5) -> None:
        """Run a few dummy inferences so the first real frame is not slow."""

    @abstractmethod
    def __call__(self, rgbt) -> List[Det]:
        """rgbt: HxWx4 uint8 numpy array (B, G, R, T). Returns detections."""


class Policy(ABC):
    @abstractmethod
    def load(self, weights: str, device: str, spec) -> None:
        """Read weights from disk and move them to the device. Slow; runs once."""

    def warmup(self, n: int = 5) -> None:
        """Run a few dummy steps so the first real tick is not slow."""

    def reset(self) -> None:
        """Forget temporal history (TCN feature buffer). Called when autonomy starts or after a gap."""

    @abstractmethod
    def __call__(self, rgbt, odom: OdomState) -> Tuple[float, float]:
        """Returns (linear_velocity m/s, angular_velocity rad/s)."""
