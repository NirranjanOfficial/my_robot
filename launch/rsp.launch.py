import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # Use sim time if enabled
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Locate and process the XACRO file
    pkg_path = os.path.join(get_package_share_directory('my_artibot'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    
    # Robot description parameters
    robot_description = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}

    # Node: robot_state_publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # Node: joint_state_publisher
    node_joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )

    # Launch description
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'
        ),
        node_joint_state_publisher,
        node_robot_state_publisher
    ])
