#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    // Get user input and re-check if n is outside 1-22 range
    do
    {
        height = get_int("Height:");
    }
    while (height < 0 || height > 23);
    // Build half pyramid of '#' where height is user input
    for (int row = 0; row < height; row++)
    {
        for (int space = height - row - 1; space > 0; space--)
        {
            printf(" ");
        }
        for (int hash = row + 2; hash > 0; hash--)
        {
            printf("#");
        }
        printf("\n");
    }
}