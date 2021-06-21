from count_min_sketch import CountMinSketch
import unittest
import numpy as np


class CMSketchTest(unittest.TestCase):
    def test1(self):
        data = [1,1,2,2,3,1,1,4,9,11,-1,9,5,-100,2]
        a = len(data)
        a_hat = 0

        epsilon = 1/16
        gamma = 1e-4
        my_CM_Sketch = CountMinSketch(epsilon=epsilon, gamma=gamma)
        my_dict = dict()
        for val in data:
            if val not in my_dict:
                my_dict[val] = 0
            my_dict[val] += 1
            my_CM_Sketch.increment(val)

        for val in my_dict:
            a_hat += my_CM_Sketch.estimate(val)
        self.assertTrue(abs(a_hat - a) <= epsilon*a)

    def test2(self):
        data = np.random.randint(low=0, high=100, size=2000)
        a = len(data)
        a_hat = 0

        epsilon = 1/36
        gamma = 1e-5
        my_CM_Sketch = CountMinSketch(epsilon=epsilon, gamma=gamma)
        my_dict = dict()
        for val in data:
            if val not in my_dict:
                my_dict[val] = 0
            my_dict[val] += 1
            my_CM_Sketch.increment(val)

        for val in my_dict:
            a_hat += my_CM_Sketch.estimate(val)
        self.assertTrue(abs(a_hat - a) <= epsilon*a)


if __name__ == '__main__':
    unittest.main()
