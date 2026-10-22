from launch import LaunchDescription
from launch_ros.actions import Node

# 여러 노드 가동을 해보겠습니다
def generate_launch_description():
    return LaunchDescription(
        [
            Node(package='my_py_pkg', executable='wheel_driver'),
            Node(package='my_py_pkg', executable='fake_camera'),
            Node(package='my_py_pkg', executable='camera_mount'),
            Node(package='my_py_pkg', executable='chaser')
        ]
    )