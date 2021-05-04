from weather import weather
import math

def test_documentation():
    assert is_close(weather("08-08-2010", "Albury"), (10.8, 10.0))

def is_close(a, b):
    return math.isclose(a[0], b[0], abs_tol=0.1) and math.isclose(a[1], b[1], abs_tol=0.1)

def test_invalid_case():
    assert(weather("08-08-2010","Alby") == (None, None))

def test_invalid_location():
    assert weather('20-01-2010','Badgerys') == (None, None)

def test_empty_town():
    assert weather('20-01-2010', '') == (None, None)

def test_spec():
    assert weather('08-08-2010','Albury') == (10.8, 10.0)

def test_na_min_temp():
    assert weather("11-09-2009", "Albury") == (None, None)

def test_na_max_temp():
    assert weather("07-09-2016", "CoffsHarbour") == (None, None)

def test_newcastle():
    # avg_min = 13.7, avg_max = 24.1
    result = weather("04-12-2008", "Newcastle")
    assert (round(result[0], 1), round(result[1], 1)) == (5.5, 0.1)

def test_data_with_zero():
    # avg_min = 11.35, avg_max = 24.45
    # day_min = 0, day_max = 16.1
    result = weather("07-08-2010", "Richmond")
    assert (round(result[0], 1), round(result[1], 1)) == (11.3, 8.3)
