import random

randomnumber = random.randint(1, 100)

print("Wanna play a game.....Guess the number between 1 and 100!")

guess = ''

while guess!= randomnumber:
    guess = int(input("Enter your guess: "))
    if guess < randomnumber:
        print("BOOOOOO too low! Try guessing higher.")
    elif guess > randomnumber:
        print("BOOOOOO too high! Try guessing lower.")


print("Congratulations! You've guessed the correct number", + randomnumber)
