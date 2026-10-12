---
rank: 141
slug: all_o1_data_structure
---

Design a counter of string keys in which every operation runs in `O(1)`. `inc(key)` adds one to the key's count, starting from 0 for a new key; `dec(key)` subtracts one, and a key whose count reaches 0 disappears; `get_max_key()` and `get_min_key()` return any key with the largest or the smallest count, or the empty string when no key is left. After `inc("hello")` twice, both queries return `hello`; after `inc("leet")`, the maximum is still `hello` and the minimum is `leet`.

A map from key to count makes `inc` and `dec` constant time but leaves each query a scan of all the keys, `O(n)`, while a heap or a balanced tree keeps the order at `O(log n)` per update. The way out is that a count only ever moves by one. Group the keys into buckets by count and keep the buckets in a doubly linked list in increasing order of count, between a head and a tail sentinel. The keys with the smallest count sit in the first bucket after the head and those with the largest in the last bucket before the tail, and a key whose count changes by one only hops to a neighboring bucket. A map from each key to its bucket finds the key's place in `O(1)`.

`inc` looks at the bucket right after the key's current one, which is the head for a new key. If that bucket holds c + 1, where c is the key's count, the key moves in; otherwise a new bucket for c + 1 is spliced in between, and the list stays sorted, because no count lies strictly between c and c + 1. `dec` mirrors this on the left with c - 1, except that a key at count 1 simply leaves the map. The bucket the key left is unlinked as soon as it is empty, so every bucket in the list holds at least one key, and the two ends of the list are always the true minimum and maximum.

```text
operation    buckets, head to tail, counts rising   what changed
inc(hello)   head ─ [1: hello] ─ tail               new bucket 1 after head
inc(hello)   head ─ [2: hello] ─ tail               new 2, then 1 unlinked
inc(leet)    head ─ [1: leet] ─ [2: hello] ─ tail   new 1 after head
             bucket_of: leet → [1], hello → [2]
             min = head.next → leet, max = tail.prev → hello
inc(leet)    head ─ [2: hello, leet] ─ tail         2 reused, 1 unlinked
dec(hello)   head ─ [1: hello] ─ [2: leet] ─ tail   new 1 before 2
dec(hello)   head ─ [2: leet] ─ tail                count 0: hello is gone
dec(leet)    head ─ [1: leet] ─ tail                new 1, then 2 unlinked
dec(leet)    head ─ tail                            empty: both queries give ""
```

```pseudo
CLASS Bucket
    FUNCTION Init(count)
        self.count ← count
        self.keys ← empty set                  // every key with exactly count
        self.prev ← null
        self.next ← null

FUNCTION AnyKey(keys)
    FOR EACH key IN keys
        RETURN key                             // the first one met will do

CLASS AllOne
    FUNCTION Init()
        self.head ← new Bucket(0)              // sentinel before the smallest
        self.tail ← new Bucket(0)              // sentinel after the largest
        self.head.next ← self.tail
        self.tail.prev ← self.head
        self.bucket_of ← empty map             // key → the bucket holding it

    FUNCTION InsertAfter(bucket, count)
        fresh ← new Bucket(count)
        fresh.prev ← bucket
        fresh.next ← bucket.next
        bucket.next.prev ← fresh
        bucket.next ← fresh
        RETURN fresh

    FUNCTION RemoveKey(bucket, key)
        bucket.keys.remove(key)
        IF len(bucket.keys) = 0                // empty: unlink the bucket
            bucket.prev.next ← bucket.next
            bucket.next.prev ← bucket.prev

    FUNCTION Inc(key)
        IF key IN self.bucket_of
            current ← self.bucket_of[key]
        ELSE
            current ← self.head                // a new key comes from count 0
        target ← current.next
        IF target = self.tail OR target.count ≠ current.count + 1
            target ← self.InsertAfter(current, current.count + 1)
        target.keys.add(key)
        self.bucket_of[key] ← target
        IF current ≠ self.head
            self.RemoveKey(current, key)       // only after target is linked

    FUNCTION Dec(key)
        IF key NOT IN self.bucket_of
            RETURN
        current ← self.bucket_of[key]
        IF current.count = 1
            self.bucket_of.remove(key)         // count 0: the key disappears
        ELSE
            target ← current.prev
            IF target = self.head OR target.count ≠ current.count - 1
                target ← self.InsertAfter(current.prev, current.count - 1)
            target.keys.add(key)
            self.bucket_of[key] ← target
        self.RemoveKey(current, key)

    FUNCTION GetMaxKey()
        IF self.tail.prev = self.head
            RETURN ""
        RETURN AnyKey(self.tail.prev.keys)

    FUNCTION GetMinKey()
        IF self.head.next = self.tail
            RETURN ""
        RETURN AnyKey(self.head.next.keys)
```

Each operation is a few map and set operations plus a fixed number of pointer changes, so all four run in `O(1)`, on average because of hashing, and n keys need at most n buckets. It is the LRU cache's trick (#44) applied to counts instead of recency: a hash map gives direct access into a doubly linked list whose order is kept by local moves alone. LFU Cache (#93) keeps the same kind of frequency buckets, each holding its keys in LRU order. The signals are min and max queries over counters that change by one, such as the most and least active users. The classic mistake is the order inside `inc`: removing the key from its old bucket first can unlink that bucket before the new one is spliced in after it. From a single key at count 1, the forward walk from the head then finds no bucket at all, so `get_min_key` returns the empty string while `get_max_key` still answers. Forgetting to unlink an empty bucket is the other: the queries then read a bucket with no keys.

*Practice:* LC 432 All O`one Data Structure · LC 460 LFU Cache · LC 895 Maximum Frequency Stack
