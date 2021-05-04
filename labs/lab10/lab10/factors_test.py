from factors import factors
from hypothesis import given, strategies
import inspect
import pytest

# Readding this here just in case students removed it from their implementation.
def is_prime(n) :
    if (n <= 1) :
        return False
    if (n <= 3) :
        return True

    if (n % 2 == 0 or n % 3 == 0) :
        return False

    i = 5
    while(i * i <= n) :
        if (n % i == 0 or n % (i + 2) == 0) :
            return False
        i = i + 6

    return True

def test_generator():
    '''
    Ensure it is generator function
    '''
    assert inspect.isgeneratorfunction(factors), "factors does not appear to be a generator"

@given(strategies.integers(min_value=2, max_value=1000))
def test_factors(n):
    '''
    Ensure the factors of n multiply to give n.
    '''
    product = 1
    for f in factors(n):
        product *= f
    assert product == n

@given(strategies.integers(min_value=2, max_value=1000))
def test_ascending(n):
    '''
    Ensure the factors are in ascending order.
    '''
    prev = None
    for f in factors(n):
        if prev:
            assert f >= prev
        prev = f

@given(strategies.integers(min_value=2, max_value=1000))
def test_prime(n):
    '''
    All the factors should be prime numbers.
    '''
    for f in factors(n):
        assert is_prime(f)

@given(strategies.integers(max_value = 1))
def test_error(n):
    '''
    Numbers less than or equal to 1 don't have prime factors.
    '''
    with pytest.raises(ValueError):
        list(factors(n))


'''from factors import factors, is_prime
from hypothesis import given, strategies
import pytest
import inspect

def test_generator():

    #Ensure it is generator function

    assert inspect.isgeneratorfunction(factors), "factors does not appear to be a generator"

def test_primes():
    assert list(factors(11)) == [11]
    assert list(factors(13)) == [13]
    assert list(factors(17)) == [17]

def test_normal():
    assert list(factors(12)) == [2,2,3]
    assert list(factors(72)) == [2,2,2,3,3]
    assert list(factors(84)) == [2,2,3,7]
'''