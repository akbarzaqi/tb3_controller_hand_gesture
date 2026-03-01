#!/usr/bin/env python3

# author : Akbar Zaqi Fiktarizaen
# 2026

import rospy 
from sensor_msgs.msg import Image 
from camera_process.msg import Message
from cv_bridge import CvBridge 
import cv2 
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def if_fist(hand_landmarks):
    fingers = [
        (8, 6),  
        (12, 10), 
        (16, 14), 
        (20, 18)  
    ]

    count = 0

    for tip, pip in fingers:
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
            count += 1
    
    if count == 4:
        return True
    
    return False

def if_open(hand_landmarks):
   fingers = [
      (4, 2),
      (8, 6),
      (12, 10),
      (16, 14),
      (20, 18)
   ]
   rospy.loginfo("Checking if hand is open")
   count1 = 0
   for tip, pip in fingers:
      if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
         count1 += 1

   if count1 == 5:
      return True
   return False

def process(frame):
   # Hiển thị hình ảnh
   # rospy.loginfo("camera process")
   state = "no detection"
   with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

         frame.flags.writeable = False
         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         results = hands.process(frame)

         # Draw the hand annotations on the frame.
         frame.flags.writeable = True
         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
         
         if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
               # rospy.loginfo("Hand landmarks detected")

               if if_fist(hand_landmarks):
                     # rospy.loginfo("Tangan menggenggam")
                     cv2.putText(frame, 'Tangan menggenggam', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                     state = "stop"
               elif if_open(hand_landmarks):
                     rospy.loginfo("Tangan terbuka")
                     state = "forward"
                     cv2.putText(frame, 'Tangan terbuka', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

         
               mp_drawing.draw_landmarks(
                     frame,
                     hand_landmarks,
                     mp_hands.HAND_CONNECTIONS,
                     mp_drawing_styles.get_default_hand_landmarks_style(),
                     mp_drawing_styles.get_default_hand_connections_style())

         publish_message(state)

         imList = []
         if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                  for i in range(21):
                     x = hand_landmarks.landmark[i].x
                     y = hand_landmarks.landmark[i].y
                     # rospy.loginfo(f"Landmark {i}: ({x}, {y})")
                     imList.append((x, y))
   cv2.imshow("camera", frame) 
   cv2.waitKey(1)

def publish_message(message):
   pub = rospy.Publisher('state', Message, queue_size=10)
   rospy.loginfo(f"Publishing message: {message}")
   if not rospy.is_shutdown():
      msg = Message()
      msg.state = message
      pub.publish(msg)


def callback(data):
   cv_br = CvBridge()
   rospy.loginfo("receiving frame")
   current_frame = cv_br.imgmsg_to_cv2(data)
   process(current_frame)


def receive_message():
   rospy.init_node('hand_gesture', anonymous=True)
   rospy.Subscriber('image', Image, callback)
   rospy.spin()

   cv2.destroyAllWindows()

if __name__ == '__main__':
   receive_message()