import math
import sys

import pytest
from hypothesis import strategies as st
from hypothesis import given

from llhist import Bin


def nextfloat(v):
    m, e = math.frexp(v)
    return (m + sys.float_info.epsilon) * 2**e


def prevfloat(v):
    m, e = math.frexp(v)
    return (m - sys.float_info.epsilon) * 2**e


POS_MIN = 1e-128
POS_MAX = prevfloat(1e128)
NEG_MIN = nextfloat(-1e128)
NEG_MAX = -1e-128
VALID_FLOATS = st.floats(min_value=NEG_MIN,
                         max_value=POS_MAX,
                         allow_nan=False,
                         allow_infinity=False)

ACCEPTABLE_VALS = set(range(-99, -9)) | set([0]) | set(range(10, 100))
ACCEPTABLE_EXPS = set(range(-128, 128))


class TestBin(object):

    def test_default_values(self):
        b = Bin()
        assert b.val == 0
        assert b.exp == 0
        assert b.count == 0

    @pytest.mark.parametrize('v, val, exp', [
        # Off-scale negative
        (-1e128, -1, 0),
        (-1e129, -1, 0),
        (-8e300, -1, 0),

        # Negative buckets
        (NEG_MIN, -99, 127),
        (-1e127, -10, 127),
        (-9.999e127, -99, 127),
        (-1.00001e-128, -10, -128),
        (-1.09999e-128, -10, -128),
        (-1.1e-128, -11, -128),
        (NEG_MAX, -10, -128),

        # Zero bucket
        (0.0, 0, 0),
        (9.9999e-129, 0, 0),
        (-9.9999e-129, 0, 0),

        # Positive buckets
        (POS_MIN, 10, -128),
        (1.00001e-128, 10, -128),
        (1.09999e-128, 10, -128),
        (1.1e-128, 11, -128),
        (1e127, 10, 127),
        (9.999e127, 99, 127),
        (POS_MAX, 99, 127),

        # Off-scale positive
        (1e128, -1, 0),
        (1e129, -1, 0),
        (8e300, -1, 0),

        # Invalid values
        (float('nan'), -1, 0),
        (float('inf'), -1, 0),
        (float('-inf'), -1, 0),
    ])
    def test_val_exp(self, v, val, exp):
        b = Bin()
        b.set(v)

        assert (b.val, b.exp) == (val, exp)

    @given(v=VALID_FLOATS)
    def test_val_range(self, v):
        b = Bin()
        b.set(v)

        assert b.val in ACCEPTABLE_VALS

    @given(v=VALID_FLOATS)
    def test_exp_range(self, v):
        b = Bin()
        b.set(v)

        assert b.exp in ACCEPTABLE_EXPS

    @pytest.mark.parametrize('v, value', [
        (99.9, 99.0),
        (43.3, 43.0),
        (10.0, 10.0),
        (1.0, 1.0),
        (0.3201, 0.32),
        (0.0035, 0.0035),
        (0.003, 0.003),
        (0.0002, 0.0002),
        (1e-129, 0.0),
        (0.0, 0.0),
        (-1e-129, 0.0),
        (-0.00123, -0.0012),
        (-1.0, -1.0),
        (-987324, -980000),
    ])
    def test_value(self, v, value):
        b = Bin()
        b.set(v)

        assert math.isclose(b.value(), value)

    @given(v=VALID_FLOATS)
    def test_value_fullrange(self, v):
        b = Bin()
        b.set(v)

        if NEG_MAX < v < POS_MIN:
            assert b.value() == 0.0
        else:
            assert math.isclose(b.value(), v, rel_tol=0.1)

    @given(v=VALID_FLOATS)
    def test_midpoint(self, v):
        b = Bin()
        b.set(v)

        if NEG_MAX < v < POS_MIN:
            assert b.midpoint() == 0.0
        else:
            assert math.isclose(b.midpoint(), v, rel_tol=0.05)

    @pytest.mark.parametrize('v, width', [
        (99.9, 1.0),
        (43.3, 1.0),
        (10.0, 1.0),
        (1.0, 0.1),
        (0.3201, 0.01),
        (0.0035, 0.0001),
        (0.003, 0.0001),
        (0.0002, 0.00001),
        (1e-129, 0.0),
        (0.0, 0.0),
        (-1e-129, 0.0),
        (-0.00123, 0.0001),
        (-1.0, 0.1),
        (-987324, 10000),
    ])
    def test_widths(self, v, width):
        b = Bin()
        b.set(v)

        assert math.isclose(b.width(), width)


def test_bench_bin_set(benchmark):
    b = Bin()
    v = VALID_FLOATS.example()
    benchmark(b.set, v)
