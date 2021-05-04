from count import count_char

def test_empty():
    assert count_char("") == {}

def test_simple():
    assert count_char("abc") == {"a": 1, "b": 1, "c": 1}

def test_double():
    assert count_char("aa") == {"a": 2}

def test_many_letters():
    assert count_char("abcdefghij") == {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1, "i": 1, "j": 1}

def test_duplicate_lowercase():
    assert count_char("aaabbbcccdddeee") == {"a": 3, "b": 3, "c": 3, "d": 3, "e": 3}

def test_uppercase_lowercase():
    assert count_char("AaaBbBCCcDdEEE") == {"A": 1, "a": 2, "B": 2, "b": 1, "C": 2, "c": 1, "D": 1, "d": 1, "E": 3}

def test_numbers():
    assert count_char("12345") == {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1}

def test_symbols():
    assert count_char("!@#$%") == {"!": 1, "@": 1, "#": 1, "$": 1, "%": 1}

def test_space():
    assert count_char("h i") == {"h": 1, " ": 1, "i": 1}

def test_sentence():
    assert count_char("I am 5 years old!?") == {"I": 1, " ":4, "a": 2, "m": 1, "5": 1, "y": 1, "e": 1, "r": 1, "s": 1, "o": 1, "l": 1, "d": 1, "!": 1, "?": 1}
