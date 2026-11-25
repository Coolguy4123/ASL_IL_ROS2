# models/registry.py
#
# The "phone book" that turns the ROS parameter `model: <name>` into a model object.
#
#   * Built-in backends register a short name:     @register("detector", "torchscript")
#   * Your own models can be loaded by path:       model: "my_pkg.my_file:MyDetector"
#
# build_detector()/build_policy() create the object, load the weights, and warm it up.
# Nodes call these from their on_configure step, so a bad path or mismatched model.yaml
# fails at startup instead of in the middle of a run.

import importlib

from .base import Detector, Policy
from .model_spec import ModelSpec

_REGISTRY = {"detector": {}, "policy": {}}


def register(kind, name):
    """Class decorator: @register("policy", "dummy")."""
    def deco(cls):
        _REGISTRY[kind][name] = cls
        return cls
    return deco


def _resolve(kind, name):
    if name in _REGISTRY[kind]:
        return _REGISTRY[kind][name]
    if ":" in name:  # "package.module:ClassName"
        module, cls = name.split(":", 1)
        return getattr(importlib.import_module(module), cls)
    raise KeyError(f"Unknown {kind} model '{name}'. Registered: {sorted(_REGISTRY[kind])}")


def _build(kind, name, weights, device, spec_path):
    model = _resolve(kind, name)()
    spec = ModelSpec.from_file(spec_path) if spec_path else ModelSpec()
    model.load(weights, device, spec)
    model.warmup()
    return model, spec


def build_detector(name, weights="", device="cuda:0", spec_path="") -> Detector:
    return _build("detector", name, weights, device, spec_path)[0]


def build_policy(name, weights="", device="cuda:0", spec_path="") -> Policy:
    return _build("policy", name, weights, device, spec_path)[0]
