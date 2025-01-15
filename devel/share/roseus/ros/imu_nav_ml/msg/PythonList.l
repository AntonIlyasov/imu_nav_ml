;; Auto-generated. Do not edit!


(when (boundp 'imu_nav_ml::PythonList)
  (if (not (find-package "IMU_NAV_ML"))
    (make-package "IMU_NAV_ML"))
  (shadow 'PythonList (find-package "IMU_NAV_ML")))
(unless (find-package "IMU_NAV_ML::PYTHONLIST")
  (make-package "IMU_NAV_ML::PYTHONLIST"))

(in-package "ROS")
;;//! \htmlinclude PythonList.msg.html


(defclass imu_nav_ml::PythonList
  :super ros::object
  :slots (_row ))

(defmethod imu_nav_ml::PythonList
  (:init
   (&key
    ((:row __row) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _row __row)
   self)
  (:row
   (&optional __row)
   (if __row (setq _row __row)) _row)
  (:serialization-length
   ()
   (+
    ;; float64[] _row
    (* 8    (length _row)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _row
     (write-long (length _row) s)
     (dotimes (i (length _row))
       (sys::poke (elt _row i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _row
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _row (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _row i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get imu_nav_ml::PythonList :md5sum-) "7f476b09ffe66a6e073b86346f9b64b0")
(setf (get imu_nav_ml::PythonList :datatype-) "imu_nav_ml/PythonList")
(setf (get imu_nav_ml::PythonList :definition-)
      "float64[] row

")



(provide :imu_nav_ml/PythonList "7f476b09ffe66a6e073b86346f9b64b0")


