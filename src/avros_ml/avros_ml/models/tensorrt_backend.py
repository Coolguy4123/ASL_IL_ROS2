# models/tensorrt_backend.py
#
# Loader for NVIDIA TensorRT engines (.engine files). Intended first use: the YOLO
# detector, which is several times faster as a TensorRT FP16/INT8 engine than as eager
# PyTorch on the Jetson AGX Orin.
#
# What it will do:
#   * Deserialize the .engine file and allocate input/output buffers once.
#   * Preprocess on the GPU (4-channel input: B, G, R, T), run inference, synchronise the
#     CUDA stream so timing is honest.
#   * Postprocess: non-max suppression, map class ids to names from ModelSpec.classes,
#     and return a list of Det objects.
#
# The model is still trained and exported from PyTorch; only the deployment format
# differs. Build engines on the Orin itself (engines are tied to the GPU/TensorRT version).

from .base import Detector, Det
from .registry import register


@register("detector", "tensorrt")
class TensorRTDetector(Detector):
    def load(self, weights, device, spec):
        # TODO: import tensorrt; deserialize engine; allocate buffers
        raise NotImplementedError

    def __call__(self, rgbt):
        # TODO: GPU preprocess -> execute -> NMS -> list[Det]
        raise NotImplementedError
