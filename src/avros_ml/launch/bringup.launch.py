# launch/bringup.launch.py
#
# THE one command to start the robot:  ros2 launch avros_ml bringup.launch.py
#
# It does no work itself; it just includes the four sub-launch files in a sensible order
# and passes shared arguments down:
#   drivers       -> cameras, IMU, wheel base
#   localization  -> OpenVINS + EKF (+ navsat_transform)
#   perception    -> fusion, detector, il_node (single process or separate)
#   safety        -> arbiter (always its own process)
#
# Arguments: use_sim_time, detector_model, il_model, single_process, record

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    share = get_package_share_directory("avros_ml")

    def include(name, args):
        return IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(share, "launch", name)),
            launch_arguments=args.items(),
        )

    shared = {"use_sim_time": LaunchConfiguration("use_sim_time")}
    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        DeclareLaunchArgument("detector_model", default_value="dummy"),
        DeclareLaunchArgument("il_model", default_value="dummy"),
        DeclareLaunchArgument("single_process", default_value="true"),
        include("drivers.launch.py", shared),
        include("localization.launch.py", shared),
        include("perception.launch.py", {
            **shared,
            "detector_model": LaunchConfiguration("detector_model"),
            "il_model": LaunchConfiguration("il_model"),
            "single_process": LaunchConfiguration("single_process"),
        }),
        include("safety.launch.py", shared),
    ])
