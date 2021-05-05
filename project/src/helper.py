import jwt
import json
from datetime import datetime

from src.error import AccessError

'''
Check if user exists

Arguments:
    u_id (integer) - id of user

Return Value:
    Returns checker (bool)
'''
def check_user_exists(u_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    checker = False
    for i in range(len(data['users'])):
        if data["users"][i]['u_id'] == u_id:
            checker = True

    return checker

def check_token_valid(token):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    valid = False
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            valid = True

    return valid

'''
Check if user is in channel

Arguments:
    u_id (integer) - id of user

Return Value:
    Returns checker (bool)
'''
def check_user_in_channel(u_id, channel_id):
    checker = False

    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    for i in range(len(data['channels'][channel_id]['all_members'])):
        if data['channels'][channel_id]['all_members'][i]["u_id"] == u_id:
            checker = True

    return checker

'''
Check if channel is valid

Arguments:
    channel_id (integer) - id of channel

Return Value:
    Returns checker (bool)
'''
def check_channel_exists(channel_id):
    checker = False
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            checker = True

    return checker

'''
Check if channel is private or not

Arguments:
    channel_id (integer) - id of channel

Return Value:
    Returns checker (bool)
'''
"""
def check_channel_public(channel_id):
    '''checker = False

    for channel in data['channels']:
        if channel['is_public'] == True:
            checker = True

    return checker'''
    return data['channels'][channel_id]['is_public']
"""
signature = 'DORRITO'
def make_token(u_id):
    '''
    creating a token
    '''
    user = {'u_id': u_id}
    return jwt.encode(user, signature, algorithm='HS256')

def convert_token(token):
    '''
    return u_id for a specific token
    '''
    user = jwt.decode(token, signature, algorithms=['HS256'])
    return user["u_id"]

def check_dm_exists(dm_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    checker = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            checker = True
    return checker

def check_user_in_dm(u_id, dm_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    checker = False
    for i in range(len(data["dms"][dm_id]["members"])):
        if u_id == data["dms"][dm_id]["members"][i]["u_id"]:
            checker = True
    return checker

def check_message_exists(message_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    checker = False
    for message in data['messages']:
        if message['message_id'] == message_id:
            checker = True
    return checker

def check_message_sent_by_user(user_id, message_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    checker = False
    for i in range(len(data["messages"])):
        if user_id == data["messages"][message_id]["u_id"]:
            i += 1
            checker = True
    return checker

def create_notifications(u_id,channel_id,dm_id,message):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    notification = {
        "u_id": u_id,
        "channel_id": channel_id,
        "dm_id": dm_id,
        "notification_message": message
    }
    data["notifications"].insert(0,notification)

    with open('src/data.json', 'w') as FILE:
        json.dump(data,FILE, indent = 4)

def check_owner_of_dm(u_id, dm_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    checker = False
    for i in range(len(data["dms"][dm_id]["owner_members"])):
        if u_id == data["dms"][dm_id]["owner_members"][i]["u_id"]:
            checker = True
    return checker

def check_owner_of_channel(u_id, channel_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    checker = False
    for i in range(len(data["channels"][channel_id]["owner_members"])):
        if u_id == data["channels"][channel_id]["owner_members"][i]["u_id"]:
            checker = True
    return checker

def calc_involement_rate(u_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    num_channels_joined = data["user_stats"][u_id]["stats"]["channels_joined"][-1]["num_channels_joined"]
    num_dms_joined = data["user_stats"][u_id]["stats"]["dms_joined"][-1]["num_dms_joined"]
    num_messages_sent = data["user_stats"][u_id]["stats"]["messages_sent"][-1]["num_messages_sent"]

    num_channels = data["dreams_stats"]["channels_exist"][-1]["num_channels_exist"]
    num_dms = data["dreams_stats"]["dms_exist"][-1]["num_dms_exist"]
    num_messages = data["dreams_stats"]["messages_exist"][-1]["num_messages_exist"]

    sum_user = int(num_channels_joined) + int(num_dms_joined) + int(num_messages_sent)
    sum_dreams = int(num_channels) + int(num_dms) + int(num_messages)

    if sum_dreams == 0:
        involvement_rate = 0
    else:
        involvement_rate = round(float(sum_user/sum_dreams), 2)
    
    data["user_stats"][u_id]["stats"]["involvement_rate"] = involvement_rate

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

def calc_utilisation_rate():
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)

    util = 0
    for i in range(len(data["user_stats"])):
        if data["user_stats"][i]["stats"]["channels_joined"][-1]["num_channels_joined"] is not 0 or data["user_stats"][i]["stats"]["dms_joined"][-1]["num_dms_joined"] is not 0:
            util += 1
    
    utilisation_rate = round(util/len(data["users"]),2)

    data["dreams_stats"]["utilization_rate"] = utilisation_rate

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

def create_timestamp():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")

    return timestampStr

def get_new_message_id():
    '''
    returns a new message id
    '''
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    if len(data["messages"]) == 0:
        return 0
    return (int(data['messages'][len(data['messages']) - 1]['message_id']) + 1)
