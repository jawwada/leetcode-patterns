---
rank: 101
slug: hash_map_open_addressing
---

Design a hash map without a built-in dictionary that stores every pair directly in one array of slots, with no chains: `put(key, value)`, `get(key)` returning `-1` for a missing key, and `remove(key)`. With 8 slots and integers hashing to themselves, key `3` lives in slot `3`; key `11` also hashes to slot `3`, finds it taken and settles in slot `4`, so after `put(3, 30)` and `put(11, 110)` the call `get(11)` returns `110`.

Separate chaining (#51) hangs a list off every bucket. Open addressing keeps one flat array and resolves a collision, a slot already holding a different key, by probing: try the home slot `hash(key) mod capacity`, then the next slot, and the next, wrapping around the end. A key therefore sits somewhere on the unbroken run of non-empty slots that starts at its home, and a search walks that run until it meets the key or an EMPTY slot. An EMPTY slot ends the search, because an insert of the key would have stopped there; the key cannot lie beyond it.

Deletion is the subtle part. Emptying a slot would cut a run in two and strand every key whose path crosses the gap, so `remove` writes a DELETED marker, a tombstone, that searches step over and inserts may reuse: once a full search has shown that a key is absent, `put` takes the first tombstone or EMPTY slot on its path. Tombstones lengthen searches just like live keys, so the load counts both, and when `(size + tombstones) / capacity` passes 0.5 the table doubles and re-puts only its live pairs, which sweeps the tombstones away. The table stays half empty because of primary clustering: occupied slots merge into runs, a key whose home falls anywhere inside a run lands at its end, and so long runs catch more keys and grow faster still. A miss inspects about 2.5 slots on average at load 0.5, but dozens at load 0.9.

```text
8 slots, home = key mod 8                · EMPTY     X tombstone
               slot   0    1    2    3    4    5    6    7
put 3                 ·    ·    ·    3    ·    ·    ·    ·    home 3
put 11                ·    ·    ·    3   11    ·    ·    ·    3 taken → 4
put 19                ·    ·    ·    3   11   19    ·    ·    3, 4 taken → 5
put 4                 ·    ·    ·    3   11   19    4    ·    home 4 → 6
remove 11             ·    ·    ·    3    X   19    4    ·
get 19:    slot 3 holds 3, slot 4 is X so keep going, slot 5 holds 19 → 190
put 27:    the search passes 3, X, 19, 4 and stops at EMPTY slot 7: absent;
           the first free slot on its path is the tombstone in slot 4
put 27                ·    ·    ·    3   27   19    4    ·
put 12:    lands in slot 7; load (5 + 0) / 8 = 0.625 > 0.5 → 16 slots,
           live keys re-put: 3 → 3, 19 → 4, 4 → 5, 27 → 11, 12 → 12
```

```pseudo
CLASS ProbingHashMap                // a slot: EMPTY, DELETED or [key, value]
    FUNCTION Init(capacity)
        self.capacity ← capacity
        self.size ← 0                       // live keys
        self.tombstones ← 0                 // DELETED slots
        self.slots ← array of capacity copies of EMPTY

    FUNCTION Find(key)                      // index of key's slot, or -1
        index ← hash(key) mod self.capacity
        WHILE self.slots[index] ≠ EMPTY
            slot ← self.slots[index]
            IF slot ≠ DELETED AND slot[0] = key
                RETURN index
            index ← (index + 1) mod self.capacity    // taken: try the next
        RETURN -1

    FUNCTION Put(key, value)
        index ← self.Find(key)
        IF index ≠ -1
            self.slots[index][1] ← value             // already stored
            RETURN
        index ← hash(key) mod self.capacity
        WHILE self.slots[index] ≠ EMPTY AND self.slots[index] ≠ DELETED
            index ← (index + 1) mod self.capacity    // skip live pairs
        IF self.slots[index] = DELETED
            self.tombstones ← self.tombstones - 1    // reuse the tombstone
        self.slots[index] ← [key, value]
        self.size ← self.size + 1
        IF (self.size + self.tombstones) / self.capacity > 0.5
            self.Resize()

    FUNCTION Get(key)
        index ← self.Find(key)
        IF index = -1
            RETURN -1
        RETURN self.slots[index][1]

    FUNCTION Remove(key)
        index ← self.Find(key)
        IF index ≠ -1
            self.slots[index] ← DELETED     // later searches step over it
            self.size ← self.size - 1
            self.tombstones ← self.tombstones + 1

    FUNCTION Resize()
        old_slots ← self.slots
        self.capacity ← 2 * self.capacity
        self.slots ← array of self.capacity copies of EMPTY
        self.size ← 0
        self.tombstones ← 0
        FOR EACH slot IN old_slots
            IF slot ≠ EMPTY AND slot ≠ DELETED
                self.Put(slot[0], slot[1])  // tombstones are dropped
```

With a good hash and the load capped at one half, every operation takes `O(1)` expected time; the worst case is `O(n)`, one run through the whole table, and a resize costs `O(n)` but is amortized away as in #51. One flat array of pairs and no pointers keeps the table compact and friendly to the cache; CPython's `dict` is an open-addressing table too, though it scrambles the probe order instead of stepping by one. The signals are a design question about hash map internals, or a follow-up asking how a map works without linked lists. The classic mistake is a `remove` that writes EMPTY: after removing `11` from the cluster in the picture, `get(19)` stops at the hole in slot 4 and reports `-1`.

*Practice:* LC 706 Design HashMap · LC 705 Design HashSet
