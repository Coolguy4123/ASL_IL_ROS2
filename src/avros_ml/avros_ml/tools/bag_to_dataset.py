# tools/bag_to_dataset.py
#
# Converts a rosbag2 recording (from record_demo.launch.py) into training data for the TCN.
#
# What it will do:
#   * Read /perception/rgbt, /odom/filtered and /cmd_vel from the bag.
#   * Resample everything onto a fixed grid at the policy rate (20 Hz, dt = 0.05 s), matching
#     il_node exactly. A policy trained at one rate and run at another misjudges speeds.
#   * Keep only MANUAL-mode segments (/autonomous_mode == False); human driving is the label.
#   * Write sequences of (frames, speeds, human command) as PyTorch tensors/shards, plus a
#     model.yaml skeleton with the right history and dt.
#
# Usage (once implemented):  ros2 run avros_ml bag_to_dataset <bag_dir> <out_dir>

import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert a rosbag2 demo recording to a training dataset.")
    parser.add_argument("bag_dir")
    parser.add_argument("out_dir")
    parser.add_argument("--rate", type=float, default=20.0)
    parser.parse_args(argv)
    raise NotImplementedError("TODO: implement bag reading, resampling and export")


if __name__ == "__main__":
    main()
