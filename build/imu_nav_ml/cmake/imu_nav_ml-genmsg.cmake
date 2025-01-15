# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "imu_nav_ml: 4 messages, 0 services")

set(MSG_I_FLAGS "-Iimu_nav_ml:/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(imu_nav_ml_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg" NAME_WE)
add_custom_target(_imu_nav_ml_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "imu_nav_ml" "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg" "geometry_msgs/Vector3:std_msgs/Header:geometry_msgs/Point"
)

get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg" NAME_WE)
add_custom_target(_imu_nav_ml_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "imu_nav_ml" "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg" "imu_nav_ml/PythonList"
)

get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg" NAME_WE)
add_custom_target(_imu_nav_ml_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "imu_nav_ml" "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg" "geometry_msgs/Vector3:std_msgs/Header:geometry_msgs/Point"
)

get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg" NAME_WE)
add_custom_target(_imu_nav_ml_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "imu_nav_ml" "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_cpp(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg"
  "${MSG_I_FLAGS}"
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_cpp(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_cpp(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_nav_ml
)

### Generating Services

### Generating Module File
_generate_module_cpp(imu_nav_ml
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_nav_ml
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(imu_nav_ml_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(imu_nav_ml_generate_messages imu_nav_ml_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_cpp _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_cpp _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_cpp _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_cpp _imu_nav_ml_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_nav_ml_gencpp)
add_dependencies(imu_nav_ml_gencpp imu_nav_ml_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_nav_ml_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_eus(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg"
  "${MSG_I_FLAGS}"
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_eus(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_eus(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_nav_ml
)

### Generating Services

### Generating Module File
_generate_module_eus(imu_nav_ml
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_nav_ml
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(imu_nav_ml_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(imu_nav_ml_generate_messages imu_nav_ml_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_eus _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_eus _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_eus _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_eus _imu_nav_ml_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_nav_ml_geneus)
add_dependencies(imu_nav_ml_geneus imu_nav_ml_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_nav_ml_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_lisp(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg"
  "${MSG_I_FLAGS}"
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_lisp(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_lisp(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_nav_ml
)

### Generating Services

### Generating Module File
_generate_module_lisp(imu_nav_ml
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_nav_ml
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(imu_nav_ml_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(imu_nav_ml_generate_messages imu_nav_ml_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_lisp _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_lisp _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_lisp _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_lisp _imu_nav_ml_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_nav_ml_genlisp)
add_dependencies(imu_nav_ml_genlisp imu_nav_ml_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_nav_ml_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_nodejs(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg"
  "${MSG_I_FLAGS}"
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_nodejs(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_nodejs(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_nav_ml
)

### Generating Services

### Generating Module File
_generate_module_nodejs(imu_nav_ml
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_nav_ml
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(imu_nav_ml_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(imu_nav_ml_generate_messages imu_nav_ml_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_nodejs _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_nodejs _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_nodejs _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_nodejs _imu_nav_ml_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_nav_ml_gennodejs)
add_dependencies(imu_nav_ml_gennodejs imu_nav_ml_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_nav_ml_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_py(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg"
  "${MSG_I_FLAGS}"
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_py(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_nav_ml
)
_generate_msg_py(imu_nav_ml
  "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_nav_ml
)

### Generating Services

### Generating Module File
_generate_module_py(imu_nav_ml
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_nav_ml
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(imu_nav_ml_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(imu_nav_ml_generate_messages imu_nav_ml_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ImuNavPrediction.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_py _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/ListOfLists.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_py _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PosVel.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_py _imu_nav_ml_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/anton202/study/ml_2_course/new/catkin_ws/src/imu_nav_ml/msg/PythonList.msg" NAME_WE)
add_dependencies(imu_nav_ml_generate_messages_py _imu_nav_ml_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_nav_ml_genpy)
add_dependencies(imu_nav_ml_genpy imu_nav_ml_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_nav_ml_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_nav_ml)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_nav_ml
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(imu_nav_ml_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(imu_nav_ml_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_nav_ml)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_nav_ml
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(imu_nav_ml_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(imu_nav_ml_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_nav_ml)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_nav_ml
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(imu_nav_ml_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(imu_nav_ml_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_nav_ml)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_nav_ml
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(imu_nav_ml_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(imu_nav_ml_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_nav_ml)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_nav_ml\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_nav_ml
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(imu_nav_ml_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(imu_nav_ml_generate_messages_py geometry_msgs_generate_messages_py)
endif()
