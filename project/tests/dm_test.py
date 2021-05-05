from src.auth import auth_register_v2
from src.auth import auth_login_v2
from src.dm import dm_invite_v1
from src.dm import dm_details_v1
from src.dm import dm_list_v1
from src.dm import dm_create_v1
from src.dm import dm_remove_v1
from src.dm import dm_leave_v1
from src.dm import dm_messages_v1
from src.message import message_senddm_v1
from src.error import InputError
from src.error import AccessError
from src.clear import clear_v1
from src.helper import make_token
from datetime import datetime

import pytest

@pytest.fixture
def user_setup():
    '''
    Clear history of all current users then register and login new users
    '''
    clear_v1()
    # register 4 users with email, password, first name and last name
    auth_register_v2("gungeetsingh@email.com", "password", "Gungeet", "Singh")
    auth_register_v2("petertran@email.com", "password", "Peter", "Tran")
    auth_register_v2("christopherluong@email.com", "password", "Christopher", "Luong")
    auth_register_v2("talavrahami@email.com", "password", "Tal", "Avrahami"),
    auth_register_v2("eyaldorfan@email.com", "password", "Eyal", "Dorfan")
    # login the 4 users who have been registered
    auth_login_v2("gungeetsingh@email.com", "password")
    auth_login_v2("petertran@email.com", "password")
    auth_login_v2("christopherluong@email.com", "password")
    auth_login_v2("talavrahami@email.com", "password")
    auth_login_v2("eyaldorfan@email.com", "password")

@pytest.fixture
def dm_setup():
    # create multiple dms for single user
    dm_create_v1(make_token(1), [0, 2]) # dm_id 0
    dm_create_v1(make_token(0), [1]) # dm_id 1
    dm_create_v1(make_token(2), [1]) # dm_id 2
    dm_create_v1(make_token(3), [0]) # dm_id 3

def test_dm_details_v1(user_setup, dm_setup):
    
    # Test 1: 
    # Lists the details of dm no.2
    assert dm_details_v1(make_token(1), 1) == {
        "name": "gungeetsingh, petertran",
        "members": [
            {
                'u_id': 0,
                'email': "gungeetsingh@email.com",
                'name_first': 'Gungeet',
                'name_last': 'Singh',
                'handle': 'gungeetsingh' 
            },
            {   
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran'
            }
        ],
    }


def test_dm_details_v1_multiple(user_setup, dm_setup):
    
    # Test 2: 
    # Lists the details of dm no.1 with multiple users in the dm
    assert dm_details_v1(make_token(1), 0) == {
        "name": "christopherluong, gungeetsingh, petertran",
        "members": [
            {
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran'
            },
            {
                'u_id': 0,
                'email': "gungeetsingh@email.com",
                'name_first': 'Gungeet',
                'name_last': 'Singh',
                'handle': 'gungeetsingh'
            },
            {
                'u_id': 2,
                'email': "christopherluong@email.com",
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong'
            }
        ],
    }

def test_dm_details_v1_errors(user_setup, dm_setup):
    # Test the errors for channel_details_v1
    # Test 1:
    # invalid token
    with pytest.raises(AccessError):
        dm_details_v1(123456, 2) # "Invalid token"

    # Test 2:
    # invalid dm
    with pytest.raises(InputError):
        dm_details_v1(make_token(1), 10) # "Invalid dm"

    # Test 3:
    # Authorised user is not a member of dm with dm_id
    with pytest.raises(AccessError):
        dm_details_v1(make_token(0), 2)
       # "Authorised user needs to be a member of dm"

def test_dm_list_v1_success(user_setup, dm_setup):
    # list out a particular users dms
    assert dm_list_v1(make_token(3)) == {
        'dms': [
            {
                "dm_id": 3,
                "name": "gungeetsingh, talavrahami",
                "members": [
                    {
                        'u_id': 3,
                        'email': "talavrahami@email.com",
                        'name_first': 'Tal',
                        'name_last': 'Avrahami',
                        'handle': 'talavrahami'
                    },
                    {
                        'u_id': 0,
                        'email': "gungeetsingh@email.com",
                        'name_first': 'Gungeet',
                        'name_last': 'Singh',
                        'handle': 'gungeetsingh'
                    },
                ],
                "owner_members": [
                    {
                        'u_id': 3,
                        'email': "talavrahami@email.com",
                        'name_first': 'Tal',
                        'name_last': 'Avrahami',
                        'handle': 'talavrahami'
                    }
                ]
            }
        ]
    }

def test_dm_list_v1_errors(user_setup, dm_setup):
    # invalid token
    with pytest.raises(AccessError):
        dm_list_v1(123456)

def test_dm_leave_v1_success(user_setup, dm_setup):
    
    # Test 1: 
    # Remove user no.3 from dm no.1
    # dm_create_v1(make_token(1), [0, 2]) # dm_id 0
    dm_leave_v1(make_token(2), 0)
    assert dm_details_v1(make_token(1), 0) == {
        "name": "gungeetsingh, petertran",
        "members": [
            {
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran'
            },
            {
                'u_id': 0,
                'email': "gungeetsingh@email.com",
                'name_first': 'Gungeet',
                'name_last': 'Singh',
                'handle': 'gungeetsingh'
            }
        ],
    }

def test_dm_leave_v1_errors(user_setup, dm_setup):
    # invalid token
    with pytest.raises(AccessError):
        dm_leave_v1(make_token(123456), 0)
    
    # invalid dm
    with pytest.raises(InputError):
        dm_leave_v1(make_token(1), 10) 

    # User is not part of the dm
    with pytest.raises(AccessError):
        dm_leave_v1(make_token(3), 0)

def test_dm_remove_v1_success(user_setup):
    dm_create_v1(make_token(0), [1])
    dm_create_v1(make_token(0), [2]) # removing this dm
    dm_remove_v1(make_token(0), 1)
    assert dm_list_v1(make_token(0)) == {
        'dms': [
            {
                "dm_id": 0,
                "name": "gungeetsingh, petertran",
                "members": [
                    {
                        'u_id': 0,
                        'email': "gungeetsingh@email.com",
                        'name_first': 'Gungeet',
                        'name_last': 'Singh',
                        'handle': 'gungeetsingh'
                    },
                    {
                        'u_id': 1,
                        'email': "petertran@email.com",
                        'name_first': 'Peter',
                        'name_last': 'Tran',
                        'handle': 'petertran'
                    },
                ],
                "owner_members": [
                    {
                        'u_id': 0,
                        'email': "gungeetsingh@email.com",
                        'name_first': 'Gungeet',
                        'name_last': 'Singh',
                        'handle': 'gungeetsingh'
                    }
                ]
            }
        ]
    }

def test_dm_remove_v1_errors(user_setup, dm_setup):
    # invalid token
    with pytest.raises(AccessError):
        dm_remove_v1(make_token(123456), 0)

    # invalid dm
    with pytest.raises(InputError):
        dm_remove_v1(make_token(1), 10)

    # User is not the owner
    with pytest.raises(AccessError):
        dm_remove_v1(make_token(0), 2)

def test_dm_invite_v1_success(user_setup, dm_setup):
    # dm_create_v1(make_token(0), [1]) # dm_id 1
    dm_invite_v1(make_token(0), 1, 2)
    dm_invite_v1(make_token(0), 1, 3)
    dm_invite_v1(make_token(0), 1, 4)
    assert dm_details_v1(make_token(0), 1) == {
        "name": "christopherluong, eyaldorfan, gungeetsingh, petertran, talavrahami",
        "members": [
            {
                'u_id': 0,
                'email': "gungeetsingh@email.com",
                'name_first': 'Gungeet',
                'name_last': 'Singh',
                'handle': 'gungeetsingh'
            },
            {
                'u_id': 1,
                'email': "petertran@email.com",
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle': 'petertran'
            },
            {
                'u_id': 2,
                'email': "christopherluong@email.com",
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong'
            },
            {
                'u_id': 3,
                'email': "talavrahami@email.com",
                'name_first': 'Tal',
                'name_last': 'Avrahami',
                'handle': 'talavrahami'
            },
            {
                'u_id': 4,
                'email': "eyaldorfan@email.com",
                'name_first': 'Eyal',
                'name_last': 'Dorfan',
                'handle': 'eyaldorfan'
            }
        ],
    }

def test_dm_invite_v1_errors(user_setup, dm_setup):
    # invalid token
    with pytest.raises(AccessError):
        dm_invite_v1(make_token(123456), 0, 0)

    # invalid dm
    with pytest.raises(InputError):
        dm_invite_v1(make_token(0), 10, 2)

    # User is not a member of the dm
    with pytest.raises(AccessError):
        dm_invite_v1(make_token(3), 1, 2)

# def test_dm_messages_v1_success(user_setup, dm_setup):
# def test_dm_messages_v1_errors(user_setup, dm_setup):

def test_dm_leave_v1_owner(user_setup, dm_setup):
    
    # dm_create_v1(make_token(1), [0, 2]) # dm_id 0
    dm_leave_v1(make_token(0), 0)
    dm_leave_v1(make_token(1), 0)
    assert dm_details_v1(make_token(2), 0) == {
        "name": "christopherluong",
        "members": [
            {
                'u_id': 2,
                'email': "christopherluong@email.com",
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle': 'christopherluong'
            },
        ],
    }

def test_dm_messages_v1_success(user_setup, dm_setup):
    message_senddm_v1(make_token(1), 0, "onions can be eaten raw")
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
    assert dm_messages_v1(make_token(1), 0, 0) == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 1,
                "message": "onions can be eaten raw",
                "time_created": timeStampStr,
                "channel_id": -1,
                "dm_id": 0,
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

    assert dm_messages_v1(make_token(1), 1, 0) == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

def test_dm_messages_v1_leave(user_setup, dm_setup):
    # testing to see if messages works after user leaves
    message_senddm_v1(make_token(0), 1, "onions cannot be eaten raw")
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
    dm_leave_v1(make_token(0), 1)
    assert dm_messages_v1(make_token(1), 1, 0) == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 0,
                "message": "onions cannot be eaten raw",
                "time_created": timeStampStr,
                "channel_id": -1,
                "dm_id": 1,
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

def test_channel_messages_fiftyone(user_setup, dm_setup):
    # send 51 messages and check the dms
    timeStampStr = []
    for i in range(51):
        message_senddm_v1(make_token(0), 1, str(i))
        dateTimeObj = datetime.now()
        timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
    
    messages = []
    for i in range(50):
        message = {
            "message_id": (49 - i),
            "u_id": 0,
            "message": str(49 - i),
            "time_created": timeStampStr[49 - i],
            "channel_id": -1,
            "dm_id": 1,
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

    assert dm_messages_v1(make_token(0), 1, 0) == {
        "messages": messages,
        "start": 0,
        "end": 50,
    }

    # sends the least recent message
    assert dm_messages_v1(make_token(0), 1, 50) == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 0,
                "message": "0",
                "time_created": timeStampStr[0],
                "channel_id": -1,
                "dm_id": 1,
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

# Test the errors for dm_messages_v1
def test_dm_messages_v1_errors(user_setup, dm_setup):
    '''
    test the errors for channel_messages_v2
    '''
    # invalid dm_id
    with pytest.raises(InputError):
        dm_messages_v1(make_token(1), 10, 0)

    # start is greater than the total number of dms
    with pytest.raises(InputError):
        dm_messages_v1(make_token(1), 1, 100)

    # authorised user is not a member of the dm
    with pytest.raises(AccessError):
        dm_messages_v1(make_token(2), 1, 0)

    # invalid authorised user
    with pytest.raises(AccessError):
        dm_messages_v1(make_token(10), 1, 0)
