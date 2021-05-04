'''
This program asks the user to think of a number between
1 and 100 (inclusive) and then repeatedly guesses a number,
and gets the user to say whether the guess loo low, too high or correct. 
'''
print("Pick a number between 1 and 100 (inclusive)")
number = 50
hi = 100
lo = 0
guess = 'a'
while guess != 'C':
    print("My guess is:", int(number))
    guess = input("Is my guess too low (L), too high (H), or correct (C)?\n")
    if guess == 'C':
        break
    elif guess == 'L':
        lo = number
    elif guess == 'H':
        hi = number
    number = (lo + hi) / 2

print("Got it!")
