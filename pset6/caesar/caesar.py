from cs50 import get_string
import sys

# Checks for single command-line argument, displays usage if not correct
if not len(sys.argv) == 2:
    print("Usage: python caesar.py key")

# Get key and plaintext to encipher
key = int(sys.argv[1])
text = get_string("plaintext: ")
print("ciphertext: ", end="")

# Encrypts by moving characters based on key value
# Converting characters to an alphabet index and back w/ chr() and ord()
for c in text:
    if c.isalpha():
        # Check if capital letter
        if c.isupper():
            x = ord(c) % 65
            y = (x + key) % 26
            print(chr(y + 65), end="")
        # Lowercase
        else:
            x = ord(c) % 97
            y = (x + key) % 26
            print(chr(y + 97), end="")
    else:
        print(c, end="")

# Newline after ciphertext
print()