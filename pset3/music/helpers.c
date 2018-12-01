// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int x = fraction[0] - '0';
    int y = fraction[2] - '0';
    return ((8 / y) * x);
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    char letter = note[0];
    char oct = note[strlen(note) - 1];

    // Factors whole octave steps A4 -> A3 etc.
    int oct_step = (oct - '4');

    // Sets starting point at A4 (440Hz)
    int int_hz = round(440 * pow(2, oct_step));
    float n = 0.;

    // Sets number of steps(n) based on note with A as 0 steps
    switch (letter)
    {
        case 'A':
            n = 0.;
            break;

        case 'B':
            n = 2.;
            break;

        case 'C':
            n = -9.;
            break;

        case 'D':
            n = -7.;
            break;

        case 'E':
            n = -5.;
            break;

        case 'F':
            n = -4.;
            break;

        case 'G':
            n = -2.;
            break;

        default:
        return 1;
    }

    // Checks for accidentals, up one step if sharp(#), down one step if flat(b)
    if (note[1] == '#')
    {
        n += 1.;
    }
    else if (note[1] == 'b')
    {
        n -= 1.;
    }

    // Calculates frequency of note and rounds
    float hz = round((pow(2, n / 12.)) * int_hz);
    return hz;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (s[0] == '\0')
    {
        return true;
    }
    return false;
}
