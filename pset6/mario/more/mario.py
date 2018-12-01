from cs50 import get_int

# Get user input and reprompt if input is outside 1 - 22 range
while True:
    height = get_int("Height:")
    if height < 24 and height > -1:
        break

# Function to build front half of pyramid
def front_half():
    print(" " * (height - i - 1), end="")
    print("#" * (i + 1), end="")

# Build pyramid of '#' where height is user input
for i in range(height):
    front_half()
    print(" " * 2, end="")
    print("#" * (i + 1))
