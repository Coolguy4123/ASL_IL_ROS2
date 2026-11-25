# fusion/thermal_warp.py
#
# Pure image maths for the fusion node: take a thermal frame and make it line up
# pixel-for-pixel with the RGB frame, then stack them into one 4-channel image.
#
# What it will do:
#   * build_warp_map(): once at startup, from RGB intrinsics + thermal intrinsics +
#     RGB<->thermal extrinsics (or a hand-measured homography), precompute a cv2.remap map.
#   * thermal_to_8bit(): convert mono16 thermal to 8 bits with a FIXED temperature window
#     (never per-frame min/max, which makes the picture flicker between frames).
#   * stack_rgbt(): return an HxWx4 uint8 array in the order B, G, R, T.
#
# Known limitation: without depth, a homography is only exact at one working distance.

import numpy as np


def build_warp_map(rgb_size, thermal_size, calibration):
    """Return (map_x, map_y) for cv2.remap. TODO: implement from calibration files."""
    raise NotImplementedError


def thermal_to_8bit(thermal16, lo, hi):
    """Clip to [lo, hi] raw counts and scale to 0..255."""
    t = np.clip(thermal16.astype(np.float32), lo, hi)
    return ((t - lo) * (255.0 / max(hi - lo, 1))).astype(np.uint8)


def stack_rgbt(bgr, thermal8):
    """Concatenate a HxWx3 BGR image and a HxW thermal image into HxWx4."""
    return np.dstack([bgr, thermal8])
