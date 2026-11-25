# safety/hazard_distance.py
#
# Turns YOLO detections into "how far away is the nearest thing in my way?" using the
# RGB camera intrinsics and the camera's mounting height. This is what lets the arbiter
# slow down for a person or obstacle even though we have no depth sensor.
#
# Idea: for an object standing on flat ground, the lower its bottom edge appears in the
# image, the closer it is:   distance ~= fy * camera_height / (v_bottom - cy)
# (corrected for camera pitch if the camera is tilted). Horizontal bearing is
# atan((u - cx) / fx); only objects inside a forward corridor matter.
#
# This is a rough estimate, so margins should be conservative. Only configured hazard
# classes (person, vehicle, ...) are considered.

import math


def hazard_distance(detections, intrinsics, cam_height_m, cam_pitch_rad,
                    hazard_classes, corridor_half_angle_rad, min_score):
    """Return the nearest hazard distance in metres, or None if nothing is in the way.

    TODO: implement the ground-plane projection described above.
    """
    raise NotImplementedError


def speed_limit_for_distance(distance_m, d_stop_m, brake_decel):
    """Fastest speed from which we can still stop before d_stop: v = sqrt(2*a*(d - d_stop))."""
    return math.sqrt(max(0.0, 2.0 * brake_decel * (distance_m - d_stop_m)))
