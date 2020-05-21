#include <stdlib.h>
#include <libusb-1.0/libusb.h>

int main (int argc, char* argv[]) 
{

	libusb_device **devs;
	ssize_t cnt;
	int r, i;

	r = libusb_init(nullptr);
	if (r < 0)
	{
		return r;
	}

	cnt = libusb_get_device_list(nullptr, &devs);
	if (cnt < 0)
	{
		return static_cast< int >(cnt);
	}

	libusb_free_device_list(devs, 1);
	libusb_exit(nullptr);

    return EXIT_SUCCESS;
}