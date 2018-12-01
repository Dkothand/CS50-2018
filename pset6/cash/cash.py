from cs50 import get_float

# Check for non-negative input from user
# Initalize coin counter to 0
coins = 0
while True:
    change = get_float("Change owed: ") * 100
    if change > 0:
        break

# While loops decrement change while adding appropriate coins
# to coin counter, assuming USD
while change >= 25:
    coins += 1
    change -= 25

while change >= 10:
    coins += 1
    change -= 10

while change >= 5:
    coins += 1
    change -= 5

while change >= 1:
    coins += 1
    change -= 1

print(coins)