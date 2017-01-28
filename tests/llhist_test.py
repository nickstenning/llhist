import math
import sys

import pytest
from hypothesis import strategies as st
from hypothesis import given, settings

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
        (0.0, 0, 0),
        (9.9999e-129, 0, 0),
        (POS_MIN, 10, -128),
        (1.00001e-128, 10, -128),
        (1.09999e-128, 10, -128),
        (1.1e-128, 11, -128),
        (1e127, 10, 127),
        (9.999e127, 99, 127),
        (1e128, -1, 0),
        (-9.9999e-129, 0, 0),
        (NEG_MAX, -10, -128),
        (-1.00001e-128, -10, -128),
        (-1.09999e-128, -10, -128),
        (-1.1e-128, -11, -128),
        (-1e127, -10, 127),
        (-9.999e127, -99, 127),
        (NEG_MIN, -99, 127),
        (-1e128, -1, 0),
        (9.999e127, 99, 127),
        (POS_MAX, 99, 127),
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

    def test_benchmark_set(self, benchmark):
        b = Bin()
        v = VALID_FLOATS.example()
        benchmark(b.set, v)
