; Auto-generated. Do not edit!


(cl:in-package imu_nav_ml-msg)


;//! \htmlinclude PosVel.msg.html

(cl:defclass <PosVel> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (position
    :reader position
    :initarg :position
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point))
   (velocity
    :reader velocity
    :initarg :velocity
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3)))
)

(cl:defclass PosVel (<PosVel>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PosVel>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PosVel)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name imu_nav_ml-msg:<PosVel> is deprecated: use imu_nav_ml-msg:PosVel instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <PosVel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:header-val is deprecated.  Use imu_nav_ml-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <PosVel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:position-val is deprecated.  Use imu_nav_ml-msg:position instead.")
  (position m))

(cl:ensure-generic-function 'velocity-val :lambda-list '(m))
(cl:defmethod velocity-val ((m <PosVel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:velocity-val is deprecated.  Use imu_nav_ml-msg:velocity instead.")
  (velocity m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PosVel>) ostream)
  "Serializes a message object of type '<PosVel>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'position) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'velocity) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PosVel>) istream)
  "Deserializes a message object of type '<PosVel>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'position) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'velocity) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PosVel>)))
  "Returns string type for a message object of type '<PosVel>"
  "imu_nav_ml/PosVel")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PosVel)))
  "Returns string type for a message object of type 'PosVel"
  "imu_nav_ml/PosVel")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PosVel>)))
  "Returns md5sum for a message object of type '<PosVel>"
  "6ee8de2de1dc511f12aad1844283cad8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PosVel)))
  "Returns md5sum for a message object of type 'PosVel"
  "6ee8de2de1dc511f12aad1844283cad8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PosVel>)))
  "Returns full string definition for message of type '<PosVel>"
  (cl:format cl:nil "std_msgs/Header header~%geometry_msgs/Point position~%geometry_msgs/Vector3 velocity~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PosVel)))
  "Returns full string definition for message of type 'PosVel"
  (cl:format cl:nil "std_msgs/Header header~%geometry_msgs/Point position~%geometry_msgs/Vector3 velocity~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PosVel>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'position))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'velocity))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PosVel>))
  "Converts a ROS message object to a list"
  (cl:list 'PosVel
    (cl:cons ':header (header msg))
    (cl:cons ':position (position msg))
    (cl:cons ':velocity (velocity msg))
))
