# launch/localization.launch.py
#
# Starts the "where am I?" stack using upstream packages (we configure, we do not fork):
#   * OpenVINS (ov_msckf)   - visual-inertial odometry  -> /ov_msckf/odomimu
#   * navsat_transform_node - turns /gnss (NavSatFix) into odometry the EKF understands
#   * robot_localization EKF- fuses VIO + wheel odometry + GNSS -> /odom/filtered (30 Hz)
#
# Config lives in config/ov_msckf/*.yaml and config/ekf.yaml. The IMU feeds OpenVINS only,
# not the EKF, so the same IMU data is not counted twice.
#
# TODO: add the OpenVINS, navsat_transform and ekf_node actions using those config files.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        # TODO: Node(package="ov_msckf", executable="run_subscribe_msckf", ...)
        # TODO: Node(package="robot_localization", executable="navsat_transform_node", ...)
        # TODO: Node(package="robot_localization", executable="ekf_node", parameters=[ekf.yaml])
    ])
