import json
import re
import urllib.request
from src.error import InputError, AccessError
from src.helper import check_user_exists, convert_token, check_token_valid

def user_profile_v1(token, u_id):

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    if check_user_exists(u_id) is False:
        raise InputError("Invalid user")
        
    return {
        'user': {
            'u_id': u_id,
            'email': data['users'][u_id]['email'],
            'name_first': data['users'][u_id]['name_first'],
            'name_last': data['users'][u_id]['name_last'],
            'handle_str': data['users'][u_id]['handle'],
        },
    }

def user_profile_setname_v1(token, name_first, name_last):

    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    # checks if first and last names are between 1-50 characters long
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("Name must be between 1-50 characters")
        
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Name must be between 1-50 characters")

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            data['users'][i]['name_first'] = name_first
            data['users'][i]['name_last'] = name_last

            with open('src/data.json', 'w') as FILE:
                json.dump(data,FILE, indent = 4)

    return {
    }

def user_profile_setemail_v1(token, email):
    # token check
    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    email_syntax = re.compile('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$')
    if not email_syntax.match(email):
        raise InputError("Invalid email")

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            data['users'][i]['email'] = email

            with open('src/data.json', 'w') as FILE:
                json.dump(data,FILE, indent = 4)

    return {
    }

def user_profile_sethandle_v1(token, handle_str):
    # token check
    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    handle = ''.join(handle_str.split())
    handle = handle.replace("@","")
    handle = handle.lower()

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    for i in range(len(data['users'])):
        if data['users'][i]['handle'] == handle:
            raise InputError("Handle already in use")

    for j in range(len(data['users'])):
        if data['users'][j]['token'] == token:
            if len(handle) < 3 or len(handle) > 20:
                raise InputError("Invalid handle")

            data['users'][j]['handle'] = handle

            with open('src/data.json', 'w') as FILE:
                json.dump(data,FILE, indent = 4)

    return {
    }

def users_all_v1(token):
    # token check
    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")
        
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    users = []

    for i in range(len(data['users'])):
        user = {
            'u_id': data['users'][i]['u_id'],
            'email': data['users'][i]['email'],
            'name_first': data['users'][i]['name_first'],
            'name_last': data['users'][i]['name_last'],
            'handle_str': data['users'][i]['handle'],
        }
        users.append(user)
    return {
        "users": users
        }

def user_stats_v1(token):
    # token check
    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    u_id = convert_token(token)
    
    return {
        "user_stats": data["user_stats"][u_id]['stats']
    }

def users_stats_v1(token):

     # token check
    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    return {
        "dreams_stats": data["dreams_stats"]
    }
'''
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    
    if check_token_valid(token) is False:
        raise AccessError("Invalid token")

    urllib.request.urlretrieve(img_url, img_url.jpg)
'''
