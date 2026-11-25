# utils/image_io.py
#
# Converts between ROS sensor_msgs/Image messages and numpy arrays WITHOUT cv_bridge.
# We avoid cv_bridge because the Humble binary is tied to NumPy 1.x and it copies data.
# Supported encodings: bgr8, rgb8, mono8, mono16, 8UC4, 16UC4.
#
# Things this file takes care of so the nodes don't have to:
#   * Row padding: ROS rows can be longer than width*channels (msg.step); we crop it off.
#   * Endianness for 16-bit images (msg.is_bigendian).
#   * Reading is zero-copy (read-only view). Copy the array yourself if you must edit it.

import numpy as np

# encoding -> (numpy dtype, channels)
_ENCODINGS = {
    "bgr8": (np.uint8, 3),
    "rgb8": (np.uint8, 3),
    "mono8": (np.uint8, 1),
    "mono16": (np.uint16, 1),
    "8UC4": (np.uint8, 4),
    "16UC4": (np.uint16, 4),
}


def imgmsg_to_numpy(msg):
    """Return an HxWxC (or HxW for single channel) numpy view of the image data."""
    if msg.encoding not in _ENCODINGS:
        raise ValueError(f"Unsupported image encoding: {msg.encoding}")
    dtype, ch = _ENCODINGS[msg.encoding]
    dtype = np.dtype(dtype).newbyteorder(">" if msg.is_bigendian else "<")
    flat = np.frombuffer(msg.data, dtype=dtype)
    row_pixels = msg.step // (dtype.itemsize * ch)  # includes any padding
    img = flat.reshape(msg.height, row_pixels, ch)[:, : msg.width, :]
    return img[:, :, 0] if ch == 1 else img


def numpy_to_imgmsg(arr, encoding, header=None):
    """Build a sensor_msgs/Image from a numpy array. Pass `header` to keep the original stamp."""
    from sensor_msgs.msg import Image  # imported here so unit tests can skip ROS

    if encoding not in _ENCODINGS:
        raise ValueError(f"Unsupported image encoding: {encoding}")
    dtype, ch = _ENCODINGS[encoding]
    arr = np.ascontiguousarray(arr, dtype=dtype)
    if arr.ndim == 2:
        arr = arr[:, :, None]
    msg = Image()
    if header is not None:
        msg.header = header
    msg.height, msg.width = int(arr.shape[0]), int(arr.shape[1])
    msg.encoding = encoding
    msg.is_bigendian = 0  # numpy on Jetson (aarch64) and x86 is little-endian
    msg.step = msg.width * ch * np.dtype(dtype).itemsize
    msg.data = arr.tobytes()
    return msg
