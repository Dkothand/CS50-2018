#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Encrypts a plain-text entry with a command-line keyword.
// Letters of plain-text are shifted by value of sequence of keys in keyword, with A/a = 0 shift and Z/z = 25 shifts.

int main(int argc, string argv[])
{
    // Return error if command-line arguments != 2
    if (argc != 2)
    {
        printf("Enter a single key.\n");
        return 1;
    }

    string k = argv[1];
    int keylen = strlen(k);

    // Return error if characters in key are not letters
    for (int i = 0; i < keylen; i++)
    {
        if (!isalpha(k[i]))
        {
            printf("Characters in key must be alphabetical.\n");
            return 1;
        }
    }

    string plain = get_string("plaintext: ");
    int plainlen = strlen(plain);
    printf("ciphertext: ");

    // Iterates through plaintext plain[j] and encrypts with key values k[m]
    // Initalize variables for character math, probably a way to refactor, but helped look at each step when debugging
    int x, y, z;

    // Sets characters in plaintext and keyword to alphabetical index (a = 0 and z = 25)
    // Moves characters based on index numbers and converts back to ASCII when printing
    for (int j = 0, m = 0; j < plainlen && m <= keylen; j++)
    {
        if (isalpha(plain[j]))
        {
            // Sets index for keyword m to 0, starts encryption back at beginning of keyword
            if (m == keylen)
            {
                m = 0;
            }
            if (isupper(plain[j]))
            {
                if (isupper(k[m]))
                {
                    x = plain[j] - 'A';
                    y = (k[m] - 'A');
                    z = (x + y) % 26;
                    printf("%c", z + 'A');
                    m++;
                }
                else
                {
                    x = plain[j] - 'A';
                    y = (k[m] - 'a');
                    z = (x + y) % 26;
                    printf("%c", z + 'A');
                    m++;
                }

            }
            else
            {
                if (isupper(k[m]))
                {
                    x = plain[j] - 'a';
                    y = (k[m] - 'A');
                    z = (x + y) % 26;
                    printf("%c", z + 'a');
                    m++;
                }
                else
                {
                    x = plain[j] - 'a';
                    y = (k[m] - 'a');
                    z = (x + y) % 26;
                    printf("%c", z + 'a');
                    m++;
                }

            }
        }
        else
        {
            printf("%c", plain[j]);
        }
    }
    printf("\n");
    return 0;
}