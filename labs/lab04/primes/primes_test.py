from primes import factors

def test_zero():
    assert(factors(0) == [])

def test_small():
    assert(factors(2) == [2])
    assert(factors(8) == [2, 2, 2])
    assert(factors(29) == [29])
    assert(factors(36) == [2, 2, 3, 3])
    assert(factors(69) == [3, 23])

def test_big():
    assert(factors(967) == [967])
    assert(factors(870) == [2, 3, 5, 29])
    assert(factors(900) == [2, 2, 3, 3, 5, 5])
    assert(factors(998) == [2, 499])
    assert(factors(782) == [2, 17, 23])