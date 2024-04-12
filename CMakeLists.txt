cmake_minimum_required(VERSION 2.8.3)
project(stereo_sonar)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O3")

find_package(Eigen3 REQUIRED)
find_package(catkin REQUIRED COMPONENTS
  pybind11_catkin
  rospy
  sensor_msgs
  message_generation
)

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
)

catkin_python_setup()

add_message_files(
   FILES
   OculusFire.msg
   OculusPing.msg
)

generate_messages(
  DEPENDENCIES
  sensor_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime roscpp sensor_msgs
  DEPENDS EIGEN3
)

pybind11_add_module(cfar src/${PROJECT_NAME}/cpp/cfar.cpp)
set_target_properties(cfar PROPERTIES LIBRARY_OUTPUT_DIRECTORY
  ${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_PYTHON_DESTINATION}
)

pybind11_add_module(match src/${PROJECT_NAME}/cpp/match.cpp)
set_target_properties(match PROPERTIES LIBRARY_OUTPUT_DIRECTORY
  ${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_PYTHON_DESTINATION}
)
