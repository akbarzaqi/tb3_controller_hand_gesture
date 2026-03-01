#!/usr/bin/env python3

import rospy 
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge 
import cv2

def publish_message():

   img_pub = rospy.Publisher('/image', Image, queue_size=10)
   rospy.init_node('camera', anonymous=True) 
   rate = rospy.Rate(10) # 10hz 
   cap = cv2.VideoCapture(0)
   cv_br = CvBridge()

   while not rospy.is_shutdown(): 
      ret, frame = cap.read()
      if ret == True: 
         rospy.loginfo('publishing image') 
         img_pub.publish(cv_br.cv2_to_imgmsg(frame)) 
      rate.sleep()

if __name__ == '__main__':
   try:
      publish_message()
   except rospy.ROSInterruptException:
      pass