# detector_node.py
#
# Finds objects (people, vehicles, ...) in the fused RGB-T image using the YOLO model.
#
#   Listens to:  /perception/rgbt
#   Publishes:   /perception/detections  (vision_msgs/Detection2DArray, about 15-20 Hz)
#
# How it will work:
#   * The model is loaded by name from the ML_Models package (set by a ROS parameter), so
#     swapping the detector never requires changing this file.
#   * It only ever works on the NEWEST frame. If the model is slower than the camera, old
#     frames are dropped instead of piling up and making the robot react to the past.
#   * Each detection message keeps the timestamp of the image it came from, so other nodes
#     can tell how old it is.
#   * It reports when the model is loaded and warmed up, so the arbiter knows it is safe to
#     allow autonomous driving.
