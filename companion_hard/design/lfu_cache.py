"""
LFU Cache (LeetCode 460) - Hard
Chapter: design
Pattern: Frequency buckets of ordered dicts + min-frequency pointer

Design a fixed-capacity cache with get(key) and put(key, value) in O(1). Each get or put of a key
increments its use count. On overflow evict the key with the smallest use count, breaking ties by
evicting the least recently used among them.
Example: capacity 2; put(1,1), put(2,2), get(1) -> 1, put(3,3) evicts 2 (count 1 < count 2),
get(2) -> -1, put(4,4) evicts 1 (1 and 3 both have count 2; 1 is older).
"""


# --- helpers ---
def first_key(d):
    """The key inserted earliest (Python dicts remember insertion order)."""
    for key in d:
        return key
    return None


# --- brute force ---
class BruteForce:
    """Dict key -> [value, count, tick]; eviction scans every key for the rarest. O(n) put."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}                        # key -> [value, use count, tick of last use]
        self.tick = 0                         # a clock that advances on every operation

    def get(self, key):
        if key not in self.data:
            return -1
        self.tick += 1
        self.data[key][1] += 1
        self.data[key][2] = self.tick
        return self.data[key][0]

    def put(self, key, value):
        if self.capacity == 0:
            return
        self.tick += 1
        if key in self.data:
            self.data[key][0] = value
            self.data[key][1] += 1
            self.data[key][2] = self.tick
            return
        if len(self.data) == self.capacity:
            victim = None
            victim_rank = None
            for other in self.data:           # scan everything for the rarest, oldest key
                rank = (self.data[other][1], self.data[other][2])   # (use count, last tick)
                if victim is None or rank < victim_rank:
                    victim = other
                    victim_rank = rank
            del self.data[victim]
        self.data[key] = [value, 1, self.tick]


# --- optimal ---
class LFUCache:
    """Dict key -> count, dict count -> ordered dict of keys, plus min_count. O(1) per op."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.count_of = {}                    # key -> use count
        self.bucket = {}                      # count -> dict key -> value, oldest key first
        self.min_count = 0

    def touch(self, key):
        count = self.count_of[key]
        value = self.bucket[count].pop(key)
        if len(self.bucket[count]) == 0:
            del self.bucket[count]
            if self.min_count == count:
                self.min_count = count + 1    # the only place the minimum moves up
        if count + 1 not in self.bucket:
            self.bucket[count + 1] = {}
        self.bucket[count + 1][key] = value   # appended last: it is the newest at this count
        self.count_of[key] = count + 1
        return value

    def get(self, key):
        if key not in self.count_of:
            return -1
        return self.touch(key)

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.count_of:
            self.touch(key)
            self.bucket[self.count_of[key]][key] = value
            return
        if len(self.count_of) == self.capacity:
            victim = first_key(self.bucket[self.min_count])   # oldest of the rarest
            del self.bucket[self.min_count][victim]
            del self.count_of[victim]
            if len(self.bucket[self.min_count]) == 0:
                del self.bucket[self.min_count]
        if 1 not in self.bucket:
            self.bucket[1] = {}
        self.bucket[1][key] = value
        self.count_of[key] = 1
        self.min_count = 1                    # a new key is always the rarest


# --- try the brute force ---
c = BruteForce(2)
c.put(1, 1)
c.put(2, 2)
print(c.get(1))      # -> 1
c.put(3, 3)          # evicts 2 (count 1 < count 2)
print(c.get(2))      # -> -1
print(c.get(3))      # -> 3
c.put(4, 4)          # 1 and 3 tie at count 2; 1 is older -> evicted
print(c.get(1))      # -> -1
print(c.get(3))      # -> 3
print(c.get(4))      # -> 4
z = BruteForce(0)
z.put(0, 0)
print(z.get(0))      # -> -1


# --- try the optimal ---
c = LFUCache(2)
c.put(1, 1)
c.put(2, 2)
print(c.get(1))      # -> 1
c.put(3, 3)          # evicts 2 (count 1 < count 2)
print(c.get(2))      # -> -1
print(c.get(3))      # -> 3
c.put(4, 4)          # 1 and 3 tie at count 2; 1 is older -> evicted
print(c.get(1))      # -> -1
print(c.get(3))      # -> 3
print(c.get(4))      # -> 4
z = LFUCache(0)
z.put(0, 0)
print(z.get(0))      # -> -1
