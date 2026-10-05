"""
Design HashMap (LeetCode 706) - Easy
Chapter: design
Pattern: Separate chaining with load-factor resizing

Implement MyHashMap without built-in hash tables: put(key, value), get(key) -> value or -1,
remove(key). Keys and values are non-negative integers up to 10^6.
Example: put(1,1), put(2,2), get(1) -> 1, get(3) -> -1, put(2,1), get(2) -> 1, remove(2),
get(2) -> -1.
"""


# --- brute force ---
class BruteForce:
    """One flat list of [key, value]; every operation scans all pairs. O(n) per operation."""

    def __init__(self):
        self.pairs = []

    def put(self, key, value):
        for pair in self.pairs:
            if pair[0] == key:
                pair[1] = value           # key already there: overwrite in place
                return
        self.pairs.append([key, value])

    def get(self, key):
        for pair in self.pairs:
            if pair[0] == key:
                return pair[1]
        return -1

    def remove(self, key):
        for i in range(len(self.pairs)):
            if self.pairs[i][0] == key:
                self.pairs.pop(i)
                return


# --- optimal ---
class MyHashMap:
    """Buckets of [key, value] pairs picked by key % bucket count; double when full. O(1) avg."""

    def __init__(self):
        self.size = 0
        self.buckets = []
        for _ in range(8):
            self.buckets.append([])       # 8 empty buckets to start

    def bucket_for(self, key):
        return self.buckets[key % len(self.buckets)]   # keys are ints, so the key is its own hash

    def put(self, key, value):
        bucket = self.bucket_for(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value           # key already there: overwrite in place
                return
        bucket.append([key, value])
        self.size += 1
        if self.size > 2 * len(self.buckets):   # load factor above 2: double and rehash
            self.resize()

    def get(self, key):
        for pair in self.bucket_for(key):
            if pair[0] == key:
                return pair[1]
        return -1

    def remove(self, key):
        bucket = self.bucket_for(key)
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self.size -= 1
                return

    def resize(self):
        old_buckets = self.buckets
        self.buckets = []
        for _ in range(2 * len(old_buckets)):
            self.buckets.append([])
        for bucket in old_buckets:
            for pair in bucket:
                self.bucket_for(pair[0]).append(pair)   # every pair moves to its new bucket


# --- try the brute force ---
m = BruteForce()
m.put(1, 1)
m.put(2, 2)
print(m.get(1))      # -> 1
print(m.get(3))      # -> -1
m.put(2, 1)
print(m.get(2))      # -> 1
m.remove(2)
print(m.get(2))      # -> -1


# --- try the optimal ---
m = MyHashMap()
m.put(1, 1)
m.put(2, 2)
print(m.get(1))      # -> 1
print(m.get(3))      # -> -1
m.put(2, 1)
print(m.get(2))      # -> 1
m.remove(2)
print(m.get(2))      # -> -1
