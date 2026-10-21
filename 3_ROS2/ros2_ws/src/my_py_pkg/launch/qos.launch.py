from launch import LaunchDescription
from launch_ros.actions import Node

# 여러 노드 가동을 해보겠습니다
def generate_launch_description():
    return LaunchDescription(
        [
            Node(package='my_py_pkg', executable='qos_talker'),
            Node(package='my_py_pkg', executable='qos_listener')
        ]
    )