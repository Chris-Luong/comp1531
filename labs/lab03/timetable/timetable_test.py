from timetable import *

def test_timetable_empty():
    assert timetable([], []) == []

def test_timetable_works():
    assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]) == [datetime(2019,9,27,10,30),
    datetime(2019,9,27,14,10), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]

def test_timetable_duplicate_date():
    assert timetable([date(2019,9,27), date(2019,9,27)], [time(14,10), time(10,30)]) == [datetime(2019,9,27,10,30),
    datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,27,14,10)]

def test_timetable_duplicate_time():
    assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(14,10)]) == [datetime(2019,9,27,14,10),
    datetime(2019,9,27,14,10), datetime(2019,9,30,14,10), datetime(2019,9,30,14,10)]

def test_timetable_duplicate_datetime():
    assert timetable([date(2019,9,27), date(2019,9,27)], [time(14,10), time(14,10)]) == [datetime(2019,9,27,14,10),
    datetime(2019,9,27,14,10), datetime(2019,9,27,14,10), datetime(2019,9,27,14,10)]