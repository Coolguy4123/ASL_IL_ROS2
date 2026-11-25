# test/test_image_io.py
# Checks that images survive the numpy <-> sensor_msgs/Image round trip without cv_bridge,
# including rows that have padding (msg.step larger than width * channels).

import numpy as np
from sensor_msgs.msg import Image

from avros_ml.utils.image_io import imgmsg_to_numpy, numpy_to_imgmsg


def test_roundtrip_8uc4():
    arr = np.random.randint(0, 255, (4, 6, 4), dtype=np.uint8)
    out = imgmsg_to_numpy(numpy_to_imgmsg(arr, "8UC4"))
    assert np.array_equal(arr, out)


def test_roundtrip_mono16():
    arr = np.random.randint(0, 65535, (4, 6), dtype=np.uint16)
    out = imgmsg_to_numpy(numpy_to_imgmsg(arr, "mono16"))
    assert np.array_equal(arr, out)


def test_row_padding_is_cropped():
    msg = Image(height=2, width=3, encoding="mono8", step=5)
    msg.data = bytes([1, 2, 3, 99, 99, 4, 5, 6, 99, 99])
    assert np.array_equal(imgmsg_to_numpy(msg), [[1, 2, 3], [4, 5, 6]])
