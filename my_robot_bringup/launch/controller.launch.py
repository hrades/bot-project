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

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                os.path.join(
                    get_package_share_directory("my_robot_description"),
                    "urdf",
                    "my_main_robot.urdf.xacro",
                ),
                " use_sim:=False"
            ]
        ),
        value_type=str,
    )
    
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
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true'),
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner
    ])
