from reduce import reduce
import pytest

@pytest.fixture
def sum():
    return lambda x, y: x + y

@pytest.fixture
def product():
    return lambda x, y: x * y

def test_empty_list(sum):
    assert reduce(sum, []) is None

def test_one_element(sum):
    assert reduce(sum, [0]) == 0

def test_sum(sum):
    assert reduce(sum, [1,2,3]) == 6

def test_product(product):
    assert reduce(product, [1,2,3]) == 6

def test_sum_zero(sum):
    assert reduce(sum, [0,1,2]) == 3

def test_product_zero(product):
    assert reduce(product, [0,1,2]) == 0
