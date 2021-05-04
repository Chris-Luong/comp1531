import pytest
from inverse import inverse
from hypothesis import given, strategies

def test_empty():
    assert inverse({}) == {}

def test_empty_items():
    assert inverse({1: ' ', 2: 'B', 3: 'A'}) == {' ': [1], 'B': [2], 'A': [3]}
    assert inverse({1: '', 2: 'B', 3: 'A'}) == {'': [1], 'B': [2], 'A': [3]}

def test_example():
    assert inverse({1: 'A', 2: 'B', 3: 'A'}) == {'A': [1, 3], 'B': [2]}

def test_all_duplicates():
    assert inverse({1: 'A', 2: 'A', 3: 'A', 4: 'A',}) == {
        'A': [1, 2, 3, 4]
    }

def test_no_duplicates():
    assert inverse({1: 'A', 2: 'B', 3: 'C', 4: 'D',}) == {
        'A': [1],
        'B': [2],
        'C': [3],
        'D': [4]
    }