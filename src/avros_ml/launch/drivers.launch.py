# launch/drivers.launch.py
#
# Starts the hardware-facing nodes: RGB camera, thermal camera, Xsens IMU/GNSS driver,
# and the actuator (wheel base). These are mostly VENDOR drivers, not code in this package,
# so this file only wraps them with the right topic names and parameters.
#
# Skipped when replaying a bag (use_sim_time:=true) because the bag provides the data.
#
# TODO: add the real driver nodes for your cameras and the xsens_mti_driver, and
#       publish static transforms from config/calibration/static_tf.yaml.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        # TODO: Node(package="<rgb_driver>", ...), Node(package="<thermal_driver>", ...),
        #       Node(package="xsens_mti_driver", ...), Node(package="avros_ml", executable="actuator_node")
    ])
