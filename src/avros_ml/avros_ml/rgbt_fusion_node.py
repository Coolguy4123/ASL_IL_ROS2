# rgbt_fusion_node.py
#
# Glues the RGB camera and the thermal camera into ONE 4-channel image (B, G, R, T) so the
# detector and the imitation-learning policy can look at both at once.
#
#   Listens to:  /rgb/image_raw, /rgb/camera_info, /thermal/image_raw, /thermal/camera_info
#   Publishes:   /perception/rgbt  (sensor_msgs/Image, 8UC4, about 15-20 Hz)
#
# How it will work:
#   * The RGB camera is the master clock: every time an RGB frame arrives, pair it with the
#     thermal frame closest in time.
#   * If no thermal frame is close enough, either skip the frame, fill the thermal channel
#     with zeros, or reuse the last thermal frame (chosen by a parameter).
#   * Line the thermal image up with the RGB image (using the camera calibration), squash
#     the 16-bit thermal values into 8 bits with a fixed window, and stack the four channels.
#   * Publish with the RGB frame's timestamp so everything downstream can measure latency.
