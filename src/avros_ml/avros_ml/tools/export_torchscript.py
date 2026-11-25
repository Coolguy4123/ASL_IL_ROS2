# tools/export_torchscript.py
#
# Turns a trained PyTorch checkpoint into the file the robot loads, plus its spec:
#   * TCN policy  -> TorchScript .pt (torch.jit.trace), in FP16-friendly form
#   * YOLO        -> use the Ultralytics export to ONNX/TensorRT instead, then build the
#                    .engine ON the Jetson Orin (see models/README.md)
#
# What it will do for the TCN: load the checkpoint, build example inputs from the sizes in
# the spec (image HxWx4, history, odometry state), trace, sanity-check that the traced
# model gives the same outputs as the original, and save <name>.pt next to a model.yaml.
#
# Usage (once implemented):  ros2 run avros_ml export_torchscript <checkpoint> <out_dir>

import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export a trained policy to TorchScript.")
    parser.add_argument("checkpoint")
    parser.add_argument("out_dir")
    parser.parse_args(argv)
    raise NotImplementedError("TODO: implement tracing and verification")


if __name__ == "__main__":
    main()
