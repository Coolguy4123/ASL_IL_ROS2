# il_node.py
#
# The imitation-learning "driver": looks at the fused image and the robot's current speed,
# and proposes how the robot should move, copying what a human driver did in the training
# demonstrations (a TCN model from the ML_Models package).
#
#   Listens to:  /perception/rgbt, /odom/filtered, /autonomous_mode
#   Publishes:   /il/cmd_vel  (velocity command, steady 20 Hz)
#
# How it will work:
#   * It runs on a fixed 20 Hz clock, using the newest image and odometry it has, so the
#     command rate stays steady even if a camera frame arrives late.
#   * If the newest image is too old, it stays silent and lets the arbiter's safety timeout
#     take over, rather than driving on stale information.
#   * It remembers a short history of recent frames (the TCN needs this). The history is
#     cleared when autonomous mode switches on and after any gap in the images.
#   * It only feeds the model the robot's speeds, not its position, because position drifts
#     and would not carry over to new places.
#   * Its output only PROPOSES a motion; the arbiter decides what actually reaches the wheels.
