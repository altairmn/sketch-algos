import random
import numpy as np

class Stream:
    """
    Produces random elements and simulates a stream.
    """
    def __init__(self, n, rand_range):
        """
        n : Number of random elements to produce.
        range : Random elements are in this range.
        """
        self.n = n
        self.range = rand_range

    def produce(self):
        for i in range(self.n):
            yield random.randrange(*self.range)

    def __iter__(self):
        return self.produce()


class BinomStream:
    """
    Produces elements from Binomial distribution
    """
    def __init__(self, n, rand_range):
        """
        n: Number of random elements to produce
        range: Random elements are in this range
        """

        self.n = n
        self.rand_range = rand_range
        self.p = np.random.uniform(0, 1)

    def get_stream(self):
        return np.random.binomial(self.rand_range[1]-self.rand_range[0], 0.5, self.n) + self.rand_range[0]

