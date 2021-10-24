#include <stdio.h>
#include <iostream>
#include <opencv2/imgproc/imgproc.hpp>

int main ()
{
	cv::Mat mat(2,2, CV_8UC3, cv::Scalar(0,0,255));
	std::cout << mat << std::endl;
    return EXIT_SUCCESS;
}
