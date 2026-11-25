# nodes/arbiter_node.py
#
# arbiter_node: the SAFETY BRAIN. The ML nodes only propose; this node decides what the
# wheels actually get. It is the only node allowed to publish /cmd_vel.
#
#   Subscribes:  /il/cmd_vel (TwistStamped), /perception/detections (Detection2DArray),
#                /rgb/camera_info, /teleop/cmd_vel (Twist), /joy (mode/e-stop buttons),
#                /avros/ready/detector, /avros/ready/il
#   Publishes:   /cmd_vel (Twist) at a FIXED 20 Hz, always, even when the answer is zero
#                /autonomous_mode (std_msgs/Bool, latched)
#                /avros/status (diagnostic_msgs/DiagnosticArray) - which rule fired and why
#   Service:     ~/set_mode (std_srvs/SetBool) to request autonomy; ~/reset to leave SAFE_STOP
#
# How it works (every 20 Hz timer tick):
#   1. Freshness: if the IL command is older than ~0.2 s (measured on a monotonic clock
#      from when it ARRIVED, not by its header) -> output zero.
#   2. Mode: MANUAL / AUTONOMOUS / SAFE_STOP (see safety/state_machine.py).
#   3. Detector watchdog: if detections go stale, creep instead of full speed.
#   4. Hazards: nearest person/vehicle in the forward corridor limits the allowed speed
#      (see safety/hazard_distance.py), with debounce so it does not flicker.
#   5. Limits: reject NaN, clamp to max speeds, slew-rate limit (safety/limiter.py).
#   6. Publish /cmd_vel. Callbacks only STORE inputs; the timer is the single place that
#      publishes, so the output rate is steady.
#
# Run this node in its OWN process (see launch/safety.launch.py) so that a stalled
# inference thread or Python garbage-collection pause elsewhere can never delay it.

import rclpy
from diagnostic_msgs.msg import DiagnosticArray
from geometry_msgs.msg import Twist, TwistStamped
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo
from std_msgs.msg import Bool
from std_srvs.srv import SetBool, Trigger
from vision_msgs.msg import Detection2DArray

from avros_ml.safety.state_machine import Mode
from avros_ml.utils.qos import CONTROL_QOS, LATCHED_QOS, SENSOR_QOS


class ArbiterNode(Node):
    def __init__(self):
        super().__init__("arbiter_node")
        # limits and timing
        self.declare_parameter("rate_hz", 20.0)
        self.declare_parameter("il_timeout_s", 0.2)
        self.declare_parameter("detection_timeout_s", 0.3)
        self.declare_parameter("v_max", 1.0)
        self.declare_parameter("w_max", 1.0)
        self.declare_parameter("v_creep", 0.1)
        self.declare_parameter("a_acc", 0.5)
        self.declare_parameter("a_dec", 1.5)
        # hazards
        self.declare_parameter("hazard_classes", ["person", "vehicle"])
        self.declare_parameter("hazard_min_score", 0.5)
        self.declare_parameter("d_stop_m", 1.5)
        self.declare_parameter("brake_decel", 1.0)
        self.declare_parameter("corridor_half_angle_deg", 18.0)
        self.declare_parameter("camera_height_m", 0.6)
        self.declare_parameter("camera_pitch_deg", 0.0)
        self.declare_parameter("debounce_on", 3)    # hazard seen in N of the last M frames to engage
        self.declare_parameter("debounce_window", 5)
        self.declare_parameter("release_hold_s", 1.0)

        self.mode = Mode.MANUAL
        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", CONTROL_QOS)
        self.mode_pub = self.create_publisher(Bool, "/autonomous_mode", LATCHED_QOS)
        self.status_pub = self.create_publisher(DiagnosticArray, "/avros/status", CONTROL_QOS)

        self.create_subscription(TwistStamped, "/il/cmd_vel", self.on_il, CONTROL_QOS)
        self.create_subscription(Detection2DArray, "/perception/detections", self.on_dets, SENSOR_QOS)
        self.create_subscription(CameraInfo, "/rgb/camera_info", self.on_info, SENSOR_QOS)
        self.create_subscription(Twist, "/teleop/cmd_vel", self.on_teleop, CONTROL_QOS)
        self.create_service(SetBool, "~/set_mode", self.on_set_mode)
        self.create_service(Trigger, "~/reset", self.on_reset)

        self.timer = self.create_timer(1.0 / self.get_parameter("rate_hz").value, self.tick)
        self.mode_pub.publish(Bool(data=False))

    # --- callbacks only store inputs (and the arrival time on a monotonic clock) ---
    def on_il(self, msg): pass          # TODO: store cmd + arrival time
    def on_dets(self, msg): pass        # TODO: store detections + arrival time
    def on_info(self, msg): pass        # TODO: cache intrinsics (fx, fy, cx, cy)
    def on_teleop(self, msg): pass      # TODO: store teleop command

    def on_set_mode(self, req, res):    # TODO: request AUTONOMOUS only if both models are ready
        res.success = False
        res.message = "not implemented"
        return res

    def on_reset(self, req, res):       # TODO: leave SAFE_STOP deliberately
        res.success = False
        res.message = "not implemented"
        return res

    def tick(self):
        # TODO: follow steps 1-6 from the header; publish /cmd_vel every tick
        self.cmd_pub.publish(Twist())   # safe default for the skeleton: always command zero


def main(args=None):
    rclpy.init(args=args)
    node = ArbiterNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
