import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    
    description = get_package_share_directory('my_robot_description')

    joy_teleop = Node(
        package="joy_teleop",
        executable="joy_teleop",
        parameters=[os.path.join(get_package_share_directory("my_robot_description"), "config", "joy_teleop.yaml")],
    )

    joy_node = Node(
        package="joy",
        executable="joy_node",
        name="joystick",
        parameters=[os.path.join(get_package_share_directory("my_robot_description"), "config", "joy_config.yaml")]
    )
    
    twist_mux_launch = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("twist_mux"),
            "launch",
            "twist_mux_launch.py"
        ),
        launch_arguments={
            "cmd_vel_out": "/diff_cont/cmd_vel_unstamped",
            "config_locks": os.path.join(description, "config", "twist_mux_locks.yaml"),
            "config_topics": os.path.join(description, "config", "twist_mux_topics.yaml"),
            "config_joy": os.path.join(description, "config", "twist_mux_joy.yaml"),
        }.items(),
    )

    return LaunchDescription(
        [
            joy_teleop,
            joy_node,
            twist_mux_launch,
        ]
    )
