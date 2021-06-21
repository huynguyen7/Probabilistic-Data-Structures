import hashlib


"""

    @author: Huy Nguyen
    - Just for academic purpose only!
    - Deleting elements from Bloom Filter is not possible since it may cause to module hash corruption to other elements.
    - Possibly false positive. (The more elements we added, the more likely we may have false positives)
    - Impossibly false negative.

"""


class BloomFilter:
    def __init__(self, num_bits):
        self.num_elements = 2**num_bits
        self.data = [0]*self.num_elements
        self.hash_fns = [hashlib.md5, hashlib.sha1, hashlib.sha256, hashlib.sha512]

    def get_hashed_indices(self, element):
        element = str(element).encode('utf-8')
        hashed_elements = [int.from_bytes(h(element).digest(), byteorder='big') for h in self.hash_fns]
        hashed_indices = [hashed_element % self.num_elements for hashed_element in hashed_elements]
        return hashed_indices

    def insert(self, element):
        hashed_indices = self.get_hashed_indices(element)
        for i in hashed_indices:
            self.data[i] = 1

    def contains_element(self, element):
        hashed_indices = self.get_hashed_indices(element)
        for i in hashed_indices:
            if self.data[i] != 1:
                return False
        return True
