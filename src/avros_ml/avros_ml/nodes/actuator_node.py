# nodes/actuator_node.py
#
# actuator_node: the bridge between ROS and the robot's motors. Receives the arbiter's
# final velocity command and reports how the wheels actually moved.
#
#   Subscribes:  /cmd_vel (Twist), /autonomous_mode (Bool)
#   Publishes:   /wheel_odom (nav_msgs/Odometry) at 50 Hz
#
# Responsibilities:
#   * Convert (v, w) into whatever the motor controller needs (wheel speeds, CAN, serial...).
#   * Its OWN watchdog: if /cmd_vel is older than ~0.25 s, command zero velocity. This must
#     not depend on the arbiter being alive.
#   * Publish wheel odometry from encoders for the EKF.
#
# If your base already ships a ROS 2 driver, replace this file with a thin wrapper around it
# (or delete the node and launch the vendor driver from launch/drivers.launch.py).
# A hardware e-stop that cuts motor power independent of ROS is still required.

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Bool

from avros_ml.utils.qos import CONTROL_QOS, LATCHED_QOS


class ActuatorNode(Node):
    def __init__(self):
        super().__init__("actuator_node")
        self.declare_parameter("cmd_timeout_s", 0.25)
        self.declare_parameter("odom_rate_hz", 50.0)
        self.odom_pub = self.create_publisher(Odometry, "/wheel_odom", CONTROL_QOS)
        self.create_subscription(Twist, "/cmd_vel", self.on_cmd, CONTROL_QOS)
        self.create_subscription(Bool, "/autonomous_mode", self.on_mode, LATCHED_QOS)
        # TODO: timers for the watchdog check and for odometry publishing

    def on_cmd(self, msg):
        pass  # TODO: remember the command and when it arrived; send to motors

    def on_mode(self, msg):
        pass  # TODO: e.g. LED/indicator, or enable motor drivers


def main(args=None):
    rclpy.init(args=args)
    node = ActuatorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
