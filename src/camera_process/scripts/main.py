#!/usr/bin/env python3

# author : Akbar Zaqi Fiktarizaen
# 2026

import rospy 
from camera_process.msg import Message
from geometry_msgs.msg import Twist

velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def move(speed, distance, isForward):
   vel_msg = Twist()

   if isForward:
      vel_msg.linear.x = abs(speed)
   else:
      vel_msg.linear.x = -abs(speed)

   vel_msg.linear.y = 0
   vel_msg.linear.z = 0
   vel_msg.angular.x = 0
   vel_msg.angular.y = 0
   vel_msg.angular.z = 0
   
   rospy.loginfo(f"publishing movement command: {vel_msg}")

   time_out = rospy.Time.now().to_sec()
   current_distance = 0.0
   rospy.loginfo(f"start time: {time_out}")

   while current_distance < distance:
      velocity_publisher.publish(vel_msg)
      current_time = rospy.Time.now().to_sec()
      current_distance = speed * (current_time - time_out)
      # rospy.spin_once()
      # rospy.Rate(10).sleep()
      rospy.loginfo(f"current time: {current_time}, current distance: {current_distance}")

   vel_msg.linear.x = 0
   velocity_publisher.publish(vel_msg)

def rotate(angular_speed, relative_angle, clockwise):
   vel_msg = Twist()

   vel_msg.linear.x = 0
   vel_msg.linear.y = 0
   vel_msg.linear.z = 0
   vel_msg.angular.x = 0
   vel_msg.angular.y = 0

   if clockwise:
      vel_msg.angular.z = -abs(angular_speed)
   else:
      vel_msg.angular.z = abs(angular_speed)
   
   rospy.loginfo(f"publishing rotation command: {vel_msg}")
   time_out = rospy.Time.now().to_sec()
   current_angle = 0.0
   

   while current_angle < relative_angle:
      velocity_publisher.publish(vel_msg)
      current_time = rospy.Time.now().to_sec()
      current_angle = angular_speed * (current_time - time_out)
      # rospy.spin_once()
      # rospy.Rate(10).sleep()
      
      rospy.loginfo(f"current time: {current_time}, current angle: {current_angle}")

   vel_msg.angular.z = 0
   velocity_publisher.publish(vel_msg)

def angle_to_radians(angle):
   return angle * 3.141592653589793 / 180.0


def driver_process():
   global speed, distance, isForward, angular_speed, relative_angle, clockwise
   
   if g_state == "forward":
      speed = 0.3
      distance = 0.01
      isForward = True
      angular_speed = 0
      relative_angle = 0
      clockwise = True
      move(speed, distance, isForward)
      rotate(angle_to_radians(angular_speed), angle_to_radians(relative_angle), clockwise)
   elif g_state == "stop":
      speed = 0.0
      distance = 0.0
      isForward = False
      angular_speed = 0.0
      relative_angle = 0
      clockwise = False
      move(speed, distance, isForward)
      rotate(angle_to_radians(angular_speed), angle_to_radians(relative_angle), clockwise)

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