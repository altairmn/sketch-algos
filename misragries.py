from collections import Counter
from stream import Stream


class MisraGries:
    """ Implements the MisraGries algorithm
    for outputting heavy hitters
    """

    def __init__(self, k):
        self.k = k
        self.freq = Counter()

    def update(self, el):
        if el in self.freq:
            self.freq.update([el])
        elif len(self.freq) < self.k - 1:
            self.freq[el] = 1
        else:
            for l in list(self.freq.keys()):
                self.freq[l] -= 1
                if self.freq[l] == 0:
                    del self.freq[l]

    def estimate_frequency(self, el):
        return self.freq[el] if el in self.freq else 0


def main():
    exact_counter = dict()
    mg = MisraGries(20)
    m = 1000000
    s = Stream(m, (0, 1000))
    for a in s:
        if a not in exact_counter:
            exact_counter[a] = 1
        else:
            exact_counter[a] += 1
        mg.update(a)
    for key in exact_counter:
        print('Value {}, estimated freq = {}, real freq = {}'.format(key, mg.estimate_frequency(key), exact_counter[key]))


main()


