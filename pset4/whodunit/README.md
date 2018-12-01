# Questions

## What's `stdint.h`?

stdint.h is a header file introduced in the C99 standard library.
It provides a set of typedefs that specify exact-width integer types, integers with no padding bits, and defined minimum and maximum values for integers.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

* uint8, uint16, and uint32 are all *unsigned* integers, integers that are either zero or positive.
* int32 is a *signed* integer and can be either positive or negative.
* Because unsigned integers are always positive or zero, they can be used when you know the values you are working with will be always positive. Also, you will have twice the range of positive values since the first bit is not reserved for signing.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE = 1 byte (8-bits)
DWORD = 4 bytes (32-bits)
LONG = 4 bytes (32-bits)
WORD = 2 bytes (16-bits)

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first two bytes must be "BM" written in ASCII, decimal, or hexadecimal.

## What's the difference between `bfSize` and `biSize`?

bfSize is the size, in bytes of the bitmap file. Whereas biSize is the number of bytes required by the struct BITMAPINFOHEADER.

## What does it mean if `biHeight` is negative?

If biHeight is negative, the bitmap is a top-down DIB with it's origin in the upper-left corner. Top-down DIB's cannot be compressed.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

BMP's color depth is specified in biBitCount.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

fopen could return 'NULL' if the file it is trying to open does not exist.

## Why is the third argument to `fread` always `1` in our code?

There is only one BITMAPINFOHEADER and one BITMAPFILEHEADER, so when specifying the number of elements to read, the quantity is 1.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

if bi.biWidth is 3, padding will equal 3.

## What does `fseek` do?

fseek() offsets a given number of bytes to a pointer of a FILE object.

## What is `SEEK_CUR`?

SEEK_CUR is the current position of the file pointer. Used as a third argument in fseek to set where the allocated bytes are to be offset.
