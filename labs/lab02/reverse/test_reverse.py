'''
Tests for reverse_words()
'''
from reverse import reverse_words

def test_example():
    assert reverse_words(["Hello World", "I am here"]) == ['World Hello', 'here am I']
    
def test_reverse_empty():
    assert reverse_words([]) == []
    assert reverse_words(["", '']) == ["", '']

def test_reverse_one_word():
    assert reverse_words(["Hello", "here"]) == ['Hello', 'here']
    assert reverse_words(["esrever", "I", "am", "here"]) == ['esrever', 'I', "am", "here"]

def test_reverse_one_number():
    assert reverse_words(["1", "2"]) == ['1', '2']
    assert reverse_words(["3", "2", "1"]) == ['3', '2', '1']

def test_reverse_alphanumeric():
    assert reverse_words(["I am 5 years old", "He is small"]) == ['old years 5 am I', 'small is He']
    assert reverse_words(["nom nom nom 1 2 3", "a 1 b 2 c 3"]) == ['3 2 1 nom nom nom', '3 c 2 b 1 a']

def test_reverse_uppcase_lowercase():
    assert reverse_words(["mEmE fONt", "LoL LMAO rofl"]) == ['fONt mEmE', 'rofl LMAO LoL']
    assert reverse_words(["HeLlO WoRlD", "I aM hErE"]) == ['WoRlD HeLlO', 'hErE aM I']

    