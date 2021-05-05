import pytest
import json
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, \
    user_profile_sethandle_v1, users_all_v1, user_stats_v1, users_stats_v1
from src.auth import auth_register_v2
from src.helper import make_token, create_timestamp
from src.other import clear_v1
from src.error import InputError, AccessError
from src.dm import dm_create_v1, dm_remove_v1, dm_leave_v1, dm_invite_v1
from src.channels import channels_create_v2
from src.channel import channel_invite_v2, channel_leave_v1, channel_join_v2
from src.message import message_send_v2, message_remove_v1, message_share_v1, message_senddm_v1

with open('src/data.json') as FILE:
    data = json.load(FILE)

@pytest.fixture
def register_users():
    clear_v1()
    # register 4 users with email, password, first name and last name
    # first user is the dream owner
    auth_register_v2("gungeetsingh@gmail.com", "password", "Gungeet", "Singh")
    auth_register_v2("petertran@gmail.com", "password", "Peter", "Tran")
    auth_register_v2("christopherluong@gmail.com", "password", "Christopher", "Luong")
    auth_register_v2("talavrahami@gmail.com", "password", "Tal", "Avrahami")

@pytest.fixture
def channel_setup():
    # create multiple public channels for single user (Non-dream owner)
    channels_create_v2(make_token(0), "PublicChannel1", True)
    channels_create_v2(make_token(0), "PublicChannel2", True)
    channels_create_v2(make_token(0), "PublicChannel3", True)

@pytest.fixture
def dm_setup():
    # create multiple dms for single user
    dm_create_v1(make_token(0), [1, 2]) # dm_id 0
    dm_create_v1(make_token(0), [1]) # dm_id 1
    dm_create_v1(make_token(0), [2]) # dm_id 2

def test_user_profile(register_users):
    assert user_profile_v1(make_token(0),0) == {
        'user': {
            'u_id': 0,
            'email': 'gungeetsingh@gmail.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        }
    }

def test_invalid_user(register_users):
    with pytest.raises(InputError):
        assert user_profile_v1(make_token(2), 4)

def test_invalid_token(register_users):
    with pytest.raises(AccessError):
        assert user_profile_v1(make_token(5), 0)
        assert user_profile_setname_v1(make_token(5), 'Eyal', 'Dorfan')
        assert user_profile_setemail_v1(make_token(5), 'eyald@gmail.com')
        assert user_profile_sethandle_v1(make_token(5), 'eyaldorfan')
        assert users_all_v1(make_token(5))
        assert user_stats_v1(make_token(5))
        assert users_stats_v1(make_token(5))

def test_valid_name(register_users):
    with pytest.raises(InputError):
        assert user_profile_setname_v1(make_token(0), '', 'Dorfan')
        assert user_profile_setname_v1(make_token(0), 'Eyal', '')
        assert user_profile_setname_v1(make_token(0), 'E'*51, 'Dorfan')
        assert user_profile_setname_v1(make_token(0), 'Eyal', 'D'*51)

def test_proper_setname():
    assert user_profile_setname_v1(make_token(0), 'Eyal', 'Dorfan') == {}
    assert user_profile_v1(make_token(0),0) == {
        'user': {
            'u_id': 0,
            'email': 'gungeetsingh@gmail.com',
            'name_first': 'Eyal',
            'name_last': 'Dorfan',
            'handle_str': 'gungeetsingh',
        }
    }

def test_invalid_email_syntax(register_users):
    with pytest.raises(InputError):
        assert user_profile_setemail_v1(make_token(0), 'eyaldgmail.com')

def test_valid_email_reset(register_users):
    result = user_profile_setemail_v1(make_token(0), 'eyald@gmail.com')
    assert result == {}
    assert user_profile_v1(make_token(0),0) == {
        'user': {
            'u_id': 0,
            'email': 'eyald@gmail.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'gungeetsingh',
        }
    }

def test_invalid_handle(register_users):
    assert user_profile_sethandle_v1(make_token(0), 'EEEEyaldorfan@  ') == {}
    assert user_profile_v1(make_token(0),0) == {
        'user': {
            'u_id': 0,
            'email': 'gungeetsingh@gmail.com',
            'name_first': 'Gungeet',
            'name_last': 'Singh',
            'handle_str': 'eeeeyaldorfan',
        }
    }

    with pytest.raises(InputError):
        user_profile_sethandle_v1(make_token(0), 'A')
        user_profile_sethandle_v1(make_token(0), 'A'*21)
        user_profile_sethandle_v1(make_token(0), 'eeeeyaldorfan')

def test_users_all(register_users):
    assert users_all_v1(make_token(0)) == {
        'users': [
            {
                'u_id': 0,
                'email': 'gungeetsingh@gmail.com',
                'name_first': 'Gungeet',
                'name_last': 'Singh',
                'handle_str': 'gungeetsingh',
            }, 
            {
                'u_id': 1,
                'email': 'petertran@gmail.com',
                'name_first': 'Peter',
                'name_last': 'Tran',
                'handle_str': 'petertran',
            },
            {
                'u_id': 2,
                'email': 'christopherluong@gmail.com',
                'name_first': 'Christopher',
                'name_last': 'Luong',
                'handle_str': 'christopherluong',
            },
            {
                'u_id': 3,
                'email': 'talavrahami@gmail.com',
                'name_first': 'Tal',
                'name_last': 'Avrahami',
                'handle_str': 'talavrahami',
            },
        ]
    }

def test_user_stats_channels(register_users, channel_setup):
    # test channels
    assert user_stats_v1(make_token(0)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 1.0
        }
    }
    channel_invite_v2(make_token(0), 0, 1)
    assert user_stats_v1(make_token(1)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 0.33
        }
    }
    channel_leave_v1(make_token(1), 0)
    assert user_stats_v1(make_token(1)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 0.0
        }
    }
    channel_join_v2(make_token(2), 0)
    assert user_stats_v1(make_token(2)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 1,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 0.33
        }
    }
    
def test_user_stats_dms(register_users, dm_setup):
    # testing dms
    assert user_stats_v1(make_token(0)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 1.0
        }
    }
    dm_remove_v1(make_token(0),2)
    assert user_stats_v1(make_token(0)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 3,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 1.0
        }
    }
    dm_leave_v1(make_token(1),0)
    assert user_stats_v1(make_token(1)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 0.5
        }
    }
    dm_invite_v1(make_token(0), 0, 1)
    assert user_stats_v1(make_token(1)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 1.0
        }
    }

def test_user_stats_message(register_users, channel_setup, dm_setup):
    message_send_v2(make_token(0), 0, "Hello")
    assert user_stats_v1(make_token(0)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 1,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 1.0
        }
    }
    message_remove_v1(make_token(0), 0)
    assert user_stats_v1(make_token(0)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 1.0
        }
    }
    message_send_v2(make_token(0), 0, "Hello")
    message_share_v1(make_token(0), 0, "Hello again", 0, -1)
    assert user_stats_v1(make_token(0)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 2,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 1.0
        }
    }
    message_senddm_v1(make_token(0), 0, "Hello")
    assert user_stats_v1(make_token(0)) == {
        'user_stats': {
            "channels_joined": [
                {
                    "num_channels_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_joined": [
                {
                    "num_dms_joined": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_joined": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_sent": [
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_sent": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "involvement_rate": 1.0
        }
    }

def test_dreams_stats(register_users, dm_setup, channel_setup):
    message_send_v2(make_token(0), 0, "Hello")
    assert users_stats_v1(make_token(0)) == {
        "dreams_stats": {
            "channels_exist": [
                {
                    "num_channels_exist": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_exist": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_exist": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_channels_exist": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "dms_exist": [
                {
                    "num_dms_exist": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_exist": 1,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_exist": 2,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_dms_exist": 3,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "messages_exist": [
                {
                    "num_messages_exist": 0,
                    "time_stamp": str(create_timestamp())
                },
                {
                    "num_messages_exist": 1,
                    "time_stamp": str(create_timestamp())
                }
            ],
            "utilization_rate": 0.75
        }
    }