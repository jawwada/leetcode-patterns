"""
LFU Cache (LeetCode 460)  — Hard
Pattern: Frequency buckets of ordered dicts + min-frequency pointer

Problem
-------
Design a fixed-capacity cache with get(key) and put(key, value) in O(1). Each get/put of a key
increments its use count. On overflow evict the key with the SMALLEST use count; break ties by
evicting the least recently used among them.
Example: capacity 2; put(1,1) put(2,2) get(1)->1 put(3,3) evicts 2 (count 1 < count 2);
get(2)->-1 get(3)->3 put(4,4) evicts 1 (1 and 3 both count 2, 1 is older).

Brute force
-----------
Keep dict key -> [value, freq, last_tick]. get/put bump freq and stamp the current tick in O(1),
but eviction scans every key to find the minimum (freq, last_tick) pair: O(n) per overflowing
put, O(capacity) space. The wasted work is the scan: we recompute "who is least frequent and
oldest" from scratch on every eviction, although only one key's count changed since last time.

From brute force to optimal
---------------------------
The scan answers two nested questions: what is the minimum frequency, and who is oldest at that
frequency. Group keys by frequency into buckets; inside a bucket keep LRU order with an
OrderedDict (move-to-end / popitem(last=False) are O(1)). The second question is now O(1). For
the first, notice a frequency count only ever goes UP by one, so the minimum frequency only
changes in two predictable ways: a brand-new key resets it to 1, and when the min bucket becomes
empty it must be exactly min+1 (the key we just moved went there). A single integer min_freq
tracks it. The tracker remembers key -> freq and freq -> ordered keys; it can forget timestamps
because ordering within a bucket IS the tie-break.

Intuition
---------
Think of frequency as floors in a building and each floor as a queue. Touching a key moves it
up one floor to the back of that floor's queue. Eviction removes the front of the lowest
non-empty floor. The lowest floor can only vanish by its last occupant moving up one floor, so
min_freq += 1 is always correct in that moment, and a new key always lands on floor 1.

Geometric view
--------------
Draw buckets left to right by frequency, each a horizontal queue (oldest at left):
freq 1: [2]      freq 2: [1, 3]      min_freq = 1
Eviction pops the leftmost item of the leftmost non-empty bucket. A touch lifts one item
one bucket to the right and appends it at the right end there.

Steps
-----
1. State: freq_of[key], bucket[freq] = OrderedDict(key -> value), min_freq.
2. _touch(key): pop from bucket[f]; if that bucket is now empty and f == min_freq, min_freq = f+1;
   insert into bucket[f+1]; freq_of[key] = f+1.
3. get: miss -> -1; hit -> _touch and return the value.
4. put existing: _touch then overwrite value. put new at capacity: popitem(last=False) from
   bucket[min_freq], delete its freq_of; then insert at bucket[1] and set min_freq = 1.

Complexity: O(1) time per operation, O(capacity) space — dict ops plus OrderedDict pop/append.
Pitfalls: capacity 0 (put must no-op); forgetting to reset min_freq = 1 on insert; evicting
          BEFORE inserting the new key (otherwise the new key could be the victim).
"""
import random
from collections import OrderedDict, defaultdict


class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.freq_of = {}                          # key -> use count
        self.bucket = defaultdict(OrderedDict)     # count -> keys in LRU order (key -> value)
        self.min_freq = 0

    def _touch(self, key: int) -> int:
        f = self.freq_of[key]
        val = self.bucket[f].pop(key)
        if not self.bucket[f]:
            del self.bucket[f]
            if self.min_freq == f:
                self.min_freq = f + 1              # only place the min can move up
        self.bucket[f + 1][key] = val
        self.freq_of[key] = f + 1
        return val

    def get(self, key: int) -> int:
        if key not in self.freq_of:
            return -1
        return self._touch(key)

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.freq_of:
            self._touch(key)
            self.bucket[self.freq_of[key]][key] = value
            return
        if len(self.freq_of) == self.cap:
            victim, _ = self.bucket[self.min_freq].popitem(last=False)   # oldest of the rarest
            del self.freq_of[victim]
            if not self.bucket[self.min_freq]:
                del self.bucket[self.min_freq]
        self.bucket[1][key] = value
        self.freq_of[key] = 1
        self.min_freq = 1


class BruteForce:
    """dict key -> [value, freq, last_tick]; eviction scans all keys for min (freq, tick)."""

    def __init__(self, capacity: int):
        self.cap = capacity
        self.data = {}
        self.tick = 0

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.tick += 1
        self.data[key][1] += 1
        self.data[key][2] = self.tick
        return self.data[key][0]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        self.tick += 1
        if key in self.data:
            self.data[key][0] = value
            self.data[key][1] += 1
            self.data[key][2] = self.tick
            return
        if len(self.data) == self.cap:
            victim = min(self.data, key=lambda k: (self.data[k][1], self.data[k][2]))   # O(n)
            del self.data[victim]
        self.data[key] = [value, 1, self.tick]


if __name__ == "__main__":
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)                      # evicts 2 (freq 1)
    assert c.get(2) == -1
    assert c.get(3) == 3
    c.put(4, 4)                      # 1 and 3 tie on freq 2; 1 is LRU -> evicted
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4

    z = LFUCache(0)                  # edge: zero capacity
    z.put(0, 0)
    assert z.get(0) == -1

    random.seed(1)
    for cap in (1, 2, 3, 4):
        fast, slow = LFUCache(cap), BruteForce(cap)
        for _ in range(600):
            k = random.randint(0, 6)
            if random.random() < 0.5:
                v = random.randint(0, 99)
                fast.put(k, v)
                slow.put(k, v)
            else:
                assert fast.get(k) == slow.get(k)
    print("ok")
