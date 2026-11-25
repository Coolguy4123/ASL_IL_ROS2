# actuator_node.py
#
# The bridge between ROS and the robot's motors: takes the arbiter's final velocity command
# and drives the wheels, and reports how the wheels actually moved.
#
#   Listens to:  /cmd_vel, /autonomous_mode
#   Publishes:   /wheel_odom  (wheel odometry, 50 Hz)
#
# How it will work:
#   * Convert the commanded speed and turn rate into whatever the motor controller expects.
#   * Its own safety timeout: if no new /cmd_vel arrives for a short time, stop the motors.
#     This must work even if the arbiter itself has crashed.
#   * Publish odometry from the wheel encoders so the EKF can use it.
#
# If the robot base already comes with its own ROS 2 driver, this file can become a thin
# wrapper around it. A hardware emergency stop that cuts motor power, independent of ROS,
# is still needed.
