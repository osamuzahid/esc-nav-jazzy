"""ROS 2 launch for the ESC differential controller.

Loads share YAML. The ROS 1 XML in this directory is historical.
"""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    share = Path(get_package_share_directory("esc_move_base_control"))
    params = share / "config" / "esc_move_base_control.yaml"
    return LaunchDescription(
        [
            Node(
                package="esc_move_base_control",
                executable="base_controller",
                name="esc_move_base_controller",
                output="screen",
                parameters=[str(params)],
            )
        ]
    )
