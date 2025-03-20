#!/usr/bin/env python3

import os
import math
import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import WheelsCmdStamped
from time import time

# Define angular velocities for each wheel (in radians per second)
W_LEFT = 8 / 4 * (2 * math.pi)  # Left wheel full rotation per second
W_RIGHT = 8 / 4 * (2 * math.pi)  # Right wheel full rotation per second

class WheelControlNode(DTROS):

    def __init__(self, node_name):
        # Initialize the DTROS parent class
        super(WheelControlNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)

        # Static parameters
        vehicle_name = os.environ['VEHICLE_NAME']
        wheels_topic = f"/{vehicle_name}/wheels_driver_node/wheels_cmd"
        wheel_radius_param = f"/{vehicle_name}/kinematics_node/radius"

        # Get the Duckiebot's wheel radius
        wheel_radius = rospy.get_param(wheel_radius_param)

        # Compute linear speeds based on the wheel radius
        self._vel_left = W_LEFT * wheel_radius
        self._vel_right = W_RIGHT * wheel_radius

        # Construct publisher
        self._publisher = rospy.Publisher(wheels_topic, WheelsCmdStamped, queue_size=1)

        # Track time for controlling movement
        self.start_time = time()

    def drive_straight(self, duration):
        """Drive straight for a specified duration"""
        message = WheelsCmdStamped(vel_left=self._vel_left, vel_right=self._vel_right)
        start_time = time()
        while time() - start_time < duration:
            if rospy.is_shutdown():
                break
            self._publisher.publish(message)
            rospy.Rate(10).sleep()  # Publish at 10 Hz
def turn_right(self, duration):
        """Turn right by rotating the wheels with different velocities"""
        # To turn right, we move the left wheel forward and the right wheel backward
        vel_left = self._vel_left
        vel_right = -self._vel_right
        message = WheelsCmdStamped(vel_left=vel_left, vel_right=vel_right)
        start_time = time()
        while time() - start_time < duration:
            if rospy.is_shutdown():
                break
            self._publisher.publish(message)
            rospy.Rate(10).sleep()  # Publish at 10 Hz

    def run(self):
        """Run the main logic to control the Duckiebot's movement in a square pattern"""
        rate = rospy.Rate(0.1)  # Publish at 0.1 Hz (one command every 10 seconds)

        # The robot needs to move in a square: 4 sides (2 straight + turn right each time)
        num_sides = 4
        side_duration = 3  # Time to drive straight for each side (in seconds)
        turn_duration = 0.7  # Time to turn right (approx. 90 degrees)

        while not rospy.is_shutdown():
            for _ in range(num_sides):
                self.drive_straight(side_duration)  # Drive straight for each side
                self.turn_right(turn_duration)      # Turn right for 90 degrees

            # After 4 sides, stop the robot (optional)
            stop = WheelsCmdStamped(vel_left=0, vel_right=0)
            self._publisher.publish(stop)
            rospy.loginfo("Completed the square path.")
            break  # Exit the loop once the square path is completed

            rate.sleep()

    def on_shutdown(self):
        """Stop the robot on shutdown"""
        stop = WheelsCmdStamped(vel_left=0, vel_right=0)
        self._publisher.publish(stop)

if __name__ == '__main__':
    # Create the node
    node = WheelControlNode(node_name='wheel_control_node')

    # Run the node
    node.run()

    # Keep the process from terminating
    rospy.spin()

