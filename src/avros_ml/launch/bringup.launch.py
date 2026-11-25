# bringup.launch.py
#
# The one command to start avros_ml:   ros2 launch avros_ml bringup.launch.py
#
# It starts the four nodes this package owns: rgbt_fusion_node, detector_node, il_node and
# arbiter_node. The actuator is NOT started here because it lives in another package; its
# launch is meant to be included at the marked spot below.
#
# Launch arguments (all optional):
#   use_sim_time    true when replaying a bag, so nodes follow the bag's clock
#   detector_model  name of the detector in ML_Models (default: dummy)
#   il_model        name of the imitation-learning policy in ML_Models (default: dummy)
#
# Note: detector_node and il_node are meant to be lifecycle nodes (they load a model first),
# so they will need to be configured and activated once they are implemented.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('detector_model', default_value='dummy'),
        DeclareLaunchArgument('il_model', default_value='dummy'),

        Node(
            package='avros_ml',
            executable='rgbt_fusion_node',
            name='rgbt_fusion_node',
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen',
        ),
        Node(
            package='avros_ml',
            executable='detector_node',
            name='detector_node',
            parameters=[{
                'use_sim_time': use_sim_time,
                'model': LaunchConfiguration('detector_model'),
            }],
            output='screen',
        ),
        Node(
            package='avros_ml',
            executable='il_node',
            name='il_node',
            parameters=[{
                'use_sim_time': use_sim_time,
                'model': LaunchConfiguration('il_model'),
            }],
            output='screen',
        ),
        # The arbiter is its own process on purpose, away from the heavy ML nodes.
        Node(
            package='avros_ml',
            executable='arbiter_node',
            name='arbiter_node',
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen',
        ),

        # TODO: include the actuator package's launch file here, e.g.
        #   IncludeLaunchDescription(PythonLaunchDescriptionSource(<path to its launch file>))
    ])
