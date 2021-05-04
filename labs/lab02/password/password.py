def check_password(password):
    '''
    Takes in a password, and returns a string based on the strength of that password.

    The returned value should be:
    * "Strong password", if at least 12 characters, contains at least one number, at least one uppercase letter, at least one lowercase letter.
    * "Moderate password", if at least 8 characters, contains at least one number.
    * "Poor password", for anything else
    * "Horrible password", if the user enters "password", "iloveyou", or "123456"
    '''
    counter = 0
    numCheck = False
    upperCheck = False
    lowerCheck = False

    if password == "password" or password == "iloveyou" or password == "123456":
        return "Horrible password"
    
    for chr in password:
        if chr.isdigit():
            numCheck = True
        if chr.isupper():
            upperCheck = True
        if chr.islower():
            lowerCheck = True
        counter += 1
    
    if counter >= 8 and numCheck == True:
        if counter >= 12 and upperCheck == True and lowerCheck == True:
            return "Strong password"
        return "Moderate password"
    
    return "Poor password"

if __name__ == '__main__':
    print(check_password("ihearttrimesters"))
    # What does this do?
