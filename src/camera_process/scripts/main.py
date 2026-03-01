#!/usr/bin/env python3

# author : Akbar Zaqi Fiktarizaen
# 2026

import rospy 
from camera_process.msg import Message
from geometry_msgs.msg import Twist

def move(speed, distance, isForward):
   vel_msg = Twist()

   if isForward:
      vel_msg.linear.x = abs(speed)
   else:
      vel_msg.linear.x = -abs(speed)
   
   velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
   rospy.loginfo(f"publishing movement command: {vel_msg}")
   velocity_publisher.publish(vel_msg)

def rotate(angular_speed, relative_angle, clockwise):
   vel_msg = Twist()
   if clockwise:
      vel_msg.angular.z = -abs(angular_speed)
   else:
      vel_msg.angular.z = abs(angular_speed)

   velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
   rospy.loginfo(f"publishing rotation command: {vel_msg}")
   velocity_publisher.publish(vel_msg)

def angle_to_radians(angle):
   return angle * 3.141592653589793 / 180.0


def driver_process():
   global speed, distance, isForward, angular_speed, relative_angle, clockwise
   
   if g_state == "forward":
      speed = 0.5
      distance = 1.0
      isForward = True
      angular_speed = 0.0
      relative_angle = 90
      clockwise = True
      move(speed, distance, isForward)
      rotate(angle_to_radians(angular_speed), relative_angle, clockwise)
   elif g_state == "stop":
      speed = 0.0
      distance = 0.0
      isForward = False
      angular_speed = 0.0
      relative_angle = 0
      clockwise = False
      move(speed, distance, isForward)
      rotate(angle_to_radians(angular_speed), relative_angle, clockwise)

def callback(data):
   global g_state

   rospy.loginfo("receiving frame")
   rospy.loginfo(f"Received message: {data.state}")
   
   g_state = data.state
   rospy.loginfo(f"Current state: {g_state}")
   driver_process()


def receive_message():
   rospy.init_node('driver_process', anonymous=True)
   rospy.Subscriber('state', Message, callback)
   rospy.spin()

   cv2.destroyAllWindows()

if __name__ == '__main__':
   receive_message()