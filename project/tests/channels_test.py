'''
channels_test.py
'''

import json
import pytest
from src.auth import auth_register_v2
from src.auth import auth_login_v2
from src.channels import channels_create_v2
from src.channels import channels_list_v2
from src.channels import channels_listall_v2
from src.channel import channel_invite_v2
from src.error import InputError
from src.error import AccessError
from src.clear import clear_v1
from src.helper import make_token

@pytest.fixture
def user_setup():
    '''
    Clear history of all current users then register and login new users
    '''
    clear_v1()
    # register 3 users with email, password, first name and last name
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
    '''
    Create multiple channels for multiple users
    '''
    channels_create_v2(make_token(0), 'Gchannel', True)
    channels_create_v2(make_token(1), 'Pchannel', True)
    channels_create_v2(make_token(2), 'Cchannel', True)

@pytest.fixture
def channel_setup_owner():
    '''
    Create multiple channels for the same user
    '''
    channels_create_v2(make_token(0), 'Gchannel1', True)
    channels_create_v2(make_token(0), 'Gchannel2', True)
    channels_create_v2(make_token(0), 'Gchannel3', False)

def test_channels_list_v2_single_user(user_setup, channel_setup):
    '''
    list the single channel associated with a single user
    '''
    assert channels_list_v2(make_token(1)) == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'Pchannel',
            },
        ],
    }

def test_channels_list_v2_invite(user_setup, channel_setup):
    '''
    list channels after inviting another user (Non-owner)
    '''
    channel_invite_v2(make_token(1), 1, 2)
    assert channels_list_v2(make_token(1)) == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'Pchannel',
            },
        ],
    }


def test_channels_list_v2_invite_by_non_owner(user_setup, channel_setup):
    '''
    list channels after inviting another user (owner)
    '''
    channel_invite_v2(make_token(1), 1, 2)
    channel_invite_v2(make_token(2), 1, 3)
    assert channels_list_v2(make_token(1)) == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'Pchannel',
            },
        ],
    }

def test_channels_list_v2_invalid_user(user_setup):
    '''
    Invalid user attempts to call channels list
    '''
    channels_create_v2(make_token(1), 'PChannel1', True)
    with pytest.raises(AccessError):
        channels_list_v2(make_token(5))

def test_channels_listall_v2_success(user_setup, channel_setup_owner):
    '''
    Lists all created channels even if user is not in any/all channels
    '''
    assert channels_listall_v2(make_token(0)) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'Gchannel1',
            },
            {
                'channel_id': 1,
                'name': 'Gchannel2',
            },
            {
                'channel_id': 2,
                'name': 'Gchannel3',
            }
        ],
    }

def test_channels_listall_v2_invalid_user(user_setup):
    '''
    Invalid user attempts to call channels listall
    '''
    channels_create_v2(make_token(1), 'PChannel1', True)
    with pytest.raises(AccessError):
        channels_list_v2(make_token(1000))

def test_channels_create_v2_works(user_setup):
    '''
    User is able to create a channel
    '''
    assert channels_create_v2(make_token(0), "channel1", True) == {'channel_id': 0}
    assert channels_create_v2(make_token(0), "channel2", True) == {'channel_id': 1}
    assert channels_create_v2(make_token(0), "channel3", True) == {'channel_id': 2}

def test_channels_create_v2_name_too_long(user_setup):
    '''
    User attempts to create a channel whose name is too long and fails
    '''
    badname1 = 'brothisnameiswaytoolongicantbelieveyouwouldeventrythisman'
    badname2 = 'youreallytryingtoputanotherlongnamebroyouneverlearn'
    # for public channel
    with pytest.raises(InputError):
        channels_create_v2(make_token(0), badname1, True)
    # for private channel
    with pytest.raises(InputError):
        channels_create_v2(make_token(0), badname2, False)
