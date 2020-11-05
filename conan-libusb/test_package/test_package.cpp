#include <stdlib.h>
#include <iostream>
#include <libusb-1.0/libusb.h>

int main (int argc, char* argv[]) 
{

	libusb_device **devs;
	ssize_t cnt;
	int r, i;

	r = libusb_init(nullptr);
	if (r < 0)
	{
		std::cout << "Can't initialize libusb" << std::endl;
		return EXIT_SUCCESS;
	}

	cnt = libusb_get_device_list(nullptr, &devs);
	if (cnt < 0)
	{
		std::cout << "Can't get device list" << std::endl;
		return EXIT_SUCCESS;
	}

	libusb_free_device_list(devs, 1);
	libusb_exit(nullptr);

    return EXIT_SUCCESS;
}