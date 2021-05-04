'''
This program calculates your BMI given user input of height and weight
'''
weight = float(input("What is your weight in kg? "))
height = float(input("What is your height in m? "))
bmi = weight/(height**2)
print("Your BMI is", round(bmi, 1))