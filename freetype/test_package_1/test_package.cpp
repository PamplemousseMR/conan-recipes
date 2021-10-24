#include <stdlib.h>

#include <ft2build.h>
#include FT_FREETYPE_H

int main(int argc, char** argv)
{
    FT_Library library;   
    FT_Error error = FT_Init_FreeType(&library);
    if(error) 
    {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}