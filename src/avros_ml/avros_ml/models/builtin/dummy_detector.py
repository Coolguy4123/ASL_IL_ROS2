# models/builtin/dummy_detector.py
#
# A pretend object detector for testing. It needs no weights and no GPU.
# By default it returns no detections; set weights="person_ahead" (via the `weights`
# parameter) to make it always report a large "person" in the middle of the image, which
# is handy for checking that the arbiter slows the robot down.

from ..base import Det, Detector
from ..registry import register


@register("detector", "dummy")
class DummyDetector(Detector):
    def load(self, weights, device, spec):
        self.mode = weights

    def __call__(self, rgbt):
        if self.mode == "person_ahead":
            h, w = rgbt.shape[:2]
            return [Det("person", 0.9, w / 2, h * 0.8, w * 0.2, h * 0.4)]
        return []
