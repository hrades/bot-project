import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription


def generate_launch_description():
    hardware_interface = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("my_robot_bringup"),
            "launch",
            "hardware_interface.launch.py"
        ),
    )

    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("my_robot_bringup"),
            "launch",
            "controller.launch.py"
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
        hardware_interface,
        controller,
        joystick
    ])