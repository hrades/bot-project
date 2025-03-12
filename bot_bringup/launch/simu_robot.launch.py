import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("bot_description"),
            "launch",
            "gazebo.launch.py"
        )
    )

    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("bot_controller"),
            "launch",
            "two_controllers.launch.py"
        ),
        launch_arguments={
            "use_simple_controller" : "False",
            "use_sim_time" : "True"
        }.items()
    )

    joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("bot_controller"),
            "launch",
            "joystick_teleop.launch.py"
        )
    )

    return LaunchDescription([
        gazebo,
        controller,
        joystick
    ])