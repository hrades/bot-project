import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription


def generate_launch_description():
    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("my_robot_bringup"),
            "launch",
            "my_gazebo_simu.launch.xml"
        ),
    )

    joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("my_robot_bringup"),
            "launch",
            "joystick.launch.py"
        ),
    )
    
    return LaunchDescription([
        gazebo,
        joystick,
    ])