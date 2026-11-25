# launch/replay_bag.launch.py
#
# Runs the software stack offline against a recorded bag, with no robot attached.
# Sets use_sim_time:=true, plays the bag with --clock, and starts perception + safety
# (but not the drivers, since the bag supplies the sensor data).
#
# Use it to: tune fusion, check latency, compare two models on identical data, and run
# regression tests before going out on the real hardware.
#
# TODO: add the `bag` launch argument, ExecuteProcess(["ros2","bag","play","--clock",...]),
#       and include perception.launch.py and safety.launch.py with use_sim_time:=true.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("bag", description="Path to the bag to replay"),
        # TODO: bag play + includes
    ])
