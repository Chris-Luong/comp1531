import json
from src.helper import convert_token, check_user_in_channel, make_token, check_token_valid
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.channel import channel_invite_v2
from src.message import message_send_v2
from src.clear import clear_v1
from src.error import InputError, AccessError
from src.helper import check_user_exists, check_user_in_dm

def search_v2(token, query_str):
    
    # token check
    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    messages = []

    # append to list all messages that match query string from
    # channels/DM that user has joined
    with open ("src/data.json") as FILE:
        data = json.load(FILE)

    u_id = convert_token(token)
    for i in range(len(data['messages'])):
        dm_id = data['messages'][i]['dm_id']
        channel_id = data['messages'][i]['channel_id']
        if dm_id == -1:
            if check_user_in_channel(u_id, channel_id):
                if query_str.lower() in data['messages'][i]['message'].lower():
                    messages.append(data['messages'][i])
        else:
            if check_user_in_dm(u_id, dm_id):
                if query_str.lower() in data['messages'][i]['message'].lower():
                    messages.append(data['messages'][i])
    
    print(messages)
    return {
        'messages': messages
    }

def admin_userpermission_change_v1(token, u_id, permission_id):

    # token check
    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    if permission_id is not 1 and permission_id is not 2:
        raise InputError("Invalid permission_id")

    if not check_user_exists(u_id):
        raise InputError("invalid u_id")

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    owner = False
    owner_id = convert_token(token)
    if data['users'][owner_id]['permission_id'] == 1:
        owner = True

    if owner == True:
        for i in range(len(data['users'])):
            if u_id == data['users'][i]['u_id']:
                data['users'][i]['permission_id'] = permission_id
    else:
        raise AccessError("Unauthorised user, user is not an owner")

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    return {
        
    }

def admin_user_remove_v1(token, u_id):

    # token check
    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    with open ("src/data.json") as FILE:
        data = json.load(FILE)

    if not check_user_exists(u_id):
        raise InputError("invalid u_id")

    owner_count = 0
    for i in range(len(data['users'])):
        if data['users'][i]['permission_id'] == 1:
            owner_count += 1
    
    if owner_count == 1:
        raise InputError("user is the only owner")

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    owner = False
    owner_id = convert_token(token)
    if data['users'][owner_id]['permission_id'] == 1:
        owner = True

    if owner == True:
        for i in range(len(data['users'])):
            if data['users'][i]['u_id'] == u_id:
                data['users'][i]['name_first'] = "Removed user"
                data['users'][i]['name_last'] = "Removed user"

        for i in range(len(data['messages'])):
            if data['messages'][i]['u_id'] == u_id:
                data['messages'][i]['message'] = "Removed user"
    else:
        raise AccessError("Unauthorised user, user is not an owner")

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    return {}

def notifications_get_v1(token):
    '''
    channel invite, channel addowner, channel removeowner
    message send, message share
    dm create, dm invite, senddm,
    admins
    '''

    # token check
    if check_token_valid(token) is False:
        raise AccessError("Invalid Token")

    with open ("src/data.json") as FILE:
        data = json.load(FILE)
        
    user_id = convert_token(token)
    notifications = []
    count = 0
    for i in range(len(data["notifications"])):
        if count < 20:
            if data["notifications"][i]["u_id"] == user_id:
                notification = {
                    "channel_id": data["notifications"][i]["channel_id"],
                    "dm_id": data["notifications"][i]["dm_id"],
                    "notification_message": data["notifications"][i]["notification_message"]
                }
                notifications.insert(0,notification)
            else:
                break
            count += 1
    
    return {
        "notifications": notifications
    }

