'''
standup.py

Main Modules:
    standup_start: starts a standup in a channel for a set amount of time
    standup_active: checks if there is an active standup in a channel
    standup_send: sends a buffered message to a standup
'''

import json
import time
import threading
from datetime import datetime, timedelta
from src.error import InputError, AccessError
from src.message import message_send_v2
from src.helper import check_user_exists, check_channel_exists, check_user_in_channel, convert_token
from src.clear import clear_v1

def standup_start_v1(token, channel_id, length):
    '''
    Starts a standup in a channel for 'length' seconds.

    Arguments:
        token (string)          - token of user starting standup
        channel_id (integer)    - id of channel standup is in
        length (integer)        - length of the period in which standup is active

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when an active standup is already running in the channel
        AccessError - Occurs when the token passed in is not valid
                    - Occurs when the authorised user is not already
                    a member of the channel

    Return Value:
        Returns {time_finish}
    '''
    # exception checks
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check valid token
    u_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data['users'][i]['u_id']
    if u_id is None:
        raise AccessError("Invalid token")
    # check if channel id is valid
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")
    # check user is in channel
    if check_user_in_channel(u_id, channel_id) == False:
        raise AccessError("Authorised user is not part of the channel")

    standupActive = standup_active_v1(token, channel_id)
    if standupActive['is_active'] == True:
        raise InputError("Active standup is currently running in this channel")

    dateTimeObj = datetime.now()
    timeStampStr = (dateTimeObj + timedelta(seconds=int(length))).strftime("%d-%b-%Y (%H:%M)")
    
    new_standup = {
        'channel_id': channel_id,
        'time_finish': timeStampStr,
        'messages': [],
    }
    data["standups"].append(new_standup)

    # send all messages in standup to channel when standup ends
    time.sleep(length)

    bundledMessages = ''
    allMessages = ''
    for i in range(len(data['standups'])):
        if data['standups'][i]['channel_id'] == channel_id:
            allMessages = data['standups'][i]['messages']
    for i in range(len(allMessages)):
        bundledMessages += allMessages[i]['name'] + ': ' + allMessages[i]['message'] + '\n'
    message_send_v2(token, channel_id, bundledMessages)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    return {'time_finish': timeStampStr}


def standup_active_v1(token, channel_id):
    '''
    Checks if there is an active standup in a channel.

    Arguments:
        token (string)          - token of user starting standup
        channel_id (integer)    - id of channel standup is in

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
        AccessError - Occurs when the token passed in is not valid

    Return Value:
        Returns {is_active, time_finish}
    '''
    # exception checks
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    u_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data['users'][i]['u_id']

    if u_id is None:
        raise AccessError("Invalid token")
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")

    active = False
    timeStampStr = None
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    for i in range(len(data['standups'])):
        if data['standups'][i]['channel_id'] == channel_id:
            active = True
            timeStampStr = data['standups'][i]['time_finish']
            
    return {
        'is_active': active,
        'time_finish': timeStampStr
    }

def standup_send_v1(token, channel_id, message):
    '''
    Starts a standup in a channel for 'length' seconds.

    Arguments:
        token (string)          - token of user starting standup
        channel_id (integer)    - id of channel standup is in
        message (string)        - buffered message that is sent to standup

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when the message is over 1000 characters in length
                    (excluding the name of the user)
                    - Occurs when there is no active standup in the channel
        AccessError - Occurs when the token passed in is not valid
                    - Occurs when the authorised user is not already
                    a member of the channel

    Return Value:
        Returns {}
    '''
    # exception checks
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    u_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data['users'][i]['u_id']
    if u_id is None:
        raise AccessError("Invalid token")
    if check_channel_exists(channel_id) == False:
        raise InputError("Invalid channel")
    if check_user_in_channel(u_id, channel_id) == False:
        raise AccessError("Authorised user is not part of the channel")
    if len(message) > 1000:
        raise InputError("Message is longer than the 1000 character limit")
    standupActive = standup_active_v1(token, channel_id)
    if standupActive['is_active'] == False:
        raise InputError("No active standup running in this channel")

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    for i in range(len(data['users'])):
        if data["users"][i]['token'] == token:
            firstName = data["users"][i]['name_first']
    
    new_message = {
        'name': firstName,
        'message': message
    }
    for i in range(len(data["standups"])):
        if data["standups"][i]["channel_id"] == channel_id:
            data["standups"][i]["messages"].append(new_message)

    return {}