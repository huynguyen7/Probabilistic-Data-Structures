#!/Users/huynguyen/miniforge3/envs/math/bin/python3


import numpy as np
import hashlib


"""

    @author: Huy Nguyen
    - PROBABILISTIC CARDINALITY ESTIMATORS.
    - Just an academia implementation.
    - HyperLogLog used for estimating the number of distinct elements (the cardinality).
    - The algorithm needs to maintain a collection of registers, each of which is at most log2log2(N) + O(1) bits, when cardinalities <= N need to be estimated.
    - While with HLL we only need, for example, log2(log2(2**32)) = 5 bits for counting up to 4 billion distinct elements.. (Morales and Welke)
    
    m ~ large multiset of input items with unknown cardinality n, n ∈ N.

    - Source:
        http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf
        http://cscubs.cs.uni-bonn.de/2016/proceedings/paper-03.pdf

"""


def count(arr, val):
    c = 0
    for x in arr:
        if x == val:
            c += 1
    return c

def get_alpha(beta, m):
    return (1/(2*np.log(2)))/(1+beta/m)

def get_beta(m):
    assert m >= 16, 'NUMBER OF REGS >= 3.'
    assert m % 16 == 0 or m % 32 == 0 or m % 64 == 0 or m % 128 == 0

    # Based on Theorem 1 in the paper.
    if m == 16:
        return 1.106
    elif m == 32:
        return 1.070
    elif m == 64:
        return 1.054
    elif m == 128:
        return 1.046
    else:
        return np.sqrt(3*np.log(2)-1)  # Used for standard_error.

class HyperLogLog(object):
    def __init__(self, hash_fn=None, encoding='utf-8', num_bits=4):
        assert hash_fn is not None, 'REQUIRED A HASH FUNCTION.'
        assert isinstance(num_bits, int) and num_bits > 3

        self.encoding = encoding  # Encoding type.
        self.hash = hash_fn  # Hash function
        self.b = num_bits

        self.m = 2**self.b  # Number of buckets.
        self.beta = get_beta(self.m)
        self.alpha = get_alpha(self.beta, self.m)  # Bias correction.
        self.std_error = self.beta/np.sqrt(self.m)
        self.regs = np.zeros(self.m, dtype=np.int64)  # Collection (Vector) of m registers with zeros.
        #print('num_bits: %d, m: %d, beta: %.7f, alpha: %.7f, std_error: %.7f' % (self.b, self.m, self.beta, self.alpha, self.std_error))

    def rho(self, w):  # Return the index of leftmost 1 bit (Based 1).
        return self.m-self.b+1 if w == 0 else bin(w)[2:].find('1')+1

    def h(self, item):  # Hash data to binary domain.
        encoded_element = str(item).encode(self.encoding)  # Encode
        return bin(int.from_bytes(self.hash(encoded_element).digest()[:self.b], byteorder='big'))

    def add(self, item):
        hashed_item = self.h(item)
        x = int(hashed_item[2:2+self.m], 2)  # Convert to int.
        j = x & (self.m-1)  # Index to update (map to index bucket).
        w = x >> self.b  # Right shift 1 ~ Get the remaining bits.
        self.regs[j] = max(self.regs[j], self.rho(w))
        #print('x: %s j: %d, regs[%d]: %d' % (x,j,j,self.regs[j]))

    def get_num_distinct(self):  # Get the cardinality.
        Z = np.sum(2.0**(self.regs*(-1)))  # Harmonic mean.
        Z = Z**(-1.0)
        E = self.alpha*float(self.m**2)*Z
        E_star = E

        if E <= (5/2)*self.m:
            V = count(self.regs, 0)
            if V != 0:
                E_star = self.m*np.log(self.m/V)
        elif E > (1/30)*(2**32):
            E_star = (-1)*(2**32)*np.log(1-E/(2**32))
        return int(np.floor(E_star))

if __name__ == "__main__":
    #data = [1,2,3,1,2,3,3,3,4,1,1,1]  # Test data.
    data = np.random.randint(low=-10000, high=10000, size=32)
    my_set = set()
    hll = HyperLogLog(hash_fn=hashlib.sha1, num_bits=5)
    for val in data:
        hll.add(val)
        my_set.add(val)
    print('ESTIMATED: %d, TRUTH: %d' % (hll.get_num_distinct(), len(my_set)))
