import pytest
import json
from src.error import InputError
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1, auth_passwordreset_request_v1
from src.other import clear_v1
from src.helper import make_token
from src.user import user_profile_v1

with open('src/data.json') as FILE:
    data = json.load(FILE)

def test_register_success():
    clear_v1()
    result = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Tal', 'Avrahami')
    assert result == {'token': make_token(0), 'auth_user_id': 0}
        
                # Tests for auth_login_v2    
               
# tests login for registered user above 
def test_logout_and_login_valid():
    result = auth_logout_v1(make_token(0))
    assert result == {'is_success': True}
    result = auth_login_v2('validemail@gmail.com', '123abc!@#')
    assert result == {'token': make_token(0),'auth_user_id': 0}
    
# tests if input error is raised for an invalid email
def test_login_invalid_email():
    with pytest.raises(InputError):
        auth_login_v2('invalidemail', '123456')

# tests if input error is raised for unregistered email
def test_login_unregistered_email():
    with pytest.raises(InputError):
        auth_login_v2('didnotregister@gmail.com', 'password')

# tests if input error is raised for password that doesnt match email
def test_login_incorrect_password():
    with pytest.raises(InputError):
        auth_login_v2('validemail@gmail.com', 'incorrectPassword')
        
                # Tests for auth_register_v2
        
# tests if InputError is raised for invalid email used during registration
def test_register_invalid_email():
    with pytest.raises(InputError):
        auth_register_v2('invalidemail', '123456', 'Tal', 'Avrahami')

# checks if email has been used on another account
def test_existing_email():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Tal', 'Avrahami')
    with pytest.raises(InputError):
        auth_register_v2('validemail@gmail.com', '123456', 'Tal', 'Avrahami')

# checks that InputError is raised for passwords less than 6 characters
def test_short_password():
    with pytest.raises(InputError):
        auth_register_v2('validemail@gmail.com', '123', 'Tal', 'Avrahami')

def test_empty_password():
    with pytest.raises(InputError):
        auth_register_v2('validemail@gmail.com', '', 'Tal', 'Avrahami')

# checks a variety of name cases where names are not within 1-50 characters
# to see if an InputError is raised
def test_name_first_empty():
    with pytest.raises(InputError):
        auth_register_v2('validemail@gmail.com', '123', '', 'Avrahami')
    
def test_name_first_long():
    with pytest.raises(InputError):
        auth_register_v2('validemail@gmail.com', '123', 'A'*51, 'Avrahami')
    
def test_name_last_empty():
    with pytest.raises(InputError):
        auth_register_v2('validemail@gmail.com', '123', 'Tal', '')
    
def test_name_last_long():
    with pytest.raises(InputError):
        auth_register_v2('validemail@gmail.com', '123', 'Tal', 'A'*51)

# checks that a handle which would have more than 20 characters because of the 
# length of the first and last name is cut at 20 characters 
def test_long_handle(): 
    clear_v1() 
    auth_register_v2('handletest@gmail.com', '123456', 'Tal', 'Avrahamiiiiiiiiiiiiiiii')
    assert user_profile_v1(make_token(0), 0) == {
        'user': {
            'u_id': 0,
            'email': 'handletest@gmail.com',
            'name_first': 'Tal',
            'name_last': 'Avrahamiiiiiiiiiiiiiiii',
            'handle_str': 'talavrahamiiiiiiiiii',
        }
    }

# checks that whitespace is removed from users names for construction of handle
def test_handle_whitespace():  
    clear_v1()
    auth_register_v2('handletest@gmail.com', '123456', 'T ad hg', 'Av rah\nami   ')
    assert user_profile_v1(make_token(0), 0) == {
        'user': {
            'u_id': 0,
            'email': 'handletest@gmail.com',
            'name_first': 'T ad hg',
            'name_last': 'Av rah\nami   ',
            'handle_str': 'tadhgavrahami',
        }
    }

# checks that the @ sign is removed from users names for construction of handle
def test_handle_at_sign():
    clear_v1()
    auth_register_v2('handletest3@gmail.com', '123456', 'Tom', '@vrah@mi   ')
    assert user_profile_v1(make_token(0), 0) == {
        'user': {
            'u_id': 0,
            'email': 'handletest3@gmail.com',
            'name_first': 'Tom',
            'name_last': '@vrah@mi   ',
            'handle_str': 'tomvrahmi',
        }
    }

# handle already exists in data from prev test, expecting iteration to talavrahami0
def test_handle_iteration():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Tal', 'Avrahami')
    result = auth_register_v2('handletest4@gmail.com', '123456', 'Tal', 'Avrahami')
    assert result == {'token': make_token(1), 'auth_user_id': 1}
    assert user_profile_v1(make_token(1), 1) == {
        'user': {
            'u_id': 1,
            'email': 'handletest4@gmail.com',
            'name_first': 'Tal',
            'name_last': 'Avrahami',
            'handle_str': 'talavrahami0',
        }
    }

                    #tests auth_passwordreset_request_v1
def test_invalid_email_password_reset():
    with pytest.raises(InputError):
        auth_passwordreset_request_v1('invalidemail') # invalid email
    with pytest.raises(InputError):
        auth_passwordreset_request_v1('didnotregister@gmail.com') # non-existent email


