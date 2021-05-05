'''
channel_test.py

Main Modules:
    test_channel_invite_v2_multiple_public
    test_channel_invite_v2_multiple_private
    test_channel_invite_v2_single_private
    test_channel_invite_v2_single_private
    test_channel_invite_v2_errors
    test_channel_details_v2
    test_channel_join_v2
    test_channel_join_v2_errors

    Tests modules in the channel.py
'''
#from src.auth import auth_register_v2
#from src.auth import auth_login_v2
#from src.channels import channels_create_v2
#from src.channel import channel_invite_v2
#from src.channel import channel_details_v2
#from src.channel import channel_join_v2
# from src.channel import channel_messages_v2
# from src.message import message_send_v2
from src.error import InputError
from src.error import AccessError
from src.clear import clear_v1
from src import config
from datetime import timezone
from datetime import datetime
from src.helper import make_token
import pytest
import json
import jwt
import requests

@pytest.fixture
def user_setup():
    '''
    Clear history of all current users then register and login new users
    '''
    clear_v1()
    # register 3 users with email, password, first name and last name
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "gungeetsingh@email.com",
        "password": "password",
        "name_first": "Gungeet",
        "name_last": "Singh",
    })
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "petertran@email.com",
        "password": "password",
        "name_first": "Peter",
        "name_last": "Tran",
    })
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "christopherluong@email.com",
        "password": "password",
        "name_first": "Christopher",
        "name_last": "Luong"
    })

@pytest.fixture
def channel_setup_single_user():
    '''
    Create 3 public and private channels by the same user
    '''
    # create multiple public channels for single user (Non-dream owner)
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(1),
        "name": "PublicChannel1",
        "is_public": True,
    })
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(1),
        "name": "PublicChannel2",
        "is_public": True,
    })
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(1),
        "name": "PublicChannel3",
        "is_public": True,
    })
    # create multiple private channels for single user
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(1),
        "name": "PrivateChannel1",
        "is_public": False,
    })
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(1),
        "name": "PrivateChannel2",
        "is_public": False,
    })
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(1),
        "name": "PrivateChannel3",
        "is_public": False,
    })

'''
# Tests for channel_invite_v2

# invites a user by adding them to the channel immediately
# ensures the output is an empty dictionary
# AND assumes that channel_details_v2() works to determine that the invite has worked

# Test 1:
# invites one user to three public channels
def test_channel_invite_v2_multiple_public(user_setup, channel_setup_single_user):
'''
#test users joining multiple public servers
'''
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
    "u_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 1,
    "u_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 2,
    "u_id": 2,
})
payload = r.json()
assert payload == {}

r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel1',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
    ]
}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 1,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel2',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
    ]
}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 2,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel3',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
    ]
}

# Test 2:
# invites one user to three private channels
def test_channel_invite_v2_multiple_private(user_setup, channel_setup_single_user):
'''
#test users joining multiple private servers
'''
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 3,
    "u_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 4,
    "u_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 5,
    "u_id": 2,
})
payload = r.json()
assert payload == {}

r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 3,
})
payload = r.json()
assert payload == {
    'name': 'PrivateChannel1',
    'is_public': 'False',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
    ]
}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 4,
})
payload = r.json()
assert payload == {
    'name': 'PrivateChannel2',
    'is_public': 'False',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
    ]
}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 5,
})
payload = r.json()
assert payload == {
    'name': 'PrivateChannel3',
    'is_public': 'False',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
    ]
}

# Test 3:
# invites the first and third users to join one public channel
def test_channel_invite_v2_single_public(user_setup, channel_setup_single_user):
'''
#test multiple users joining one public server
'''
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
    "u_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
    "u_id": 0,
})
payload = r.json()
assert payload == {}

r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 0
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel1',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
        {
            'u_id': 0,
        },
    ]
}

# Test 4:
# invites the first and third users to join one private channel
def test_channel_invite_v2_single_private(user_setup, channel_setup_single_user):
'''
#test multiple users joining one private server
'''
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 3,
    "u_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 3,
    "u_id": 0,
})
payload = r.json()
assert payload == {}

r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 3,
})
payload = r.json()
assert payload == {
    'name': 'PrivateChannel1',
    'is_public': 'False',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
        {
            'u_id': 0,
        },
    ]
}

'''
    # Test the errors for channel_invite_v2

def test_channel_invite_v2_errors(user_setup, channel_setup_single_user):
    '''
    test the errors for the function channel_invite_v2
    '''
    # Test 5:
    # invites an invalid user to a private channel
    with pytest.raises(requests.exceptions.HTTPError):
        requests.get(config.url + 'channel/invite/v2', json = {
            'token': make_token(1),
            'channel_id': 5,
            'u_id': 10,
        }).raise_for_status() # "Invalid user"

    # Test 6:
    # invites an invalid user to a public channel
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/invite/v2', json = {
            'token': make_token(1),
            'channel_id': 2,
            'u_id': 10,
        }).raise_for_status() # "Invalid user"

    # Test 7:
    # invites a user to an invalid channel
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/invite/v2', json = {
            'token': make_token(1),
            'channel_id': 10,
            'u_id': 2,
        }).raise_for_status() # "Invalid channel"

    # Test 8:
    # invitation to a channel from an invalid user
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/invite/v2', json = {
            'token': make_token(10),
            'channel_id': 4,
            'u_id': 2,
        }).raise_for_status() # "Invalid authorised user"

    # Test 9:
    # the authorised user sending an invite is not a member of the channel
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "talavrahami@email.com",
        "password": "password",
        "name_first": "Tal",
        "name_last": "Avrahami",
    })
    requests.post(config.url + 'auth/login/v2', json = {
        "email": "talavrahami@email.com",
        "password": "password",
    })
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/invite/v2', json = {
            'token': make_token(0),
            'channel_id': 4,
            'u_id': 3,
        }).raise_for_status()      # "Authorised user needs to be a member/
                                   # of the channel to invite others"

'''
# Tests for channel_details_v2

# The tests above already cover some tests for channel_details
# The following ensure the function works at every step/
#    and assumes channel_invite_v2() works successfully
def test_channel_details_v2(user_setup, channel_setup_single_user):
'''
#multiple tests for channel_details_v2 for private and public channels
'''
# Test 1:
# Lists the details of a public channel associated with the channel owner
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel1',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
    ],
}

# Test 2:
# invites the 3rd user to a public channel and then make sure the details/
#   are correct once again

requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
    "u_id": 2,
})
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(2),
    "channel_id": 0,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel1',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
    ],
}

# Test 3:
# invites the 1st user to the public channel and then make sure the details/
#   are correct once again
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
    "u_id": 0,
})
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(2),
    "channel_id": 0,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel1',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
        {
            'u_id': 0,
        },
    ],
}

# Test the errors for channel_details_v2
'''
def test_channel_details_v2_errors(user_setup, channel_setup_single_user):
    '''
    test the errors for channel_details_v2
    '''
    # Test 4:
    # invalid channel
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/invite/v2', json = {
            'token': make_token(1),
            'channel_id': 10,
        }).raise_for_status() # "Invalid channel"

    # Test 5:
    # invalid authorised user
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/invite/v2', json = {
            'token': make_token(10),
            'channel_id': 0,
        }).raise_for_status() # "Invalid authorised user"

    # Test 6:
    # Authorised user is not a member of channel with channel_id
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "talavrahami@email.com",
        "password": "password",
        "name_first": "Tal",
        "name_last": "Avrahami",
    })
    requests.post(config.url + 'auth/login/v2', json = {
        "email": "talavrahami@email.com",
        "password": "password",
    })
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/invite/v2', json = {
            'token': make_token(3),
            'channel_id': 0,
        }).raise_for_status() # "Authorised user needs to be a member of the channel"

'''
# Tests for channel_join_v2 and channel_leave_v1

# The following ensure the function works at every step/
#    and assumes channel_invite_v2() works successfully
def test_channel_join_leave_v2(user_setup, channel_setup_single_user):
'''
#test that channel_join_v2 and channel_leave_v1 are working correctly
'''
# Test 1:
# the 3rd user joins a public channel and then make sure the details/
#   are correct

r = requests.post(config.url + "channel/join/v2", json = {
    "token": make_token(2),
    "channel_id": 0,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(2),
    "channel_id": 0,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel1',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 1,
        },
    ],
    'all_members': [
        {
            'u_id': 1,
        },
        {
            'u_id': 2,
        },
    ],
}

# Test 2:
# the 1st user joins and then make sure the details/
#   are correct once again
r = requests.post(config.url + "channel/join/v2", json = {
    "token": make_token(0),
    "channel_id": 0,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel1',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },
    ],
    'all_members': [
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
        {
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
    ],
}

# Test 3:
# the first and second user leaves and rejoins and then/
#   make sure the details are correct once again
r = requests.post(config.url + "channel/leave/v1", json = {
    "token": make_token(0),
    "channel_id": 0,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/leave/v1", json = {
    "token": make_token(1),
    "channel_id": 0,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/join/v2", json = {
    "token": make_token(0),
    "channel_id": 0,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/join/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel1',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
    ],
    'all_members': [
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
        {
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
    ],
}

# Test 4:
# the 1st and 3rd users are invited to a private channel/
#   then the 1st and 2nd users leave/
#   and make sure the details are correct
# essentially owner leaves and last user becomes the owner
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(0),
    "channel_id": 3,
})
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(2),
    "channel_id": 3,
})
r = requests.post(config.url + "channel/leave/v1", json = {
    "token": make_token(0),
    "channel_id": 3,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/leave/v1", json = {
    "token": make_token(1),
    "channel_id": 3,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(2),
    "channel_id": 3,
})
payload = r.json()
assert payload == {
    'name': 'PrivateChannel1',
    'is_public': 'False',
    'owner_members': [
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
    ],
    'all_members': [
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
    ],
}

# Test 5: 
# owner leaves a public channel and 3rd user joins/
#   then make sure details are correct
r = requests.post(config.url + "channel/leave/v1", json = {
    "token": make_token(1),
    "channel_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/join/v2", json = {
    "token": make_token(2),
    "channel_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(2),
    "channel_id": 2,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel3',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
    ],
    'all_members': [
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
    ],
}

# Test the errors for channel_join_v2 and channel_leave_v2

def test_channel_join_leave_errors(user_setup, channel_setup_single_user):
'''
#test the errors for channel_join_v2 and channel_leave_v2
'''
# Test 6:
# invalid authorised user
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/join/v2', json = {
        'token': make_token(10),
        'channel_id': 2,
    }).raise_for_status() # "Invalid authorised user"

# Test 7:
# invalid channel id
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/join/v2', json = {
            'token': make_token(1),
            'channel_id': 10,
        }).raise_for_status() # "Invalid channel"

# Test 8:
# channel_id refers to a private channel and the authorised user is not a member
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/join/v2', json = {
            'token': make_token(2),
            'channel_id': 5,
        }).raise_for_status() # "Channel is private"

# Test 6:
# invalid authorised user
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/leave/v1', json = {
            'token': make_token(10),
            'channel_id': 2,
        }).raise_for_status() # "Invalid authorised user"

# Test 7:
# invalid channel id
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/leave/v1', json = {
            'token': make_token(1),
            'channel_id': 10,
        }).raise_for_status() # "Invalid channel"

# Test 8:
# channel_id refers to a private channel and the authorised user is not a member
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/leave/v1', json = {
            'token': make_token(2),
            'channel_id': 5,
        }).raise_for_status() # "Channel is private"

# Tests for channel_addowner_v1 and channel_removeowner_v1

def test_channel_add_remove_owner_v1(user_setup, channel_setup_single_user):
'''
#tests for the channel_addowner_v1 and channel_removeowner_v1
'''
# Test 1:
# Invite the third user to an empty public channel and then add/ 
#   the second user as an owner

requests.post(config.url + "channel/leave/v1", json = {
    "token": make_token(1),
    "channel_id": 0,
})
requests.post(config.url + "channel/join/v2", json = {
    "token": make_token(2),
    "channel_id": 0,
})
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
    "u_id": 1,
})
r = requests.post(config.url + "channel/addowner/v1", json = {
    "token": make_token(2),
    "channel_id": 0,
    "u_id": 1,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel1',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },
    ],
    'all_members': [
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },
    ],
}

# Test 2:
# Add the first user into a public channel/
#   make them the owner and remove the first owner from being the owner/
#   check that the details are the same

requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 1,
    "u_id": 0,
})
requests.post(config.url + "channel/addowner/v1", json = {
    "token": make_token(1),
    "channel_id": 1,
    "u_id": 0,
})
r = requests.post(config.url + "channel/removeowner/v1", json = {
    "token": make_token(0),
    "channel_id": 1,
    "u_id": 1,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 1,
})
payload = r.json()
assert payload == {
    'name': 'PublicChannel2',
    'is_public': 'True',
    'owner_members': [
        {
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
    ],
    'all_members': [
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },{
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
    ],
}


# Test 3:
# Add the first user into a private channel/
#   make them the owner and remove the first owner from being the owner/
#   check that the details are the same

requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 4,
    "u_id": 0,
})
requests.post(config.url + "channel/addowner/v1", json = {
    "token": make_token(1),
    "channel_id": 4,
    "u_id": 0,
})
r = requests.post(config.url + "channel/removeowner/v1", json = {
    "token": make_token(0),
    "channel_id": 4,
    "u_id": 1,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 4,
})
payload = r.json()
assert payload == {
    'name': 'PrivateChannel2',
    'is_public': 'False',
    'owner_members': [
        {
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
    ],
    'all_members': [
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },
        {
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
    ],
}

# Test 4:
# Invite the first and third user to a private channel/
#    and make them both owners
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 5,
    "u_id": 0,
})
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 5,
    "u_id": 2,
})
requests.post(config.url + "channel/addowner/v1", json = {
    "token": make_token(1),
    "channel_id": 5,
    "u_id": 0,
})
r = requests.post(config.url + "channel/addowner/v1", json = {
    "token": make_token(0),
    "channel_id": 5,
    "u_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 5,
})
payload = r.json()
assert payload == {
    'name': 'PrivateChannel3',
    'is_public': 'False',
    'owner_members': [
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },
        {
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
    ],
    'all_members': [
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },
        {
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
    ],
}

# Test 5:
# Remove the 2nd and 3rd being an owner and everyone/
#   leaves the public channel
r = requests.post(config.url + "channel/removeowner/v1", json = {
    "token": make_token(0),
    "channel_id": 2,
    "u_id": 2,
})
payload = r.json()
assert payload == {}
r = requests.post(config.url + "channel/removeowner/v1", json = {
    "token": make_token(0),
    "channel_id": 2,
    "u_id": 1,
})
payload = r.json()
assert payload == {}
r = requests.get(config.url + "channel/details/v2", json = {
    "token": make_token(1),
    "channel_id": 2,
})
payload = r.json()
assert payload == {
    "name": "PublicChannel3",
    "is_public": True,
    "owner_members": [
        {
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
    ],
    "all_members": [
        {
            'u_id': 1,
            'email': 'petertran@email.com',
            'name_first': 'Peter',
            'name_last': 'Tran',
            'handle_str': 'petertran',
        },
        {
            'u_id': 0,
            'email': 'gungeetsingh@email.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        },
        {
            'u_id': 2,
            'email': 'christopherluong@email.com',
            'name_first': 'Christopher',
            'name_last': 'Luong',
            'handle_str': 'christopherluong',
        },
    ],
}

# Test the errors for channel_addowner_v1 and channel_removeowner_v1

def test_channel_add_leave_owner_v1_errors(user_setup, channel_setup_single_user):
'''
#test the errors for channel_addowner_v1 and channel_removeowner_v1
'''
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 1,
    "u_id": 0,
})
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 1,
    "u_id": 2,
})
# Test 6:
# invalid channel
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/addowner/v1', json = {
            'token': make_token(1),
            'channel_id': 10,
            'u_id': 0,
        }).raise_for_status()

# Test 7:
# authorised user doesn't exist
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/addowner/v1', json = {
            'token': make_token(10),
            'channel_id': 1,
            'u_id': 0,
        }).raise_for_status()

# Test 8:
# user is already an owner
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/addowner/v1', json = {
            'token': make_token(1),
            'channel_id': 1,
            'u_id': 1,
        }).raise_for_status()


# Test 9:
# authorised user is not an owner
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + "channel/addowner/v1", json = {
        "token": make_token(0),
        "channel_id": 1,
        "u_id": 2,
    }).raise_for_status()

# Test 10:
# invalid channel
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/removeowner/v1', json = {
            'token': make_token(1),
            'channel_id': 10,
            'u_id': 1,
        }).raise_for_status()

# Test 11:
# authorised user doesn't exist
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/removeowner/v1', json = {
            'token': make_token(10),
            'channel_id': 1,
            'u_id': 1,
        }).raise_for_status()

# Test 12:
# user is currently the only owner
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + 'channel/removeowner/v1', json = {
            'token': make_token(1),
            'channel_id': 1,
            'u_id': 1,
        }).raise_for_status()

# Test 13:
# authorised user is not an owner
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + "channel/removeowner/v1", json = {
        "token": make_token(0),
        "channel_id": 1,
        "u_id": 1,
    }).raise_for_status()

# Test 14:
# user is not the owner of the channel
with pytest.raises(requests.exceptions.HTTPError):
    requests.post(config.url + "channel/removeowner/v1", json = {
        "token": make_token(1),
        "channel_id": 1,
        "u_id": 2,
    })

# Tests for channel_messages_v2

def test_channel_messages_v2():
'''
#Tests for channel_messages_v2
'''
# Test 1:
# send a message to a public channel and check the message exists
requests.post(config.url + "message/send/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
    "message": "onions can be eaten raw",
})
dateTimeObj = datetime.now()
timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(1),
    "channel_id": 0,
    "start": 0,
})
payload = r.json()
assert payload == {
    "messages": [
        {
        "message_id": 0,
        "u_id": 1,
        "message": "onions can be eaten raw",
        "time_created": timeStampStr,
        },
    ],
    "start": 0,
    "end": -1,
}

# Test 2:
# check the messages in a fresh public channel
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(1),
    "channel_id": 1,
    "start": 0,
})
payload == r.json()
assert payload == {
    "messages": [],
    "start": 0,
    "end": -1,
}

# Test 3:
# add a user to a public channel and they send a message
# check the messages sent in a public channel/
#   after the user leaves the channel
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 1,
    "u_id": 0,
})
requests.post(config.url + "messages/send/v2", json = {
    "token": make_token(0),
    "channel_id": 1,
    "message": "onions cannot be eaten raw",
})
dateTimeObj = datetime.now()
timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
requests.post(config.url + "channel/leave/v1", json = {
    "token": make_token(0),
    "channel_id": 1,
})
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(1),
    "channel_id": 1,
    "start": 0,
})
payload = r.json()
assert payload == {
    "messages": [
        {
        "message_id": 0,
        "u_id": 0,
        "message": "onions cannot be eaten raw",
        "time_created": timeStampStr,
        },
    ],
    "start": 0,
    "end": -1,
}

# Test 4:
# invite the first and third user to join a public channel
# everyone sends an identical message from the first to the third user/ 
#   and check the messages in the channel
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 2,
    "u_id": 0,
})
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 2,
    "u_id": 2,
})
timeStampStr = []
requests.post(config.url + "messages/send/v2", json = {
    "token": make_token(0),
    "channel_id": 2,
    "message": "wait until you try raw radishes",
})
dateTimeObj = datetime.now()
timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
requests.post(config.url + "messages/send/v2", json = {
    "token": make_token(1),
    "channel_id": 2,
    "message": "wait until you try raw radishes",
})
dateTimeObj = datetime.now()
timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
requests.post(config.url + "messages/send/v2", json = {
    "token": make_token(2),
    "channel_id": 2,
    "message": "wait until you try raw radishes",
})
dateTimeObj = datetime.now()
timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(1),
    "channel_id": 2,
    "start": 0,
})
payload = r.json()
assert payload == {
    "messages": [
        {
        "message_id": 2,
        "u_id": 2,
        "message": "wait until you try raw radishes",
        "time_created": timeStampStr[2],
        },
        {
        "message_id": 1,
        "u_id": 1,
        "message": "wait until you try raw radishes",
        "time_created": timeStampStr[1],
        },
        {
        "message_id": 0,
        "u_id": 0,
        "message": "wait until you try raw radishes",
        "time_created": timeStampStr[0],
        },
    ],
    "start": 0,
    "end": -1,
}

# Test 5:
# send a message to a private channel and check the message exists
requests.post(config.url + "message/send/v2", json = {
    "token": make_token(1),
    "channel_id": 3,
    "message": "onions can be eaten raw",
})
dateTimeObj = datetime.now()
timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(1),
    "channel_id": 3,
    "start": 0,
})
payload == r.json()
assert payload == {
    "messages": [
        {
        "message_id": 0,
        "u_id": 1,
        "message": "onions can be eaten raw",
        "time_created": timeStampStr,
        },
    ],
    "start": 0,
    "end": -1,
}

# Test 6:
# check the messages in a fresh private channel
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(1),
    "channel_id": 4,
    "start": 0,
})
payload == r.json()
assert payload == {
    "messages": [],
    "start": 0,
    "end": -1,
}

# Test 7:
# add a user to a private channel and they send a message
# check the messages sent in a private channel/
#   after the user leaves the channel
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 4,
    "u_id": 0,
})
requests.post(config.url + "messages/send/v2", json = {
    "token": make_token(0),
    "channel_id": 4,
    "message": "onions cannot be eaten raw",
})
dateTimeObj = datetime.now()
timeStampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
requests.post(config.url + "channel/leave/v1", json = {
    "token": make_token(0),
    "channel_id": 4,
})
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(1),
    "channel_id": 4,
    "start": 0,
})
payload = r.json()
assert payload == {
    "messages": [
        {
        "message_id": 0,
        "u_id": 0,
        "message": "onions cannot be eaten raw",
        "time_created": timeStampStr,
        },
    ],
    "start": 0,
    "end": -1,
}

# Test 8:
# invite the first and third user to join a public channel
# everyone sends an identical message from the first to the third user/ 
#   and check the messages in the channel
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 5,
    "u_id": 0,
})
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 5,
    "u_id": 2,
})
timeStampStr = []
requests.post(config.url + "messages/send/v2", json = {
    "token": make_token(0),
    "channel_id": 5,
    "message": "wait until you try raw radishes",
})
dateTimeObj = datetime.now()
timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
requests.post(config.url + "messages/send/v2", json = {
    "token": make_token(1),
    "channel_id": 5,
    "message": "wait until you try raw radishes",
})
dateTimeObj = datetime.now()
timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
requests.post(config.url + "messages/send/v2", json = {
    "token": make_token(2),
    "channel_id": 5,
    "message": "wait until you try raw radishes",
})
dateTimeObj = datetime.now()
timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(1),
    "channel_id": 5,
    "start": 0,
})
payload = r.json()
assert payload == {
    "messages": [
        {
        "message_id": 2,
        "u_id": 2,
        "message": "wait until you try raw radishes",
        "time_created": timeStampStr[2],
        },
        {
        "message_id": 1,
        "u_id": 1,
        "message": "wait until you try raw radishes",
        "time_created": timeStampStr[1],
        },
        {
        "message_id": 0,
        "u_id": 0,
        "message": "wait until you try raw radishes",
        "time_created": timeStampStr[0],
        },
    ],
    "start": 0,
    "end": -1,
}

# Test 9:
# invite the third user to a public server/
#   they send 51 messages and check the messages
requests.post(config.url + 'channels/create/v2', json = {
    "token": make_token(1),
    "name": "PublicChannel4",
    "is_public": True,
})
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 6,
    "u_id": 2,
})
timeStampStr = []
for i in range(51):
    requests.post(config.url + "messages/send/v2", json = {
        "token": make_token(2),
        "channel_id": 6,
        "message": str(i),
    })
    dateTimeObj = datetime.now()
    timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(2),
    "channel_id": 6,
    "start": "0",
})
messages = []
for i in range(50):
    message = {
        "message_id": (50 - i),
        "u_id": 2,
        "message": str(50 - i),
        "time_created": timeStampStr[50 - i],
    }
    messages.append(message)
payload = r.json()
assert payload == {
    "messages": messages,
    "start": 0,
    "end": 49,
}
# sends the least recent message
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(2),
    "channel_id": 6,
    "start": 50,
})
payload = r.json()
assert payload == {
    "messages": [
        {
            "message_id": 0,
            "u_id": 2,
            "message": "0",
            "time_created": timeStampStr[0],
        }
    ],
    "start": 50,
    "end": -1,
}

# Test 10:
# invite the third user to a private server/
#   they send 51 messages and check the messages
requests.post(config.url + 'channels/create/v2', json = {
    "token": make_token(1),
    "name": "PrivateChannel4",
    "is_public": False,
})
requests.post(config.url + "channel/invite/v2", json = {
    "token": make_token(1),
    "channel_id": 7,
    "u_id": 2,
})
timeStampStr = []
for i in range(51):
    requests.post(config.url + "messages/send/v2", json = {
        "token": make_token(2),
        "channel_id": 7,
        "message": str(i),
    })
    dateTimeObj = datetime.now()
    timeStampStr.append(dateTimeObj.strftime("%d-%b-%Y (%H:%M)"))
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(2),
    "channel_id": 7,
    "start": 0,
})
messages = []
for i in range(50):
    message = {
        "message_id": (50 - i),
        "u_id": 2,
        "message": str(50 - i),
        "time_created": timeStampStr[50 - i],
    }
    messages.append(message)
payload = r.json()
assert payload == {
    "messages": messages,
    "start": 0,
    "end": 49,
}
# sends the least recent message
r = requests.get(config.url + "channel/messages/v2", json = {
    "token": make_token(2),
    "channel_id": 7,
    "start": 50,
})
payload = r.json()
assert payload == {
    "messages": [
        {
            "message_id": 0,
            "u_id": 2,
            "message": "0",
            "time_created": timeStampStr[0],
        }
    ],
    "start": 50,
    "end": -1,
}

# Test the errors for channel_messages_v2
'''
def test_channel_messages_v2_errors(user_setup, channel_setup_single_user):
    '''
    test the errors for channel_messages_v2
    '''
    # Test 11:
    # invalid channel id
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/messages/v2', json = {
                'token': make_token(1),
                'channel_id': 10,
                'start': 0,
            }).raise_for_status()
    
    # Test 12:
    # start is greater than the total of messages in the channel
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/messages/v2', json = {
                'token': make_token(1),
                'channel_id': 1,
                'start': 100,
            }).raise_for_status()

    # Test 13:
    # authorised user is not a member of the channel
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/messages/v2', json = {
                'token': make_token(2),
                'channel_id': 1,
                'start': 0,
            }).raise_for_status()

    # Test 14:
    # invalid authorised user
    with pytest.raises(requests.exceptions.HTTPError):
        requests.post(config.url + 'channel/messages/v2', json = {
                'token': make_token(10),
                'channel_id': 1,
                'start': 0,
            }).raise_for_status()
