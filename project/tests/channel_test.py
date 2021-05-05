from src.auth import auth_register_v2
from src.auth import auth_login_v2
from src.channels import channels_create_v2
from src.channel import channel_invite_v2
from src.channel import channel_details_v2
from src.channel import channel_join_v2
from src.channel import channel_leave_v1
from src.channel import channel_addowner_v1
from src.channel import channel_removeowner_v1
from src.channel import channel_messages_v2
from src.message import message_send_v2
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.helper import make_token
from datetime import datetime
import pytest

@pytest.fixture
def user_setup():
    '''
    Clear history of all current users then register and login new users
    '''
    clear_v1()
    # register 3 users with email, password, first name and last name
    # first user is the dream owner
    auth_register_v2("gungeetsingh@email.com", "password", "Gungeet", "Singh")
    auth_register_v2("petertran@email.com", "password", "Peter", "Tran")
    auth_register_v2("christopherluong@email.com", "password", "Christopher", "Luong")
    auth_register_v2("talavrahami@email.com", "password", "Tal", "Avrahami")
    # login the 3 users who have been registered
    auth_login_v2("gungeetsingh@email.com", "password")
    auth_login_v2("petertran@email.com", "password")
    auth_login_v2("christopherluong@email.com", "password")
    auth_login_v2("talavrahami@email.com", "password")

@pytest.fixture
def channel_setup():
    # create multiple public channels for single user (Non-dream owner)
    channels_create_v2(make_token(1), "PublicChannel1", True)
    channels_create_v2(make_token(1), "PublicChannel2", True)
    channels_create_v2(make_token(1), "PublicChannel3", True)
    # create multiple private channels for single user
    channels_create_v2(make_token(1), "PrivateChannel1", False)
    channels_create_v2(make_token(1), "PrivateChannel2", False)
    channels_create_v2(make_token(1), "PrivateChannel3", False)

# invites a user by adding them to the channel immediately
# ensures the output is an empty dictionary
# AND assumes that channel_details_v2() works to determine that the invite has worked

# Test 1:
# invites one user to three public channels
def test_channel_invite_v2_multiple_public(user_setup, channel_setup):
    
    assert channel_invite_v2(make_token(1), 0, 2) == {}
    assert channel_details_v2(make_token(1), 0) == {
        'name': 'PublicChannel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': "Peter",
                'name_last': "Tran",
                'handle': "petertran"
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': "Peter",
                'name_last': "Tran",
                'handle': "petertran"
            },
            {
                'u_id': 2,
                'email': "christopherluong@email.com",
                'name_first': "Christopher",
                'name_last': "Luong",
                'handle': "christopherluong"
            }
        ]
    }

# Test 2:
# invites one user to three private channels
def test_channel_invite_v2_multiple_private(user_setup, channel_setup):
    assert channel_invite_v2(make_token(1), 3, 2) == {}
    assert channel_details_v2(make_token(1), 3) == {
        'name': 'PrivateChannel1',
        'is_public': False,
        'owner_members': [
            {
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': "Peter",
                'name_last': "Tran",
                'handle': "petertran"
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': "Peter",
                'name_last': "Tran",
                'handle': "petertran"
            },
            {
                'u_id': 2,
                'email': "christopherluong@email.com",
                'name_first': "Christopher",
                'name_last': "Luong",
                'handle': "christopherluong"
            }
        ]
    }

# Test 3
# Test the errors for channel_invite_v2
def test_channel_invite_v2_errors(user_setup, channel_setup):

    # invites an invalid user to a private channel
    with pytest.raises(InputError):
        channel_invite_v2(make_token(1), 5, 10)

    # invites an invalid user to a public channel
    with pytest.raises(InputError):
        channel_invite_v2(make_token(1), 2, 10)

    # invites a user to an invalid channel
    with pytest.raises(InputError):
        channel_invite_v2(make_token(1), 10, 2)

    # invitation to a channel from an invalid user
    with pytest.raises(AccessError):
        channel_invite_v2(make_token(10), 4, 2)

    # the authorised user sending an invite is not a member of the channel
    with pytest.raises(AccessError):
        channel_invite_v2(make_token(0), 4, 3)

# Test 4
def test_channel_details_v2_errors(user_setup, channel_setup):

    # invalid channel
    with pytest.raises(InputError):
        channel_details_v2(make_token(1), 10)

    # invalid authorised user
    with pytest.raises(AccessError):
        channel_details_v2(make_token(10), 0)

    # Authorised user is not a member of channel with channel_id
    with pytest.raises(AccessError):
        channel_details_v2(make_token(3), 0)

# Test 5
def test_channel_join_v2(user_setup, channel_setup):

    channel_join_v2(make_token(2), 0)
    assert channel_details_v2(make_token(2), 0) == {
        'name': 'PublicChannel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': "Peter",
                'name_last': "Tran",
                'handle': "petertran"
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': "Peter",
                'name_last': "Tran",
                'handle': "petertran"
            },
            {
                'u_id': 2,
                'email': "christopherluong@email.com",
                'name_first': "Christopher",
                'name_last': "Luong",
                'handle': "christopherluong"
            }
        ]
    }

# Test 6
# Test the errors for channel_join_v2
def test_channel_join_v2_errors(user_setup, channel_setup):

    # invalid authorised user
    with pytest.raises(AccessError):
        channel_join_v2(make_token(10), 2)

    # invalid channel id
    with pytest.raises(InputError):
        channel_join_v2(make_token(1), 10)

    # channel_id refers to a private channel and the authorised user is not a member
    with pytest.raises(AccessError):
        channel_join_v2(make_token(2), 5)

"""
# Test 7
def test_channel_messages_v1(user_setup, channel_setup):
    message_send_v1(make_token(1), 0, 'Hello')
    assert channel_messages_v1(1, 0, 0) == {
        'messages': [
            {
                'channel_id': 0,
                'dm_id': -1,
                'message': "hello",
                'message_id': 0,
            },
        ],
        'start': 0,
        'end': -1,
    }
"""

# Tests for channel_join_v2 and channel_leave_v1

# The following ensure the function works at every step/
#    and assumes channel_invite_v2() works successfully
def test_channel_join_leave_v2(user_setup, channel_setup):

    #test that channel_join_v2 and channel_leave_v1 are working correctly

    # Test 1:
    # the 3rd user joins a public channel and then make sure the details/
    #   are correct
    channel_join_v2(make_token(2), 0)
    assert channel_details_v2(make_token(2), 0) == {
        'name': 'PublicChannel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': 1,
                'email': 'petertran@email.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran',
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'petertran@email.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran',
            },
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
        ],
    }

    # Test 2:
    # joining the dream owner into the channel
    channel_join_v2(make_token(0), 0)
    assert channel_details_v2(make_token(1), 0) == {
        'name': 'PublicChannel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': 1,
                'email': 'petertran@email.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran',
            },
            {
                'u_id': 0,
                'email': 'gungeetsingh@email.com',
                'name_first': 'Gungeet',
                'name_last': 'Singh',
                'handle': 'gungeetsingh',
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'petertran@email.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran',
            },
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
            {
                'u_id': 0,
                'email': 'gungeetsingh@email.com',
                'name_first': 'Gungeet',
                'name_last': 'Singh',
                'handle': 'gungeetsingh',
            },
        ],
    }
    
    # Test 3:
    # the first and second user leaves and rejoins and then/
    #   make sure the details are correct once again
    assert channel_leave_v1(make_token(0), 0) == {}
    assert channel_leave_v1(make_token(1), 0) == {}
    assert channel_join_v2(make_token(0), 0) == {}
    assert channel_join_v2(make_token(1), 0) == {}
    
    
    assert channel_details_v2(make_token(1), 0) == {
        'name': 'PublicChannel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
            {
                'u_id': 0,
                'email': 'gungeetsingh@email.com',
                'name_first': 'Gungeet',
                'name_last': 'Singh',
                'handle': 'gungeetsingh',
            },
        ],
        'all_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
            {
                'u_id': 0,
                'email': 'gungeetsingh@email.com',
                'name_first': 'Gungeet',
                'name_last': 'Singh',
                'handle': 'gungeetsingh',
            },
            {
                'u_id': 1,
                'email': 'petertran@email.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran',
            },
        ],
    }

    # Test 4:
    # the 1st and 3rd users are invited to a private channel/
    #   then the 1st and 2nd users leave/
    #   and make sure the details are correct
    # essentially owner leaves and last user becomes the owner
    assert channel_invite_v2(make_token(1), 3, 0) == {}
    assert channel_invite_v2(make_token(1), 3, 2) == {}
    assert channel_leave_v1(make_token(0), 3) == {}
    assert channel_leave_v1(make_token(1), 3) == {}

    assert channel_details_v2(make_token(2), 3) == {
        'name': 'PrivateChannel1',
        'is_public': False,
        'owner_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
        ],
        'all_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
        ],
    }

    # Test 5: 
    # owner leaves a public channel and 3rd user joins/
    #   then make sure details are correct
    assert channel_leave_v1(make_token(1), 2) == {}
    assert channel_join_v2(make_token(2), 2) == {}
    assert channel_details_v2(make_token(2), 2) == {
        'name': 'PublicChannel3',
        'is_public': True,
        'owner_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
        ],
        'all_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
        ],
    }

# Test the errors for channel_join_v2 and channel_leave_v2

def test_channel_join_leave_errors(user_setup, channel_setup):
    '''
    #test the errors for channel_join_v2 and channel_leave_v2
    '''
    # Test 6:
    # invalid authorised user
    with pytest.raises(AccessError):
        channel_join_v2(make_token(10), 2)

    # Test 7:
    # invalid channel id
    with pytest.raises(InputError):
        channel_join_v2(make_token(1), 10)

    # Test 8:
    # channel_id refers to a private channel
    with pytest.raises(AccessError):
        channel_join_v2(make_token(2), 5)

    # Test 6:
    # invalid authorised user
    with pytest.raises(AccessError):
        channel_leave_v1(make_token(10), 2)

    # Test 7:
    # invalid channel id
    with pytest.raises(InputError):
        channel_leave_v1(make_token(1), 10)

    # Test 8:
    # channel_id refers to a private channel and the authorised user is not a member
    with pytest.raises(AccessError):
        channel_leave_v1(make_token(2), 5)

# Tests for channel_addowner_v1 and channel_removeowner_v1
def test_channel_add_remove_owner_v1(user_setup, channel_setup):
    '''
    #tests for the channel_addowner_v1 and channel_removeowner_v1
    '''
    # Test 1:
    # Invite the third user to an empty public channel and then add/ 
    #   the second user as an owner
    channel_leave_v1(make_token(1), 0) # peter leaves
    channel_join_v2(make_token(2), 0) # chris joins
    channel_invite_v2(make_token(2), 0, 1) # chris invites peter
    channel_addowner_v1(make_token(2), 0, 1) # chris adds peter as an owner
    assert channel_details_v2(make_token(1), 0) == {
        'name': 'PublicChannel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
            {
                'u_id': 1,
                'email': 'petertran@email.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran',
            },
        ],
        'all_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
            {
                'u_id': 1,
                'email': 'petertran@email.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran',
            },
        ],
    }

    # Test 2:
    # Add the first user into a public channel/
    #   make them the owner and remove the first owner from being the owner/
    #   check that the details are the same

    channel_invite_v2(make_token(1), 1, 2)
    channel_addowner_v1(make_token(1), 1, 2)
    channel_removeowner_v1(make_token(2), 1, 1)
    assert channel_details_v2(make_token(1), 1) == {
        'name': 'PublicChannel2',
        'is_public': True,
        'owner_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'petertran@email.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran',
            },
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
        ],
    }

    # Test 3:
    # Add the first user into a private channel/
    #   make them the owner and remove the first owner from being the owner/
    #   check that the details are the same

    channel_invite_v2(make_token(1), 4, 2)
    channel_addowner_v1(make_token(1), 4, 2)
    channel_removeowner_v1(make_token(2), 4, 1)
    assert channel_details_v2(make_token(1), 4) == {
        'name': 'PrivateChannel2',
        'is_public': False,
        'owner_members': [
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'petertran@email.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran',
            },
            {
                'u_id': 2,
                'email': 'christopherluong@email.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong',
            },
        ],
    }

# Test the errors for channel_addowner_v1 and channel_removeowner_v1

def test_channel_add_leave_owner_v1_errors(user_setup, channel_setup):
    '''
    #test the errors for channel_addowner_v1 and channel_removeowner_v1
    '''
    # Test 6:
    # user is currently the only owner
    with pytest.raises(AccessError):
        channel_removeowner_v1(make_token(1), 1, 1)
    
    channel_invite_v2(make_token(1), 1, 0) # invite gungeet
    channel_invite_v2(make_token(1), 1, 2) # invite chris
    channel_invite_v2(make_token(1), 1, 3)
    # Test 6:
    # invalid channel
    with pytest.raises(InputError):
        channel_addowner_v1(make_token(1), 10, 0)

    # Test 7:
    # authorised user doesn't exist
    with pytest.raises(AccessError):
        channel_addowner_v1(make_token(10), 1, 0)

    # Test 8:
    # user is already an owner
    with pytest.raises(InputError):
        channel_addowner_v1(make_token(1), 1, 1)

    # Test 9:
    # authorised user is not an owner
    with pytest.raises(AccessError):
        channel_addowner_v1(make_token(3), 1, 2)

    # Test 10:
    # invalid channel
    with pytest.raises(InputError):
        channel_removeowner_v1(make_token(0), 1, 2)

    # Test 11:
    # authorised user doesn't exist
    with pytest.raises(AccessError):
        channel_removeowner_v1(make_token(10), 1, 1)

    # Test 12:
    # invalid channel
    with pytest.raises(InputError):
        channel_addowner_v1(make_token(1), 10, 0)

    # Test 13:
    # authorised user is not an owner
    with pytest.raises(AccessError):
        channel_removeowner_v1(make_token(2), 1, 1)

    # Test 14:
    # user is not the owner of the channel
    with pytest.raises(InputError):
        channel_removeowner_v1(make_token(1), 1, 2)

# Tests for channel_messages_v2

def test_channel_messages_v2(user_setup, channel_setup):
    '''
    #Tests for channel_messages_v2
    '''
    # Test 1:
    # send a message to a public channel and check the message exists
    message_send_v2(make_token(1), 0, "onions can be eaten raw")
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
    assert channel_messages_v2(make_token(1), 0, 0) == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 1,
                "message": "onions can be eaten raw",
                "time_created": timeStampStr,
                "channel_id": 0,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
        ],
        "start": 0,
        "end": -1,
    }
 
    # Test 2:
    # check the messages in a fresh public channel
    assert channel_messages_v2(make_token(1), 1, 0) == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

    # Test 3:
    # add a user to a public channel and they send a message
    # check the messages sent in a public channel/
    #   after the user leaves the channel
    channel_invite_v2(make_token(1), 1, 0)
    message_send_v2(make_token(0), 1, "onions cannot be eaten raw")
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
    channel_leave_v1(make_token(0), 1)
    assert channel_messages_v2(make_token(1), 1, 0) == {
        "messages": [
            {
                "message_id": 1,
                "u_id": 0,
                "message": "onions cannot be eaten raw",
                "time_created": timeStampStr,
                "channel_id": 1,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
        ],
        "start": 0,
        "end": -1,
    }

    # Test 4:
    # invite the first and third user to join a public channel
    # everyone sends an identical message from the first to the third user/ 
    #   and check the messages in the channel
    channel_invite_v2(make_token(1), 2, 0)
    channel_invite_v2(make_token(1), 2, 2)
    timeStampStr = []

    message_send_v2(make_token(0), 2, "wait until you try raw radishes")
    dateTimeObj = datetime.now()
    timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))

    message_send_v2(make_token(1), 2, "wait until you try raw radishes")
    dateTimeObj = datetime.now()
    timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))

    message_send_v2(make_token(2), 2, "wait until you try raw radishes")
    dateTimeObj = datetime.now()
    timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))

    assert channel_messages_v2(make_token(1), 2, 0) == {
        "messages": [
            {
                "message_id": 4,
                "u_id": 2,
                "message": "wait until you try raw radishes",
                "time_created": timeStampStr[2],
                "channel_id": 2,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
            {
                "message_id": 3,
                "u_id": 1,
                "message": "wait until you try raw radishes",
                "time_created": timeStampStr[1],
                "channel_id": 2,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
            {
                "message_id": 2,
                "u_id": 0,
                "message": "wait until you try raw radishes",
                "time_created": timeStampStr[0],
                "channel_id": 2,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
        ],
        "start": 0,
        "end": -1,
    }

    # Test 5:
    # send a message to a private channel and check the message exists
    message_send_v2(make_token(1), 3, "onions can be eaten raw")
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
    assert channel_messages_v2(make_token(1), 3, 0) == {
        "messages": [
            {
                "message_id": 5,
                "u_id": 1,
                "message": "onions can be eaten raw",
                "time_created": timeStampStr,
                "channel_id": 3,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
        ],
        "start": 0,
        "end": -1,
    }

    # Test 6:
    # check the messages in a fresh private channel
    assert channel_messages_v2(make_token(1), 4, 0) == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

    # Test 7:
    # add a user to a private channel and they send a message
    # check the messages sent in a private channel/
    #   after the user leaves the channel
    channel_invite_v2(make_token(1), 4, 0)
    message_send_v2(make_token(0), 4, "onions cannot be eaten raw")
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
    channel_leave_v1(make_token(0), 4)
    assert channel_messages_v2(make_token(1), 4, 0) == {
        "messages": [
            {
                "message_id": 6,
                "u_id": 0,
                "message": "onions cannot be eaten raw",
                "time_created": timeStampStr,
                "channel_id": 4,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
        ],
        "start": 0,
        "end": -1,
    }

    # Test 8:
    # invite the first and third user to join a public channel
    # everyone sends an identical message from the first to the third user/ 
    #   and check the messages in the channel
    channel_invite_v2(make_token(1), 5, 0)
    channel_invite_v2(make_token(1), 5, 2)
    timeStampStr = []
    message_send_v2(make_token(0), 5, "wait until you try raw radishes")
    dateTimeObj = datetime.now()
    timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))

    message_send_v2(make_token(1), 5, "wait until you try raw radishes")
    dateTimeObj = datetime.now()
    timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))

    message_send_v2(make_token(2), 5, "wait until you try raw radishes")
    dateTimeObj = datetime.now()
    timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
    assert channel_messages_v2(make_token(1), 5, 0) == {
        "messages": [
            {
                "message_id": 9,
                "u_id": 2,
                "message": "wait until you try raw radishes",
                "time_created": timeStampStr[2],
                "channel_id": 5,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
            {
                "message_id": 8,
                "u_id": 1,
                "message": "wait until you try raw radishes",
                "time_created": timeStampStr[1],
                "channel_id": 5,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
            {
                "message_id": 7,
                "u_id": 0,
                "message": "wait until you try raw radishes",
                "time_created": timeStampStr[0],
                "channel_id": 5,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            },
        ],
        "start": 0,
        "end": -1,
    }

def test_channel_messages_fiftyone(user_setup, channel_setup):
    # Test 9:
    # invite the third user to a public server/
    #   they send 51 messages and check the messages
    channels_create_v2(make_token(1), "PublicChannel4", True)
    channel_invite_v2(make_token(1), 6, 2)
    timeStampStr = []
    for i in range(51):
        message_send_v2(make_token(2), 6, str(i))
        dateTimeObj = datetime.now()
        timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
    
    messages = []
    for i in range(50):
        message = {
            "message_id": (49 - i),
            "u_id": 2,
            "message": str(49 - i),
            "time_created": timeStampStr[49 - i],
            "channel_id": 6,
            "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
        }
        messages.append(message)

    assert channel_messages_v2(make_token(2), 6, 0) == {
        "messages": messages,
        "start": 0,
        "end": 50,
    }

    # sends the least recent message
    assert channel_messages_v2(make_token(2), 6, 50) == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 2,
                "message": "0",
                "time_created": timeStampStr[0],
                "channel_id": 6,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            }
        ],
        "start": 50,
        "end": -1,
    }

def test_channel_messages_fiftyone_private(user_setup, channel_setup):
    # Test 10:
    # invite the third user to a private server/
    #   they send 51 messages and check the messages
    channels_create_v2(make_token(1), "PrivateChannel4", False)
    channel_invite_v2(make_token(1), 6, 2)
    timeStampStr = []
    for i in range(100):
        message_send_v2(make_token(2), 6, str(i))
        dateTimeObj = datetime.now()
        timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
    
    messages = []
    for i in range(50):
        message = {
            "message_id": (49 - i),
            "u_id": 2,
            "message": str(49 - i),
            "time_created": timeStampStr[49 - i],
            "channel_id": 6,
            "dm_id": -1,
            'reacts': [
                {
                    'react_id': 1, 
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ],
            'is_pinned': False
        }
        messages.append(message)
    assert channel_messages_v2(make_token(2), 6, 0) == {
        "messages": messages,
        "start": 0,
        "end": 50,
    }
    
    messages = []
    for i in range(50):
        message = {
            "message_id": (99 - i),
            "u_id": 2,
            "message": str(99 - i),
            "time_created": timeStampStr[99 - i],
            "channel_id": 6,
            "dm_id": -1,
            'reacts': [
                {
                    'react_id': 1, 
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ],
            'is_pinned': False
        }
        messages.append(message)
    # sends the least recent message
    assert channel_messages_v2(make_token(2), 6, 50) == {
        "messages": messages,
        "start": 50,
        "end": 100,
    }

# Test the errors for channel_messages_v2

def test_channel_messages_v2_errors(user_setup, channel_setup):
    '''
    test the errors for channel_messages_v2
    '''
    # Test 11:
    # invalid channel id
    with pytest.raises(InputError):
        channel_messages_v2(make_token(1), 10, 0)
    
    # Test 12:
    # start is greater than the total of messages in the channel
    with pytest.raises(InputError):
        channel_messages_v2(make_token(1), 1, 100)

    # Test 13:
    # authorised user is not a member of the channel
    with pytest.raises(AccessError):
        channel_messages_v2(make_token(2), 1, 0)

    # Test 14:
    # invalid authorised user
    with pytest.raises(AccessError):
        channel_messages_v2(make_token(10), 1, 0)
