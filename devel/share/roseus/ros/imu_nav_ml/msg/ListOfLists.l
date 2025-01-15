;; Auto-generated. Do not edit!


(when (boundp 'imu_nav_ml::ListOfLists)
  (if (not (find-package "IMU_NAV_ML"))
    (make-package "IMU_NAV_ML"))
  (shadow 'ListOfLists (find-package "IMU_NAV_ML")))
(unless (find-package "IMU_NAV_ML::LISTOFLISTS")
  (make-package "IMU_NAV_ML::LISTOFLISTS"))

(in-package "ROS")
;;//! \htmlinclude ListOfLists.msg.html


(defclass imu_nav_ml::ListOfLists
  :super ros::object
  :slots (_matrix ))

(defmethod imu_nav_ml::ListOfLists
  (:init
   (&key
    ((:matrix __matrix) ())
    )
   (send-super :init)
   (setq _matrix __matrix)
   self)
  (:matrix
   (&rest __matrix)
   (if (keywordp (car __matrix))
       (send* _matrix __matrix)
     (progn
       (if __matrix (setq _matrix (car __matrix)))
       _matrix)))
  (:serialization-length
   ()
   (+
    ;; imu_nav_ml/PythonList[] _matrix
    (apply #'+ (send-all _matrix :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; imu_nav_ml/PythonList[] _matrix
     (write-long (length _matrix) s)
     (dolist (elem _matrix)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; imu_nav_ml/PythonList[] _matrix
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _matrix (let (r) (dotimes (i n) (push (instance imu_nav_ml::PythonList :init) r)) r))
     (dolist (elem- _matrix)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get imu_nav_ml::ListOfLists :md5sum-) "fae0d37fb284617a626d94525abd3508")
(setf (get imu_nav_ml::ListOfLists :datatype-) "imu_nav_ml/ListOfLists")
(setf (get imu_nav_ml::ListOfLists :definition-)
      "PythonList[] matrix

================================================================================
MSG: imu_nav_ml/PythonList
float64[] row

")



(provide :imu_nav_ml/ListOfLists "fae0d37fb284617a626d94525abd3508")


