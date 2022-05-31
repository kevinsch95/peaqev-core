import pytest
from ..hoursselection import Hoursselectionbase as h
from ..Models import (CAUTIONHOURTYPE_AGGRESSIVE, CAUTIONHOURTYPE_INTERMEDIATE, CAUTIONHOURTYPE_SUAVE, CAUTIONHOURTYPE)

MOCKPRICES1 =[0.129, 0.123, 0.077, 0.064, 0.149, 0.172, 1, 2.572, 2.688, 2.677, 2.648, 2.571, 2.561, 2.07, 2.083, 2.459, 2.508, 2.589, 2.647, 2.648, 2.603, 2.588, 1.424, 0.595]
MOCKPRICES2 =[0.392, 0.408, 0.418, 0.434, 0.408, 0.421, 0.45, 0.843, 0.904, 1.013, 0.939, 0.915, 0.703, 0.445, 0.439, 0.566, 0.913, 1.4, 2.068, 2.182, 1.541, 2.102, 1.625, 1.063]
MOCKPRICES3 = [0.243, 0.282, 0.279, 0.303, 0.299, 0.314, 0.304, 0.377, 0.482, 0.484, 0.482, 0.268, 0.171, 0.174, 0.171, 0.277, 0.52, 0.487, 0.51, 0.487, 0.451, 0.397, 0.331, 0.35]
MOCKPRICES4 = [0.629,0.37,0.304,0.452,0.652,1.484,2.704,3.693,3.64,3.275,2.838,2.684,2.606,1.463,0.916,0.782,0.793,1.199,1.825,2.108,1.909,1.954,1.168,0.268]
MOCKPRICES5 = [0.299,0.388,0.425,0.652,0.94,1.551,2.835,3.62,3.764,3.313,2.891,2.723,2.621,1.714,1.422,1.187,1.422,1.422,1.673,1.63,1.551,1.669,0.785,0.264]
MOCKPRICES6 = [1.057,1.028,0.826,0.87,1.15,1.754,2.42,2.918,3.262,3.009,2.594,2.408,2.364,2.34,2.306,2.376,2.494,2.626,2.626,2.516,2.564,2.565,2.489,1.314]
MOCKPRICES7 = [0.475, 1.051, 0.329, 0.396, 0.394, 2.049, 2.145, 3.019, 2.92, 2.534, 2.194, 2.12, 2.073, 1.86, 1.765, 1.578, 1.59, 1.943, 2.07, 2.098, 2.088, 2.041, 1.888, 0.475]
MOCKPRICES_FLAT = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
MOCKPRICES_SHORT = [0.51, 0.487, 0.451, 0.397, 0.331, 0.35]
PRICES_BLANK = ",,,,,,,,,,,,,,,,,,,,,,,"
PRICS_ARRAY_WITH_STRING = "6,6,6,6,6,6,6,6,hej,6,6,6,6,6,6"
PRICES_ARRAYSTR = "6.0,6.0,6.0,6.06,6.0,6.0,6.6,6,6,6,6,6,6,6"
MOCKPRICES6 = [1.057, 1.028, 0.826, 0.87, 1.15, 1.754, 2.42, 2.918, 3.262, 3.009, 2.594, 2.408, 2.364, 2.34, 2.306, 2.376, 2.494, 2.626, 2.626, 2.516, 2.564, 2.565, 2.489, 1.314]

def test_mockprices1_non_hours():
    r = h()
    r.prices = MOCKPRICES1
    r.update(21)
    assert r.non_hours == [21]

def test_mockprices1_caution_hours():
    r = h()
    r.prices = MOCKPRICES1
    r.update(21)
    assert r.caution_hours == [22]

def test_mockprices1_caution_hours_aggressive():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES1
    r.update(21)
    assert r.caution_hours == [22]

def test_mockprices1_caution_hours_per_type():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES1
    r.update(21)
    r2 = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_INTERMEDIATE])
    r2.prices = MOCKPRICES1
    r2.update(21)
    r3 = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r3.prices = MOCKPRICES1
    r3.update(21)
    assert len(r.caution_hours) <= len(r2.caution_hours)
    assert len(r2.caution_hours) <= len(r3.caution_hours)
    assert len(r.non_hours) >= len(r2.non_hours)
    assert len(r2.non_hours) >= len(r3.non_hours)
    
def test_mockprices2_non_hours():
    r = h()
    r.prices = MOCKPRICES2
    r.update(21)
    assert r.non_hours == [21]

def test_mockprices2_caution_hours():
    r = h()
    r.prices = MOCKPRICES2
    r.update(21)
    assert r.caution_hours == [22,23]

def test_mockprices3_non_hours():
    r = h()
    r.prices = MOCKPRICES3
    r.update(21)
    assert r.non_hours == [21]

def test_mockprices3_caution_hours():
    r = h()
    r.prices = MOCKPRICES3
    r.update(21)
    assert r.caution_hours == [22,23]

def test_cautionhour_over_max_error():
    with pytest.raises(AssertionError):
        h(cautionhour_type=2)
    
def test_cautionhour_zero_error():
    with pytest.raises(AssertionError):
        h(cautionhour_type=0)

def test_cautionhour_negative_error():
    with pytest.raises(AssertionError):
        h(cautionhour_type=-1)

def test_create_dict():
    r = h()
    ret = r._create_dict(MOCKPRICES1)
    assert ret[20] == 2.603
    assert len(ret) == 24

def test_create_dict_error():
    r = h()
    with pytest.raises(ValueError):
              r._create_dict(MOCKPRICES_SHORT)

# def test_rank_prices():
#     r = h()
#     hourly = r._create_dict(MOCKPRICES1)
#     norm_hourly = r._create_dict(r._normalize_prices(MOCKPRICES1))
#     ret = r._rank_prices(hourly, norm_hourly)
#     assert ret == {6: {'permax': 0.37, 'val': 1}, 7: {'permax': 0.96, 'val': 2.572}, 8: {'permax': 1.0, 'val': 2.688}, 9: {'permax': 1.0, 'val': 2.677}, 10: {'permax': 0.99, 'val': 2.648}, 11: {'permax': 0.96, 'val': 2.571}, 12: {'permax': 0.95, 'val': 2.561}, 13: {'permax': 0.77, 'val': 2.07}, 14: {'permax': 0.77, 'val': 2.083}, 15: {'permax': 0.91, 'val': 2.459}, 16: {'permax': 0.93, 'val': 2.508}, 17: {'permax': 0.96, 'val': 2.589}, 18: {'permax': 0.98, 'val': 2.647}, 19: {'permax': 0.99, 'val': 2.648}, 20: {'permax': 0.97, 'val': 2.603}, 21: {'permax': 0.96, 'val': 2.588}, 22: {'permax': 0.53, 'val': 1.424}} == {6: {'permax': 0.37, 'val': 1}, 7: {'permax': 0.96, 'val': 2.572}, 8: {'permax': 1.0, 'val': 2.688}, 9: {'permax': 1.0, 'val': 2.677}, 10: {'permax': 0.99, 'val': 2.648}, 11: {'permax': 0.96, 'val': 2.571}, 12: {'permax': 0.95, 'val': 2.561}, 13: {'permax': 0.77, 'val': 2.07}, 14: {'permax': 0.77, 'val': 2.083}, 15: {'permax': 0.91, 'val': 2.459}, 16: {'permax': 0.93, 'val': 2.508}, 17: {'permax': 0.96, 'val': 2.589}, 18: {'permax': 0.98, 'val': 2.647}, 19: {'permax': 0.99, 'val': 2.648}, 20: {'permax': 0.97, 'val': 2.603}, 21: {'permax': 0.96, 'val': 2.588}, 22: {'permax': 0.53, 'val': 1.424}, 23: {'permax': 0.22, 'val': 0.595}}

def test_rank_prices_permax():
    r = h()
    hourly = r._create_dict(MOCKPRICES1)
    norm_hourly = r._create_dict(r._normalize_prices(MOCKPRICES1))
    ret = r._rank_prices(hourly, norm_hourly)
    for r in ret:
        assert 0 <= ret[r]["permax"] <= 1

# def test_rank_prices_flat_curve():
#     r = h()
#     hourly = r._create_dict(MOCKPRICES_FLAT)
#     norm_hourly = r._create_dict(r._normalize_prices(MOCKPRICES_FLAT))
#     ret = r._rank_prices(hourly, norm_hourly)
#     assert ret == {}

def test_add_expensive_non_hours():
    r = h()
    pass

def test_add_expensive_non_hours_flat_curve():
    r = h()
    r.prices = MOCKPRICES_FLAT
    r._absolute_top_price = 0.5
    r.update(18)
    assert len(r.non_hours) == 6

def test_add_expensive_non_hours_error():
    r = h()
    pass

def test_determine_hours():
    r = h()
    pass

def test_determine_hours_error():
    r = h()
    pass


def test_mockprices4_suave():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r.prices = MOCKPRICES4
    r.update(0)
    assert r.non_hours ==[7,8,9,10]
    assert r.caution_hours ==[5,6,11,12,13,17,18,19,20,21,22]
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours

def test_mockprices4_intermediate():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_INTERMEDIATE])
    r.prices = MOCKPRICES4
    r.update(0)
    assert r.non_hours==[6,7,8,9,10,11,12,19,20,21]
    assert r.caution_hours ==[5,13,17,18,22] 
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours

def test_mockprices4_aggressive():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES4
    r.update(0)
    assert r.non_hours == [6,7,8,9,10,11,12,18,19,20,21]
    assert r.caution_hours == [5,13,17,22]
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours

def test_mockprices5_suave():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r.prices = MOCKPRICES5
    r.update(0)
    assert r.non_hours == [7,8,9,10]
    assert r.caution_hours == [5,6,11,12,13,14,15,16,17,18,19,20,21]
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours

def test_mockprices5_intermediate():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_INTERMEDIATE])
    r.prices = MOCKPRICES5
    r.update(0)
    assert r.non_hours == [6,7,8,9,10,11,12]
    assert r.caution_hours == [5,13,14,15,16,17,18,19,20,21]
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours

def test_mockprices5_aggressive():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES5
    r.update(0)
    assert r.non_hours == [6,7,8,9,10,11,12,13]
    assert r.caution_hours == [5,14,15,16,17,18,19,20,21]
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours


def test_dynamic_cautionhours_no_max_price_suave():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r.prices = MOCKPRICES5
    r.update(0)
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours
    assert r.non_hours == [7, 8, 9, 10]
    assert r._dynamic_caution_hours == {5: 0.74, 6: 0.4, 11: 0.43, 12: 0.45, 13: 0.69, 14: 0.77, 15: 0.83, 16: 0.77, 17: 0.77, 18: 0.71, 19: 0.72, 20: 0.74, 21: 0.71}

def test_dynamic_cautionhours_with_max_price_suave():
    r = h(absolute_top_price=2, cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r.prices = MOCKPRICES5
    r.update(0)
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours
    assert r.non_hours == [6, 7, 8, 9, 10,11,12]
    assert r._dynamic_caution_hours == {5: 0.74, 13: 0.69, 14: 0.77, 15: 0.83, 16: 0.77, 17: 0.77, 18: 0.71, 19: 0.72, 20: 0.74, 21: 0.71}


def test_dynamic_cautionhours_no_max_price_aggressive():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES5
    r.update(0)
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours
    assert r.non_hours == [6, 7, 8, 9, 10, 11, 12,13]

def test_prices7():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES7
    r.update(0)
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours
    assert r.non_hours == [5, 6, 7, 8, 9, 10, 11, 12,13,14,17,18,19,20,21,22]


def test_dynamic_cautionhours_very_low_peaqstdev():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r.prices = MOCKPRICES6
    r.update(0)
    assert list(r._dynamic_caution_hours.keys()) == r.caution_hours
    assert len(r.non_hours) + len(r._dynamic_caution_hours) < 24
    

def test_total_charge_just_today():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    MOCKHOUR = 0
    r.prices = MOCKPRICES1
    r.update(MOCKHOUR)
    assert r.get_total_charge(2, MOCKHOUR) == 17.2

def test_total_charge_today_tomorrow():
    MOCKHOUR = 18
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r.prices = MOCKPRICES1
    r.prices_tomorrow = MOCKPRICES2
    r.update(MOCKHOUR)
    assert r.get_total_charge(2, MOCKHOUR) == 34.7

def test_average_kwh_price_just_today():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    MOCKHOUR = 0
    r.prices = MOCKPRICES1
    r.update(MOCKHOUR)
    assert r.get_average_kwh_price(MOCKHOUR) == 0.35

def test_average_kwh_price_today_tomorrow():
    MOCKHOUR = 18
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r.prices = MOCKPRICES1
    r.prices_tomorrow = MOCKPRICES2
    r.update(MOCKHOUR)
    assert r.get_average_kwh_price(MOCKHOUR) == 0.56