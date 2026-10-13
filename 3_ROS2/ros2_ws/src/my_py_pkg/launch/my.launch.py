from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_py_pkg',
            executable='argument',
            
        ),
        Node(
            package='my_py_pkg',
            executable='calculator',
            
        ),
    ])
