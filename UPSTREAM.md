# Upstream

- Original URL: https://github.com/CardiffUniversityComputationalRobotics/esc-nav-stack
- Base SHA: `c67d74ab13b893547a98b5e6cc2e310ffe28b28f` (Cardiff `humble-devel`)
- Licence: **MIT**. Root [LICENSE](LICENSE) is the upstream file (copyright 2021 Steven A. Silva). Package `package.xml` files declare MIT. `esc_move_base_control/LICENSE` is the upstream MIT body without that copyright line.
- Date inspected: 2026-09-06

## External dependencies (not vendored)

- **pedsim_msgs** — mapper and planner subscribe `AgentStates`. Source: [stephenadhi/pedsim_ros](https://github.com/stephenadhi/pedsim_ros) (`humble`). Licence: BSD in that package’s `package.xml`. This repository does **not** vendor the messages.

## Divergence summary

Relative to `c67d74a`:

- ROS 2 Jazzy port: control `setup.py` installs share YAML and launch; mapping/planning CMake `find_package` extras and share install; `world_modeler.hpp` uses Jazzy `.hpp` headers and PCL transforms.
- Offline OcTree path builds a GridMap before `/get_grid_map`; live laser is always subscribed; `comfort` is rebuilt to match `full`.
- `/cmd_vel` publisher is BEST_EFFORT; transient Fast DDS `RCLError` skips the tick instead of killing the node.
- Planner `isValid` checks matrix index bounds and falls back if comfort size ≠ obstacle size. An **empty** obstacle matrix still returns valid (`true`) — that is freeze behaviour, not fail-closed.

## Known freeze deltas

These paths differ from the patched freeze working tree on purpose:

- `esc_move_base_mapping/package.xml` now declares `cv_bridge`, `visualization_msgs`, `sensor_msgs`, `std_srvs`, and `message_filters` (already `find_package`’d in CMake).
- ROS 2 `*.launch.py` next to the historical ROS 1 XML. Control `setup.py` still lists only the XML (freeze blob); mapping and planning CMake install the whole `launch/` directory.
- [README.md](README.md) keeps the Cardiff text and adds a short Jazzy note below.
- This file, `pytest.ini`, and `tests/` (ROS interface / lifecycle contracts; no Isaac Sim).
