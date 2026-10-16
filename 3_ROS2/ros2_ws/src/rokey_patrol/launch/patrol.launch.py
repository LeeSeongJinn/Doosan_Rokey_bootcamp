from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rokey_patrol',
            executable='robot_sensor',
            parameters=[{"threshold":0.4, "base_temp":30.0}] #문서상으로 설정값 바꿀 수 있게 해준다. 터미널 파라미터 명령은 1회성
            
        ),
        Node(
            package='rokey_patrol',
            executable='robot_patrol',
            
        ),
    ])
