from os.path import join

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([join(
                    get_package_share_directory('my_robot_bringup'),'launch','joystick.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items())


    return LaunchDescription([
        joystick
    ])