# nodes/detector_node.py
#
# detector_node: finds objects (people, vehicles, ...) in the fused RGB-T image with YOLO.
#
#   Subscribes:  /perception/rgbt (8UC4)
#   Publishes:   /perception/detections (vision_msgs/Detection2DArray), ~15-20 Hz
#                /avros/ready/detector (std_msgs/Bool, latched) once the model is warm
#
# How it works:
#   * Lifecycle node. on_configure loads the model (TensorRT engine for YOLO) and warms it
#     up, which takes seconds; on_activate starts listening. The arbiter will not allow
#     autonomy until this node says it is ready.
#   * The ROS callback only drops the newest frame into a one-slot mailbox (LatestSlot).
#     A worker thread does the heavy lifting, so slow inference drops old frames instead of
#     building up a queue of stale ones.
#   * The output copies the input header, so every downstream node can measure how old a
#     detection is.
#
# The model is chosen by parameters (`model`, `weights`, `spec`, `device`); no code changes
# are needed to swap models.

import threading

import rclpy
from rclpy.lifecycle import Node as LifecycleNode
from rclpy.lifecycle import State, TransitionCallbackReturn
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray

from avros_ml.models.registry import build_detector
from avros_ml.utils.image_io import imgmsg_to_numpy
from avros_ml.utils.latency_monitor import LatencyMonitor
from avros_ml.utils.latest_slot import LatestSlot
from avros_ml.utils.qos import LATCHED_QOS, SENSOR_QOS


class DetectorNode(LifecycleNode):
    def __init__(self):
        super().__init__("detector_node")
        self.declare_parameter("model", "dummy")
        self.declare_parameter("weights", "")
        self.declare_parameter("spec", "")
        self.declare_parameter("device", "cuda:0")
        self.declare_parameter("score_threshold", 0.4)
        self.monitor = LatencyMonitor("detector_node")
        self.slot = LatestSlot()
        self._run = False

    # --- lifecycle -------------------------------------------------------------
    def on_configure(self, state: State):
        p = self.get_parameter
        self.model = build_detector(p("model").value, p("weights").value, p("device").value, p("spec").value)
        self.pub = self.create_publisher(Detection2DArray, "/perception/detections", SENSOR_QOS)
        self.ready_pub = self.create_publisher(Bool, "/avros/ready/detector", LATCHED_QOS)
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State):
        self.sub = self.create_subscription(Image, "/perception/rgbt", self.slot.put, SENSOR_QOS)
        self._run = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        self.ready_pub.publish(Bool(data=True))
        return super().on_activate(state)

    def on_deactivate(self, state: State):
        self._run = False
        self.ready_pub.publish(Bool(data=False))
        return super().on_deactivate(state)

    # --- worker ----------------------------------------------------------------
    def _loop(self):
        while self._run:
            msg = self.slot.get(0.1)
            if msg is None:
                continue
            rgbt = imgmsg_to_numpy(msg)
            with self.monitor.stage("infer"):
                dets = self.model(rgbt)
            # TODO: convert `dets` (list[Det]) into Detection2DArray with msg.header and publish


def main(args=None):
    rclpy.init(args=args)
    node = DetectorNode()
    # TODO: trigger configure + activate (launch lifecycle events, or node.trigger_* in single-process mode)
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
