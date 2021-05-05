import pytest
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.other import search_v2, admin_userpermission_change_v1, admin_user_remove_v1, notifications_get_v1
from src.helper import make_token, create_timestamp
from src.channels import channels_create_v2
from src.channel import channel_invite_v2, channel_messages_v2
from src.dm import dm_create_v1
from src.message import message_send_v2, message_senddm_v1
from src.clear import clear_v1
from src.user import user_profile_v1


@pytest.fixture
def register_users():
    clear_v1()
    # register 4 users with email, password, first name and last name
    # first user is the dream owner
    auth_register_v2("gungeetsingh@gmail.com", "password", "Gungeet", "Singh")
    auth_register_v2("petertran@gmail.com", "password", "Peter", "Tran")
    auth_register_v2("christopherluong@gmail.com", "password", "Christopher", "Luong")
    auth_register_v2("talavrahami@gmail.com", "password", "Tal", "Avrahami")

def test_invalid_tokens():
    with pytest.raises(AccessError):
        search_v2(make_token(5), "Hello")
        admin_userpermission_change_v1(make_token(5), 0, 0)
        admin_user_remove_v1(make_token(5), 1)
        notifications_get_v1(make_token(5))

def test_search_success(register_users):
    channels_create_v2(make_token(0), "PublicChannel1", True)
    dm_create_v1(make_token(0), [1, 2]) # dm_id 0
    message_send_v2(make_token(0), 0, "Hello")
    message_senddm_v1(make_token(0), 0, "Goodbye")

    assert search_v2(make_token(0), "Hello") == {
        "messages": [
             {
                "message_id": 0,
                "u_id": 0,
                "message": "Hello",
                "time_created": str(create_timestamp()),
                "channel_id": 0,
                "dm_id": -1,
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False
                    }
                ],
                "is_pinned": False
            }
        ]
    }

    assert search_v2(make_token(0), "Good") == {
        "messages": [
            {
                "message_id": 1,
                "u_id": 0,
                "message": "Goodbye",
                "time_created": str(create_timestamp()),
                "channel_id": -1,
                "dm_id": 0,
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False
                    }
                ],
                "is_pinned": False
            }
        ]
    }

    assert search_v2(make_token(0), "o") == {
        "messages": [
            {
                "message_id": 0,
                "u_id": 0,
                "message": "Hello",
                "time_created": str(create_timestamp()),
                "channel_id": 0,
                "dm_id": -1,
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False
                    }
                ],
                "is_pinned": False
            },
            {
                "message_id": 1,
                "u_id": 0,
                "message": "Goodbye",
                "time_created": str(create_timestamp()),
                "channel_id": -1,
                "dm_id": 0,
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False
                    }
                ],
                "is_pinned": False
            }
        ]
    }
    clear_v1()

def test_search_no_match(register_users):

    assert search_v2(make_token(0), "Ciao") == {
        "messages": [

        ]
    }

    channels_create_v2(make_token(0), "PublicChannel1", True)
    dm_create_v1(make_token(0), [1, 2]) # dm_id 0
    message_send_v2(make_token(0), 0, "Hello")
    message_senddm_v1(make_token(0), 0, "Goodbye")

    assert search_v2(make_token(0), "Ciao") == {
        "messages": [

        ]
    }

def test_invalid_permission_id(register_users):
    with pytest.raises(InputError):
        admin_userpermission_change_v1(make_token(0), 1, 5)

def test_invalid_u_id(register_users):
    with pytest.raises(InputError):
        admin_userpermission_change_v1(make_token(0), 20, 1)
        admin_user_remove_v1(make_token(0), 20)

def test_not_owner(register_users):
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(make_token(2), 1, 1)
        admin_user_remove_v1(make_token(2), 1)

def test_permission_change_valid():
    assert admin_userpermission_change_v1(make_token(0), 1, 1) == {}

def test_remove_admin():
    channels_create_v2(make_token(1), "PublicChannel1", True)
    channel_invite_v2(make_token(1), 0, 0)
    message_send_v2(make_token(1), 0, "Hello")
    assert admin_user_remove_v1(make_token(0), 1) == {}
    assert user_profile_v1(make_token(0), 1) == {
        'user': {
            'u_id': 1,
            'email': 'petertran@gmail.com',
            'name_first': 'Removed user',
            'name_last': 'Removed user',
            'handle_str': 'petertran',
        }
    }
    assert channel_messages_v2(make_token(0), 0, 0) == {
        'messages': [
            {
                "message_id": 0,
                "u_id": 1,
                "message": "Removed user",
                "time_created": str(create_timestamp()),
                "channel_id": 0,
                "dm_id": -1,
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False
                    }
                ],
                "is_pinned": False
            }
        ],
        'start': 0,
        'end': -1,
    }

def test_remove_only_owner(register_users):
     with pytest.raises(InputError):
        admin_user_remove_v1(make_token(0), 0)

def test_notifications(register_users):
    channels_create_v2(make_token(1), "PublicChannel1", True)
    channel_invite_v2(make_token(1), 0, 0)
    assert notifications_get_v1(make_token(0)) == {
        "notifications": [
            {
                "channel_id": 0,
                "dm_id": -1,
                "notification_message": "petertran invited you to PublicChannel1"
            }
        ]
    }
    dm_create_v1(make_token(0), [1]) # dm_id 0
    assert notifications_get_v1(make_token(1)) == {
        "notifications": [
            {
                "channel_id": -1,
                "dm_id": 0,
                "notification_message": "gungeetsingh added you to dm gungeetsingh, petertran"
            }
        ]
    }
    clear_v1()