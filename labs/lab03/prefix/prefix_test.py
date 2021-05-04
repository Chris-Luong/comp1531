from prefix import prefix_search
import pytest

def test_documentation():
    assert prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a") == { "ac": 1, "ab": 3}

def test_exact_match():
    assert prefix_search({"category": "math", "cat": "animal"}, "cat") == {"category": "math", "cat": "animal"}

def test_no_match_num_prefix():
    with pytest.raises(KeyError):
        prefix_search({"ac": 1, "ba": 2, "ab": 3}, "100")

def test_no_match_string_prefix():
    with pytest.raises(KeyError):
        prefix_search({"ac": 1, "ba": 2, "ab": 3}, "zzz")

def test_no_match_misc_prefix():
    with pytest.raises(KeyError):
        prefix_search({"!#%": 1, "^#%$#": 2, "*&^<?": 3}, "yo")

def test_misc_prefix_match():
    assert prefix_search({"!#%": 1, "^#%$#": 2, "*&^<?": 3, "!^#>?": 4}, "!") == { "!#%": 1, "!^#>?": 4}

def test_prefix_too_big():
    with pytest.raises(KeyError):
        prefix_search({"ac": 1, "ba": 2, "ab": 3}, "abcd")