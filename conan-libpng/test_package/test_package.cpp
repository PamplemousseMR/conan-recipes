#include <stdlib.h>
#include <png.h>

int main (int argc, char* argv[]) 
{
	png_structp png_ptr = png_create_read_struct(PNG_LIBPNG_VER_STRING, nullptr, nullptr, nullptr);
    return EXIT_SUCCESS;
}
