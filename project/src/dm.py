import json
from src.helper import check_user_in_dm, create_notifications, convert_token, calc_involement_rate, calc_utilisation_rate, create_timestamp, \
    check_user_exists, check_dm_exists, check_owner_of_dm
from src.error import InputError, AccessError
from src.clear import clear_v1

def dm_details_v1(token, dm_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check if token exists
    auth_user_id = None
    for user in data["users"]:
        if user["token"] == token:
            auth_user_id = user["u_id"]
    if auth_user_id is None:
        raise AccessError("Invalid token")
    # check if the dm_id exists
    if check_dm_exists(dm_id) == False:
        raise InputError("Invalid dm")
    # check whether user belongs in this dm 
    if check_user_in_dm(auth_user_id, dm_id) == False:
        raise AccessError("Authorised user needs to be a \
        member of the dm")
    return {
        'name': data["dms"][dm_id]['name'],
        'members': data["dms"][dm_id]['members']
    }

def dm_list_v1(token):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check if token is valid
    dmlist = []
    auth_user_id = None
    for user in data["users"]:
        if user["token"] == token:
            auth_user_id = user["u_id"]
    if auth_user_id is None:
        raise AccessError("Invalid token")
    for dm in data["dms"]:
        for user in dm['members']:
            if auth_user_id == user['u_id']:
                new_dm = {
                    "dm_id": dm['dm_id'],
                    "name": dm['name'],
                    "members": dm['members'],
                    "owner_members": dm['owner_members']
                }
                dmlist.append(new_dm)
    return {
        'dms': dmlist
    }

def dm_create_v1(token, u_ids):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    u_id = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            # getting the specfic u_id for the owner
            u_id = data['users'][i]['u_id']   
    if u_id is None:
        raise AccessError("Invalid token")
    new_dm = {
        "dm_id": len(data["dms"]),
        "name": [],
        "members": [],
        "owner_members": [],
    }
    new_owner = {
        'u_id': u_id,
        'email': data["users"][u_id]["email"],
        'name_first': data["users"][u_id]["name_first"],
        'name_last': data["users"][u_id]["name_last"],
        'handle': data["users"][u_id]["handle"]
    }
    new_dm["owner_members"].append(new_owner)
    new_dm["members"].append(new_owner)
    # go through each u_id separately
    '''
    u_ids contains the user(s) that this DM is directed to, and will not include the creator. 
    '''
    memberslist = []
    for user_id in u_ids:
        '''
        name should be automatically generated based on the user(s) that is 
        in this dm (have to also include owner). The name should be an 
        alphabetically-sorted, comma-separated list of user handles, 
        e.g. 'handle1, handle2, handle3'.
        '''
        if check_user_exists(user_id) == False:
            raise InputError("Invalid User")
        handlenew = data['users'][user_id]['handle']
        new_user = {
            'u_id': user_id,
            'email': data["users"][user_id]["email"],
            'name_first': data["users"][user_id]["name_first"],
            'name_last': data["users"][user_id]["name_last"],
            'handle': handlenew
        }  
        memberslist.append(handlenew)
        # adding user info into dm member list
        new_dm["members"].append(new_user)
    memberslist.append(data["users"][u_id]["handle"])

    sortedlist = sorted(memberslist, key=str.lower)
    new_dm["name"] = ", ".join(sortedlist)
    data["dms"].append(new_dm)
    
    num_dms_joined = data["user_stats"][u_id]["stats"]["dms_joined"][-1]["num_dms_joined"] + 1
    dms_joined = {
        "num_dms_joined": num_dms_joined,
        "time_stamp": create_timestamp()
    }
    data["user_stats"][u_id]["stats"]["dms_joined"].append(dms_joined)

    for user_id in u_ids:
        num_dms_joined = data["user_stats"][user_id]["stats"]["dms_joined"][-1]["num_dms_joined"] + 1
        dms_joined = {
            "num_dms_joined": num_dms_joined,
            "time_stamp": create_timestamp()
        }
        data["user_stats"][user_id]["stats"]["dms_joined"].append(dms_joined)

    num_dms = data["dreams_stats"]["dms_exist"][-1]["num_dms_exist"] + 1
    dreams_dms = {
        "num_dms_exist": num_dms,
        "time_stamp": create_timestamp()
    }
    
    data["dreams_stats"]["dms_exist"].append(dreams_dms)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)
    with open ('src/data.json', 'r') as FILE:
        data2 = json.load(FILE)
    
    dm_id = len(data2["dms"])-1
    
    notif_msg = data2["users"][u_id]["handle"] + " added you to dm " + data2["dms"][dm_id]["name"]
    for i in range(len(data2["dms"][dm_id]["members"])):
        member_id = data2["dms"][dm_id]["members"][i]["u_id"]
        if member_id == u_id:
            pass
        else:
            create_notifications(member_id,-1,dm_id,notif_msg)

    calc_involement_rate(u_id)
    for user_id in u_ids:
        calc_involement_rate(user_id)
    calc_utilisation_rate()

    return {
        'dm_id': new_dm["dm_id"],
        'dm_name': new_dm["name"]
    }

def dm_remove_v1(token, dm_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    u_id = None
    # check that token is valid and that the token belongs to the owner
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            u_id = data['users'][i]['u_id']   
    if u_id is None:
        raise AccessError("Invalid token")
    # check if the dm_id exists
    if check_dm_exists(dm_id) == False:
        raise InputError("Invalid dm")
    # check that the owner is attempting to remove
    if check_owner_of_dm(u_id, dm_id) == False:
        raise AccessError("Only the dm owner can delete this dm")

    for i in range(len(data["dms"])):
        if data["dms"][i]["dm_id"] == dm_id:
            for j in range(len(data["dms"][dm_id]["members"])):
                u_id = data["dms"][dm_id]["members"][j]["u_id"]
                num_dms_joined = data["user_stats"][u_id]["stats"]["dms_joined"][-1]["num_dms_joined"] - 1
                dms_joined = {
                    "num_dms_joined": num_dms_joined,
                    "time_stamp": create_timestamp()
                }
                data["user_stats"][u_id]["stats"]["dms_joined"].append(dms_joined)

    num_dms = data["dreams_stats"]["dms_exist"][-1]["num_dms_exist"] - 1
    dreams_dms = {
        "num_dms_exist": num_dms,
        "time_stamp": create_timestamp()
    }
    data["dreams_stats"]["dms_exist"].append(dreams_dms)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    with open('src/data.json') as FILE:
        data2 = json.load(FILE)
        for i in range(len(data2["dms"])):
            if data2["dms"][i]["dm_id"] == dm_id:
                del data2["dms"][i]
                break
     
    with open ('src/data.json', 'w') as FILE:
        json.dump(data2, FILE, indent = 4)
    
    calc_involement_rate(u_id)
    for u_id in range(len(data["dms"][dm_id]["members"])):
        calc_involement_rate(u_id)
    calc_utilisation_rate()

    return {}

def dm_invite_v1(token, dm_id, u_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    inviteid = None
    # check that token is valid
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            inviteid = data["users"][i]["u_id"]
    if inviteid is None:
        raise AccessError("Invalid token")
    # check if the dm_id exists
    if check_dm_exists(dm_id) == False:
        raise InputError("Invalid dm")
    # check if the u_id is valid
    if check_user_exists(u_id) == False:
        raise InputError("Invalid User")
    # checking if the person inviting is in the dm
    if check_user_in_dm(inviteid, dm_id) == False:
        raise AccessError("Authorised user needs to be a member of the dm")
    # checking if the person being invited is already in the dm
    if check_user_in_dm(u_id, dm_id) == True:
        raise InputError("User already a member of this dm")
    new_user = {
        'u_id': u_id,
        'email': data["users"][u_id]["email"],
        'name_first': data["users"][u_id]["name_first"],
        'name_last': data["users"][u_id]["name_last"],
        'handle': data["users"][u_id]["handle"]
    }

    memberslist = data["dms"][dm_id]["name"].split(", ")
    memberslist.append(data["users"][u_id]["handle"])
    sortedlist = sorted(memberslist, key=str.lower)
    final_list = ", ".join(sortedlist)
    
    #name = data["dms"][dm_id]["name"] + ", " + data["users"][u_id]["handle"]
    data["dms"][dm_id]["members"].append(new_user)
    data["dms"][dm_id]["name"] = final_list


    num_dms_joined = data["user_stats"][u_id]["stats"]["dms_joined"][-1]["num_dms_joined"] + 1
    dms_joined = {
        "num_dms_joined": num_dms_joined,
        "time_stamp": create_timestamp()
    }
    data["user_stats"][u_id]["stats"]["dms_joined"].append(dms_joined)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    notif_msg = data["users"][inviteid]["handle"] + " added you to dm " + final_list
    create_notifications(u_id,-1,dm_id,notif_msg)

    calc_involement_rate(u_id)
    calc_utilisation_rate()

    return {}

def dm_leave_v1(token, dm_id):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check that token is valid
    leaveid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            leaveid = data["users"][i]["u_id"]
    if leaveid is None:
        raise AccessError("Invalid token")
    # check if the dm_id exists
    if check_dm_exists(dm_id) == False:
        raise InputError("Invalid dm")
    # check that the user attempting to leave is a member of the dm
    if check_user_in_dm(leaveid, dm_id) == False:
        raise AccessError("Authorised user needs to be a member of the dm")
    
    memberslist = data["dms"][dm_id]["name"].split(", ")
    memberslist.remove(data["users"][leaveid]["handle"])
    final_list = ", ".join(memberslist)

    data["dms"][dm_id]["name"] = final_list

    for i in range(len(data["dms"][dm_id]["members"])):
        if leaveid == data["dms"][dm_id]["members"][i]["u_id"]:
            del data["dms"][dm_id]["members"][i]
            break

    for i in range(len(data["dms"][dm_id]["owner_members"])):
        if leaveid == data["dms"][dm_id]["owner_members"][i]["u_id"]:
            del data["dms"][dm_id]["owner_members"][i]
            data["dms"][dm_id]["owner_members"].append(data["dms"][dm_id]["members"][0])
    
    num_dms_joined = data["user_stats"][leaveid]["stats"]["dms_joined"][-1]["num_dms_joined"] - 1
    dms_joined = {
        "num_dms_joined": num_dms_joined,
        "time_stamp": create_timestamp()
    }
    data["user_stats"][leaveid]["stats"]["dms_joined"].append(dms_joined)

    with open ('src/data.json', 'w') as FILE:
        json.dump(data, FILE, indent = 4)

    calc_involement_rate(leaveid)
    calc_utilisation_rate()

    return {}

def dm_messages_v1(token, dm_id, start):
    with open('src/data.json', 'r') as FILE:
        data = json.load(FILE)
    # check that token is valid
    userid = None
    for i in range(len(data['users'])):
        if data['users'][i]['token'] == token:
            userid = data['users'][i]['u_id']
    if userid is None:
        raise AccessError("Invalid token")
    # check if the dm_id exists
    if check_dm_exists(dm_id) == False:
        raise InputError("Invalid dm")
    # check user belongs in dm
    if check_user_in_dm(userid, dm_id) == False:
        raise AccessError("Authorised User must be a part of the dm")
    
    end = start + 50
    counter = 0
    messagelist1 = []
    messagelist2 = []
    finallist = []
    for i in range(len(data["messages"])):
        if data["messages"][i]["dm_id"] == dm_id:
            messagelist1.insert(0, data["messages"][i])
            messagelist2.append(data["messages"][i])
    # check for start being less than total messages in dm
    if start > len(messagelist1):
        raise InputError("Not enough messages in dm")

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
