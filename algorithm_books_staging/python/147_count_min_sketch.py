"""
Count-Min Sketch - Approximate Counts for Heavy Hitters

Count a stream in a fixed grid of depth rows by width counters: add bumps one
counter per row and estimate returns the smallest, never below the true count.
Width 5, depth 3, stream cat dog cat fish cat dog bird cat dog ->
estimate("bird") = 2 (true 1), top 2 = [(4, 'cat'), (3, 'dog')].
"""
import heapq                # heappush / heappop keep the smallest at index 0
import random               # a seeded generator picks the row hashes


# --- algorithm ---
MOD = 1000000007                    # a large prime


def string_hash(word):
    """The word read as a base-31 number, mod MOD. O(len(word))."""
    h = 0
    for ch in word:
        h = (h * 31 + ord(ch)) % MOD
    return h


class CountMinSketch:
    """depth rows of width counters; each row has its own hash."""

    def __init__(self, width, depth, seed):
        self.width = width
        self.depth = depth
        self.table = []             # depth rows of width counters
        self.a = []                 # row r sends x to column
        self.b = []                 # ((a[r] * x + b[r]) mod MOD) mod width
        rng = random.Random(seed)   # the same seed gives the same hashes
        for row in range(depth):
            self.table.append([0] * width)
            self.a.append(rng.randint(1, MOD - 1))
            self.b.append(rng.randint(0, MOD - 1))

    def columns(self, item):
        """The item's column in each row. O(L + depth)."""
        x = string_hash(item)
        result = []
        for row in range(self.depth):
            h = (self.a[row] * x + self.b[row]) % MOD
            result.append(h % self.width)
        return result

    def add(self, item, count):
        """Add count to the item's counter in every row. O(L + depth)."""
        cols = self.columns(item)
        for row in range(self.depth):
            self.table[row][cols[row]] += count

    def estimate(self, item):
        """The smallest of the item's counters, never below its true count.
        O(L + depth)."""
        cols = self.columns(item)
        best = self.table[0][cols[0]]
        for row in range(1, self.depth):
            best = min(best, self.table[row][cols[row]])
        return best                 # collisions only ever add


class HeavyHitters:
    """The sketch counts every item; a size-k min-heap keeps the leaders."""

    def __init__(self, k, width, depth, seed):
        self.k = k
        self.sketch = CountMinSketch(width, depth, seed)
        self.counts = {}            # leader -> its estimate when last seen
        self.heap = []              # (estimate, leader), one entry per leader

    def add(self, item):
        """Count the item, then keep the k largest estimates as in Top-K.
        O(L + depth + log k) amortized."""
        self.sketch.add(item, 1)
        estimate = self.sketch.estimate(item)
        if item in self.counts:
            self.counts[item] = estimate        # its heap entry is now stale
            return
        self.counts[item] = estimate
        heapq.heappush(self.heap, (estimate, item))
        if len(self.heap) > self.k:             # one too many: drop the weakest
            estimate, weakest = heapq.heappop(self.heap)
            while estimate != self.counts[weakest]:     # stale: it grew since
                heapq.heappush(self.heap, (self.counts[weakest], weakest))
                estimate, weakest = heapq.heappop(self.heap)
            del self.counts[weakest]

    def top(self):
        """The leaders as (estimate, item), largest first. O(k log k)."""
        pairs = []
        for item in self.counts:
            pairs.append((self.counts[item], item))
        pairs.sort()
        return pairs[::-1]                      # largest estimate first


# --- try it ---
stream = ["cat", "dog", "cat", "fish", "cat", "dog", "bird", "cat", "dog"]
sketch = CountMinSketch(5, 3, 6)                # width 5, depth 3, seed 6
for word in stream:
    sketch.add(word, 1)
print(sketch.table)     # -> [[0, 7, 0, 0, 2], [4, 3, 2, 0, 0], [0, 0, 1, 5, 3]]
print(sketch.estimate("cat"), sketch.estimate("dog"))       # -> 4 3
print(sketch.estimate("fish"), sketch.estimate("bird"))     # -> 1 2
print(sketch.estimate("emu"), sketch.estimate("owl"))       # -> 0 1
hitters = HeavyHitters(2, 5, 3, 6)
for word in stream:
    hitters.add(word)
print(hitters.top())                            # -> [(4, 'cat'), (3, 'dog')]
big = HeavyHitters(3, 200, 4, 1)                # 800 counters
for i in range(3000):                           # 3003 distinct words in all
    big.add("w" + str(i))                       # 3000 words, once each
    if i % 10 == 0:
        big.add("hot")                          # 300 times
    if i % 15 == 0:
        big.add("warm")                         # 200 times
    if i % 25 == 0:
        big.add("mild")                         # 120 times
print(big.top())        # -> [(308, 'hot'), (213, 'warm'), (132, 'mild')]
