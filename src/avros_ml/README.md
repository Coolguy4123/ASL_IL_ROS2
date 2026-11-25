# avros_ml

Perception (RGB-T fusion + YOLO), imitation learning (TCN) and a safety arbiter for the
AVROS robot, as one ROS 2 (Humble) `ament_python` package for a Jetson AGX Orin.

## Layout

| Path | What it is |
|---|---|
| `avros_ml/nodes/` | The ROS nodes: fusion, detector, il, arbiter, actuator, and `perception_main` (fusion+detector+il in one process) |
| `avros_ml/models/` | Plug-and-play model layer: `base.py` interfaces, `registry.py`, TorchScript/TensorRT backends, dummy models |
| `avros_ml/fusion/` | ROS-free image maths for RGB-T fusion |
| `avros_ml/safety/` | ROS-free arbiter rules: state machine, hazard distance, limiters |
| `avros_ml/utils/` | QoS profiles, image<->numpy (no cv_bridge), latest-frame slot, latency monitor |
| `avros_ml/tools/` | Bag -> dataset and model export helpers |
| `config/` | Node parameters, OpenVINS config, EKF config, calibration files |
| `launch/` | `bringup`, `drivers`, `localization`, `perception`, `safety`, `record_demo`, `replay_bag` |
| `models/` | Weights + `model.yaml` specs (weights are git-ignored) |
| `test/` | Unit and launch tests |

## Build

```bash
cd ~/VS_Code/ASL_IL_ROS2
colcon build --packages-select avros_ml --symlink-install
source install/setup.bash
ros2 launch avros_ml bringup.launch.py
```

## Jetson setup notes (not handled by rosdep)

- Install PyTorch from NVIDIA's Jetson wheels (JetPack 6), not PyPI.
- Use JetPack's OpenCV; do not `pip install opencv-python` over it.
- Build TensorRT engines on the Orin itself.
- Ultralytics YOLO is AGPL-3.0: check licensing before shipping.

## Status

Skeleton only. See the `TODO` markers; each file's header comment says what it will do.
