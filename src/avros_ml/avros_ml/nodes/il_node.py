# nodes/il_node.py
#
# il_node: the imitation-learning "driver". Looks at the fused image and the robot's
# current speed and proposes how to drive (a TCN policy trained from human demonstrations).
#
#   Subscribes:  /perception/rgbt (8UC4), /odom/filtered (nav_msgs/Odometry),
#                /autonomous_mode (std_msgs/Bool, latched)
#   Publishes:   /il/cmd_vel (geometry_msgs/TwistStamped) at a FIXED 20 Hz
#                /avros/ready/il (std_msgs/Bool, latched) once the model is warm
#
# How it works:
#   * TIME-DRIVEN: a 20 Hz timer (in its own callback group, so image callbacks can never
#     block it). Each tick it uses the newest frame and newest odometry it has.
#   * Subscriptions only store the latest frame/odometry; no heavy work in callbacks.
#   * Each tick: skip if the frame is too stale -> feed the policy -> publish a command.
#     The command carries the stamp of the frame it was computed from (for latency tracing).
#   * The policy's temporal history (TCN buffer) is reset when autonomy turns on and after
#     any gap in frames, so the model never sees a broken timeline.
#   * Only speeds (v, w) from odometry are fed to the model, not absolute pose, because pose
#     drifts and would not generalise to other places.
#   * At configure time it checks that model.yaml's `dt` matches the tick period.
#   * Lifecycle node: the model is loaded in on_configure (slow), and the node is only
#     "ready" afterwards.
#
# The model is chosen by parameters, so swapping the TCN needs no code change.

import rclpy
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.lifecycle import Node as LifecycleNode
from rclpy.lifecycle import State, TransitionCallbackReturn
from sensor_msgs.msg import Image
from std_msgs.msg import Bool

from avros_ml.models.base import OdomState
from avros_ml.models.registry import build_policy
from avros_ml.utils.image_io import imgmsg_to_numpy
from avros_ml.utils.latency_monitor import LatencyMonitor
from avros_ml.utils.qos import CONTROL_QOS, LATCHED_QOS, SENSOR_QOS


class IlNode(LifecycleNode):
    def __init__(self):
        super().__init__("il_node")
        self.declare_parameter("model", "dummy")
        self.declare_parameter("weights", "")
        self.declare_parameter("spec", "")
        self.declare_parameter("device", "cuda:0")
        self.declare_parameter("rate_hz", 20.0)
        self.declare_parameter("max_frame_age_s", 0.15)
        self.monitor = LatencyMonitor("il_node")
        self.latest_frame = None
        self.latest_odom = None
        self.autonomous = False
        self.timer_group = MutuallyExclusiveCallbackGroup()

    def on_configure(self, state: State):
        p = self.get_parameter
        self.policy = build_policy(p("model").value, p("weights").value, p("device").value, p("spec").value)
        # TODO: compare ModelSpec.dt with 1 / rate_hz and fail with TransitionCallbackReturn.FAILURE if different
        self.pub = self.create_publisher(TwistStamped, "/il/cmd_vel", CONTROL_QOS)
        self.ready_pub = self.create_publisher(Bool, "/avros/ready/il", LATCHED_QOS)
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State):
        self.create_subscription(Image, "/perception/rgbt", self.on_frame, SENSOR_QOS)
        self.create_subscription(Odometry, "/odom/filtered", self.on_odom, CONTROL_QOS)
        self.create_subscription(Bool, "/autonomous_mode", self.on_mode, LATCHED_QOS)
        self.timer = self.create_timer(1.0 / self.get_parameter("rate_hz").value, self.tick,
                                       callback_group=self.timer_group)
        self.ready_pub.publish(Bool(data=True))
        return super().on_activate(state)

    def on_deactivate(self, state: State):
        self.destroy_timer(self.timer)
        self.ready_pub.publish(Bool(data=False))
        return super().on_deactivate(state)

    # --- callbacks only store data --------------------------------------------
    def on_frame(self, msg):
        self.latest_frame = msg

    def on_odom(self, msg):
        self.latest_odom = msg

    def on_mode(self, msg):
        if msg.data and not self.autonomous:
            self.policy.reset()  # fresh history when autonomy starts
        self.autonomous = msg.data

    # --- the 20 Hz control tick -----------------------------------------------
    def tick(self):
        # TODO: skip if no frame/odom or frame older than max_frame_age_s (and reset history on a gap)
        # TODO: rgbt = imgmsg_to_numpy(frame); v, w = self.policy(rgbt, OdomState(vx, wz))
        # TODO: publish TwistStamped with header = frame.header
        pass


def main(args=None):
    rclpy.init(args=args)
    node = IlNode()
    # TODO: trigger configure + activate (launch lifecycle events, or node.trigger_* in single-process mode)
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
