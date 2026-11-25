# arbiter_node.py
#
# The safety brain. The ML nodes only propose; this node decides what the wheels really get,
# and it is the only node allowed to publish /cmd_vel.
#
#   Listens to:  /il/cmd_vel, /perception/detections, /rgb/camera_info, teleop commands
#   Publishes:   /cmd_vel (steady 20 Hz, always, even when the answer is "stop"),
#                /autonomous_mode (so other nodes know who is driving)
#
# How it will work, every 20 Hz tick:
#   * Check that inputs are fresh. If the imitation-learning command has gone quiet, stop.
#   * Keep track of the mode: MANUAL (human drives), AUTONOMOUS (the model drives, with
#     safety checks), or SAFE_STOP (stopped until someone deliberately resets it).
#   * If a person or vehicle is detected ahead, estimate how far away it is from where it
#     touches the ground in the image, and limit the speed so the robot can stop in time.
#   * Reject nonsense commands (NaN), cap the top speed, and limit how quickly the speed
#     may change, so a jumpy model can never cause a jerky or dangerous motion.
#
# It should run in its own process, away from the heavy ML code, so a slow neural network
# can never delay the safety loop.
