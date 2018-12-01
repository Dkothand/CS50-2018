// Reads through provided file "card.raw", identifying and writing JPEG's to their own respective files.

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>


// Set BYTE struct
typedef uint8_t BYTE;

int main(void)
{
    // Open input file
    FILE* file_ptr = fopen("card.raw", "r");
    if (file_ptr == NULL)
    {
        fprintf(stderr, "Could not open card.raw\n");
        return 1;
    }

    // Declares array for jpeg filenames
    char jpeg_name[8];

    // Assigns buffer block (assumes FAT format of 512 byte storage)
    BYTE buffer[512];

    // Counter for JPEG files
    int file_count = 0;

    // Declare JPEG file pointer
    FILE* jpeg_ptr = NULL;

    // Continues until end of file, reading 512 bytes at a time
    while (fread(buffer, sizeof(buffer), 1, file_ptr) == 1)
    {
        // Checks for JPEG signature in first bytes of read block
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] == 0xe0 || buffer[3] == 0xe1))
        {
            // Names and opens JPEG file for writing
            sprintf(jpeg_name, "%03i.jpg", file_count);
            jpeg_ptr = fopen(jpeg_name, "w");
            file_count++;

            if (jpeg_ptr == NULL)
            {
                fclose(file_ptr);
                fprintf(stderr, "Could not create file\n");
                return 2;
            }
        }
        // Checks JPEG file was created before writing to it
        if (jpeg_ptr != NULL)
        {
            // Writes block to JPEG file currently opened
            fwrite(buffer, sizeof(buffer), 1, jpeg_ptr);
        }

    }

    fclose(jpeg_ptr);
    fclose(file_ptr);
    return 0;
}