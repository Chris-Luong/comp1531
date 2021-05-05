import pytest
import requests
import json
import jwt
from src import config
from src.clear import clear_v1
from src.helper import make_token

'''
def test_echo():
'''
#A simple test to check echo
'''
    resp = requests.get(config.url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}
'''

def test_auth_register_v2():
    clear_v1()
    resp = requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
        "name_first": "Eyal",
        "name_last": "Dorfan",
    })
    payload = resp.json()
    assert payload == {
        'token': make_token(0),
        'auth_user_id': 0
    }

def test_auth_login_v2():
    resp = requests.post(config.url + 'auth/login/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
    })
    payload = resp.json()
    assert payload == {
        'token': make_token(0),
        'auth_user_id': 0
    }

def test_auth_logout_v1():
    resp = requests.post(config.url + 'auth/logout/v1', json = {
        "token": make_token(0)
    })
    payload = resp.json()
    assert payload == {
        "is_success": True
    }

def test_auth_invalid_email():
    clear_v1()
    resp = requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyaldgmail.com",
        "password": "Dorfan91!!!",
        "name_first": "Eyal",
        "name_last": "Dorfan",
    })
    assert resp.status_code == 400

    resp = requests.post(config.url + 'auth/login/v2', json = {
        "email": "eyaldgmail.com",
        "password": "Dorfan91!!!",
    })
    assert resp.status_code == 400

def test_auth_register_invalid_password():
    resp = requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyal@gmail.com",
        "password": "hi",
        "name_first": "Eyal",
        "name_last": "Dorfan",
    })
    assert resp.status_code == 400

def test_auth_login_wrong_password():
    resp = requests.post(config.url + 'auth/login/v2', json = {
        "email": "eyald@gmail.com",
        "password": "incorrectpassword",
    })
    assert resp.status_code == 400

def test_auth_login_invalid_user():
    resp = requests.post(config.url + 'auth/login/v2', json = {
        "email": "tal@gmail.com",
        "password": "doesntmatter",
    })
    assert resp.status_code == 400

def test_auth_register_email_exists():
    clear_v1()
    requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
        "name_first": "Eyal",
        "name_last": "Dorfan",
    })

    resp = requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
        "name_first": "Eyal",
        "name_last": "Dorfan",
    })
    assert resp.status_code == 400

def test_auth_register_name_errors():
    clear_v1()
    resp = requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
        "name_first": "",
        "name_last": "Dorfan",
    })
    assert resp.status_code == 400

    resp = requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
        "name_first": "Eyal",
        "name_last": "",
    })
    assert resp.status_code == 400

    resp = requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
        "name_first": "A"*100,
        "name_last": "Dorfan",
    })
    assert resp.status_code == 400

    resp = requests.post(config.url + 'auth/register/v2', json = {
        "email": "eyald@gmail.com",
        "password": "Dorfan91!!!",
        "name_first": "Eyal",
        "name_last": "D"*100,
    })
    assert resp.status_code == 400
