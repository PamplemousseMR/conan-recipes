#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 3.0)
project("test_package" VERSION 1.0 LANGUAGES CXX)

#=======================================
#               EXECUTABLE              
#======================================= 

add_executable(
	${PROJECT_NAME}
	test_package.cpp
	)

#=======================================
#                SETTINGS               
#=======================================

set_target_properties(
	${PROJECT_NAME} PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    )

#=======================================
#                PACKAGE                
#=======================================

find_package(OpenCV REQUIRED CONFIG)

if("${OpenCV_VERSION}" VERSION_LESS_EQUAL "4.5.3")
	target_link_libraries(${PROJECT_NAME} opencv_core opencv_flann opencv_imgproc opencv_ml opencv_photo opencv_features2d opencv_imgcodecs opencv_videoio opencv_calib3d opencv_highgui opencv_objdetect opencv_stitching opencv_video)
else()
	message(FATAL_ERROR "Unhandle version " ${OpenCV_VERSION})
endif()