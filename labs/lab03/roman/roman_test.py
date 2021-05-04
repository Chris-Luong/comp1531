from roman import *

def test_roman_empty():
    assert roman('') == 0

def test_roman_works():
    assert roman('III') == 3
    assert roman('LXIX') == 69    
    assert roman('XXI') == 21
    assert roman('CDXX') == 420

def test_roman_big():
    assert roman('MMMM') == 4000
    assert roman('MDCCLXXVI') == 1776
    assert roman('MMXIX') == 2019