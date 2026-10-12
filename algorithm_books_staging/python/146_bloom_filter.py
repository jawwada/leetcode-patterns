"""
Bloom Filter - k Hash Functions into One Bit Array

Remember a set in m bits: add(item) sets k bits and might_contain(item) checks
them, so False is always right and True is probably right. With 19 bits and 3
hashes, add cat, dog and fish -> might_contain("owl") is False and
might_contain("colt") is True, a false positive.
"""
import math                         # exp for the error formula
import random                       # random words to measure the error


# --- algorithm ---
MOD = 1000000007                    # a large prime, as in Rabin-Karp


def string_hash(word, base):
    """The word read as a number in the given base, mod MOD. O(len(word))."""
    h = 0
    for ch in word:
        h = (h * base + ord(ch)) % MOD
    return h


class BloomFilter:
    """m bits and k probes per item; bits are set and never cleared."""

    def __init__(self, m, k):
        self.m = m                  # number of bits, best a prime
        self.k = k                  # number of hash functions
        self.bits = [0] * m

    def positions(self, item):
        """The item's k bits, (h1 + i * step) mod m for i = 0..k-1. O(L + k)."""
        h1 = string_hash(item, 31)
        h2 = string_hash(item, 37)          # a second, different hash
        step = 1 + h2 % (self.m - 1)        # 1..m-1: the probes always move
        result = []
        for i in range(self.k):
            result.append((h1 + i * step) % self.m)
        return result

    def add(self, item):
        """Set the item's k bits to 1. O(L + k)."""
        for p in self.positions(item):
            self.bits[p] = 1

    def might_contain(self, item):
        """False: never added. True: added, or a false positive. O(L + k)."""
        for p in self.positions(item):
            if self.bits[p] == 0:
                return False                # adding it would have set this bit
        return True                         # added, or a false positive


def expected_rate(m, n, k):
    """False-positive rate after n adds, (1 - e^(-k n / m))^k. O(1)."""
    return (1 - math.exp(-k * n / m)) ** k


def random_word(length):
    """Random lowercase letters; seed random to repeat a run. O(length)."""
    word = ""
    for i in range(length):
        word += chr(ord("a") + random.randint(0, 25))
    return word


def measured_rate(m, k, n, trials):
    """Add n random words, then return the share of trials fresh random words
    the filter wrongly reports as present. O((n + trials) * (L + k))."""
    bloom = BloomFilter(m, k)
    added = set()
    for i in range(n):
        word = random_word(8)
        bloom.add(word)
        added.add(word)
    false_positives = 0
    tested = 0
    for i in range(trials):
        word = random_word(8)
        if word not in added:               # only never-added words count
            tested += 1
            if bloom.might_contain(word):
                false_positives += 1
    return false_positives / tested


# --- try it ---
bloom = BloomFilter(19, 3)                  # 19 bits (a prime), 3 hashes
for word in ["cat", "dog", "fish"]:
    bloom.add(word)
print(bloom.positions("cat"))               # -> [13, 1, 8]
print(bloom.positions("dog"))               # -> [8, 17, 7]
print(bloom.might_contain("cat"), bloom.might_contain("fish"))  # -> True True
print(bloom.might_contain("owl"))           # -> False
print(bloom.might_contain("colt"))          # -> True
random.seed(1)
rate = measured_rate(997, 7, 100, 10000)    # about 10 bits per word
print(round(expected_rate(997, 100, 7), 4), round(rate, 4))   # -> 0.0083 0.0093
print(rate < 2 * expected_rate(997, 100, 7))    # -> True
