"""Load ROS 2 launch stubs without Isaac (skipped if launch_ros is absent)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_launch(path: Path, monkeypatch: pytest.MonkeyPatch, share: Path):
    pytest.importorskip("launch")
    pytest.importorskip("launch_ros")
    ament = pytest.importorskip("ament_index_python.packages")
    monkeypatch.setattr(
        ament, "get_package_share_directory", lambda _name: str(share)
    )
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = mod
    spec.loader.exec_module(mod)
    return mod.generate_launch_description()


def _first_node(ld):
    nodes = [
        e
        for e in ld.entities
        if getattr(e, "node_package", None) is not None
    ]
    assert nodes, ld.entities
    return nodes[0]


@pytest.mark.parametrize(
    "rel,pkg,exe,yaml_name",
    [
        (
            "esc_move_base_control/launch/esc_move_base_control.launch.py",
            "esc_move_base_control",
            "base_controller",
            "esc_move_base_control.yaml",
        ),
        (
            "esc_move_base_mapping/launch/esc_move_base_mapping.launch.py",
            "esc_move_base_mapping",
            "esc_move_base_mapper",
            "esc_move_base_mapping.yaml",
        ),
        (
            "esc_move_base_planning/launch/esc_move_base_planning.launch.py",
            "esc_move_base_planning",
            "esc_move_base_planner",
            "esc_move_base_planning.yaml",
        ),
    ],
)
def test_launch_description_nodes(monkeypatch, tmp_path, rel, pkg, exe, yaml_name):
    share = tmp_path / "share"
    (share / "config").mkdir(parents=True)
    (share / "config" / yaml_name).write_text("# test\n", encoding="utf-8")
    ld = _load_launch(ROOT / rel, monkeypatch, share)
    node = _first_node(ld)
    assert node.node_package == pkg
    assert node.node_executable == exe
