;; Auto-generated. Do not edit!


(when (boundp 'imu_nav_ml::ImuNavPrediction)
  (if (not (find-package "IMU_NAV_ML"))
    (make-package "IMU_NAV_ML"))
  (shadow 'ImuNavPrediction (find-package "IMU_NAV_ML")))
(unless (find-package "IMU_NAV_ML::IMUNAVPREDICTION")
  (make-package "IMU_NAV_ML::IMUNAVPREDICTION"))

(in-package "ROS")
;;//! \htmlinclude ImuNavPrediction.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass imu_nav_ml::ImuNavPrediction
  :super ros::object
  :slots (_header _position _velocity _position_error_3d _velocity_error_3d _inference_time ))

(defmethod imu_nav_ml::ImuNavPrediction
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:position __position) (instance geometry_msgs::Point :init))
    ((:velocity __velocity) (instance geometry_msgs::Vector3 :init))
    ((:position_error_3d __position_error_3d) 0.0)
    ((:velocity_error_3d __velocity_error_3d) 0.0)
    ((:inference_time __inference_time) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _position __position)
   (setq _velocity __velocity)
   (setq _position_error_3d (float __position_error_3d))
   (setq _velocity_error_3d (float __velocity_error_3d))
   (setq _inference_time (float __inference_time))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:position
   (&rest __position)
   (if (keywordp (car __position))
       (send* _position __position)
     (progn
       (if __position (setq _position (car __position)))
       _position)))
  (:velocity
   (&rest __velocity)
   (if (keywordp (car __velocity))
       (send* _velocity __velocity)
     (progn
       (if __velocity (setq _velocity (car __velocity)))
       _velocity)))
  (:position_error_3d
   (&optional __position_error_3d)
   (if __position_error_3d (setq _position_error_3d __position_error_3d)) _position_error_3d)
  (:velocity_error_3d
   (&optional __velocity_error_3d)
   (if __velocity_error_3d (setq _velocity_error_3d __velocity_error_3d)) _velocity_error_3d)
  (:inference_time
   (&optional __inference_time)
   (if __inference_time (setq _inference_time __inference_time)) _inference_time)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; geometry_msgs/Point _position
    (send _position :serialization-length)
    ;; geometry_msgs/Vector3 _velocity
    (send _velocity :serialization-length)
    ;; float32 _position_error_3d
    4
    ;; float32 _velocity_error_3d
    4
    ;; float32 _inference_time
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; geometry_msgs/Point _position
       (send _position :serialize s)
     ;; geometry_msgs/Vector3 _velocity
       (send _velocity :serialize s)
     ;; float32 _position_error_3d
       (sys::poke _position_error_3d (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _velocity_error_3d
       (sys::poke _velocity_error_3d (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _inference_time
       (sys::poke _inference_time (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; geometry_msgs/Point _position
     (send _position :deserialize buf ptr-) (incf ptr- (send _position :serialization-length))
   ;; geometry_msgs/Vector3 _velocity
     (send _velocity :deserialize buf ptr-) (incf ptr- (send _velocity :serialization-length))
   ;; float32 _position_error_3d
     (setq _position_error_3d (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _velocity_error_3d
     (setq _velocity_error_3d (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _inference_time
     (setq _inference_time (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get imu_nav_ml::ImuNavPrediction :md5sum-) "2a3de14811f7c35ef90a6a889e58a171")
(setf (get imu_nav_ml::ImuNavPrediction :datatype-) "imu_nav_ml/ImuNavPrediction")
(setf (get imu_nav_ml::ImuNavPrediction :definition-)
      "std_msgs/Header header
geometry_msgs/Point position
geometry_msgs/Vector3 velocity
float32 position_error_3d
float32 velocity_error_3d
float32 inference_time

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space. 
# It is only meant to represent a direction. Therefore, it does not
# make sense to apply a translation to it (e.g., when applying a 
# generic rigid transformation to a Vector3, tf2 will only apply the
# rotation). If you want your data to be translatable too, use the
# geometry_msgs/Point message instead.

float64 x
float64 y
float64 z
")



(provide :imu_nav_ml/ImuNavPrediction "2a3de14811f7c35ef90a6a889e58a171")


