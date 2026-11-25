# launch/record_demo.launch.py
#
# Collects imitation-learning training data. Drive the robot by hand (MANUAL mode) while
# this records, in one bag, EXACTLY what the policy will see and what it should learn:
#   inputs : /perception/rgbt, /odom/filtered
#   labels : /cmd_vel (the human's driving)
#   context: /autonomous_mode, /tf, /tf_static, /avros/metrics, /perception/detections
#
# Uses rosbag2 with the mcap storage plugin and zstd compression. /perception/rgbt is about
# 25 MB/s, fine for the Orin's NVMe. Afterwards run `ros2 run avros_ml bag_to_dataset`
# to turn the bag into PyTorch training tensors.
#
# TODO: add ExecuteProcess(["ros2", "bag", "record", "-s", "mcap", ...topics...]) and
#       an output-folder launch argument.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("bag_dir", default_value="~/avros_bags"),
        # TODO: ros2 bag record process
    ])
