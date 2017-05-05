#!/usr/bin/env python3

import numpy as np
from stream import Stream
from stream import BinomStream

class CountMedianSketch:
    """
    Implements the Count-Median-Sketch probabilistic data
    structure that allows count frequencies of elements
    in a large data stream.
    """


    def __init__(self,d,w):
        """
        d: Number of d different hash functions. Height of matrix.
        w: cardinality of result domain of hash functions.
        """
        self.d = d
        self.w = w
        self.estimators = np.ndarray((self.d, self.w), dtype=np.int)
        self.estimators.fill(0)


        # coefficients for linear hash functions
        self.a = np.zeros(d, dtype=np.int)
        self.b = np.zeros(d, dtype=np.int)

        self.x = np.zeros(d, dtype=np.int)
        self.y = np.zeros(d, dtype=np.int)

        self.p = 2**31 - 1 # large prime number
        self.g = None

        self.init_hash_functions()

    def init_hash_functions(self):
        for i in range(self.d):
            self.a[i] = np.random.randint(1, self.p)
            self.b[i] = np.random.randint(1, self.p)
            self.x[i] = np.random.randint(1, self.p)
            self.y[i] = np.random.randint(1, self.p)

    def hash(self, value, i):
        h = ((self.a[i] * value + self.b[i]) % self.p) % self.w
        return h

    def g_hash(self, value, i):
        g = -1 if ((self.x[i] * value + self.y[i]) % self.p) % 2 == 0 else 1
        return g

    def add_value(self, value):
        for i in range(self.d):
            self.estimators[i][self.hash(value, i)] += self.g_hash(value, i)

    def estimate_frequency(self, value):
        return np.median([self.estimators[i][self.hash(value, i)] * self.g_hash(value, i) for i in range(self.d)])

    def is_heavy_hitter(self, value, phi, total):
        return 1 if self.estimate_frequency(value)/(total * 1.0) >= phi else 0

def main():
    exact_counter = dict()
    cms = CountMedianSketch(15, 2**10)
    m = 1000000
    s = Stream(m, (0, 1000))
    for a in s:
        if a not in exact_counter:
            exact_counter[a] = 1
        else:
            exact_counter[a] += 1
        cms.add_value(a)

    # L2 accuracy measure
    acc = 0

    for key in exact_counter:
        acc += (cms.estimate_frequency(key) - exact_counter[key])**2
        #print('Value {}, estimated freq = {}, real freq = {}'.format(key, cms.estimate_frequency(key), exact_counter[key]))

    acc = acc/m

    print("Size: {}, acc: {}".format(m, acc))

    #phi = 0.1
    #for key in exact_counter:
    #    if cms.is_heavy_hitter(key, phi, m):
    #        print("Value {} is a {},L1-heavy hitter".format(key, phi))

main()

