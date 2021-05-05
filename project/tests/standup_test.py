from src.auth import auth_register_v2
from src.auth import auth_login_v2
from src.channels import channels_create_v2
from src.channel import channel_details_v2
from src.channel import channel_join_v2, channel_invite_v2
from src.channel import channel_messages_v2
from src.standup import standup_start_v1
from src.standup import standup_active_v1
from src.standup import standup_send_v1
from src.error import InputError
from src.error import AccessError
from src.clear import clear_v1
from src.helper import make_token
from datetime import datetime, timedelta

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
def channel_setup():
    # create multiple public channels for single user (last one is dream owner)
    channels_create_v2(make_token(0), "Channel1", True)
    channels_create_v2(make_token(1), "Channel2", True)
    channels_create_v2(make_token(2), "Channel3", True)
    channels_create_v2(make_token(0), "Channel4", True)
    channel_invite_v2(make_token(0), 3, 1)
    channel_invite_v2(make_token(0), 3, 2)
    channel_invite_v2(make_token(0), 3, 3)
    # channel0: user 0
    # channel1: user 1
    # channel2: user 2, 3
    # channel3: user 0, 1, 2, 3

@pytest.fixture
def standup_setup():
    standup_start_v1(make_token(2), 2, 1)
    # channel2: standup active for 1 minute

#------------------Tests for standup_start_v1-------------------


def test_standup_start_v1_errors(user_setup, channel_setup, standup_setup):

    # Test 1:
    # invalid token
    with pytest.raises(AccessError):
        standup_start_v1(make_token(414345), 0, 5)
    # "Invalid token"

    # Test 2:
    # auhtorised user is not part of channel
    with pytest.raises(AccessError):
        standup_start_v1(make_token(2), 0, 5)
    # "Authorised user is not part of the channel"

    # Test 3:
    # invalid channel id
    with pytest.raises(InputError):
        standup_start_v1(make_token(2), 414345, 5)
    # "Invalid channel"

    # Test 4:
    # active standup is running in channel
    with pytest.raises(InputError):
        standup_start_v1(make_token(2), 2, 5)
    # "an active standup is already running blah blah"


def test_standup_start_v1(user_setup, channel_setup):

    dateTimeObj = datetime.now()
    timeStampStr = (dateTimeObj + timedelta(seconds=1)).strftime("%d-%b-%Y (%H:%M)")

    assert standup_start_v1(make_token(1), 1, 1) == {"time_finish": timeStampStr}

#------------------Tests for standup_active_v1-------------------

def test_standup_active_v1(user_setup, channel_setup, standup_setup):

    # Test 1:
    # invalid token
    with pytest.raises(AccessError):
        standup_active_v1(make_token(414345), 0)
    # "Invalid token"

    # Test 2:
    # invalid channel id
    with pytest.raises(InputError):
        standup_active_v1(make_token(2), 414345)
    # "Invalid channel"

    # Test 3:
    # no active standup
    assert standup_active_v1(make_token(0), 0) == {
        "is_active": False,
        "time_finish": None
    }

    # Test 4:
    # active standup
    dateTimeObj = datetime.now()
    timeStampStr = (dateTimeObj + timedelta(seconds=1)).strftime("%d-%b-%Y (%H:%M)")
    assert standup_active_v1(make_token(3), 2) == {
        "is_active": True,
        "time_finish": timeStampStr
    }

#------------------Tests for standup_send_v1-------------------

def test_standup_send_v1_errors(user_setup, channel_setup, standup_setup):

    # Test 1:
    # invalid token
    with pytest.raises(AccessError):
        standup_send_v1(make_token(414345), 0, "invalid token error")
    # "Invalid token"

    # Test 2:
    # auhtorised user is not part of channel
    with pytest.raises(AccessError):
        standup_send_v1(make_token(2), 0, "Not part of channel error")
    # "Authorised user is not part of the channel"

    # Test 3:
    # invalid channel id
    with pytest.raises(InputError):
        standup_send_v1(make_token(2), 414345, "invalid channel error")
    # "Invalid channel"

    # Test 4:
    # message too long
    with pytest.raises(AccessError):
        standup_send_v1(make_token(2), 0, "1"*999 + "Message too long error")
    # "Authorised user is not part of the channel"

    # Test 5:
    # no active standup is running in channel
    with pytest.raises(InputError):
        standup_send_v1(make_token(1), 1, "no active standup error")
    # "no active standup is running blah blah"

def test_standup_send_v1(user_setup, channel_setup):

    # send some messages to standup
    standup_start_v1(make_token(0), 3, 1)
    assert standup_send_v1(make_token(0), 3, "0") == {}
    assert standup_send_v1(make_token(1), 3, "1") == {}
    assert standup_send_v1(make_token(2), 3, "2") == {}
    assert standup_send_v1(make_token(3), 3, "3") == {}