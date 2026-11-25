# models/model_spec.py
#
# Reads the model.yaml that sits next to a model's weights. This is the "user manual" of
# a model: image size, channel order, normalisation, how many past steps a TCN needs,
# the time step it was trained at, and the class names for a detector.
#
# Nodes use it to (1) prepare inputs exactly the way the model was trained, and
# (2) refuse to start if the spec disagrees with the live pipeline (e.g. the TCN was
# trained at dt=0.05 s but the node ticks at 15 Hz). See the example in models/example_model.yaml.

from dataclasses import dataclass, field
from typing import List, Optional

import yaml


@dataclass
class ModelSpec:
    input_size: List[int] = field(default_factory=lambda: [480, 640])  # [height, width]
    channels: List[str] = field(default_factory=lambda: ["B", "G", "R", "T"])
    mean: Optional[List[float]] = None
    std: Optional[List[float]] = None
    dtype: str = "float16"
    # detector only
    classes: List[str] = field(default_factory=list)
    # policy only
    history: int = 1          # number of past steps the model needs (TCN receptive field)
    dt: float = 0.05          # seconds between steps the model was trained with
    output_scale: List[float] = field(default_factory=lambda: [1.0, 1.0])  # (v, w) scaling

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as f:
            raw = yaml.safe_load(f) or {}
        flat = {**raw.get("input", {}), **raw.get("output", {}), **raw.get("policy", {})}
        if "size" in flat:
            flat["input_size"] = flat.pop("size")
        known = {k: v for k, v in flat.items() if k in cls.__dataclass_fields__}
        return cls(**known)
