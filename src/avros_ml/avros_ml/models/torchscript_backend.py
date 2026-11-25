# models/torchscript_backend.py
#
# Generic loader for any PyTorch model exported with torch.jit.trace / torch.jit.script.
# Intended first use: the TCN imitation-learning policy (small, fine in FP16 on the Orin).
#
# What it will do:
#   * torch.jit.load() the .pt file, move it to the GPU, switch to eval + half precision.
#   * Preprocess the frame on the GPU (resize / normalise using ModelSpec).
#   * For TCN policies: keep a ring buffer of per-frame features so that each 20 Hz tick
#     only runs the image encoder on the NEWEST frame, then the TCN over the buffer.
#   * Postprocess: scale and clamp (v, w).
#
# torch is imported lazily so that the rest of the package (and unit tests) work on
# machines without PyTorch.

from .base import Detector, OdomState, Policy
from .registry import register


@register("policy", "torchscript")
class TorchScriptPolicy(Policy):
    def load(self, weights, device, spec):
        # TODO: import torch; self.net = torch.jit.load(weights, map_location=device).eval()
        raise NotImplementedError

    def reset(self):
        # TODO: clear the feature ring buffer
        pass

    def __call__(self, rgbt, odom: OdomState):
        # TODO: preprocess -> encode newest frame -> push to buffer -> TCN -> (v, w)
        raise NotImplementedError


@register("detector", "torchscript")
class TorchScriptDetector(Detector):
    def load(self, weights, device, spec):
        # TODO: load a TorchScript detector (use tensorrt_backend for YOLO on the Orin)
        raise NotImplementedError

    def __call__(self, rgbt):
        raise NotImplementedError
