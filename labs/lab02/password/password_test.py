'''
Tests for check_password()
'''
from password import check_password

def test_password_horrible():
    assert check_password("password") == "Horrible password"
    assert check_password("iloveyou") == "Horrible password"
    assert check_password("123456") == "Horrible password"
    assert check_password("Hi") != "Horrible password"

def test_password_poor():
    assert check_password("lidfudughlsifgbsidl") == "Poor password"
    assert check_password("thisIsAGreatPasswordIMO") == "Poor password"
    assert check_password("HelloWorld") == "Poor password"
    assert check_password("YourMum1") != "Poor password"


def test_password_moderate():
    assert check_password("12345678") == "Moderate password"
    assert check_password("Iam1yearold") == "Moderate password"
    assert check_password("atleast8charactesr") == "Moderate password"
    assert check_password("Iam5yearsold") != "Moderate password"

def test_password_strong():
    assert check_password("IAm7YearsOld") == "Strong password"
    assert check_password("ThisPasswordIsSTR0nk") == "Strong password"
    assert check_password("itugsghsgh;G9") == "Strong password"
    assert check_password("password") != "Strong password"