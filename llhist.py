import math

DEFAULT_HIST_SIZE = 100
POWER_OF_TEN = [
    1, 10, 100, 1000, 10000, 100000, 1e+06, 1e+07, 1e+08, 1e+09, 1e+10, 1e+11,
    1e+12, 1e+13, 1e+14, 1e+15, 1e+16, 1e+17, 1e+18, 1e+19, 1e+20, 1e+21,
    1e+22, 1e+23, 1e+24, 1e+25, 1e+26, 1e+27, 1e+28, 1e+29, 1e+30, 1e+31,
    1e+32, 1e+33, 1e+34, 1e+35, 1e+36, 1e+37, 1e+38, 1e+39, 1e+40, 1e+41,
    1e+42, 1e+43, 1e+44, 1e+45, 1e+46, 1e+47, 1e+48, 1e+49, 1e+50, 1e+51,
    1e+52, 1e+53, 1e+54, 1e+55, 1e+56, 1e+57, 1e+58, 1e+59, 1e+60, 1e+61,
    1e+62, 1e+63, 1e+64, 1e+65, 1e+66, 1e+67, 1e+68, 1e+69, 1e+70, 1e+71,
    1e+72, 1e+73, 1e+74, 1e+75, 1e+76, 1e+77, 1e+78, 1e+79, 1e+80, 1e+81,
    1e+82, 1e+83, 1e+84, 1e+85, 1e+86, 1e+87, 1e+88, 1e+89, 1e+90, 1e+91,
    1e+92, 1e+93, 1e+94, 1e+95, 1e+96, 1e+97, 1e+98, 1e+99, 1e+100, 1e+101,
    1e+102, 1e+103, 1e+104, 1e+105, 1e+106, 1e+107, 1e+108, 1e+109, 1e+110,
    1e+111, 1e+112, 1e+113, 1e+114, 1e+115, 1e+116, 1e+117, 1e+118, 1e+119,
    1e+120, 1e+121, 1e+122, 1e+123, 1e+124, 1e+125, 1e+126, 1e+127, 1e+128,
    1e-128, 1e-127, 1e-126, 1e-125, 1e-124, 1e-123, 1e-122, 1e-121, 1e-120,
    1e-119, 1e-118, 1e-117, 1e-116, 1e-115, 1e-114, 1e-113, 1e-112, 1e-111,
    1e-110, 1e-109, 1e-108, 1e-107, 1e-106, 1e-105, 1e-104, 1e-103, 1e-102,
    1e-101, 1e-100, 1e-99, 1e-98, 1e-97, 1e-96, 1e-95, 1e-94, 1e-93, 1e-92,
    1e-91, 1e-90, 1e-89, 1e-88, 1e-87, 1e-86, 1e-85, 1e-84, 1e-83, 1e-82,
    1e-81, 1e-80, 1e-79, 1e-78, 1e-77, 1e-76, 1e-75, 1e-74, 1e-73, 1e-72,
    1e-71, 1e-70, 1e-69, 1e-68, 1e-67, 1e-66, 1e-65, 1e-64, 1e-63, 1e-62,
    1e-61, 1e-60, 1e-59, 1e-58, 1e-57, 1e-56, 1e-55, 1e-54, 1e-53, 1e-52,
    1e-51, 1e-50, 1e-49, 1e-48, 1e-47, 1e-46, 1e-45, 1e-44, 1e-43, 1e-42,
    1e-41, 1e-40, 1e-39, 1e-38, 1e-37, 1e-36, 1e-35, 1e-34, 1e-33, 1e-32,
    1e-31, 1e-30, 1e-29, 1e-28, 1e-27, 1e-26, 1e-25, 1e-24, 1e-23, 1e-22,
    1e-21, 1e-20, 1e-19, 1e-18, 1e-17, 1e-16, 1e-15, 1e-14, 1e-13, 1e-12,
    1e-11, 1e-10, 1e-09, 1e-08, 1e-07, 1e-06, 1e-05, 0.0001, 0.001, 0.01, 0.1,
]


class Bin(object):
    __slots__ = ['val', 'exp', 'count']

    def __init__(self, val=0, exp=0, count=0):
        self.val = val
        self.exp = exp
        self.count = count

    def set(self, v):
        self.val = -1

        if math.isinf(v) or math.isnan(v):
            return

        if v == 0:
            self.val = 0
            return

        sign = 1 if v > 0 else -1
        v = abs(v)

        self.exp = math.floor(math.log10(v))

        if self.exp > 128:
            self.exp = 0
            return
        elif self.exp < -128:
            self.val = 0
            self.exp = 0
            return

        v /= POWER_OF_TEN[self.exp]
        v *= 10

        if v < 10 and self.exp > 127:
            v *= 10
            self.exp -= 1

        if self.exp > 127:
            self.exp = 0
            return

        self.val = sign * math.floor(v)

    def value(self):
        if -10 < self.val < 10:
            return 0.0
        return (self.val / 10.0) * POWER_OF_TEN[self.exp]

    def width(self):
        if -10 < self.val < 10:
            return 0.0
        return POWER_OF_TEN[self.exp] / 10.0

    def midpoint(self):
        v = self.value()
        if v == 0:
            return 0.0
        elif v < 0:
            return v - self.width() / 2
        else:
            return v + self.width() / 2

    def sortkey(self):
        if self.val == 0:
            return (0, 0, 0)
        elif self.val > 0:
            return (1, self.exp, self.val)
        else:
            return (-1, -self.exp, self.val)

    def compare(self, other):
        key = self.sortkey()
        key_other = other.sortkey()
        if key > key_other:
            return -1
        elif key < key_other:
            return 1
        else:
            return 0

    def __repr__(self):
        return '<Bin value={} count={}>'.format(self.value(), self.count)


class Histogram(object):
    __slots__ = ['bins', 'len', 'cap', '_lookup']

    def __init__(self):
        self.bins = [Bin() for _ in range(DEFAULT_HIST_SIZE)]
        self.len = 0
        self.cap = DEFAULT_HIST_SIZE
        self._lookup = [None for _ in range(256)]

    def record_value(self, v, count=1):
        b = Bin()
        b.set(v)
        self._insert_bin(b, count)

    def approx_mean(self):
        divisor = 0
        sum_ = 0
        for i in range(self.len):
            midpoint = self.bins[i].midpoint()
            cardinality = self.bins[i].count
            divisor += cardinality
            sum_ += midpoint * cardinality
        if divisor == 0.0:
            return float('nan')
        return sum_ / divisor

    def approx_sum(self):
        sum_ = 0
        for i in range(self.len):
            midpoint = self.bins[i].midpoint()
            cardinality = self.bins[i].count
            sum_ += midpoint * cardinality
        return sum_

    def _insert_bin(self, b, count):
        found, idx = self._find_bin(b)

        if not found:
            if self.len == self.cap:
                self.bins.insert(idx, Bin())
                self.bins.extend([Bin() for _ in range(DEFAULT_HIST_SIZE - 1)])
                self.cap += DEFAULT_HIST_SIZE
            else:
                self.bins[idx+1:self.len+1], self.bins[idx] = self.bins[idx:self.len], self.bins[self.len]
            self.bins[idx].val = b.val
            self.bins[idx].exp = b.exp
            self.bins[idx].count = count
            self.len += 1

            for i in range(idx, self.len):
                l1, l2 = _lookupkey(self.bins[i])
                if self._lookup[l1] is None:
                    self._lookup[l1] = [0 for _ in range(256)]
                self._lookup[l1][l2] = i + 1

            return self.bins[idx].count

        newval = self.bins[idx].count + count

        # FIXME: wtf?
        # if newval < self.bins[idx].count:  # rolled
        #     newval = 2**64 - 1

        self.bins[idx].count = newval

    def _find_bin(self, b):
        if self.len == 0:
            return False, 0

        l1, l2 = _lookupkey(b)

        if self._lookup[l1] is not None:
            idx = self._lookup[l1][l2]
            if idx != 0:
                return True, idx - 1

        rv = -1
        idx = 0
        l = 0
        r = self.len - 1

        while l < r:
            check = (r + l) // 2
            rv = self.bins[check].compare(b)
            if rv == 0:
                l = check
                r = check
            elif rv > 0:
                l = check + 1
            else:
                r = check - 1

        if rv != 0:
            rv = self.bins[l].compare(b)

        idx = l

        if rv == 0:
            return True, idx
        if rv < 0:
            return False, idx
        idx += 1
        return False, idx


def _lookupkey(b):
    return b.exp & 0xFF, b.val & 0xFF
