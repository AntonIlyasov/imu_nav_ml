
(cl:in-package :asdf)

(defsystem "imu_nav_ml-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "ImuNavPrediction" :depends-on ("_package_ImuNavPrediction"))
    (:file "_package_ImuNavPrediction" :depends-on ("_package"))
    (:file "ListOfLists" :depends-on ("_package_ListOfLists"))
    (:file "_package_ListOfLists" :depends-on ("_package"))
    (:file "PosVel" :depends-on ("_package_PosVel"))
    (:file "_package_PosVel" :depends-on ("_package"))
    (:file "PythonList" :depends-on ("_package_PythonList"))
    (:file "_package_PythonList" :depends-on ("_package"))
  ))