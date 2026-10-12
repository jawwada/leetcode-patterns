---
rank: 51
slug: hash_map_chaining
---

Design a hash map without a built-in dictionary: `put(key, value)` inserts a key or overwrites its value, `get(key)` returns the value or `-1` when the key is missing, and `remove(key)` deletes the key. With 8 buckets and integers hashing to themselves, `put(1, 10)` and `put(9, 90)` send both keys to bucket 1, because `1 mod 8 = 9 mod 8 = 1`, and `get(9)` must still return `90`.

A plain list of pairs works, but every call scans all of it, `O(n)` per operation. A hash map splits that one long list into many short ones. It keeps an array of `capacity` buckets and sends each key to bucket `hash(key) mod capacity`, so an operation computes one index and touches only that bucket. Different keys can land in the same bucket; that is a collision, and separate chaining simply lets it happen: each bucket is a small list, a chain, of `[key, value]` pairs. The hash chooses the chain and comparing keys inside the chain chooses the pair, so a `put` of an existing key overwrites in place, a new key is appended, and `remove` unlinks its pair.

The load factor `size / capacity` is the average chain length. With a hash that spreads keys evenly, a lookup scans about that many pairs, so keeping the load factor at most 0.75 makes every operation `O(1)` on average. When a `put` pushes it past 0.75, the map doubles the bucket array and rehashes every pair, because the bucket index depends on the capacity: each old chain splits between bucket `b` and bucket `b + old capacity`.

```text
8 buckets, bucket = key mod 8; put keys 1, 9, 17, 2, 10, 4 with value 10 × key
  bucket 0     ·
  bucket 1     1:10 → 9:90 → 17:170      1, 9 and 17 collide
  bucket 2     2:20 → 10:100             2 and 10 collide
  bucket 3     ·
  bucket 4     4:40
  bucket 5-7   ·                         load = 6 / 8 = 0.75, no resize yet

get(17): bucket 17 mod 8 = 1; compare keys 1 ✗, 9 ✗, 17 ✓ → 170

put(25): bucket 1 again; load 7 / 8 = 0.875 > 0.75 → 16 buckets, rehash
  bucket 1     1:10 → 17:170             the old chain 1 splits
  bucket 9     9:90 → 25:250             between buckets 1 and 9
  bucket 2     2:20                      and chain 2 between
  bucket 10    10:100                    buckets 2 and 10
  bucket 4     4:40                      every other bucket is empty
```

```pseudo
CLASS ChainedHashMap
    FUNCTION Init(capacity)
        self.capacity ← capacity
        self.size ← 0                           // number of keys stored
        self.buckets ← empty list
        FOR i FROM 0 TO capacity - 1
            self.buckets.append(empty list)     // one empty chain per bucket

    FUNCTION BucketOf(key)                      // the chain that holds key
        RETURN self.buckets[hash(key) mod self.capacity]

    FUNCTION Put(key, value)
        bucket ← self.BucketOf(key)
        FOR EACH pair IN bucket
            IF pair[0] = key                    // same key: overwrite the value
                pair[1] ← value
                RETURN
        bucket.append([key, value])             // new key: the chain grows
        self.size ← self.size + 1
        IF self.size / self.capacity > 0.75
            self.Resize()                       // load factor too high: grow

    FUNCTION Get(key)
        bucket ← self.BucketOf(key)
        FOR EACH pair IN bucket
            IF pair[0] = key                    // compare keys, not hashes
                RETURN pair[1]
        RETURN -1

    FUNCTION Remove(key)
        bucket ← self.BucketOf(key)
        FOR EACH pair IN bucket
            IF pair[0] = key
                bucket.remove(pair)
                self.size ← self.size - 1
                RETURN

    FUNCTION Resize()
        old_buckets ← self.buckets
        self.capacity ← 2 * self.capacity
        self.buckets ← empty list
        FOR i FROM 0 TO self.capacity - 1
            self.buckets.append(empty list)
        FOR EACH bucket IN old_buckets
            FOR EACH pair IN bucket
                new_bucket ← self.BucketOf(pair[0])   // uses the new capacity
                new_bucket.append(pair)
```

Every operation costs `O(1)` on average and `O(n)` in the worst case, when all keys hash to the same bucket and the map degenerates into one long chain; Java's `HashMap` turns a long chain into a balanced tree for exactly that reason. A resize costs `O(n)`, but the next one waits until the key count has nearly doubled, so the rehashing over `n` puts adds up to `O(n)`, amortized `O(1)` per put. The space is `O(n + capacity)`. The signals are a request to design a hash map or hash set, or a question about how a dictionary works inside; a good answer names the bucket index, collisions, the load factor and resizing. The classic mistake is copying each old chain to the same index of the bigger array instead of rehashing: key 9 stays in bucket 1, while `get(9)` now looks in bucket `9 mod 16 = 9` and misses it.

*Practice:* LC 706 Design HashMap · LC 705 Design HashSet
