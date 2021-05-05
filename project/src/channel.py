import json
from src.error import InputError, AccessError
from src.helper import create_notifications,check_user_in_channel, check_user_exists, check_channel_exists, convert_token, make_token, check_owner_of_channel, create_timestamp, calc_involement_rate, calc_utilisation_rate
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.clear import clear_v1

def channel_invite_v2(token, channel_id, u_id):
    '''
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately.

    Arguments:
        auth_user_id (integer)  - id of user sending invite
        channel_id (integer)    - id of channel being invited to
        u_id (integer) - id of user being invited to channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel.
                    - Occurs when u_id does not refer to a valid user
        AccessError - Occurs when the auth_user_id passed in is not valid
                    - Occurs when the authorised user is not already
                    a member of the channel

    Return Value:
        Returns {}
    '''

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check that token is valid
    inviteid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            inviteid = data['users'][i]['u_id']
    if inviteid is None:
        raise AccessError("Invalid token")
    # check if the channel_id exists
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")
    # check if the u_id is valid
    if check_user_exists(u_id) == False:
        raise InputError("Invalid User")
    # checking if the person inviting is in the channel
    if check_user_in_channel(inviteid, channel_id) == False:
        raise AccessError("Authorised user needs to be a member of the channel")
    
    invited_user = {
        'u_id': u_id,
        'email': data["users"][u_id]["email"],
        'name_first': data["users"][u_id]["name_first"],
        'name_last': data["users"][u_id]["name_last"],
        'handle': data["users"][u_id]["handle"]
    }
    # check if the user is already a member of the channel
    for i in range(len(data["channels"][channel_id]["all_members"])):
        if u_id == data["channels"][channel_id]["all_members"][i]["u_id"]:
            raise InputError("User already a member of channel")

    num_channels_joined = data["user_stats"][u_id]["stats"]["channels_joined"][-1]["num_channels_joined"] + 1
    channels_joined = {
        "num_channels_joined": num_channels_joined,
        "time_stamp": create_timestamp()
    }
    
    with open('src/data.json') as FILE:
        data2 = json.load(FILE)
        temp = data2["channels"][channel_id]["all_members"]
        y = invited_user
        temp.append(y)
        # if user invited is an owner
        if data2["users"][u_id]["permission_id"] is 1:
            temp2 = data2["channels"][channel_id]["owner_members"]
            y = invited_user
            temp2.append(y)

        temp3 = data2["user_stats"][u_id]["stats"]["channels_joined"]
        y = channels_joined
        temp3.append(y)
        
    with open ('src/data.json', 'w') as FILE:
        json.dump(data2, FILE, indent = 4)

    notif_msg = data["users"][inviteid]["handle"] + " invited you to " + data["channels"][channel_id]["name"]
    create_notifications(u_id,channel_id,-1,notif_msg)

    calc_involement_rate(u_id)
    calc_utilisation_rate()

    return {}


def channel_details_v2(token, channel_id):
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel

    Arguments:
        auth_user_id (integer)  - id of user who is part of the channel
        channel_id (integer)    - id of channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel.
        AccessError - Occurs when the auth_user_id passed in is not valid 
                    - Occurs when the authorised user is not already
                    a member of the channel
                    
    Return Value:
        Returns {name, owner_members, all_members}
    '''

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check if token exists
    auth_user_id = False
    for i in range(len(data["users"])):
        if data["users"][i]["token"] == token:
            auth_user_id = data["users"][i]["u_id"]
    if auth_user_id is False:
        raise AccessError("Invalid token")
    auth_user_id = convert_token(token)
    # check if the channel_id exists
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")
    # check whether user belongs in this channel 
    if check_user_in_channel(auth_user_id, channel_id) == False:
        raise AccessError("Authorised user needs to be a member of the channel")
    return {
        'name': data["channels"][channel_id]['name'],
        'is_public': data["channels"][channel_id]['is_public'],
        'owner_members': data["channels"][channel_id]['owner_members'],
        'all_members': data["channels"][channel_id]['all_members'],
    }

def channel_messages_v2(token, channel_id, start):
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50".

    Arguments:
        auth_user_id (integer)  - id of user who is part of the channel
        channel_id (integer)    - id of channel
        start (integer)         - index indicating start of messages

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel.
                    - Occurs when start is greater than the total number of messages
                    in the channel.
        AccessError - Occurs when the auth_user_id passed in is not valid
                    - Occurs when the authorised user is not already
                    a member of the channel

    Return Value:
        Returns {messages, start, end}
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check that token is valid
    auth_user_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            auth_user_id = data['users'][i]['u_id']
    if auth_user_id is None:
        raise AccessError("Invalid token")
    # check if the channel_id exists
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")
    # check that user belongs in the channel
    if check_user_in_channel(auth_user_id, channel_id) == False:
        raise AccessError("Authorised user needs to be a member of the channel")

    end = start + 50
    counter = 0
    messagelist1 = []
    messagelist2 = []
    finallist = []
    for i in range(len(data["messages"])):
        if data["messages"][i]["channel_id"] == channel_id:
            messagelist1.insert(0, data["messages"][i])
            messagelist2.append(data["messages"][i])
    # check for start being less than total messages in channel
    if start > len(messagelist1):
        raise InputError("Not enough messages in channel")

    for i in range(start,len(messagelist1)):
        if counter is 50:
            break
        if end > len(messagelist1):
            finallist.append(messagelist1[i])
        else:
            finallist.insert(0, messagelist2[i])
        counter += 1
    if counter < 50:
        end = -1

    return {
        'messages': finallist,
        'start': start,
        'end': end,
    }

def channel_leave_v1(token, channel_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check that token is valid
    u_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data["users"][i]["u_id"]
    if u_id is None:
        raise AccessError("Invalid token")

    # check if the channel_id exists
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")
    # check that the user attempting to leave is a member of the channel
    if check_user_in_channel(u_id, channel_id) == False:
        raise AccessError("Authorised user needs to be a member of the channel")
    
    with open('src/data.json') as FILE:
        data2 = json.load(FILE)

    for i in range(len(data2["channels"][channel_id]["all_members"])):
        if u_id == data2["channels"][channel_id]["all_members"][i]["u_id"]:
            del data2["channels"][channel_id]["all_members"][i]
            break
    for i in range(len(data2["channels"][channel_id]["owner_members"])):
        if u_id == data2["channels"][channel_id]["owner_members"][i]["u_id"]:
            del data2["channels"][channel_id]["owner_members"][i]
            if len(data2["channels"][channel_id]["owner_members"]) == 0 and len(data2["channels"][channel_id]["all_members"]) > 0:
                data2["channels"][channel_id]["owner_members"].append(data2["channels"][channel_id]["all_members"][0])
            break
    
    num_channels_joined = data["user_stats"][u_id]["stats"]["channels_joined"][-1]["num_channels_joined"] - 1
    channels_joined = {
        "num_channels_joined": num_channels_joined,
        "time_stamp": create_timestamp()
    }
    
    data2["user_stats"][u_id]["stats"]["channels_joined"].append(channels_joined)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data2, FILE, indent = 4)

    calc_involement_rate(u_id)
    calc_utilisation_rate()

    return {}

def channel_join_v2(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join,
    adds them to that channel.

    Arguments:
        auth_user_id (integer) - id of user who can join the channel
        channel_id (integer) - id of channel

    Exceptions:
        InputError - Occurs when channel_id does not refer to a valid channel.
        AccessError - Occurs when channel_id refers to a channel that is
                    private (when authorised user is not a global owner)
                    
    Return Value:
        Returns {}
    '''

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check that token is valid
    u_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data['users'][i]['u_id']
    if u_id is None:
        raise AccessError("Invalid token")
    # check if the channel_id exists
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")

    for i in range(len(data['channels'][channel_id]['all_members'])):
        if data['channels'][channel_id]['all_members'][i]['u_id'] == u_id:
            raise InputError("User is already part of the channel")
    
    joining_user = {
        "u_id": u_id,
        'email': data["users"][u_id]["email"],
        'name_first': data["users"][u_id]["name_first"],
        'name_last': data["users"][u_id]["name_last"],
        'handle': data["users"][u_id]["handle"]
    }
   
    if data["channels"][channel_id]["is_public"]:
        if data["users"][u_id]["permission_id"] is 1:
            data["channels"][channel_id]["owner_members"].append(joining_user)
        if len(data["channels"][channel_id]["all_members"]) == 0:
            data["channels"][channel_id]["owner_members"].append(joining_user)
        data["channels"][channel_id]["all_members"].append(joining_user)
    else:
        raise AccessError("Channel is not public")

    num_channels_joined = data["user_stats"][u_id]["stats"]["channels_joined"][-1]["num_channels_joined"] + 1
    channels_joined = {
        "num_channels_joined": num_channels_joined,
        "time_stamp": create_timestamp()
    }
    
    data["user_stats"][u_id]["stats"]["channels_joined"].append(channels_joined)
    
    with open('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    calc_involement_rate(u_id)
    calc_utilisation_rate()

    return {}

def channel_addowner_v1(token, channel_id, u_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check that token is valid
    user_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            user_id = data['users'][i]['u_id']
    if user_id is None:
        raise AccessError("Invalid token")
    # check if the channel_id exists
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")

    # check if the user is already an owner of the channel
    for i in range(len(data["channels"][channel_id]["owner_members"])):
        if data["channels"][channel_id]["owner_members"][i]["u_id"] == u_id:
            raise InputError("User already an owner")
    
    # check if u_id belongs to an existing member of the channel
    if check_user_in_channel(u_id, channel_id) == False:
        raise InputError("User must be a member of the channel to become owner")

    dreamsowner = False
    channelowner = False
    
    # confirm if token belongs to a dream owner
    if data['users'][user_id]['permission_id'] == 1:
        dreamsowner = True
    
    # confirm if token belongs to an owner
    for i in range(len(data["channels"][channel_id]["owner_members"])):
        if data["channels"][channel_id]["owner_members"][i]["u_id"] == user_id:
            channelowner = True

    if dreamsowner or channelowner:
        # information of new owner to be added
        new_owner = {
            "u_id": u_id,
            'email': data["users"][u_id]["email"],
            'name_first': data["users"][u_id]["name_first"],
            'name_last': data["users"][u_id]["name_last"],
            'handle': data["users"][u_id]["handle"]
        }
        data["channels"][channel_id]["owner_members"].append(new_owner)
    else:
        raise AccessError("Unauthorised user, user is not an owner")

    with open('src/data.json', 'w') as FILE:
        json.dump(data,FILE, indent = 4)

    notif_msg = data["users"][u_id]["handle"] + " added you as owner in " + data["channels"][channel_id]["name"]
    create_notifications(u_id,channel_id,-1,notif_msg)

    return {}

def channel_removeowner_v1(token, channel_id, u_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check that token is valid
    removeid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            removeid = data['users'][i]['u_id']
    if removeid is None:
        raise AccessError("Invalid token")
    # check if the channel_id exists
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")

    ownercheck = False
    index = 0

    # make sure person being removed is an existing owner
    for i in range(len(data["channels"][channel_id]["owner_members"])):
        if data["channels"][channel_id]["owner_members"][i]["u_id"] == u_id:
            ownercheck = True
            index = i
    if ownercheck is False:
        raise InputError("User not an owner")

    dreamsowner = False
    channelowner = False
    
    if len(data["channels"][channel_id]["owner_members"]) == 1 and len(data["channels"][channel_id]["all_members"]) == 1:
        raise AccessError("Last member can not remove themselves as an owner")
    # check person trying to remove owner is a dreams owner
    if data['users'][removeid]['permission_id'] == 1:
        dreamsowner = True
    # check person trying to remove owner is a channel owner
    for i in range(len(data["channels"][channel_id]["owner_members"])):
        if data["channels"][channel_id]["owner_members"][i]["u_id"] == removeid:
            channelowner = True
    
    if dreamsowner or channelowner:
        del data["channels"][channel_id]["owner_members"][index]
    else:
        raise AccessError("Unauthorised user, user is not an owner")

    with open('src/data.json', 'w') as FILE:
        json.dump(data,FILE, indent = 4)

    notif_msg = data["users"][removeid]["handle"] + " removed you as owner in " + data["channels"][channel_id]["name"]
    create_notifications(u_id,channel_id,-1,notif_msg)

    return {}