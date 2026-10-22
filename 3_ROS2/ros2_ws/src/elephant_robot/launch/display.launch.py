"""Launch the elephant robot description, joint state publisher and RViz2.

The package ships a pre-expanded plain URDF (``urdf/elephant_robot.urdf``)
so the robot can be displayed even when the ``xacro`` package is not
installed.  When xacro *is* available you can work with the parameterized
source instead:

    ros2 launch elephant_robot display.launch.py \
        model:=$(ros2 pkg prefix --share elephant_robot)/urdf/elephant_robot.urdf.xacro
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _load_model(model_path):
    """Return the URDF/XML text for ``model_path``.

    A ``.xacro`` file is expanded with xacro when available, otherwise the
    pre-expanded ``.urdf`` sitting next to it is used.
    """
    if model_path.endswith('.xacro'):
        try:
            import xacro
        except ImportError:
            plain = os.path.splitext(model_path)[0] + '.urdf'
            with open(plain, 'r') as fh:
                return fh.read()
        return xacro.process_file(model_path).toprettyxml(indent='  ')
    with open(model_path, 'r') as fh:
        return fh.read()


def _package_available(name):
    try:
        get_package_share_directory(name)
        return True
    except Exception:
        return False


def _spawn(context, *args, **kwargs):
    """Resolve the launch arguments and build the node list."""
    model_path = LaunchConfiguration('model').perform(context)
    use_sim_time = LaunchConfiguration('use_sim_time').perform(context)
    robot_description = _load_model(model_path)

    nodes = [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': use_sim_time == 'true',
            }],
        ),
    ]

    if LaunchConfiguration('jsp').perform(context) == 'true' and \
            _package_available('joint_state_publisher'):
        nodes.append(Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time == 'true'}],
        ))

    if LaunchConfiguration('gui').perform(context) == 'true' and \
            _package_available('joint_state_publisher_gui'):
        nodes.append(Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time == 'true'}],
        ))

    if LaunchConfiguration('rviz').perform(context) == 'true' and \
            _package_available('rviz2'):
        nodes.append(Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.join(
                get_package_share_directory('elephant_robot'), 'rviz', 'elephant.rviz')],
            parameters=[{'use_sim_time': use_sim_time == 'true'}],
        ))

    return nodes


def generate_launch_description():
    pkg_share = get_package_share_directory('elephant_robot')
    default_model = os.path.join(pkg_share, 'urdf', 'elephant_robot.urdf')

    args = [
        DeclareLaunchArgument(
            'model', default_value=default_model,
            description='Absolute path to the URDF or xacro file to load.'),
        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use the /clock topic instead of wall time.'),
        DeclareLaunchArgument(
            'jsp', default_value='true',
            description='Start joint_state_publisher (needs the package).'),
        DeclareLaunchArgument(
            'gui', default_value='true',
            description='Start joint_state_publisher_gui (needs the gui package).'),
        DeclareLaunchArgument(
            'rviz', default_value='true',
            description='Start RViz2 with the bundled configuration.'),
    ]

    return LaunchDescription(args + [OpaqueFunction(function=_spawn)])
