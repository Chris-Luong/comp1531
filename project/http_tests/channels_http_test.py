'''
channels_test.py
'''
"""
import pytest
import requests
from src import config
from src.helper import make_token
import json
from src.clear import clear_v1

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
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "talavrahami@email.com",
        "password": "password",
        "name_first": "Tal",
        "name_last": "Avrahami"
    })
    # login the 3 users who have been registered
    requests.post(config.url + 'auth/login/v2', json = {
        "email": "gungeetsingh@email.com",
        "password": "password",
    })
    requests.post(config.url + 'auth/login/v2', json = {
        "email": "petertran@email.com",
        "password": "password",
    })
    requests.post(config.url + 'auth/login/v2', json = {
        "email": "christopherluong@email.com",
        "password": "password",
    })
    requests.post(config.url + 'auth/login/v2', json = {
        "email": "talavrahami@email.com",
        "password": "password",
    })

@pytest.fixture
def channel_setup():
    '''
    Create 3 public and private channels by the same user
    '''
    # create multiple public channels for single user (Non-dream owner)
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(0),
        "name": "Gchannel1",
        "is_public": True,
    })
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(1),
        "name": "Pchannel1",
        "is_public": True,
    })
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(2),
        "name": "Cchannel1",
        "is_public": True,
    })

@pytest.fixture
def channel_setup_owner():
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(0),
        "name": "Gchannel1",
        "is_public": True,
    })
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(0),
        "name": "Gchannel2",
        "is_public": True,
    })
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(0),
        "name": "Gchannel3",
        "is_public": False,
    })

def test_channels_list_v2_single_user(user_setup, channel_setup):
    '''
    list the single channel associated with a single user
    '''
    r = requests.get(config.url + 'channels/list/v2', json = {
        "token": make_token(1),
    })
    payload = r.json()
    assert payload == {
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
    requests.post(config.url + "channel/invite/v2", json = {
        "token": make_token(1),
        "channel_id": 1,
        "u_id": 2,
    })
    r = requests.get(config.url + 'channels/list/v2', json = {
        "token": make_token(1),
    })
    payload = r.json()
    assert payload == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'Pchannel',
            },
        ],
    }

def test_channels_list_v2_invited_by_non_owner(user_setup, channel_setup):
    '''
    list channels after inviting another user (owner)
    '''
    requests.post(config.url + "channel/invite/v2", json = {
        "token": make_token(1),
        "channel_id": 1,
        "u_id": 2,
    })
    requests.post(config.url + "channel/invite/v2", json = {
        "token": make_token(2),
        "channel_id": 1,
        "u_id": 3,
    })
    r = requests.get(config.url + 'channels/list/v2', json = {
        "token": make_token(1),
    })
    payload = r.json()
    assert payload == {
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
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(1),
        "name": "Pchannel1",
        "is_public": True,
    })
    
    r = requests.get(config.url + 'channels/list/v2', json = {
        'token': make_token(5),
    })
    
    assert r.status_code == 403

def test_channels_listall_v2_success(user_setup, channel_setup_owner):
    '''
    Lists all created channels even if user is not in any/all channels
    '''
    r = requests.get(config.url + 'channels/listall/v2', json = {
        'token': make_token(0),
    })
    payload = r.json()
    assert payload == {
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
    requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(1),
        "name": "Pchannel1",
        "is_public": True,
    })
    
    r = requests.get(config.url + 'channels/listall/v2', json = {
        'token': make_token(1000),
    })

    assert r.status_code == 403

def test_channels_create_v2_works(user_setup):
    '''
    User is able to create a channel
    '''
    r = requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(0),
        "name": "channel1",
        "is_public": True,
    })
    payload = r.json()
    assert payload == {'channel_id': 0}
    r = requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(0),
        "name": "channel2",
        "is_public": True,
    })
    payload = r.json()
    assert payload == {'channel_id': 1}
    r = requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(0),
        "name": "channel3",
        "is_public": True,
    })
    payload = r.json()
    assert payload == {'channel_id': 2}

def test_channels_create_v2_name_too_long(user_setup):
    '''
    User attempts to create a channel whose name is too long and fails
    '''
    badname1 = 'brothisnameiswaytoolongicantbelieveyouwouldeventrythisman'
    badname2 = 'youreallytryingtoputanotherlongnamebroyouneverlearn'
    # for public channel
    r = requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(0),
        "name": badname1,
        "is_public": True,
    })
    
    assert r.status_code == 400

    # for private channel
    r = requests.post(config.url + 'channels/create/v2', json = {
        "token": make_token(0),
        "name": badname2,
        "is_public": False,
    })
    
    assert r.status_code == 400
"""
