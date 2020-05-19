#include <stdlib.h>
#include <zzip/zzip.h>
#include <zzip/fseeko.h>

int main (int argc, char * argv[]) 
{
	ZZIP_DIR* dir = zzip_dir_open("test.zip",0);
	if(dir) 
	{
		ZZIP_DIRENT dirent;
		zzip_dir_read(dir,&dirent);
		zzip_dir_close(dir);
	}

	ZZIP_ENTRY* entry = nullptr;
	zzip_entry_fopen(entry, 0);
    return EXIT_SUCCESS;
}
