; Auto-generated. Do not edit!


(cl:in-package imu_nav_ml-msg)


;//! \htmlinclude ListOfLists.msg.html

(cl:defclass <ListOfLists> (roslisp-msg-protocol:ros-message)
  ((matrix
    :reader matrix
    :initarg :matrix
    :type (cl:vector imu_nav_ml-msg:PythonList)
   :initform (cl:make-array 0 :element-type 'imu_nav_ml-msg:PythonList :initial-element (cl:make-instance 'imu_nav_ml-msg:PythonList))))
)

(cl:defclass ListOfLists (<ListOfLists>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ListOfLists>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ListOfLists)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name imu_nav_ml-msg:<ListOfLists> is deprecated: use imu_nav_ml-msg:ListOfLists instead.")))

(cl:ensure-generic-function 'matrix-val :lambda-list '(m))
(cl:defmethod matrix-val ((m <ListOfLists>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader imu_nav_ml-msg:matrix-val is deprecated.  Use imu_nav_ml-msg:matrix instead.")
  (matrix m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ListOfLists>) ostream)
  "Serializes a message object of type '<ListOfLists>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'matrix))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'matrix))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ListOfLists>) istream)
  "Deserializes a message object of type '<ListOfLists>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'matrix) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'matrix)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'imu_nav_ml-msg:PythonList))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ListOfLists>)))
  "Returns string type for a message object of type '<ListOfLists>"
  "imu_nav_ml/ListOfLists")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ListOfLists)))
  "Returns string type for a message object of type 'ListOfLists"
  "imu_nav_ml/ListOfLists")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ListOfLists>)))
  "Returns md5sum for a message object of type '<ListOfLists>"
  "fae0d37fb284617a626d94525abd3508")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ListOfLists)))
  "Returns md5sum for a message object of type 'ListOfLists"
  "fae0d37fb284617a626d94525abd3508")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ListOfLists>)))
  "Returns full string definition for message of type '<ListOfLists>"
  (cl:format cl:nil "PythonList[] matrix~%~%================================================================================~%MSG: imu_nav_ml/PythonList~%float64[] row~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ListOfLists)))
  "Returns full string definition for message of type 'ListOfLists"
  (cl:format cl:nil "PythonList[] matrix~%~%================================================================================~%MSG: imu_nav_ml/PythonList~%float64[] row~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ListOfLists>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'matrix) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ListOfLists>))
  "Converts a ROS message object to a list"
  (cl:list 'ListOfLists
    (cl:cons ':matrix (matrix msg))
))
