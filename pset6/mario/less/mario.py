from cs50 import get_int

# Get user input and reprompt if input is outside 1 - 22 range
while True:
    height = get_int("Height:")
    if height < 24 and height > -1:
        break

# Build half pyramid of '#' where height is user input
for i in range(height):
    print(" " * (height - i - 1), end="")
    print("#" * (i + 2), end="")
    print()