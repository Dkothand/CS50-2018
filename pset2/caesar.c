#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

// Cypher that takes plain text and shifts letters by numerical key entered in command line

int main(int argc, string argv[])
{
    // Check for single command-line argument, argc must be = 2
    if (argc != 2)
    {
        printf("Incorrect, enter single key\n");
        return 1;
    }

    // Convert key entered (argv[1]) to integer
    int k = atoi(argv[1]);

    // Get plaintext to encrypt
    string text = get_string("plaintext: ");
    printf("ciphertext: ");

    // Encryption by moving letters based on number entered as key
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];
        int x;
        int y;
        // Checks if character is a letter, returns character if not
        if (isalpha(c))
        {
            // Checks for capitalization
            if (isupper(c))
            {
                x = c % 65;
                y = (x + k) % 26;
                printf("%c", y + 65);
            }
            // Lowercase letters
            else
            {
                x = c % 97;
                y = (x + k) % 26;
                printf("%c", y + 97);
            }
        }
        else
        {
            printf("%c", c);
        }
    }
    // newline after ciphertext, exit by returning 0 from main
    printf("\n");
    return 0;
}