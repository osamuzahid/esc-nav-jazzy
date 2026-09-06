"""Mapper offline-octomap and planner validity freeze contracts (no Isaac)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELER = ROOT / "esc_move_base_mapping" / "src" / "world_modeler.cpp"
VALIDITY = (
    ROOT
    / "esc_move_base_planning"
    / "src"
    / "state_validity_checker_grid_map_R2.cpp"
)


def test_offline_octomap_builds_grid_before_service() -> None:
    text = MODELER.read_text(encoding="utf-8")
    ctor, _, rest = text.partition("WorldModeler::WorldModeler()")
    body, _, _ = rest.partition("void WorldModeler::laserScanCallback")
    assert "if (offline_octomap_path_.size() > 0)" in body
    assert "defineSocialGridMap();" in body
    assert body.find("defineSocialGridMap();") < body.find(
        'create_service<grid_map_msgs::srv::GetGridMap>'
    )


def test_live_laser_always_subscribed() -> None:
    text = MODELER.read_text(encoding="utf-8")
    assert "always subscribe to laser" in text
    assert "laser_scan_mn_->registerCallback(&WorldModeler::laserScanCallback, this);" in text
    laser_cb = text.split("void WorldModeler::laserScanCallback", 1)[1]
    assert "defineSocialGridMap();" in laser_cb.split("void WorldModeler::", 1)[0]


def test_comfort_rebuilt_to_match_full() -> None:
    text = MODELER.read_text(encoding="utf-8")
    fn = text.split("void WorldModeler::defineSocialGridMap()", 1)[1]
    assert 'grid_map_.erase("comfort")' in fn
    assert 'grid_map_.add("comfort")' in fn
    assert "comfort_grid_map.rows() != full_grid_map.rows()" in fn


def test_planner_index_bounds_empty_grid_still_valid() -> None:
    text = VALIDITY.read_text(encoding="utf-8")
    assert "bool matrixIndexInBounds(const grid_map::Matrix &m, const grid_map::Index &index)" in text
    assert "if (!matrixIndexInBounds(obstacles_grid_map_, index))" in text
    assert "if (grid_map_.getIndex(query, index) && matrixIndexInBounds(comfort_grid_map_, index))" in text
    assert "if (obstacles_grid_map_.size() == 0)" in text
    empty = text.split("if (obstacles_grid_map_.size() == 0)", 1)[1]
    assert "return true;" in empty.split("}", 1)[0]
    assert "return false;" not in empty.split("}", 1)[0]


def matrix_index_in_bounds(rows: int, cols: int, size: int, i: int, j: int) -> bool:
    """Same predicate as the C++ helper (rows/cols unused when size is 0)."""
    return size > 0 and i >= 0 and j >= 0 and i < rows and j < cols


def test_matrix_index_in_bounds_predicate() -> None:
    assert not matrix_index_in_bounds(0, 0, 0, 0, 0)
    assert matrix_index_in_bounds(4, 4, 16, 0, 0)
    assert matrix_index_in_bounds(4, 4, 16, 3, 3)
    assert not matrix_index_in_bounds(4, 4, 16, 4, 0)
    assert not matrix_index_in_bounds(4, 4, 16, -1, 0)
