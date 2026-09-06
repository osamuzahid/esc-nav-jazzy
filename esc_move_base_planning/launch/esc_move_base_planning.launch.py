"""ROS 2 launch for the ESC planner.

Loads share YAML. Goals are PoseStamped on query_goal (Goto2D server is
commented out upstream). The ROS 1 XML in this directory is historical.
"""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    share = Path(get_package_share_directory("esc_move_base_planning"))
    params = share / "config" / "esc_move_base_planning.yaml"
    return LaunchDescription(
        [
            Node(
                package="esc_move_base_planning",
                executable="esc_move_base_planner",
                name="esc_move_base_planner",
                output="screen",
                parameters=[str(params)],
            )
        ]
    )
