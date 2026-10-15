from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='hangman',executable='game_node'),
        Node(package='hangman', executable='game_client'),
    ])

# hangman game node, client 두 개를 launch를 이용해 가동하기
# 1. setup.py 내부에 entripoint 등록 & data files 내용 구성
# 2. launch 폴더 생성 -> xxxxxx.launch.py 를 만들기 -> 내용 채우기 
# 3. cb->ss-> ros2 launch ... 켜기