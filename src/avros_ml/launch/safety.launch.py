# launch/safety.launch.py
#
# Starts the arbiter in its OWN process, separate from all ML code. This is deliberate:
# if inference stalls, the GIL is busy or Python garbage-collects in the perception
# process, the arbiter's 20 Hz safety loop must keep running on time.
#
# Loads limits and thresholds from config/arbiter.yaml.
# Optional hardening (not done here): run under a real-time priority with `chrt -f` and
# pin to dedicated CPU cores with `taskset`.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory("avros_ml")
    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        Node(
            package="avros_ml",
            executable="arbiter_node",
            name="arbiter_node",
            parameters=[os.path.join(share, "config", "arbiter.yaml"),
                        {"use_sim_time": LaunchConfiguration("use_sim_time")}],
            output="screen",
        ),
    ])
