#!/Users/huynguyen/miniforge3/envs/math/bin/python3


import unittest
import numpy as np
from hll import HyperLogLog
import hashlib


beta = np.sqrt(3*np.log(2)-1)  # Used with standard_error()

def standard_error(m):  # Threshold for testing.
    return beta/np.sqrt(m)

'''

    *We need at max log2(n) bits to estimate n cardinality!
    This test is written based on this assumption.

'''


class HLLTest(unittest.TestCase):
    def test_1(self):
        size = 32
        data = np.random.randint(low=-10000, high=10000, size=size)
        b = int(np.log2(size))  # Num bits needed.
        hll = HyperLogLog(hash_fn=hashlib.sha1, num_bits=b)
        my_set = set()
        for val in data:
            hll.add(val)
            my_set.add(val)
        my_set_n = len(my_set)
        hll_n = hll.get_num_distinct()
        error_rate = np.abs(float(my_set_n-hll_n)/float(my_set_n+hll_n))
        accepted_error_rate = np.abs(standard_error(2**b))
        assert(error_rate <= accepted_error_rate)

    def test_2(self):
        size = 100000
        data = np.random.randint(low=-90000, high=10000, size=size)
        b = int(np.log2(size))  # Num bits needed.
        hll = HyperLogLog(hash_fn=hashlib.sha1, num_bits=b)
        my_set = set()
        for val in data:
            hll.add(val)
            my_set.add(val)
        my_set_n = len(my_set)
        hll_n = hll.get_num_distinct()
        error_rate = np.abs(float(my_set_n-hll_n)/float(my_set_n+hll_n))
        accepted_error_rate = np.abs(standard_error(2**b))
        assert(error_rate <= accepted_error_rate)

    def test_3(self):
        size = int(1e5)
        data = np.random.randint(low=(-1)*int(1e10), high=int(1e10), size=size)
        b = int(np.log2(size))  # Num bits needed.
        hll = HyperLogLog(hash_fn=hashlib.sha1, num_bits=b)
        my_set = set()
        for val in data:
            hll.add(val)
            my_set.add(val)
        my_set_n = len(my_set)
        hll_n = hll.get_num_distinct()
        error_rate = np.abs(float(my_set_n-hll_n)/float(my_set_n+hll_n))
        accepted_error_rate = np.abs(standard_error(2**b))
        assert(error_rate <= accepted_error_rate)

    def test_4(self):  # Boundary n test
        size = int(1e6)
        data = np.random.randint(low=(-1)*int(1e10), high=int(1e10), size=size)
        my_set = set()
        for val in data:
            my_set.add(val)
        my_set_n = len(my_set)
        b = int(np.log2(my_set_n))  # Num bits needed.
        hll = HyperLogLog(hash_fn=hashlib.sha1, num_bits=b)
        for val in data:
            hll.add(val)
        hll_n = hll.get_num_distinct()
        error_rate = np.abs(float(my_set_n-hll_n)/float(my_set_n+hll_n))
        accepted_error_rate = np.abs(standard_error(2**b))
        assert(error_rate <= accepted_error_rate)
        

if __name__ == "__main__":
    unittest.main()
