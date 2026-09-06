"""ESC ROS interface contracts (no Isaac Sim)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_path2d_msg_waypoints() -> None:
    text = _read("esc_move_base_msgs/msg/Path2D.msg")
    assert "geometry_msgs/Pose2D[] waypoints" in text


def test_goto2d_action_idl() -> None:
    text = _read("esc_move_base_msgs/action/Goto2D.action")
    goal, result, _feedback = text.split("---")
    assert "geometry_msgs/Pose2D goal" in goal
    assert "bool success" in result


def test_query_goal_is_posestamped_goto2d_server_commented() -> None:
    src = _read("esc_move_base_planning/src/planning_framework_main.cpp")
    assert (
        "create_subscription<geometry_msgs::msg::PoseStamped>(query_goal_topic_"
        in src
    )
    assert "void OnlinePlannFramework::queryGoalCallback" in src
    assert "// goto_action_server_ = new EscBaseGoToActionServer(" in src
    assert "// goto_action_server_->start();" in src


def test_historical_ros1_launch_still_present() -> None:
    for rel in (
        "esc_move_base_control/launch/esc_move_base_control.launch",
        "esc_move_base_mapping/launch/esc_move_base_mapping.launch",
        "esc_move_base_planning/launch/esc_move_base_planning.launch",
    ):
        xml = _read(rel)
        assert "<launch>" in xml
        assert "$(find " in xml


def test_ros2_launch_py_wraps_existing_nodes() -> None:
    expected = {
        "esc_move_base_control/launch/esc_move_base_control.launch.py": (
            "esc_move_base_control",
            "base_controller",
        ),
        "esc_move_base_mapping/launch/esc_move_base_mapping.launch.py": (
            "esc_move_base_mapping",
            "esc_move_base_mapper",
        ),
        "esc_move_base_planning/launch/esc_move_base_planning.launch.py": (
            "esc_move_base_planning",
            "esc_move_base_planner",
        ),
    }
    banned = (
        "isaac",
        "_hop.sh",
        "qos_relay",
        "stretch",
        "reachy",
        "/home/osamuzahid",
    )
    for rel, (pkg, exe) in expected.items():
        text = _read(rel)
        assert f'package="{pkg}"' in text
        assert f'executable="{exe}"' in text
        assert "esc_move_base_" in rel and "config" in text
        lowered = text.lower()
        for token in banned:
            assert token not in lowered, f"{rel} contains {token!r}"


def test_mapping_package_xml_declares_cmake_extras() -> None:
    text = _read("esc_move_base_mapping/package.xml")
    for dep in (
        "cv_bridge",
        "visualization_msgs",
        "sensor_msgs",
        "std_srvs",
        "message_filters",
    ):
        assert f"<depend>{dep}</depend>" in text


def test_no_vendored_pedsim_or_lab_home() -> None:
    assert not (ROOT / "pedsim_msgs").exists()
    assert not (ROOT / "patches").exists()
    needle = "/home/" + "osamuzahid"
    hits = []
    skip_parts = {".git", "tests"}
    for path in ROOT.rglob("*"):
        if skip_parts.intersection(path.parts) or not path.is_file():
            continue
        if path.suffix in {".png", ".bt", ".dae", ".usd"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if needle in text:
            hits.append(str(path.relative_to(ROOT)))
    assert hits == []
