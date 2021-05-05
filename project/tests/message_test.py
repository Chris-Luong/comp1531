from src.auth import auth_register_v2
from src.auth import auth_login_v2
from src.channels import channels_create_v2
from src.channel import channel_details_v2
from src.channel import channel_join_v2
from src.channel import channel_messages_v2
from src.dm import dm_details_v1
from src.dm import dm_create_v1
from src.dm import dm_remove_v1
from src.dm import dm_leave_v1
from src.dm import dm_messages_v1
from src.message import message_send_v2
from src.message import message_edit_v2
from src.message import message_remove_v1
from src.message import message_share_v1
from src.message import message_senddm_v1
from src.error import InputError
from src.error import AccessError
from src.clear import clear_v1
from src.helper import make_token, create_timestamp
from src.message import message_react_v1, message_pin_v1, message_sendlater_v1
from src.message import message_unreact_v1, message_unpin_v1, message_sendlaterdm_v1
import datetime

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
    auth_register_v2("talavrahami@email.com", "password", "Tal", "Avrahami")
    # login the 4 users who have been registered
    auth_login_v2("gungeetsingh@email.com", "password")
    auth_login_v2("petertran@email.com", "password")
    auth_login_v2("christopherluong@email.com", "password")
    auth_login_v2("talavrahami@email.com", "password")

@pytest.fixture
def dm_setup():
    # create multiple public dms for single user with varying users
    dm_create_v1(make_token(1), [0, 2])
    dm_create_v1(make_token(0), [1])
    dm_create_v1(make_token(2), [1])
    # dm0: user 1, 0, 2
    # dm1: user 0, 1
    # dm2: user 2, 1

@pytest.fixture
def channel_setup():
    # create multiple public channels for single user (last one is dream owner)
    channels_create_v2(make_token(2), "Channel1", True)
    channels_create_v2(make_token(1), "Channel2", True)
    channels_create_v2(make_token(0), "Channel3", True)
    channel_join_v2(make_token(3), 0)
    # channel0: user 2, 3
    # channel1: user 1
    # channel2: user 0

@pytest.fixture
def message_setup():
    # send 10 messages to first channel
    message_send_v2(make_token(3), 0, "0")
    message_send_v2(make_token(1), 1, "1")
    message_send_v2(make_token(3), 0, "2")
    message_send_v2(make_token(2), 0, "3")
    message_send_v2(make_token(2), 0, "4")
    message_send_v2(make_token(2), 0, "5")
    message_send_v2(make_token(2), 0, "6")
    message_send_v2(make_token(2), 0, "7")
    message_send_v2(make_token(2), 0, "8")
    message_send_v2(make_token(2), 0, "9")
    
    # send 10 dms
    message_senddm_v1(make_token(1), 1, "10")
    message_senddm_v1(make_token(1), 1, "11")
    message_senddm_v1(make_token(1), 1, "12")
    message_senddm_v1(make_token(1), 1, "13")
    message_senddm_v1(make_token(1), 1, "14")
    message_senddm_v1(make_token(1), 1, "15")
    message_senddm_v1(make_token(1), 1, "16")
    message_senddm_v1(make_token(1), 1, "17")
    message_senddm_v1(make_token(2), 2, "18")
    message_senddm_v1(make_token(2), 0, "19")

#------------------Tests for message_send_v2-------------------

def test_message_send_v2_errors(user_setup, channel_setup):
    
    # Test 1:
    # invalid token
    with pytest.raises(AccessError):
        message_send_v2(make_token(414345), 0, "invalid token error")
    # "Invalid token"

    # Test 2:
    # auhtorised user is not part of channel
    with pytest.raises(AccessError):
        message_send_v2(make_token(2), 2, "user not part of channel error")
    # "Authorised user is not part of the channel"

    # Test 3:
    # message too long
    with pytest.raises(InputError):
        message_send_v2(make_token(1), 1, "1" * 1000 + "too many chars error")
    # "Message is longer than the 1000 character limit"

def test_message_send_v2(user_setup, channel_setup):
    '''
    Test for message_id, send a bunch and check if the id increases accordingly i.e. 0, 1, 2, etc.
    then send identical message in another channel and see if it still increases accordingly
    '''
    # Test one channel
    assert message_send_v2(make_token(2), 0, "0") == {'message_id': 0}
    assert message_send_v2(make_token(0), 2, "1") == {'message_id': 1}
    assert message_send_v2(make_token(2), 0, "2") == {'message_id': 2}
    # Test another channel
    assert message_send_v2(make_token(1), 1, "3") == {'message_id': 3}
    assert message_send_v2(make_token(1), 1, "4") == {'message_id': 4}
    # Test duplicate messages and different channels
    assert message_send_v2(make_token(0), 2, "3") == {'message_id': 5}
    assert message_send_v2(make_token(1), 1, "3") == {'message_id': 6}
    assert message_send_v2(make_token(0), 2, "3") == {'message_id': 7}
    assert message_send_v2(make_token(1), 1, "8") == {'message_id': 8}
    assert message_send_v2(make_token(1), 1, "3") == {'message_id': 9}
    assert message_send_v2(make_token(0), 2, "10") == {'message_id': 10}
    assert message_send_v2(make_token(2), 0, "11") == {'message_id': 11}

#------------------Tests for message_remove_v1-------------------


def test_message_remove_v1_errors(user_setup, channel_setup, dm_setup, message_setup):
    '''
    removing message doesnt change other message ids
    '''
    # Test 1:
    # invalid token
    with pytest.raises(AccessError):
        message_remove_v1(make_token(414345), 0)
    # "Invalid token"

    # Test 2:
    # authorised user did not send this message and is not owner of channel/Dreams
    with pytest.raises(AccessError):
        message_remove_v1(make_token(1), 0)
    # "Authorised User is not the owner of this channel/Dreams and did not send this message"
    with pytest.raises(AccessError):
        message_remove_v1(make_token(1), 19)
    # "Authorised User is not an owner of Dreams and did not send this message"

    # Test 3:
    # removing a deleted/non-existent message
    message_remove_v1(make_token(2), 9)
    with pytest.raises(InputError):
        message_remove_v1(make_token(2), 9)
    with pytest.raises(InputError):
        message_remove_v1(make_token(2), 1000)
    # "Message does not exist"

def test_message_remove_v1_success(user_setup, channel_setup, dm_setup, message_setup):
    message_remove_v1(make_token(2), 9)
    message_remove_v1(make_token(2), 8)
    message_remove_v1(make_token(2), 7)
    message_remove_v1(make_token(2), 6)
    message_remove_v1(make_token(2), 5)
    message_remove_v1(make_token(2), 4)
    message_remove_v1(make_token(2), 3)
    message_remove_v1(make_token(3), 2)
    message_remove_v1(make_token(1), 1)
    message_remove_v1(make_token(3), 0)
    assert channel_messages_v2(make_token(2), 0, 0) == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

def test_message_remove_then_add(user_setup, channel_setup, dm_setup, message_setup):
    message_remove_v1(make_token(3), 0)
    message_remove_v1(make_token(1), 1)
    assert message_send_v2(make_token(2), 0, "hello") == {'message_id': 20}
    assert message_send_v2(make_token(2), 0, "hello2") == {'message_id': 21}
    
    message_remove_v1(make_token(1), 10)
    assert message_senddm_v1(make_token(1), 1, "hello2") == {'message_id': 22}
#------------------Tests for message_edit_v2-------------------

def test_message_edit_v2_errors(user_setup, channel_setup, dm_setup, message_setup):

    # Test 1:
    # invalid token
    with pytest.raises(AccessError):
        message_edit_v2(make_token(414345), 0, "invalid token error")

    # Test 2:
    # authorised user did not send this message and is not owner of channel/Dreams
    with pytest.raises(AccessError):
        message_edit_v2(make_token(1), 0, "user didnt send this msg error")
    # "Authorised User is not the owner of this channel and did not send this message"
    with pytest.raises(AccessError):
        message_edit_v2(make_token(2), 10, "user didnt send this msg error")
    # "Authorised User is not an owner of Dreams and did not send this message"
    
    # Test 3:
    # message too long
    with pytest.raises(InputError):
        message_edit_v2(make_token(2), 2, "1" * 1000 + "too many chars error")
    # "Message is longer than the 1000 character limit"
    # testing to remove a message and then try edit that removed message
    message_edit_v2(make_token(2), 9, '')
    with pytest.raises(InputError):
        message_edit_v2(make_token(2), 9, "deleted msg error")
    with pytest.raises(InputError):
        message_edit_v2(make_token(2), 1000, "non-existent msg error")
    # "Message does not exist"

def test_message_edit_v2(user_setup, channel_setup, dm_setup, message_setup):
    
    message_edit_v2(make_token(3), 0, "sender changed")
    assert channel_messages_v2(make_token(3), 0, 0) == {
        "messages": [
            {
                "message_id": 9,
                "u_id": 2,
                "message": "9",
                "time_created": create_timestamp(),
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
            {
                "message_id": 8,
                "u_id": 2,
                "message": "8",
                "time_created": create_timestamp(),
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
            {
                "message_id": 7,
                "u_id": 2,
                "message": "7",
                "time_created": create_timestamp(),
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
            {
                "message_id": 6,
                "u_id": 2,
                "message": "6",
                "time_created": create_timestamp(),
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
            {
                "message_id": 5,
                "u_id": 2,
                "message": "5",
                "time_created": create_timestamp(),
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
            {
                "message_id": 4,
                "u_id": 2,
                "message": "4",
                "time_created": create_timestamp(),
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
            {
                "message_id": 3,
                "u_id": 2,
                "message": "3",
                "time_created": create_timestamp(),
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
            {
                "message_id": 2,
                "u_id": 3,
                "message": "2",
                "time_created": create_timestamp(),
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
            {
                "message_id": 0,
                "u_id": 3,
                "message": "sender changed",
                "time_created": create_timestamp(),
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

#------------------Tests for message_share_v1-------------------


def test_message_share_v1_errors(user_setup, channel_setup, dm_setup, message_setup):

    # Test 1:
    # invalid token
    with pytest.raises(AccessError):
        message_share_v1(make_token(414345), 0, "invalid token error", 0, -1)
    # "Invalid token"

    # Test 2:
    # auhtorised user is not part of channel
    with pytest.raises(AccessError):
        message_share_v1(make_token(2), 3, "user not part of channel error", 2, -1)
    # "Authorised user is not part of the channel"
    with pytest.raises(AccessError):
        message_share_v1(make_token(0), 18, "user not part of dm error", -1, 2)
    # "Authorised user needs to be a member of the dm"
'''
def test_message_share_v1_success(user_setup, channel_setup, dm_setup, message_setup):
    channel_join_v2(make_token(3), 1)
    channel_join_v2(make_token(2), 1)

    message_share_v1(make_token(3), 0, "0", 1, -1)
    message_share_v1(make_token(3), 2, "2", 1, -1)
    message_share_v1(make_token(2), 3, "3", 1, -1)

    assert channel_messages_v2(make_token(1), 1, 0) == {
        "messages": [
            {
                "message_id": 1,
                "u_id": 1,
                "message": "1",
                "time_created": create_timestamp(),
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
            {
                "message_id": 3,
                "u_id": 2,
                "message": "2",
                "time_created": create_timestamp(),
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
            {
                "message_id": 2,
                "u_id": 3,
                "message": "2",
                "time_created": create_timestamp(),
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
            {
                "message_id": 0,
                "u_id": 3,
                "message": "0",
                "time_created": create_timestamp(),
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
'''
#------------------Tests for message_senddm_v1-------------------

def test_message_senddm_v1_errors(user_setup, dm_setup):
    
    # Test 1:
    # invalid token
    with pytest.raises(AccessError):
        message_senddm_v1(make_token(414345), 0, "invalid token error")
    # "Invalid token"

    # Test 2:
    # auhtorised user is not part of channel
    with pytest.raises(AccessError):
        message_senddm_v1(make_token(2), 1, "user not part of channel error")
    # "Authorised user is not a member of the dm"

    # Test 3:
    # message too long
    with pytest.raises(InputError):
        message_senddm_v1(make_token(1), 1, "1" * 1000 + "too many chars error")
    # "Message is longer than the 1000 character limit"

def test_message_senddm_v1(user_setup, dm_setup):
    '''
    Test for message_id, send a bunch and check if the id increases accordingly i.e. 0, 1, 2, etc.
    then send identical message in another channel and see if it still increases accordingly
    '''
    # dm0: user 1, 0, 2
    # dm1: user 0, 1
    # dm2: user 2, 1
    # Test one dm
    assert message_senddm_v1(make_token(2), 0, "0") == {'message_id': 0}
    assert message_senddm_v1(make_token(0), 1, "1") == {'message_id': 1}
    assert message_senddm_v1(make_token(2), 0, "2") == {'message_id': 2}
    # Test another dm
    assert message_senddm_v1(make_token(1), 1, "3") == {'message_id': 3}
    assert message_senddm_v1(make_token(1), 1, "4") == {'message_id': 4}
    # Test duplicate messages and different dms
    assert message_senddm_v1(make_token(0), 1, "3") == {'message_id': 5}
    assert message_senddm_v1(make_token(1), 1, "3") == {'message_id': 6}
    assert message_senddm_v1(make_token(0), 1, "3") == {'message_id': 7}
    assert message_senddm_v1(make_token(1), 1, "8") == {'message_id': 8}
    assert message_senddm_v1(make_token(1), 1, "3") == {'message_id': 9}
    assert message_senddm_v1(make_token(0), 1, "10") == {'message_id': 10}
    assert message_senddm_v1(make_token(2), 0, "11") == {'message_id': 11}

def test_react_and_unreact_v1(user_setup, dm_setup, channel_setup):
    # react to the message in the channel
    message_send_v2(make_token(2), 0, "0")
    assert message_react_v1(make_token(2), 0, 1) == {}
    # react to the message in the dm
    
    message_senddm_v1(make_token(2), 0, "1")
    assert message_react_v1(make_token(2), 1, 1) == {}
    assert channel_messages_v2(make_token(2), 0, 0) == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 2,
                "message": "0",
                "time_created": create_timestamp(),
                "channel_id": 0,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [2], 
                        'is_this_user_reacted': True
                    }
                ],
                'is_pinned': False
            },
        ],
        "start": 0,
        "end": -1,
    }
    assert dm_messages_v1(make_token(2), 0, 0) == {
        "messages": [
            {
                "message_id": 1,
                "u_id": 2,
                "message": "1",
                "time_created": create_timestamp(),
                "channel_id": -1,
                "dm_id": 0,
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [2], 
                        'is_this_user_reacted': True
                    }
                ],
                'is_pinned': False
            },
        ],
        "start": 0,
        "end": -1,
    }

    # remove all the reacts
    assert message_unreact_v1(make_token(2), 0, 1) == {}
    assert message_unreact_v1(make_token(2), 1, 1) == {}
    assert channel_messages_v2(make_token(2), 0, 0) == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 2,
                "message": "0",
                "time_created": create_timestamp(),
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

def test_message_pin_and_unpin(user_setup, dm_setup, channel_setup):
    message_send_v2(make_token(2), 0, "0")
    assert message_pin_v1(make_token(2), 0) == {}
    assert channel_messages_v2(make_token(2), 0, 0) == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 2,
                "message": "0",
                "time_created": create_timestamp(),
                "channel_id": 0,
                "dm_id": -1,
                'reacts': [
                    {
                        'react_id': 1, 
                        'u_ids': [], 
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': True
            },
        ],
        "start": 0,
        "end": -1,
    }
    assert message_unpin_v1(make_token(2), 0) == {}
    assert channel_messages_v2(make_token(2), 0, 0) == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 2,
                "message": "0",
                "time_created": create_timestamp(),
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

def test_message_sendlater_sendlaterdm(user_setup, dm_setup, channel_setup):
    assert message_sendlater_v1(make_token(2), 0, "Hello", datetime.datetime.now().timestamp() + 1) == {"message_id": 0}
    assert message_sendlater_v1(make_token(2), 0, "Hi", datetime.datetime.now().timestamp() + 1) == {"message_id": 1}
    assert message_sendlaterdm_v1(make_token(2), 0, "Hello", datetime.datetime.now().timestamp() + 1) == {"message_id": 2}
    assert message_sendlaterdm_v1(make_token(2), 0, "Hi", datetime.datetime.now().timestamp() + 1) == {"message_id": 3}

def test_message_sendlater_errors(user_setup, dm_setup, channel_setup, message_setup):
    # invalid token
    with pytest.raises(AccessError):
        message_sendlater_v1(make_token(100000), 0, "hello", datetime.datetime.now().timestamp() + 1)
    
    # channel id is not a valid channel
    with pytest.raises(InputError):
        message_sendlater_v1(make_token(1), 10, "hello", datetime.datetime.now().timestamp() + 1)

    # message is more than 1000 characters
    thousand_string = ''
    for i in range(1005):
        thousand_string += str(i)
    with pytest.raises(InputError):
        message_sendlater_v1(make_token(2), 0, thousand_string, datetime.datetime.now().timestamp() + 1)

    # time sent is a time in the past
    with pytest.raises(InputError):
        message_sendlater_v1(make_token(2), 0, "hello", datetime.datetime.now().timestamp() - 5)

    # authorised user has not joined the channel they are trying to post to
    with pytest.raises(AccessError):
        message_sendlater_v1(make_token(1), 2, "hello", datetime.datetime.now().timestamp() + 1)

def test_message_sendlaterdm_errors(user_setup, dm_setup, channel_setup, message_setup):
    # invalid token
    with pytest.raises(AccessError):
        message_sendlater_v1(make_token(100000), 0, "hello", datetime.datetime.now().timestamp() + 1)

    # DM ID is not a valid DM
    with pytest.raises(InputError):
        message_sendlaterdm_v1(make_token(2), 20, "hello", datetime.datetime.now().timestamp() + 1)

    # Message is more than 1000 characters
    thousand_string = ''
    for i in range(1005):
        thousand_string += str(i)
    with pytest.raises(InputError):
        message_sendlaterdm_v1(make_token(2), 0, thousand_string, datetime.datetime.now().timestamp() + 1)
    # Time sent is a time in the past
    with pytest.raises(InputError):
        message_sendlaterdm_v1(make_token(2), 0, "hello", datetime.datetime.now().timestamp() - 5)

    # the authorised user is not a member of the DM they are trying to post to
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(make_token(2), 1, "hello", datetime.datetime.now().timestamp() + 1)

def test_message_react_errors(user_setup, dm_setup, channel_setup, message_setup):
    with pytest.raises(AccessError):
        message_react_v1(make_token(10000), 0, 1)

    # message_id is not a valid message within a channel or DM that the authorised user has joined
    with pytest.raises(InputError):
        message_react_v1(make_token(1), 100, 1)

    # react_id is not a valid React ID
    with pytest.raises(InputError):
        message_react_v1(make_token(2), 0, 5)

    # Message with ID message_id already contains an active React with ID/
    #   react_id from the authorised user
    message_react_v1(make_token(2), 0, 1)
    with pytest.raises(InputError):
        message_react_v1(make_token(2), 0, 1)

    # The authorised user is not a member of the channel or DM that the message is within
    message_send_v2(make_token(0), 2, "yuh")
    with pytest.raises(AccessError):
        message_react_v1(make_token(1), 20, 1)

def test_message_unreact_errors(user_setup, dm_setup, channel_setup, message_setup):
    with pytest.raises(AccessError):
        message_unreact_v1(make_token(10000), 0, 1)

    # message_id is not a valid message within a channel or DM that the authorised user has joined
    with pytest.raises(InputError):
        message_unreact_v1(make_token(1), 100, 1)

    # react_id is not a valid React ID
    with pytest.raises(InputError):
        message_unreact_v1(make_token(2), 0, 5)

    # Message with ID message_id does not contain an active React with/
    #   ID react_id from the authorised user
    with pytest.raises(InputError):
        message_unreact_v1(make_token(2), 0, 1)

    # The authorised user is not a member of the channel or DM that the message is within
    message_send_v2(make_token(0), 2, "yuh")
    message_react_v1(make_token(0), 20, 1)
    with pytest.raises(AccessError):
        message_react_v1(make_token(1), 20, 1)

def test_message_pin_errors(user_setup, dm_setup, channel_setup, message_setup):
    with pytest.raises(AccessError):
        message_pin_v1(make_token(10000), 0)

    # message_id is not a valid message
    with pytest.raises(InputError):
        message_pin_v1(make_token(0), 25)

    # Message with ID message_id is already pinned
    message_pin_v1(make_token(2), 0)
    with pytest.raises(InputError):
        message_pin_v1(make_token(2), 0)

    # authorised user is not a member of the channel or DM that the message is within
    with pytest.raises(AccessError):
        message_pin_v1(make_token(0), 0)

    # The authorised user is not an owner of the channel or DM
    with pytest.raises(AccessError):
        message_pin_v1(make_token(3), 0)

def test_message_unpin_errors(user_setup, dm_setup, channel_setup, message_setup):
    with pytest.raises(AccessError):
        message_unpin_v1(make_token(10000), 0)

    # message_id is not a valid message
    with pytest.raises(InputError):
        message_unpin_v1(make_token(0), 25)

    # Message with ID message_id is already unpinned
    with pytest.raises(InputError):
        message_unpin_v1(make_token(2), 0)

    # The authorised user is not a member of the channel or DM that the message is within
    message_pin_v1(make_token(2), 0)
    with pytest.raises(AccessError):
        message_unpin_v1(make_token(0), 0)

    # The authorised user is not an owner of the channel or DM
    with pytest.raises(AccessError):
        message_unpin_v1(make_token(3), 0)