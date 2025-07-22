import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                os.path.join(
                    get_package_share_directory("my_robot_description"),
                    "urdf",
                    "my_main_robot.urdf.xacro",
                ),
                " use_sim:=false"
            ]
        ),
        value_type=str,
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description, "use_sim_time": use_sim_time}],
    )

    rplidar_c1_params = os.path.join(get_package_share_directory('my_robot_description'),'config','rplidar_c1.yaml')
    rplidar_c1 = Node(
            package='sllidar_ros2',
            executable='sllidar_node',
            name='sllidar_node',
            parameters=[rplidar_c1_params],
            output='screen')

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'use_sim_time',
                default_value='false',
            ),
            robot_state_publisher_node,
            rplidar_c1,
        ]
    )
