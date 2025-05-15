from os.path import join

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from launch.actions import AppendEnvironmentVariable



def generate_launch_description():
    
    ''' If you'd like to control the robot with the keyboard, run teleop_twist_keyboard node from package with the same name
        If you'd like to control the robot with a joystick instead of the keyboard, launch teleop_joy.launch.py'''

    twist_mux_params = os.path.join(get_package_share_directory('my_robot_description'),'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params, {'use_sim_time': True}],
            remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
        )

    gazebo_params_file = join(get_package_share_directory('my_robot_description'), 'config', 'gazebo_params.yaml')
    
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
             )
    
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_main_robot'])

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )


    return LaunchDescription([
        AppendEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=join(get_package_share_directory('my_robot_description'), "models")),
        #joystick,
        twist_mux,
        #gazebo,
        #spawn_entity,
        diff_drive_spawner,
        joint_broad_spawner
    ])
