import hashlib
import json
from src.helper import make_token, create_timestamp, calc_utilisation_rate, calc_involement_rate
from src.helper import convert_token
from src.error import InputError
from src.error import AccessError
from src.auth import auth_register_v2
from src.clear import clear_v1

def channels_list_v2(token):
    '''
    Provides a list of all channels (and their associated details) that
    the authorised user is part of

    Arguments:
        auth_user_id (integer) - id of user whose channels are to be listed

    Exceptions:
        AccessError - Occurs when the authorised user does not have a corresponding
                      u_id
    Return Value:
        {channels}
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check if token is valid - still have to do
    userch = []
    auth_user_id = None

    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            auth_user_id = data['users'][i]['u_id']
    if auth_user_id is None:
        raise AccessError("Invalid token")
    
    for channel in data['channels']:
        for user in channel['all_members']:
            if auth_user_id == user['u_id']:
                new_dict = {
                    'channel_id': channel["channel_id"],
                    'name': channel['name']
                }
                userch.append(new_dict)
    return {
        'channels': userch
    }

def channels_listall_v2(token):
    '''
    Provides a list of all channels (and their associated details)

    Arguments:
        auth_user_id (integer) - id of user whose channels are to be listed

    Exceptions:
        AccessError - Occurs when the authorised user does not have a corresponding
                      u_id
    Return Value:
        { channels }
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check if token is valid - still have to do
    auth_user_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            auth_user_id = int(data['users'][i]['u_id'])
    if auth_user_id is None:
        raise AccessError("Invalid token")
    userch = []
    for channel in data['channels']:
        new_dict = {
            'channel_id': channel["channel_id"],
            'name': channel['name']
        }
        userch.append(new_dict)
    return {
        'channels': userch
    }

def channels_create_v2(token, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel

    Arguments:
        auth_user_id (integer) - id of user who will own the new channel created
        name (string) - name of channel to be created
        is_public (boolean) - confirms whether channel is public or private

    Return Value:
        { channel_id }
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    u_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data['users'][i]['u_id']
    if u_id is None:
        raise AccessError("Invalid token")
    if len(name) > 20:
        raise InputError("Name is longer than the 20 character limit")
    new_user = {
        'u_id': u_id,
        'email': data["users"][u_id]["email"],
        'name_first': data["users"][u_id]["name_first"],
        'name_last': data["users"][u_id]["name_last"],
        'handle': data["users"][u_id]["handle"]
    }
    # store the details of the new channel in a dictionary
    new_channel = {
        "channel_id": len(data["channels"]),
        "name": name,
        "owner_members": [],
        "all_members": [],
        "is_public": is_public,
    }
    # add the creator of the channel to the owners list and members list
    new_channel["owner_members"].append(new_user)
    new_channel["all_members"].append(new_user)

    num_channels_joined = data["user_stats"][u_id]["stats"]["channels_joined"][-1]["num_channels_joined"] + 1
    channels_joined = {
        "num_channels_joined": num_channels_joined,
        "time_stamp": create_timestamp()
    }

    num_channels = data["dreams_stats"]["channels_exist"][-1]["num_channels_exist"] + 1
    dreams_channels = {
        "num_channels_exist": num_channels,
        "time_stamp": create_timestamp()
    }

    with open('src/data.json') as FILE:
        data2 = json.load(FILE)
        temp = data2["channels"]
        y = new_channel
        temp.append(y)

        temp2 = data2["user_stats"][u_id]["stats"]["channels_joined"]
        z = channels_joined
        temp2.append(z)

        temp3 = data2["dreams_stats"]["channels_exist"]
        x = dreams_channels
        temp3.append(x)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data2, FILE, indent = 4)

    calc_involement_rate(u_id)
    calc_utilisation_rate()
        
    return {
        'channel_id': new_channel["channel_id"]
    }
