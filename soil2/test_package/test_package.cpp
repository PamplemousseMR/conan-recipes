#include <stdlib.h>
#include <SOIL2/SOIL2.h>

int main (int argc, char* argv[]) 
{
    int width, height, chanel;
    int soilFormat = SOIL_LOAD_RGB;
    unsigned char* data = SOIL_load_image("img.png", &width, &height, &chanel, soilFormat);
    return EXIT_SUCCESS;
}
