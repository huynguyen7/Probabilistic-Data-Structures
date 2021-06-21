from utils import available_hash_functions
import numpy as np


"""

    @author: Huy Nguyen
    - FREQUENCY ESTIMATOR.
    - Count–min Sketch (CM Sketch) implementation (for academia purpose only!).
    - Used for constructing large amounts of frequency data. For example, how many times the item has been added to the set..
    - The more resources we allocate, the better estimate should be (increase width and depth specifically).
    - SOURCE:
        +https://en.wikipedia.org/wiki/Count–min_sketch
        +http://dimacs.rutgers.edu/~graham/pubs/papers/cmencyc.pdf
        +http://web.stanford.edu/class/archive/cs/cs166/cs166.1206/lectures/10/Slides10.pdf

    *Ideally (How to choose w for a number of distinct items):
    Pick w = e * ε^-1.
    Pr[âi−ai > ε*L1_norm(a)] ≤ δ.

    Gamma: Confidence, the lower, the better.
    Epsilon: Accuracy, the lower, the better.

"""


#np.random.seed(1)  # Deterministic seed, just for testing purpose!


class CountMinSketch(object):
    def __init__(self, epsilon=None, gamma=None, depth=None, width=None):
        if epsilon is not None and gamma is not None:
            assert epsilon > 0 and epsilon <= 1 and gamma > 0 and gamma <= 1
            self.depth = int(np.log(gamma**(-1))+1)
            self.width = int(np.e*(epsilon**(-1))+1)
        elif depth is not None and width is not None:
            self.depth = depth  # Number of hash functions, we don't support shake..
            self.width = width  # Number of buckets.
        assert self.width > 0 and self.depth > 0 and self.depth <= 12
        self.counters = np.zeros(shape=(self.depth,self.width), dtype=np.int64)  # The space required is fixed.
        self.hash_functions = np.random.choice(available_hash_functions(), size=self.depth)  # Uniformly choosing hash functions.

    # d is depth.
    # Time: O(d), space: O(1)
    def increment(self, val):  # Update the number of time we have seen the value.
        for i in range(self.depth):
            x = str(val).encode('utf-8')
            h_x = int.from_bytes(self.hash_functions[i](x).digest(), byteorder='little') % self.width
            self.counters[i,h_x] += 1

    def estimate(self, val):  # Return the number of time we have updated the value.
        x = str(val).encode('utf-8')
        result = np.inf
        for i in range(self.depth):
            h_x = int.from_bytes(self.hash_functions[i](x).digest(), byteorder='little') % self.width
            result = min(result, self.counters[i,h_x])
        return result
