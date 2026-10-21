from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    return LaunchDescription(
        [
            ComposableNodeContainer(
                package='rclcpp_components',
                namespace='my_ns',
                executable='component_container',
                name='my_container',
                composable_node_descriptions=[
                    ComposableNode(
                        package='composition',
                        plugin='composition::Talker',
                        name='talker_node',
                        extra_arguments=[
                            {'use_intra_process_comms': True}
                        ]
                    ),
                    ComposableNode(
                        package='composition',
                        plugin='composition::Listener',
                        name='listener_node',
                        extra_arguments=[
                            {'use_intra_process_comms': True}
                        ]
                    )
                ],
                output='screen'
            )
        ]
    )