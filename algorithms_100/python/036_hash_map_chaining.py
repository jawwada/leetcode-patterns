"""
Hash Map with Separate Chaining - Collisions Live in Buckets

Design a hash map without a built-in dict: put(key, value) inserts or
overwrites, get(key) returns the value or -1, remove(key) deletes the key.
With 8 buckets, keys 1 and 9 share bucket 1:
put(1, 10), put(9, 90), get(9) -> 90.
"""


# --- algorithm ---
class ChainedHashMap:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0                       # number of keys stored
        self.buckets = []
        for i in range(capacity):
            self.buckets.append([])         # one empty chain per bucket

    def bucket_of(self, key):
        """The chain that holds key: bucket hash(key) mod capacity. O(1)."""
        return self.buckets[hash(key) % self.capacity]

    def put(self, key, value):
        """Overwrite the key in its chain or append a new pair. Average O(1)."""
        bucket = self.bucket_of(key)
        for pair in bucket:
            if pair[0] == key:              # same key: overwrite the value
                pair[1] = value
                return
        bucket.append([key, value])         # new key: the chain grows by one
        self.size += 1
        if self.size / self.capacity > 0.75:
            self.resize()                   # load factor too high: grow

    def get(self, key):
        """Scan only the key's chain. Average O(1), worst O(n)."""
        bucket = self.bucket_of(key)
        for pair in bucket:
            if pair[0] == key:              # compare keys, not hashes
                return pair[1]
        return -1

    def remove(self, key):
        """Unlink the key's pair from its chain if present. Average O(1)."""
        bucket = self.bucket_of(key)
        for pair in bucket:
            if pair[0] == key:
                bucket.remove(pair)
                self.size -= 1
                return

    def resize(self):
        """Double the bucket array and rehash every pair. O(n), but rare."""
        old_buckets = self.buckets
        self.capacity = 2 * self.capacity
        self.buckets = []
        for i in range(self.capacity):
            self.buckets.append([])
        for bucket in old_buckets:
            for pair in bucket:
                new_bucket = self.bucket_of(pair[0])    # uses the new capacity
                new_bucket.append(pair)


# --- try it ---
table = ChainedHashMap()
table.put(1, 10)
table.put(9, 90)                            # 9 mod 8 = 1: same bucket as 1
table.put(1, 11)                            # overwrite
print(table.get(1), table.get(9), table.get(2))     # -> 11 90 -1
table.remove(9)
print(table.get(9), table.size)             # -> -1 1
for key in range(2, 8):
    table.put(key, key * 10)
print(table.capacity, table.size, table.get(7))     # -> 16 7 70
