# setup.py - the build recipe for the avros_ml Python package.
#
# What it does, in plain words:
#   * Lists the Python code to install (everything under avros_ml/).
#   * Copies launch files, YAML configs and model specs into the ROS install folder
#     so that `ros2 launch avros_ml ...` and get_package_share_directory() can find them.
#   * Registers the "console scripts": the commands you run with `ros2 run avros_ml <name>`.
#     Add a line to `entry_points` whenever you add a new node.

import os
from glob import glob

from setuptools import find_packages, setup

package_name = "avros_ml"


def tree(src_dir, dest_dir):
    """Collect every file under src_dir (recursively) so nested config folders get installed."""
    out = {}
    for path in glob(os.path.join(src_dir, "**", "*"), recursive=True):
        if os.path.isfile(path):
            target = os.path.join(dest_dir, os.path.relpath(os.path.dirname(path), src_dir))
            out.setdefault(os.path.normpath(target), []).append(path)
    return list(out.items())


data_files = [
    ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
    ("share/" + package_name, ["package.xml"]),
    (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
]
data_files += tree("config", os.path.join("share", package_name, "config"))
data_files += tree("models", os.path.join("share", package_name, "models"))

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=data_files,
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Freeman",
    maintainer_email="fyiu@cpp.edu",
    description="Perception, imitation learning and safety arbitration for AVROS.",
    license="TODO",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "rgbt_fusion_node = avros_ml.nodes.rgbt_fusion_node:main",
            "detector_node = avros_ml.nodes.detector_node:main",
            "il_node = avros_ml.nodes.il_node:main",
            "arbiter_node = avros_ml.nodes.arbiter_node:main",
            "actuator_node = avros_ml.nodes.actuator_node:main",
            "perception_main = avros_ml.nodes.perception_main:main",
            "bag_to_dataset = avros_ml.tools.bag_to_dataset:main",
            "export_torchscript = avros_ml.tools.export_torchscript:main",
        ],
    },
)
