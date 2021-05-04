from list_exercises import *

def test_reverse():
    l = ["how", "are", "you"]
    reverse_list(l)
    assert l == ["you", "are", "how"]
    l = []
    reverse_list(l)
    assert l == []
    l = ["hi", "hi", "hi", "hi", "hi"]
    reverse_list(l)
    assert l == ["hi", "hi", "hi", "hi", "hi"]    

def test_min_positive():
    assert minimum([1, 2, 3, 10]) == 1
    assert minimum([0,0]) == 0
    assert minimum([1,1,1,1,2]) == 1

def test_sum_positive():
    assert sum_list([7, 7, 7]) == 21
    assert sum_list([]) == 0
    assert sum_list([-1, 0, 1]) == 0
