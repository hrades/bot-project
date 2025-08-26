import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import  TimerAction, DeclareLaunchArgument
from launch.substitutions import Command
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch_ros.parameter_descriptions import ParameterValue

from launch_ros.actions import Node

def generate_launch_description():
    
    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])
    
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description,
             "use_sim_time": False},
            os.path.join(
                get_package_share_directory("my_robot_description"),
                "config",
                "robot_controllers.yaml",
            ),
        ],
    )

    delayed_controller_manager = TimerAction(period=3.0, actions=[controller_manager])

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[diff_drive_spawner],
        )
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_broad_spawner],
        )
    )

    return LaunchDescription([
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner
    ])
