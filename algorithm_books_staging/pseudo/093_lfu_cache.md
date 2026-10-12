---
rank: 93
slug: lfu_cache
---

Design a cache with a fixed capacity whose `get(key)` and `put(key, value)` both run in `O(1)`. `get` returns the value or `-1`, and every `get` that finds its key and every `put` counts as one use of that key. When a new key arrives and the cache is full, it evicts the least frequently used key, and among keys with the same count the least recently used one. With capacity 2, after `put(1, 10)`, `get(1)` and `put(2, 20)`, the call `put(3, 30)` evicts key 2, used once, and keeps key 1, used twice, even though key 1 is the less recent of the two.

The brute force stores a use count and a last-use time with every key and scans all of them at each eviction, `O(n)`. That scan answers two nested questions, the smallest count in the cache and the oldest key with that count, and grouping the keys makes both answers immediate. Put the keys into buckets by use count, and keep each bucket in recency order with the doubly linked list of the LRU Cache (#44): newest after `head`, oldest before `tail`. One map sends each key to its node, which carries the key, the value and the count `freq`; a second map sends each count to its bucket. The oldest key with a given count is now `bucket.tail.prev`. The smallest count is one integer, `min_freq`, because a count only ever grows by one, so the minimum can move in just two ways. A use moves a node from bucket `f` to the front of bucket `f + 1`, and when that empties bucket `f` and `f` was the minimum, the minimum becomes `f + 1`, where the node just landed. A new key enters bucket 1 and sets `min_freq` back to 1, since nothing is used less than once.

Picture the buckets as the floors of a building, each floor a queue ordered by recency. A use lifts a key one floor and puts it at the newest end; eviction takes the oldest key on the lowest occupied floor. Evict before inserting: a cache that inserts first and then evicts from bucket 1 throws out the newcomer itself whenever every older key has been used at least twice.

```text
after get(3) → 30, both keys sit in bucket 2:
    freq 2   head ─ 3:30 ─ 1:10 ─ tail      put(4, 40) evicts tail.prev = 1
                    newest  oldest

operation       freq: keys, newest     min_freq  note
put(1, 10)      1: [1]                 1
get(1) → 10     2: [1]                 2         bucket 1 empties: min rises
put(2, 20)      1: [2]  2: [1]         1         a new key resets min to 1
put(3, 30)      1: [3]  2: [1]         1         full: evict 2, used once
get(2) → -1     1: [3]  2: [1]         1         a miss changes nothing
get(3) → 30     2: [3, 1]              2         a tie at 2 uses
put(4, 40)      1: [4]  2: [3]         1         full: evict 1, the older
get(1) → -1     1: [4]  2: [3]         1
get(3) → 30     1: [4]  3: [3]         1
get(4) → 40     2: [4]  3: [3]         2         bucket 1 empties: min rises
```

```pseudo
CLASS Node
    FUNCTION Init(key, value)
        self.key ← key                  // kept so eviction can clean the map
        self.value ← value
        self.freq ← 1                   // how many times the key was used
        self.prev ← null
        self.next ← null

CLASS Bucket                            // the list of #44, one per freq
    FUNCTION Init()
        self.head ← Node(0, 0)          // sentinel: head.next is the newest
        self.tail ← Node(0, 0)          // sentinel: tail.prev is the oldest
        self.head.next ← self.tail
        self.tail.prev ← self.head
    // AddFront(node) and Remove(node): exactly as in LRU Cache (#44)

    FUNCTION IsEmpty()
        RETURN self.head.next = self.tail

CLASS LFUCache
    FUNCTION Init(capacity)
        self.capacity ← capacity
        self.nodes ← empty map          // key → node
        self.buckets ← empty map        // freq → bucket of keys used freq times
        self.min_freq ← 0               // the smallest freq that has a key

    FUNCTION Add(node)
        IF node.freq NOT IN self.buckets
            self.buckets[node.freq] ← Bucket()
        self.buckets[node.freq].AddFront(node)

    FUNCTION Touch(node)
        bucket ← self.buckets[node.freq]
        bucket.Remove(node)
        IF bucket.IsEmpty()
            self.buckets.remove(node.freq)
            IF self.min_freq = node.freq
                self.min_freq ← self.min_freq + 1   // node moves up to it
        node.freq ← node.freq + 1
        self.Add(node)

    FUNCTION Get(key)
        IF key NOT IN self.nodes
            RETURN -1
        node ← self.nodes[key]
        self.Touch(node)
        RETURN node.value

    FUNCTION Put(key, value)
        IF self.capacity = 0
            RETURN
        IF key IN self.nodes
            node ← self.nodes[key]
            node.value ← value
            self.Touch(node)
            RETURN
        IF len(self.nodes) = self.capacity
            self.Evict()                // before the new key is added
        node ← Node(key, value)
        self.nodes[key] ← node
        self.Add(node)
        self.min_freq ← 1               // a new key is the least used

    FUNCTION Evict()
        bucket ← self.buckets[self.min_freq]
        victim ← bucket.tail.prev       // least used, then least recent
        bucket.Remove(victim)
        IF bucket.IsEmpty()
            self.buckets.remove(self.min_freq)
        self.nodes.remove(victim.key)
```

Every operation is a constant number of map lookups and pointer changes, so `get` and `put` run in `O(1)`, and the cache holds at most `capacity` nodes. After an eviction `min_freq` may name a bucket that is gone, but the insertion that follows resets it to 1, so no search is ever needed. LRU evicts a key used a thousand times as soon as `capacity` other keys have been used after it; LFU protects popular keys but lets a key that was hot long ago linger, which is why real caches age their counts or blend the two policies. A Python dict keeps insertion order too, but finding its first key walks over the empty slots that deletions leave at the front, so a bucket that churns like a queue slows down as it grows; an `OrderedDict` or the hand-built list keeps every step `O(1)`. All O(1) Data Structure (#141) reuses the buckets, chained into a linked list of counts, and Maximum Frequency Stack turns them upside down: it keeps the largest count and pops the newest entry of that bucket. The classic mistakes are forgetting that a `put` to an existing key is a use, and dropping the capacity-0 guard, so that the first `put` tries to evict from a `buckets[0]` that does not exist.

*Practice:* LC 460 LFU Cache · LC 146 LRU Cache · LC 895 Maximum Frequency Stack
