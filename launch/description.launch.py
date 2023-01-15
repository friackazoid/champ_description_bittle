import os

import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")
    #description_path = LaunchConfiguration("description_path")

    declare_use_sim_time = DeclareLaunchArgument("use_sim_time", default_value="false", description="Use simulation (Gazebo) clock if true")

    pkg_share = launch_ros.substitutions.FindPackageShare(package="champ_description_bittle").find("champ_description_bittle")

    #declare_description_path = DeclareLaunchArgument(name="description_path", default_value=default_model_path, description="Absolute path to robot urdf file")
    urdf = os.path.join(get_package_share_directory('champ_description_bittle'), 'urdf/bittle.urdf')
    with open(urdf, 'r') as f:
        robot_description = f.read()

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {"robot_description": robot_description},
            {"use_tf_static": False},
            {"publish_frequency": 200.0},
            {"ignore_timestamp": True},
            {'use_sim_time': use_sim_time}
        ],
        # remappings=(("robot_description", "robot_description")),
    )

    return LaunchDescription(
        [
            #declare_description_path,
            declare_use_sim_time,
            robot_state_publisher_node,
        ]
    )
