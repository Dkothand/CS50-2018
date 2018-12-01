from cs50 import get_string
import sys

# Return error if command-line argument != 2
if not len(sys.argv) == 2:
    print("Usage: python vigenere.py key")
    sys.exit(1)

# Check for alphabetical key
key = sys.argv[1]
if not key.isalpha():
    print("Key must be alphabetical.")
    sys.exit(1)

# Make key case-insensitive
key = key.lower()

text = get_string("plaintext: ")
print("ciphertext: ", end="")

# Declares key length variable and key index counter
key_len = len(key)
i = 0

# Iterates through and encrypts plaintext with corresponding key index
for c in text:
    if c.isupper():
        x = (ord(c) - ord('A'))
        y = (ord(key[i % key_len]) - ord('a'))
        print(chr((x + y) % 26 + ord('A')), end="")
        i += 1
    elif c.islower():
        x = (ord(c) - ord('a'))
        y = (ord(key[i % key_len]) - ord('a'))
        print(chr((x + y) % 26 + ord('a')), end="")
        i += 1
    else:
        print(c, end="")

# Prints newline
print()