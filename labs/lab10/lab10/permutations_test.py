from permutations import permutations
from hypothesis import given, strategies, assume
import pytest

def test_empty():
    assert permutations("") == {""}
    assert permutations(" ") == {" "}

def test_duplicates():
    assert permutations("AAA") == {"AAA"}
    assert permutations("DDDDD") == {"DDDDD"}

def test_normal():
    assert permutations('ABC') == {'ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA'}
    assert permutations("PEPE") == {"EEPP", "EPEP", "EPPE", "PEEP", "PEPE", "PPEE"}
    assert permutations("LMAO") == {
        "LMAO", "MLAO", "ALMO", "LAMO", "MALO", "AMLO", "OMLA", "MOLA", 
        "LOMA", "OLMA", "MLOA", "LMOA", "LAOM", "ALOM", "OLAM", "LOAM", 
        "AOLM", "OALM", "OAML", "AOML", "MOAL", "OMAL", "AMOL", "MAOL"
    }