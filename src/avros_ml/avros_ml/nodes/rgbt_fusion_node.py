# nodes/rgbt_fusion_node.py
#
# rgbt_fusion_node: glues the RGB camera and the thermal camera into ONE 4-channel image.
#
#   Subscribes:  /rgb/image_raw (bgr8), /rgb/camera_info,
#                /thermal/image_raw (mono16), /thermal/camera_info
#   Publishes:   /perception/rgbt (sensor_msgs/Image, 8UC4: B, G, R, T), ~15-20 Hz
#
# How it works (RGB is the "master clock"):
#   1. Every thermal frame is stored in a short history.
#   2. When an RGB frame arrives, pick the thermal frame closest in time.
#   3. If none is close enough (parameter max_time_diff_s), follow `on_missing_thermal`:
#      "drop" the frame, fill T with "zeros", or "hold_last" thermal frame.
#   4. Warp thermal into the RGB view (map computed once at startup), convert to 8 bits,
#      stack to 8UC4, and publish with the RGB header stamp so latency can be traced.
#   5. A rate gate (max_rate_hz) keeps the output at the configured rate.
#
# Regular node (not lifecycle): it loads no model, so it starts instantly.

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image

from avros_ml.utils.qos import SENSOR_QOS


class RgbtFusionNode(Node):
    def __init__(self):
        super().__init__("rgbt_fusion_node")
        self.declare_parameter("max_rate_hz", 20.0)
        self.declare_parameter("max_time_diff_s", 0.04)
        self.declare_parameter("on_missing_thermal", "zeros")  # drop | zeros | hold_last
        self.declare_parameter("thermal_raw_min", 0)
        self.declare_parameter("thermal_raw_max", 65535)
        self.declare_parameter("calibration_dir", "")

        self.pub = self.create_publisher(Image, "/perception/rgbt", SENSOR_QOS)
        self.create_subscription(Image, "/rgb/image_raw", self.on_rgb, SENSOR_QOS)
        self.create_subscription(Image, "/thermal/image_raw", self.on_thermal, SENSOR_QOS)
        self.create_subscription(CameraInfo, "/rgb/camera_info", self.on_rgb_info, SENSOR_QOS)
        self.create_subscription(CameraInfo, "/thermal/camera_info", self.on_thermal_info, SENSOR_QOS)

    def on_thermal(self, msg):
        # TODO: append to a short deque (maxlen ~5)
        pass

    def on_rgb(self, msg):
        # TODO: nearest thermal -> warp -> stack -> publish with msg.header
        pass

    def on_rgb_info(self, msg):
        # TODO: cache once; (re)build the warp map when both infos are known
        pass

    def on_thermal_info(self, msg):
        pass


def main(args=None):
    rclpy.init(args=args)
    node = RgbtFusionNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
