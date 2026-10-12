---
rank: 94
slug: ttl_cache
---

Design a cache whose keys expire. `put(key, value, ttl, now)` stores a value that lives until the deadline `now + ttl`, and putting the key again replaces both its value and its deadline. `get(key, now)` returns the value only while `now` is earlier than the deadline, and `null` otherwise, and `size(now)` counts the keys still alive. Every call receives the current time from the caller, so the cache never reads a clock and any sequence of calls can be replayed exactly. After `put(b, 2, 3, 1)` the key `b` lives until time 4: `get(b, 3)` returns `2` and `get(b, 4)` returns `null`.

A timer per key is the heavy design, and a `size` that scans every key for dead ones costs `O(n)` per call. Expiry splits into two jobs, and each has a cheap answer. A read checks a single deadline, so `get` expires its own key lazily: when the key it finds is already dead, it deletes the key and reports a miss. Keys that are never read again would pile up, so `size` also expires keys in bulk, and to find them without a scan it keeps every deadline in a min-heap of `(expire_at, key)` pairs. The earliest deadline sits on top, so popping while the top is `≤ now` visits exactly the pairs whose time has come, in time order, and stops at the first one still in the future.

A plain heap cannot change or remove a pair in the middle, so a rewrite simply pushes a new pair and leaves the old one behind, stale, and a lazy delete in `get` leaves its pair behind as well. The map is the source of truth: a popped pair deletes its key only when the map still holds that key with that very deadline, and every other pair is dropped without a word. This is the lazy deletion of Dijkstra's algorithm (#42). Picture two layers: the map holds one current deadline per key, and the heap holds the deadlines promised and not yet popped, in time order, some of them already broken.

```text
call              entries key(value, expire_at)   heap, earliest first
put(a, 1, 5, 0)   a(1, 5)                         (5, a)
put(b, 2, 3, 1)   a(1, 5) b(2, 4)                 (4, b) (5, a)
put(c, 3, 10, 2)  a(1, 5) b(2, 4) c(3, 12)        (4, b) (5, a) (12, c)
get(b, 3) → 2     3 < 4: b is live
get(b, 4) → null  a(1, 5) c(3, 12)                (4, b) is left behind
put(a, 7, 5, 4)   a(7, 9) c(3, 12)                (4, b) (5, a) (9, a) (12, c)
size(6) → 2       pop (4, b): b is gone, skip
                  pop (5, a): a expires at 9, stale, skip
                  a(7, 9) c(3, 12)                (9, a) (12, c)
get(a, 8) → 7     8 < 9: a is live
get(a, 9) → null  c(3, 12)                        (9, a) is left behind
size(11) → 1      pop (9, a): a is gone, skip     (12, c)
size(12) → 0      pop (12, c): current, delete c  empty
```

```pseudo
CLASS TTLCache
    FUNCTION Init()
        self.entries ← empty map            // key → (value, expire_at)
        self.deadlines ← empty min-heap     // (expire_at, key), some stale

    FUNCTION Put(key, value, ttl, now)
        expire_at ← now + ttl
        self.entries[key] ← (value, expire_at)
        self.deadlines.push((expire_at, key))   // old pair goes stale

    FUNCTION Get(key, now)
        IF key NOT IN self.entries
            RETURN null
        (value, expire_at) ← self.entries[key]
        IF now ≥ expire_at
            self.entries.remove(key)        // lazy expiry: found dead on a read
            RETURN null
        RETURN value

    FUNCTION Purge(now)
        WHILE len(self.deadlines) > 0 AND self.deadlines.top()[0] ≤ now
            (expire_at, key) ← self.deadlines.pop()      // earliest first
            IF key IN self.entries AND self.entries[key][1] = expire_at
                self.entries.remove(key)    // current pair: the key expired
            // any other pair is stale: the key was rewritten or removed

    FUNCTION Size(now)
        self.Purge(now)
        RETURN len(self.entries)
```

`get` costs `O(1)`, `put` costs `O(log n)` for the push, and `size` costs `O(k log n)` for the `k` pairs it pops; every pair is pushed once and popped at most once, so the purging is paid for by the puts. Stale pairs make the heap larger than the map, and each one lingers until a purge reaches its deadline, so a key rewritten often with a long TTL leaves a trail of them. Both checks call a key dead at its deadline, `now ≥ expire_at` in `get` and `top ≤ now` in the purge; they must agree, and time must never run backwards between calls. A capacity bound turns this into an LRU cache with expiry: the map points at the list nodes of #44, and a full `put` can purge first and evict the least recently used key only when that freed no room. Redis expires keys the same two ways, passively when a client touches a key that has timed out, and periodically by testing a few random keys among those with a TTL and deleting the expired ones. The signals are sessions, tokens, DNS records and anything with a time to live; Stock Price Tracker (#140) uses the same check of a heap entry against the map. The classic mistake is deleting the key of every popped pair without comparing deadlines: in the trace, the stale `(5, a)` would delete `a` at time 6, although its rewrite keeps it alive until 9.

*Practice:* LC 1797 Design Authentication Manager · LC 2034 Stock Price Fluctuation · LC 146 LRU Cache
