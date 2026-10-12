---
rank: 70
slug: time_based_kv_store
---

Design a store that keeps every version of a key. `set(key, value, timestamp)` records a value at a time, with the timestamps of each key arriving in increasing order, and `get(key, timestamp)` returns the value set at the largest time `≤ timestamp`, or the empty string if the key had no value yet. After setting `status` to `draft` at time `1`, `review` at `4` and `live` at `9`, `get("status", 5)` is `"review"` and `get("status", 0)` is `""`.

The brute force keeps one log of every `set` call and scans all of it on each `get`, `O(n)` per query. The order in which versions arrive is the gift: because the timestamps of a key only grow, appending to that key's list keeps it sorted for free, and a sorted list answers "the last time at or before `t`" by binary search. Each key therefore owns two parallel lists, the times and the values set at those times; `set` appends to both and `get` searches the times. The search finds the first time strictly after `t`, the upper bound, and steps one slot to the left, where the newest version that already existed at time `t` sits. If the upper bound is slot `0`, every version is newer than `t` and the answer is empty.

Picture each key as a timeline with a dot at every version. A query drops a pin at time `t` and walks left to the nearest dot. The binary search keeps every slot before `left` at or before `t` and every slot from `right` on after it, and halves the unknown gap between them until it closes.

```text
           draft          review                   live
time ─┼────●──────────────●────┼───────────────────●─────────→
      0    1              4    5                   9
                               ▲ get("status", 5) walks left to the dot at 4
get("status", 5): left = 0, right = 3
  mid = 1: time 4 ≤ 5 → left = 2
  mid = 2: time 9 > 5 → right = 2
  the first time after 5 is slot 2, so the answer is slot 1 → "review"
get("status", 0): every time is after 0, left stays 0 → ""
```

```pseudo
CLASS TimeMap
    FUNCTION Init()
        self.times ← empty map                // key → increasing set times
        self.values ← empty map               // key → values, in the same order

    FUNCTION Set(key, value, timestamp)
        IF key NOT IN self.times
            self.times[key] ← empty list
            self.values[key] ← empty list
        self.times[key].append(timestamp)     // times only grow: stays sorted
        self.values[key].append(value)

    FUNCTION Get(key, timestamp)
        IF key NOT IN self.times
            RETURN ""
        times ← self.times[key]
        left ← 0
        right ← len(times)
        WHILE left < right                    // find the first time > timestamp
            mid ← floor((left + right) / 2)
            IF times[mid] ≤ timestamp
                left ← mid + 1                // mid is not after timestamp
            ELSE
                right ← mid                   // mid is after: maybe the first
        IF left = 0
            RETURN ""                         // every version is newer
        RETURN self.values[key][left - 1]
```

`set` costs amortized `O(1)` and `get` costs `O(log n)` for a key with `n` versions, because each step halves the gap; the store keeps every version, so space is linear in the number of `set` calls. The signals are values that change over time and questions asked "as of" a moment: versioned configs, snapshots, prices or election leaders at a time. The search is the lower-bound template of #9 with `≤` in place of `<`, which turns lower bound into upper bound, and Snapshot Array (LC 1146) is the same structure with one timeline per index and snapshot ids as times. If timestamps could arrive out of order, appending would break the sorting and each key would need a balanced search tree (a `TreeMap` in Java) instead of a list. The classic mistake is forgetting the `left = 0` case: Python then reads `values[-1]` and silently returns the newest version for a time before the first one.

*Practice:* LC 981 Time Based Key-Value Store · LC 1146 Snapshot Array · LC 911 Online Election
