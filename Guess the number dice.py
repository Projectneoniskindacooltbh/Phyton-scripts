import random

print("Let's play a dice guessing game!")

sides = input("How many sides should the die have? (press Enter for 6): ")
if sides.strip() == "":
    sides = 6
else:
    sides = int(sides)

guess = int(input(f"Guess a number between 1 and {sides}: "))

rolled = random.randint(1, sides)
print(f"The die rolled... {rolled}")

if guess == rolled:
    print("You got it! Nice one!")
else:
    print("Nope, try again next time!")
