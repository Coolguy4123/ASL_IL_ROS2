# launch/perception.launch.py
#
# Starts the perception + imitation-learning nodes: rgbt_fusion, detector, il_node.
#
#   single_process:=true  -> one process (`perception_main`): one CUDA context, shared
#                            memory, least RAM on the Orin. Default for the robot.
#   single_process:=false -> three separate processes: easier to debug or restart one stage.
#
# Which models run is set by the launch arguments detector_model / il_model
# ("dummy", "tensorrt", "torchscript" or "my_pkg.module:Class"); weights and model.yaml
# paths come from config/detector.yaml and config/il.yaml.
#
# TODO: pass the YAML configs as parameters, and (multi-process mode) add lifecycle
#       configure/activate events so the model nodes come up automatically.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        DeclareLaunchArgument("detector_model", default_value="dummy"),
        DeclareLaunchArgument("il_model", default_value="dummy"),
        DeclareLaunchArgument("single_process", default_value="true"),
        # TODO: GroupAction(condition=IfCondition(single_process), actions=[Node(executable="perception_main")])
        # TODO: GroupAction(condition=UnlessCondition(single_process), actions=[fusion, detector, il nodes])
    ])
