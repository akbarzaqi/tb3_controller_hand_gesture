;; Auto-generated. Do not edit!


(when (boundp 'camera_process::Message)
  (if (not (find-package "CAMERA_PROCESS"))
    (make-package "CAMERA_PROCESS"))
  (shadow 'Message (find-package "CAMERA_PROCESS")))
(unless (find-package "CAMERA_PROCESS::MESSAGE")
  (make-package "CAMERA_PROCESS::MESSAGE"))

(in-package "ROS")
;;//! \htmlinclude Message.msg.html


(defclass camera_process::Message
  :super ros::object
  :slots (_state ))

(defmethod camera_process::Message
  (:init
   (&key
    ((:state __state) "")
    )
   (send-super :init)
   (setq _state (string __state))
   self)
  (:state
   (&optional __state)
   (if __state (setq _state __state)) _state)
  (:serialization-length
   ()
   (+
    ;; string _state
    4 (length _state)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _state
       (write-long (length _state) s) (princ _state s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _state
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _state (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get camera_process::Message :md5sum-) "af6d3a99f0fbeb66d3248fa4b3e675fb")
(setf (get camera_process::Message :datatype-) "camera_process/Message")
(setf (get camera_process::Message :definition-)
      "string state
")



(provide :camera_process/Message "af6d3a99f0fbeb66d3248fa4b3e675fb")


