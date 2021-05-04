from circle import Circle
import pytest

def test_small():
    c = Circle(3)
    assert(round(c.circumference(), 1) == 18.8)
    assert(round(c.area(), 1) == 28.3)

def test_big():
    c = Circle(9000)
    assert(round(c.circumference(), 1) == 56548.7)
    assert(round(c.area(), 1) == 254469004.9)

def test_zero():
    c = Circle(0)
    with pytest.raises(ValueError):
        c.valid_radius()

def test_negative():
    c = Circle(-1)
    with pytest.raises(ValueError):
        c.valid_radius()