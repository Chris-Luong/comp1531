import random

incorrect = True
num1 = random.randint(2, 12)
num2 = random.randint(2, 12)
answer = num1 * num2

while incorrect:
    userGuess = int(input(f"What is {num1} x {num2}? "))
    if userGuess == answer:
        print("Correct!")
        incorrect = False
    else:
        print("Incorrect - try again.")

exit()