import pytest
from divisors import divisors
from hypothesis import given, strategies

def test_12():
    assert divisors(12) == {1,2,3,4,6,12}

def test_NaN():
    with pytest.raises(ValueError):
        divisors("hello")

def test_zero():
    with pytest.raises(ValueError):
        divisors(0)

def test_negative():
    with pytest.raises(ValueError):
        divisors(-100)

def test_prime():
    assert divisors(97) == {1,97}

def test_big():
    assert divisors(2048) == {1,2,4,8,16,32,64,128,256,512,1024,2048}