strings = ["This", "list", "is", "now", "all", "together"]
"""new_string = ''
for i in strings[0:-1]:
    new_string += i + " "
new_string += strings[-1]
print(new_string)"""
print(' '.join(strings))