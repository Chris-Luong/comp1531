'''
This program calculates your tax owing 
'''
income = float(input("Enter your income: "))
if income >= 0 and income <= 18200:
    tax = 0
elif income >= 18201 and income <= 37000:
    tax = 0.19 * (income - 18200)
elif income >= 37001 and income <= 87000:
    tax = 3572 + 0.325 * (income - 37000)
elif income >= 87001 and income <= 180000:
    tax = 19822 + 0.37 * (income - 87000)
elif income >= 180001:
    tax = 54232 + 0.45 * (income - 180000)
    
print("The estimated tax on your income is ${:0,.2f}".format(tax))