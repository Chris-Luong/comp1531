import re
import hashlib
import jwt
import json
from src.error import InputError
from src.helper import make_token, create_timestamp, calc_utilisation_rate
from datetime import datetime
from random import randint

def auth_login_v2(email, password):

    '''
    auth_login_v1 takes an email and password as input and checks that there is a
    dictionary in our users list that has the same email and password combination
    and generates an authentication token with their user ID

    Arguments:
        email (string) - email entered by user
        password (string) - pasword entered by user 

    Exceptions:
        InputError  - Occurs when
            * email entered is not valid (syntax)
            * email entered doesnt belong to a users
            * password doesn't match the users password 

    Return Value:
        Returns auth_user_id on condition that the correct email and password 
        combination has been entered
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    # checks for correct email syntax using regular expression
    email_syntax = re.compile('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$')
    if not email_syntax.match(email):
        raise InputError("Invalid email")        
    
    password = hashlib.sha256(password.encode()).hexdigest()

    # checks if email has been registered and if password is correct
    # otherwise raise InputError for email or password
    for i in range(len(data["users"])):
        if data['users'][i]['email'] == email:
            if data['users'][i]['password'] == password:

                with open('src/data.json', 'w') as FILE:
                    data['users'][i]['logged_in'] = True
                    json.dump(data,FILE, indent = 4)

                return {
                    'token': data['users'][i]['token'],
                    'auth_user_id': data['users'][i]['u_id']
                }
            else:
                raise InputError("Incorrect password")
        
    raise InputError("Email is not registered")

def auth_register_v2(email, password, name_first, name_last):

    '''
    function takes new users first name, last name, email and password and generates
    a new user dictionary with all the input data, handle which is a concatenation
    of the users first and last name and a user id and generates authentication 
    token for the users first session

    Arguments:
        email (string) - email entered by new user
        password (string) - password entered by new user
        name_first (string) - first name entered by new user
        name_last (string) - last name entered by new user

    Exceptions:
        InputError - Occurs when:
            * email is not valid (syntax)
            * email address is being used by another user
            * password entered is less than 6 characters long
            * name_first not between 1-50 characters inclusive
            * name_last not between 1-50 characters inclusive

    Return Value:
        Returns auth_user_id on condition that the data entered is all valid and 
        unused as specified in exceptions above
        
        New user is also stored as a dictionary in the users list in the data 
        dictionary in data.py
    '''

    email_syntax = re.compile('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$')
    if not email_syntax.match(email):
        raise InputError("Invalid email")

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    # checks if email has already been used    
    for i in range(len(data["users"])):
        if data['users'][i]['email'] == email:
            raise InputError("Email already in use")
    
    # checks if password is less than 6 characters       
    if len(password) < 6:
        raise InputError("Password too short")
    
    # checks if first and last names are between 1-50 characters long
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("Name must be between 1-50 characters")
        
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Name must be between 1-50 characters")
    
    # creates handle from concatenation of first and last name
    # then removes any whitespace and @ characters
    # then checks if handle is longer than 20 characters and caps it at 20    
    handle = name_first.lower() + name_last.lower()
    handle = ''.join(handle.split())
    handle = handle.replace("@","")    
    if len(handle) > 20:
        handle = handle[0:20]
    
    # loop to check if handle already exists and append a number to the end    
    orig_handle = handle
    count = 0
    for i in range(len(data["users"])):
        if data['users'][i]['handle'] == handle:
            handle = orig_handle + str(count)
            count += 1
            
    u_id = len(data["users"])
    token = make_token(u_id)
    if u_id == 0:
        permission_id = 1
    else:
        permission_id = 2
    # create a new dictionary for the user with all relevant data
    new_user = {
            "u_id": u_id,
            "email": email,
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "name_first": name_first,
            "name_last": name_last,
            "handle": handle,
            "token": token,
            "permission_id": permission_id,
            "logged_in": True,
    }

    new_user_stats = {
                    "u_id": u_id,
                    "stats":
                        {
                            "channels_joined": [
                                {
                                    "num_channels_joined": 0,
                                    "time_stamp": create_timestamp()
                                },
                            ],
                            "dms_joined": [
                                {
                                    "num_dms_joined": 0,
                                    "time_stamp": create_timestamp()
                                }
                            ], 
                            "messages_sent": [
                                {
                                    "num_messages_sent": 0,
                                    "time_stamp": create_timestamp()
                                }
                            ], 
                            "involvement_rate": 0.0
                        }
                }  
    
    # appends the new dictionary to the "users" list in the data dictionary in data.py

    with open('src/data.json') as FILE:
        data2 = json.load(FILE)
        temp = data2["users"]
        y = new_user
        temp.append(y)
        temp2 = data2["user_stats"]
        z = new_user_stats
        temp2.append(z)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data2, FILE, indent = 4)

    calc_utilisation_rate()
    
    # return the user id of the newly registered user as the authenticated user id
    return {
        'token': new_user["token"],
        'auth_user_id': new_user["u_id"],
    }

def auth_logout_v1(token):
    
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    for i in range(len(data["users"])):
        if data['users'][i]['token'] == token and data['users'][i]['logged_in']:
            with open('src/data.json', 'w') as FILE:
                data['users'][i]['logged_in'] = False
                json.dump(data,FILE, indent = 4)

            return {
                "is_success": True
            }
        else:
            return {
                "is_success": False
            }

def auth_passwordreset_request_v1(email):

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    verified = False
    for i in range(len(data["users"])):
        if data['users'][i]['email'] == email:
            verified = True
    
    if verified is False:
        raise InputError("Unregistered email")

    reset_code = randint(100000, 999999)
    reset_dict = {"email": email, "reset_code": reset_code}
    data["reset_codes"].append(reset_dict)

    with open('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    return {"email": email, "reset_code": reset_code}

def auth_passwordreset_reset_v1(reset_code, new_password):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    
    # check for valid code
    valid = False
    for i in range(len(data["reset_codes"])):
        if data["reset_codes"][i]["reset_code"] == reset_code:
            email = data["reset_codes"][i]["email"]
            valid = True
    
    if valid == False:
        raise InputError("Invalid code")

    # checks if password is less than 6 characters       
    if len(new_password) < 6:
        raise InputError("Password too short")

    # encode new password and set it
    new_password = hashlib.sha256(new_password.encode()).hexdigest()
    for i in range(len(data["users"])):
        if data['users'][i]['email'] == email:
            data['users'][i]['password'] = new_password

    # remove reset code from data once it has been used
    for i in range(len(data["reset_codes"])):
        if data["reset_codes"][i]["reset_code"] == reset_code:
            del data["reset_codes"][i]

    with open('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    return {}