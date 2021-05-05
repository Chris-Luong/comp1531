import json
from datetime import datetime
from src.error import InputError, AccessError
from src.helper import check_user_in_channel, create_notifications, create_timestamp, check_channel_exists, check_user_in_dm, check_user_in_channel, get_new_message_id, check_message_exists, check_message_sent_by_user, calc_involement_rate, calc_utilisation_rate
from src.auth import auth_register_v2
from src.dm import dm_create_v1
from src.channels import channels_create_v2
from src.clear import clear_v1
from src.helper import check_owner_of_channel, check_owner_of_dm, check_dm_exists
from datetime import datetime
import time

def message_send_v2(token, channel_id, message):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    u_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data["users"][i]["u_id"]
    if u_id is None:
        raise AccessError("Invalid token")
    if len(message) > 1000:
        raise InputError("Message is longer than the 1000 character limit")
    if check_user_in_channel(u_id, channel_id) == False:
        raise AccessError("Authorised user is not part of the channel")
    dm_id = -1

    new_message = {
        'message_id': get_new_message_id(),
        'u_id': u_id,
        'message': message,
        'time_created': create_timestamp(),
        'channel_id': channel_id,
        'dm_id': dm_id,
        'reacts': [
            {
                'react_id': 1, 
                'u_ids': [], 
                'is_this_user_reacted': False
            }
        ],
        'is_pinned': False

    }

    data["messages"].append(new_message)

    num_messages_sent = data["user_stats"][u_id]["stats"]["messages_sent"][-1]["num_messages_sent"] + 1
    messages_sent = {
        "num_messages_sent": num_messages_sent,
        "time_stamp": create_timestamp()
    }
    data["user_stats"][u_id]["stats"]["messages_sent"].append(messages_sent)

    num_messages = data["dreams_stats"]["messages_exist"][-1]["num_messages_exist"] + 1
    dreams_messages = {
        "num_messages_exist": num_messages,
        "time_stamp": create_timestamp()
    }
    data["dreams_stats"]["messages_exist"].append(dreams_messages)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    calc_involement_rate(u_id)
    calc_utilisation_rate()

    return {
        'message_id': new_message["message_id"],
    }

def message_remove_v1(token, message_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check to see if message exists
    if check_message_exists(message_id) == False:
        raise InputError("Message does not exist")
    u_id = None
    # token check
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data["users"][i]["u_id"]
    if u_id is None:
        raise AccessError("Invalid token")
    # check message was sent by the authorised user making the request
    valid = True
    if check_message_sent_by_user(u_id, message_id) == False:
        valid = False
    # check to see if token belongs to the owner of message being deleted
    for i in range(len(data["messages"])):
        if data["messages"][i]["message_id"] == message_id:
            channel_id = data["messages"][i]["channel_id"]

    if channel_id is not -1:
        for i in range(len(data["channels"][channel_id]["owner_members"])):
            if data["channels"][channel_id]["owner_members"][i]["u_id"] == u_id:
                valid = True
        if valid == False:
            raise AccessError("Authorised User is not the owner of this channel and did not send this message")
    else:
        if valid == False:
            raise AccessError("Authorised User is not the owner of this dm and did not send this message")
    
    num_messages_sent = data["user_stats"][u_id]["stats"]["messages_sent"][-1]["num_messages_sent"] - 1
    messages_sent = {
        "num_messages_sent": num_messages_sent,
        "time_stamp": create_timestamp()
    }
    data["user_stats"][u_id]["stats"]["messages_sent"].append(messages_sent)

    num_messages = data["dreams_stats"]["messages_exist"][-1]["num_messages_exist"] - 1
    dreams_messages = {
        "num_messages_exist": num_messages,
        "time_stamp": create_timestamp()
    }
    data["dreams_stats"]["messages_exist"].append(dreams_messages)

    for i in range(len(data["messages"])):
        if data["messages"][i]["message_id"] == message_id:
            del data["messages"][i]
            break 
    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    calc_involement_rate(u_id)
    calc_utilisation_rate()

    return {}

def message_edit_v2(token, message_id, message):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    editorid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            editorid = data["users"][i]["u_id"]
    if editorid is None:
        raise AccessError("Invalid token")
    if len(message) > 1000:
        raise InputError("Message is longer than the 1000 character limit")
    # check to see if message exists
    if check_message_exists(message_id) == False:
        raise InputError("Message does not exist")
    # check to see if message is being edited by authorised user
    valid = True
    if check_message_sent_by_user(editorid, message_id) == False:
        valid = False
    # check to see if token belongs to the owner of channel being deleted
    for i in range(len(data["messages"])):
        if data["messages"][i]["message_id"] == message_id:
            channel_id = data["messages"][i]["channel_id"]
            
    if channel_id is not -1:
        for i in range(len(data["messages"])):
            if data["messages"][i]["message_id"] == message_id:
                channel_id = data["messages"][i]["channel_id"]
        for i in range(len(data["channels"][channel_id]["owner_members"])):
            if data["channels"][channel_id]["owner_members"][i]["u_id"] == editorid:
                valid = True
        if valid == False:
            raise AccessError("Authorised User is not the owner of this channel and did not send this message")
    else:
        if valid == False:
            raise AccessError("Authorised User is not the owner of this dm and did not send this message")

    with open('src/data.json') as FILE:
        data2 = json.load(FILE)
    for i in range(len(data2["messages"]) - 1):
        if data2["messages"][i]["message_id"] == message_id:
            if message is '':
                del data2["messages"][i]
            else:
                data2["messages"][i]["message"] = message
    with open ('src/data.json', 'w') as FILE:
        json.dump(data2, FILE, indent = 4)
    return {}

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check token
    shareid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            shareid = data["users"][i]["u_id"]
    if shareid is None:
        raise AccessError("Invalid token")
    # check whether user is part of the channel/dm
    if channel_id == -1:
        if check_user_in_dm(shareid, dm_id) == False:
            raise AccessError("Authorised user is not part of the channel")
        new_message = message + "\n\"\"\"\n" + data["messages"][og_message_id]["message"] + "\n\"\"\""
        shared_message_id = message_senddm_v1(token, dm_id, new_message)

    if dm_id == -1:
        if check_user_in_channel(shareid, channel_id) == False:
            raise AccessError("Authorised user needs to be a member of the dm")
        new_message = message + "\n\"\"\"\n" + data["messages"][og_message_id]["message"] + "\n\"\"\""
        shared_message_id = message_send_v2(token, channel_id, new_message)

    return {
        'shared_message_id': shared_message_id["message_id"],
    }

def message_senddm_v1(token, dm_id, message):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    u_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data["users"][i]["u_id"]
    if u_id is None:
        raise AccessError("Invalid token")
    if len(message) > 1000:
        raise InputError("Message is longer than the 1000 character limit")
    if check_user_in_dm(u_id, dm_id) == False:
        raise AccessError("Authorised user is not part of the channel")
    channel_id = -1

    new_message = {
        'message_id': get_new_message_id(),
        'u_id': u_id,
        'message': message,
        'time_created': create_timestamp(),
        'channel_id': channel_id,
        'dm_id': dm_id,
        'reacts': [
            {
                'react_id': 1, 
                'u_ids': [], 
                'is_this_user_reacted': False
            }
        ],
        'is_pinned': False
    }

    num_messages_sent = data["user_stats"][u_id]["stats"]["messages_sent"][-1]["num_messages_sent"] + 1
    messages_sent = {
        "num_messages_sent": num_messages_sent,
        "time_stamp": create_timestamp()
    }
    data["user_stats"][u_id]["stats"]["messages_sent"].append(messages_sent)

    num_messages = data["dreams_stats"]["messages_exist"][-1]["num_messages_exist"] + 1
    dreams_messages = {
        "num_messages_exist": num_messages,
        "time_stamp": create_timestamp()
    }
    data["dreams_stats"]["messages_exist"].append(dreams_messages)
    data["messages"].append(new_message)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    calc_involement_rate(u_id)
    calc_utilisation_rate()

    return {
        'message_id': new_message["message_id"],
    }

def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    Send a message from authorised_user to the channel specified
    by channel_id automatically at a specified time in the future 
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check for valid token and get u_id
    senderid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            senderid = data["users"][i]["u_id"]
    if senderid is None:
        raise AccessError("Invalid token")
    # check that the channel_id is valid
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")
    # check that the message does not contain more than 1000 characters
    if len(message) > 1000:
        raise InputError("Message is longer than the 1000 character limit")
    # check sender is part of the channel
    if check_user_in_channel(senderid, channel_id) == False:
        raise AccessError("Authorised user is not part of the channel")
    now = datetime.now()
    if int(time_sent) < int(datetime.timestamp(now)):
         raise InputError("Time sent is in the past")
    timeout = int(time_sent) - int(datetime.timestamp(now))
    
    time.sleep(timeout)
    dm_id = -1
    new_message = {
        'message_id': get_new_message_id(),
        'u_id': senderid,
        'message': message,
        'time_created': time_sent,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'reacts': [
            {
                'react_id': 1, 
                'u_ids': [], 
                'is_this_user_reacted': False
            }
        ],
        'is_pinned': False
    }

    num_messages_sent = data["user_stats"][senderid]["stats"]["messages_sent"][-1]["num_messages_sent"] + 1
    messages_sent = {
        "num_messages_sent": num_messages_sent,
        "time_stamp": time_sent
    }
    data["user_stats"][senderid]["stats"]["messages_sent"].append(messages_sent)

    num_messages = data["dreams_stats"]["messages_exist"][-1]["num_messages_exist"] + 1
    dreams_messages = {
        "num_messages_exist": num_messages,
        "time_stamp": time_sent
    }
    data["dreams_stats"]["messages_exist"].append(dreams_messages)


    data["messages"].append(new_message)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    calc_involement_rate(senderid)
    calc_utilisation_rate()

    return {
        'message_id': new_message["message_id"],
    }

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    Send a message from authorised_user to the channel specified
    by channel_id automatically at a specified time in the future 
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check for valid token and get u_id
    senderid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            senderid = data["users"][i]["u_id"]
    if senderid is None:
        raise AccessError("Invalid token")
    # check that the channel_id is valid
    if check_dm_exists(dm_id) == False:
        raise InputError("Invalid dm")
    # check that the message does not contain more than 1000 characters
    if len(message) > 1000:
        raise InputError("Message is longer than the 1000 character limit")
    # check sender is part of the channel
    if check_user_in_dm(senderid, dm_id) == False:
        raise AccessError("Authorised user is not part of the dm")
    # check time sent is not in the past
    now = datetime.now()
    if int(time_sent) < int(datetime.timestamp(now)):
         raise InputError("Time sent is in the past")
    timeout = int(time_sent) - int(datetime.timestamp(now))
    
    time.sleep(timeout)
    channel_id = -1
    new_message = {
        'message_id': get_new_message_id(),
        'u_id': senderid,
        'message': message,
        'time_created': time_sent,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'reacts': [
            {
                'react_id': 1, 
                'u_ids': [], 
                'is_this_user_reacted': False
            }
        ],
        'is_pinned': False
    }

    num_messages_sent = data["user_stats"][senderid]["stats"]["messages_sent"][-1]["num_messages_sent"] + 1
    messages_sent = {
        "num_messages_sent": num_messages_sent,
        "time_stamp": time_sent
    }
    data["user_stats"][senderid]["stats"]["messages_sent"].append(messages_sent)

    num_messages = data["dreams_stats"]["messages_exist"][-1]["num_messages_exist"] + 1
    dreams_messages = {
        "num_messages_exist": num_messages,
        "time_stamp": time_sent
    }
    data["dreams_stats"]["messages_exist"].append(dreams_messages)

    data["messages"].append(new_message)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    calc_involement_rate(senderid)
    calc_utilisation_rate()

    return {
        'message_id': new_message["message_id"],
    }

def message_react_v1(token, message_id, react_id):
    ''' 
    Given a message within a channel the authorised user is
    part of, add a "react" to that particular message
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check for valid token and get u_id
    reactorid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            reactorid = data["users"][i]["u_id"]
    if reactorid is None:
        raise AccessError("Invalid token")
    # check message exists
    if check_message_exists(message_id) == False:
        raise InputError("Message does not exist")
    # check whether user is within channel/Dm which the message is in
    for i in range(len(data["messages"])):
        if data["messages"][i]["message_id"] == message_id:
            channel_id = data["messages"][i]["channel_id"]
            dm_id = data["messages"][i]["dm_id"]
    
    if channel_id == -1:
        if check_user_in_dm(reactorid, dm_id) == False:
            raise AccessError("Authorised user is not part of the dm")
    if dm_id == -1:
        if check_user_in_channel(reactorid, channel_id) == False:
            raise AccessError("Authorised user is not part of the channel")
    # check react_id is valid
    if react_id != 1:
        raise InputError("Invalid react_id")
    reacts_list = data["messages"][message_id]["reacts"]
    # check if react_id already exists
    if reactorid in reacts_list[int(react_id) - 1]['u_ids']:
        raise InputError("Message already contains this react_id")
    # adding the u_id of the person making a react
    reacts_list[int(react_id) - 1]['u_ids'].append(reactorid)
    reacts_list[int(react_id) - 1]['is_this_user_reacted'] = True

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    return {}

def message_unreact_v1(token, message_id, react_id):
    ''' 
    Given a message within a channel the authorised user is
    part of, remove a "react" to that particular message
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check for valid token and get u_id
    reactorid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            reactorid = data["users"][i]["u_id"]
    if reactorid is None:
        raise AccessError("Invalid token")
    # check message exists
    if check_message_exists(message_id) == False:
        raise InputError("Message does not exist")
    # check whether user is within channel/Dm which the message is in
    for i in range(len(data["messages"])):
        if data["messages"][i]["message_id"] == message_id:
            channel_id = data["messages"][i]["channel_id"]
            dm_id = data["messages"][i]["dm_id"]
    
    if channel_id == -1:
        if check_user_in_dm(reactorid, dm_id) == False:
            raise AccessError("Authorised user is not part of the dm")
    if dm_id == -1:
        if check_user_in_channel(reactorid, channel_id) == False:
            raise AccessError("Authorised user is not part of the channel")
    # check react_id is valid
    if react_id != 1:
        raise InputError("Invalid react_id")
    reacts_list = data["messages"][message_id]["reacts"]
    # check if react_id already exists
    if reactorid not in reacts_list[int(react_id) - 1]['u_ids']:
        raise InputError("Message does not contain this react_id")
    # removing the u_id of the person who reacted
    reacts_list[int(react_id) - 1]['u_ids'].remove(reactorid)
    reacts_list[int(react_id) - 1]['is_this_user_reacted'] = False
    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    return {}

def message_pin_v1(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to
    be given special display treatment by the frontend
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check for valid token and get u_id
    pinnerid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            pinnerid = data["users"][i]["u_id"]
    if pinnerid is None:
        raise AccessError("Invalid token")
    # check that message_id is valid
    if check_message_exists(message_id) == False:
        raise InputError("Message does not exist")
    for i in range(len(data["messages"])):
        if data["messages"][i]["message_id"] == message_id:
            channel_id = data["messages"][i]["channel_id"]
            dm_id = data["messages"][i]["dm_id"]
    # check whether user is within channel/Dm which the message is in
    if channel_id == -1:
        if check_user_in_dm(pinnerid, dm_id) == False:
            raise AccessError("Authorised user is not part of the dm")
        if check_owner_of_dm(pinnerid, dm_id) == False:
            raise AccessError("Authorised user is not an owner of the dm")
    if dm_id == -1:
        if check_user_in_channel(pinnerid, channel_id) == False:
            raise AccessError("Authorised user is not part of the channel")
        if check_owner_of_channel(pinnerid, channel_id) == False:
            raise AccessError("Authorised user is not an owner of the channel")
    # check whether the message is already pinned
    if data["messages"][message_id]['is_pinned']:
        raise InputError("Message is already pinned")
    # pin the message
    data["messages"][message_id]['is_pinned'] = True
    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    return {}

def message_unpin_v1(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to
    be given special display treatment by the frontend
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check for valid token and get u_id
    pinnerid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            pinnerid = data["users"][i]["u_id"]
    if pinnerid is None:
        raise AccessError("Invalid token")
    # check that message_id is valid
    if check_message_exists(message_id) == False:
        raise InputError("Message does not exist")
    for i in range(len(data["messages"])):
        if data["messages"][i]["message_id"] == message_id:
            channel_id = data["messages"][i]["channel_id"]
            dm_id = data["messages"][i]["dm_id"]
    # check whether user is within channel/Dm which the message is in
    if channel_id == -1:
        if check_user_in_dm(pinnerid, dm_id) == False:
            raise AccessError("Authorised user is not part of the dm")
        if check_owner_of_dm(pinnerid, dm_id) == False:
            raise AccessError("Authorised user is not an owner of the dm")
    if dm_id == -1:
        if check_user_in_channel(pinnerid, channel_id) == False:
            raise AccessError("Authorised user is not part of the channel")
        if check_owner_of_channel(pinnerid, channel_id) == False:
            raise AccessError("Authorised user is not an owner of the channel")
    # check whether the message is already unpinned
    if data["messages"][message_id]['is_pinned'] == False:
        raise InputError("Message is already unpinned")
    # unpin the message
    data["messages"][message_id]['is_pinned'] = False
    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    return {}
