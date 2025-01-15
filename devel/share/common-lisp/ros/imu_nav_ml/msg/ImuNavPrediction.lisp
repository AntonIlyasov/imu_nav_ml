; Auto-generated. Do not edit!


(cl:in-package imu_nav_ml-msg)


;//! \htmlinclude ImuNavPrediction.msg.html

(cl:defclass <ImuNavPrediction> (roslisp-msg-protocol:ros-message)
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
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (position_error_3d
    :reader position_error_3d
    :initarg :position_error_3d
    :type cl:float
    :initform 0.0)
   (velocity_error_3d
    :reader velocity_error_3d
    :initarg :velocity_error_3d
    :type cl:float
    :initform 0.0)
   (inference_time
    :reader inference_time
    :initarg :inference_time
    :type cl:float
    :initform 0.0))
)

(cl:defclass ImuNavPrediction (<ImuNavPrediction>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ImuNavPrediction>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ImuNavPrediction)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name imu_nav_ml-msg:<ImuNavPrediction> is deprecated: use imu_nav_ml-msg:ImuNavPrediction instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <ImuNavPrediction>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:header-val is deprecated.  Use imu_nav_ml-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <ImuNavPrediction>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:position-val is deprecated.  Use imu_nav_ml-msg:position instead.")
  (position m))

(cl:ensure-generic-function 'velocity-val :lambda-list '(m))
(cl:defmethod velocity-val ((m <ImuNavPrediction>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:velocity-val is deprecated.  Use imu_nav_ml-msg:velocity instead.")
  (velocity m))

(cl:ensure-generic-function 'position_error_3d-val :lambda-list '(m))
(cl:defmethod position_error_3d-val ((m <ImuNavPrediction>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:position_error_3d-val is deprecated.  Use imu_nav_ml-msg:position_error_3d instead.")
  (position_error_3d m))

(cl:ensure-generic-function 'velocity_error_3d-val :lambda-list '(m))
(cl:defmethod velocity_error_3d-val ((m <ImuNavPrediction>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:velocity_error_3d-val is deprecated.  Use imu_nav_ml-msg:velocity_error_3d instead.")
  (velocity_error_3d m))

(cl:ensure-generic-function 'inference_time-val :lambda-list '(m))
(cl:defmethod inference_time-val ((m <ImuNavPrediction>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:inference_time-val is deprecated.  Use imu_nav_ml-msg:inference_time instead.")
  (inference_time m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ImuNavPrediction>) ostream)
  "Serializes a message object of type '<ImuNavPrediction>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'position) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'velocity) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'position_error_3d))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'velocity_error_3d))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'inference_time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ImuNavPrediction>) istream)
  "Deserializes a message object of type '<ImuNavPrediction>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'position) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'velocity) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'position_error_3d) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'velocity_error_3d) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'inference_time) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ImuNavPrediction>)))
  "Returns string type for a message object of type '<ImuNavPrediction>"
  "imu_nav_ml/ImuNavPrediction")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ImuNavPrediction)))
  "Returns string type for a message object of type 'ImuNavPrediction"
  "imu_nav_ml/ImuNavPrediction")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ImuNavPrediction>)))
  "Returns md5sum for a message object of type '<ImuNavPrediction>"
  "2a3de14811f7c35ef90a6a889e58a171")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ImuNavPrediction)))
  "Returns md5sum for a message object of type 'ImuNavPrediction"
  "2a3de14811f7c35ef90a6a889e58a171")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ImuNavPrediction>)))
  "Returns full string definition for message of type '<ImuNavPrediction>"
  (cl:format cl:nil "std_msgs/Header header~%geometry_msgs/Point position~%geometry_msgs/Vector3 velocity~%float32 position_error_3d~%float32 velocity_error_3d~%float32 inference_time~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ImuNavPrediction)))
  "Returns full string definition for message of type 'ImuNavPrediction"
  (cl:format cl:nil "std_msgs/Header header~%geometry_msgs/Point position~%geometry_msgs/Vector3 velocity~%float32 position_error_3d~%float32 velocity_error_3d~%float32 inference_time~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ImuNavPrediction>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'position))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'velocity))
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ImuNavPrediction>))
  "Converts a ROS message object to a list"
  (cl:list 'ImuNavPrediction
    (cl:cons ':header (header msg))
    (cl:cons ':position (position msg))
    (cl:cons ':velocity (velocity msg))
    (cl:cons ':position_error_3d (position_error_3d msg))
    (cl:cons ':velocity_error_3d (velocity_error_3d msg))
    (cl:cons ':inference_time (inference_time msg))
))
