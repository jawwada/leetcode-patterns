---
rank: 69
slug: randomized_set
---

Design a set of integers with three operations, `insert(val)`, `remove(val)` and `get_random()`, each in average `O(1)` time. Insert and remove return whether the set changed, and `get_random` returns every stored value with the same probability. After inserting `10`, `20` and `30` and removing `10`, the set holds `30` and `20`, and `get_random` returns each of them half the time.

Neither familiar structure delivers all three. A hash set inserts and removes in `O(1)` but cannot pick a random member without walking to it, `O(n)`; a plain list picks a random index in `O(1)` but needs an `O(n)` search to refuse a duplicate or to find a value, and deleting from its middle shifts the whole tail left, `O(n)` again. The design keeps both. A list `values` stays packed from index `0` with no holes, so a uniformly random index is a uniformly random value, and a map `index_of` sends each value to its slot, so finding a value is one lookup. Insertion appends and records the new slot. Removal is the one clever step: deleting from the middle would open a hole, and closing it by shifting is exactly the cost to avoid, so the last value jumps into the hole, its map entry is corrected, and the tail slot is popped. A set has no order to preserve, which is what makes the jump legal.

Picture the list as a row of tiles. A removal never slides the row; the rightmost tile fills the gap and the row shrinks by one from the right. After every operation `index_of[values[i]] = i` holds for every slot `i`, and there is exactly one slot per key.

```text
                         values          index_of
insert 10, 20, 30        [10, 20, 30]    {10: 0, 20: 1, 30: 2}
remove(10)               i = 0 (the slot of 10), last = 30
  last into slot 0       [30, 20, 30]    {10: 0, 20: 1, 30: 0}
  pop tail, delete 10    [30, 20]        {20: 1, 30: 0}
get_random               RandomInt(0, 1) → slot 0 or 1 → 30 or 20, half each
```

```pseudo
CLASS RandomizedSet
    FUNCTION Init()
        self.values ← empty list              // packed from index 0, no holes
        self.index_of ← empty map             // value → its slot in values

    FUNCTION Insert(val)
        IF val IN self.index_of
            RETURN false
        self.index_of[val] ← len(self.values)
        self.values.append(val)
        RETURN true

    FUNCTION Remove(val)
        IF val NOT IN self.index_of
            RETURN false
        i ← self.index_of[val]
        last ← self.values[len(self.values) - 1]
        self.values[i] ← last                 // the last value fills the hole
        self.index_of[last] ← i               // and learns its new slot
        self.values.pop()                     // drop the tail slot
        self.index_of.remove(val)             // only now: last may be val
        RETURN true

    FUNCTION GetRandom()
        i ← RandomInt(0, len(self.values) - 1)    // uniform, both ends included
        RETURN self.values[i]
```

Every operation is a constant number of hash-map steps plus work at the end of the list, so each costs `O(1)` on average (hashing gives the average; appending and popping the end are amortized `O(1)`), and the structure takes `O(n)` space. Reach for it whenever a problem wants uniform random sampling from a collection that changes, or an `O(1)` delete from an array whose order does not matter; it is the same pairing of a map with a structure the map points into that powers the LRU cache of #35. With duplicates allowed (LC 381) the map holds a set of slots for each value and removal takes any one of them, with the same jump of the last tile. The classic mistake is deleting `val` from the map before correcting the moved value's slot: when `val` is itself the last value, the correction writes it straight back, leaving a ghost key that points past the end of the list, and a later `insert(val)` wrongly returns false.

*Practice:* LC 380 Insert Delete GetRandom O(1) · LC 381 Insert Delete GetRandom O(1) - Duplicates allowed · LC 710 Random Pick with Blacklist
