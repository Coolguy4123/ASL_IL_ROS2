# utils/qos.py
#
# One place that defines the three QoS (delivery-behaviour) profiles used across the
# whole package, so every node talks to its neighbours with compatible settings.
#
#   SENSOR_QOS  - images, IMU, detections. Best-effort and tiny queue: if we are slow,
#                 we would rather lose an old frame than process it late.
#   CONTROL_QOS - velocity commands and odometry. Reliable, queue of 1-5: commands must
#                 arrive, but only the newest one matters.
#   LATCHED_QOS - "state" topics such as /autonomous_mode and /avros/ready. Reliable and
#                 transient_local: a node that starts late still receives the last value.

from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy

SENSOR_QOS = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=2,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
)

CONTROL_QOS = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=2,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
)

LATCHED_QOS = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
)
