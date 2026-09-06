"""Controller /cmd_vel QoS and skip-tick contract (no Isaac Sim)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTRL = (
    ROOT
    / "esc_move_base_control"
    / "esc_move_base_control"
    / "base_controller.py"
)


def test_cmd_vel_best_effort_and_rclerror_skip() -> None:
    text = CTRL.read_text(encoding="utf-8")
    assert "from rclpy._rclpy_pybind11 import RCLError" in text
    assert "ReliabilityPolicy.BEST_EFFORT" in text
    assert "DurabilityPolicy.VOLATILE" in text
    assert "def _publish_cmd_vel(self, twist: Twist) -> None:" in text
    assert "except RCLError:" in text
    assert "self.control_output_pub_.publish(twist)" in text
    assert "self._publish_cmd_vel(Twist())" in text
    assert "self._publish_cmd_vel(control_input)" in text
    assert "self.control_output_pub_.publish(control_input)" not in text


def test_controller_main_lifecycle() -> None:
    text = CTRL.read_text(encoding="utf-8")
    assert "def main(args=None):" in text
    assert "rclpy.init(args=args)" in text
    assert "controller_node = Controller()" in text
    assert "rclpy.spin(controller_node)" in text
    assert "controller_node.destroy_node()" in text
    assert "rclpy.shutdown()" in text
