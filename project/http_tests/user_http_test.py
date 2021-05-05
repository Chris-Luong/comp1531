"""
import pytest
import requests
import json
import jwt
from src import config
from src.clear import clear_v1

def test_user_profile_v1():

    clear_v1()
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
        "name_first": "Eyal",
        "name_last": "Dorfan",
    })
    token = jwt.encode({"handle": "eyaldorfan"},'',algorithm = "HS256")    

    resp = requests.get(config.url + 'user/profile/v2', params={'token': token, "u_id": '0'})

    payload = resp.json()
    assert payload == {
        'user': {
            'u_id': '0',
            "email": "eyald@gmail.com",
            "name_first": "Eyal",
            "name_last": "Dorfan",
            'handle_str': "eyaldorfan",
        },
    }

def test_users():
    clear_v1()
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
        "name_first": "Eyal",
        "name_last": "Dorfan",
    })
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "tal@gmail.com",
        "password": "Tal123456",
        "name_first": "Tal",
        "name_last": "Avrahami",
    })

    token = jwt.encode({"handle": "eyaldorfan"},'',algorithm = "HS256")

    resp = requests.get(config.url + 'users/all/v1', params={'token': token})

    payload = resp.json()
    assert payload == {
        "users": [
            {
                "u_id": "0",
                "email": "eyald@gmail.com",
                "name_first": "Eyal",
                "name_last": "Dorfan",
                "handle_str": "eyaldorfan"
            },
            {
                "u_id": "1",
                "email": "tal@gmail.com",
                "name_first": "Tal",
                "name_last": "Avrahami",
                "handle_str": "talavrahami"
            }
        ]
    }
"""
