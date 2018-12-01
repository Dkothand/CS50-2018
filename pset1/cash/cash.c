#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // Check for non-negative float input from user
    // Initialize coins counter to 0
    float change;
    int coins = 0;
    do
    {
        change = get_float("Change owed: ");
    }
    while (change < 0);
    // Set change to power of 100 (0.41 = 41) and rounds to nearest int
    change = round(change * 100);
    // Add to coins counter and subtract input based on value of coins
    while (change >= 25)
    {
        coins += 1;
        change -= 25;
    }
    while (change >= 10)
    {
        coins += 1;
        change -= 10;
    }
    while (change >= 5)
    {
        coins += 1;
        change -= 5;
    }
    while (change >= 1)
    {
        coins += 1;
        change -= 1;
    }
    // Return number of coins in printf statement
    printf("%i\n", coins);
}