import os
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import (
        DeclareLaunchArgument,
        IncludeLaunchDescription
)

from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    #descr_pkg_share = launch_ros.substitutions.FindPackageShare(
    #        package="champ_description_bittle"
    #        ).find("champ_description_bittle")
    rviz_config = os.path.join(get_package_share_directory("champ_description_bittle"),"rviz", "urdf_viewer.rviz")
    #default_model_path = os.path.join(get_package_share_directory("champ_description_bittle"), "urdf", "bittle.urdf")

    declare_use_sim_time = DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use simulation (Gazebo) clock if true",
        )
#    declare_description_path = DeclareLaunchArgument(
#            name="description_path",
#            default_value=default_model_path,
#            description="Absolute path to robot urdf file",
#        )

    declare_rviz = DeclareLaunchArgument(
            "rviz", default_value="true", description="Launch rviz"
    )

    declare_rviz_ref_frame = DeclareLaunchArgument(
        "rviz_ref_frame", default_value="base-frame-link", description="Rviz ref frame"
    )

    declare_base_link_frame = DeclareLaunchArgument(
            "base_link_frame", default_value="base-frame-link",
            description="Base link frame"
    )

    declare_publish_joint_states = DeclareLaunchArgument(
            "publish_joint_states",
            default_value="false",
            description="Publish joint control",
    )

    declare_publish_joint_states_gui = DeclareLaunchArgument(
            "publish_joint_states_gui",
            default_value="true",
            description="Publish joint control with GUI",
    )

    description_ld = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory("champ_description_bittle"),
                    "launch",
                    "description.launch.py",
                )
            ),
            launch_arguments={
                "use_sim_time": LaunchConfiguration("use_sim_time"),
                #"description_path":  LaunchConfiguration("description_path"),
            }.items(),
    )


    node_joint_state_publisher = Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            condition=IfCondition(LaunchConfiguration("publish_joint_states"))
        )

    node_joint_state_publisher_gui = Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            condition=IfCondition(LaunchConfiguration("publish_joint_states_gui"))
        )

    rviz2 = Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
            arguments=[
                '-d', rviz_config,
                '-f', LaunchConfiguration("rviz_ref_frame")
            ],
            condition=IfCondition(LaunchConfiguration("rviz"))
    )

    return LaunchDescription (
            [
                declare_use_sim_time,
                #declare_description_path,
                declare_rviz,
                declare_rviz_ref_frame,
                declare_base_link_frame,
                declare_publish_joint_states,
                declare_publish_joint_states_gui,
                node_joint_state_publisher,
                node_joint_state_publisher_gui,
                description_ld,
                rviz2
            ]
        )
