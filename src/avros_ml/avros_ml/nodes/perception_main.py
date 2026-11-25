# nodes/perception_main.py
#
# Entry point that runs fusion + detector + il_node together in ONE process.
#
# Why: on the Jetson AGX Orin the CPU and GPU share memory. One process means one CUDA
# context (less RAM and less GPU contention with your other packages) and no DDS hop
# between these three nodes. Launch with `single_process:=false` to run them separately
# (easier for debugging or restarting a single stage).
#
# It creates the three nodes, puts them on one MultiThreadedExecutor, and walks the two
# lifecycle nodes through configure -> activate once their models are loaded.
#
# Note: the arbiter is deliberately NOT in this process (see launch/safety.launch.py).

import rclpy
from rclpy.executors import MultiThreadedExecutor

from avros_ml.nodes.detector_node import DetectorNode
from avros_ml.nodes.il_node import IlNode
from avros_ml.nodes.rgbt_fusion_node import RgbtFusionNode


def main(args=None):
    rclpy.init(args=args)
    nodes = [RgbtFusionNode(), DetectorNode(), IlNode()]
    executor = MultiThreadedExecutor(num_threads=6)
    for n in nodes:
        executor.add_node(n)
    # TODO: trigger configure + activate on the DetectorNode and IlNode (lifecycle)
    try:
        executor.spin()
    finally:
        for n in nodes:
            n.destroy_node()
        rclpy.shutdown()
