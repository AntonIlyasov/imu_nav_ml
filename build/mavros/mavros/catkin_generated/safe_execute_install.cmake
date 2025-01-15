execute_process(COMMAND "/home/anton202/study/ml_2_course/new/catkin_ws/build/mavros/mavros/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/anton202/study/ml_2_course/new/catkin_ws/build/mavros/mavros/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
