#include <cstdlib>
#include <cstring>
#include <zlib.h>

int main (int argc, char * argv[]) 
{
   char buffer_in [32] = {"Conan Package Manager"};
    char buffer_out [32] = {0};

    z_stream defstream;
    defstream.zalloc = Z_NULL;
    defstream.zfree = Z_NULL;
    defstream.opaque = Z_NULL;
    defstream.avail_in = static_cast<uInt>(strlen(buffer_in));
    defstream.next_in = reinterpret_cast<Bytef*>(buffer_in);
    defstream.avail_out = static_cast<uInt>(sizeof(buffer_out));
    defstream.next_out = reinterpret_cast<Bytef*>(buffer_out);

    deflateInit(&defstream, Z_BEST_COMPRESSION);
    deflate(&defstream, Z_FINISH);
    deflateEnd(&defstream);

    return EXIT_SUCCESS;
}
