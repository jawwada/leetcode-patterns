---
rank: 47
slug: snapshot_array
---

Design an array of `length` zeros that can take snapshots: `set(index, val)` writes a value, `snap()` takes a snapshot and returns its id, counting up from 0, and `get(index, snap_id)` returns the value the index held when that snapshot was taken. With length 3, after `set(0, 5)` the first `snap()` returns 0; after `set(0, 6)` and `set(0, 8)`, `get(0, 0)` still returns 5.

The brute force copies the whole array on every `snap()`, which costs `O(length)` time per snapshot and `O(length × snaps)` memory, even when only a few cells changed since the last one. Store the changes instead. Each index keeps its own history, a list of `(snap_id, value)` pairs. `set` records the value under the id of the snapshot that is still open, the one the next `snap()` will return, and `snap()` does nothing but move that counter forward. Writes since the last snapshot carry an id that no query may ask for yet, so a late write can never leak into an older snapshot. A second write to the same index before the next snap rewrites the newest pair instead of appending, which keeps one pair per index per snapshot.

Snap ids only grow, so every history is sorted for free, and `get(index, snap_id)` wants the last pair at or before `snap_id`: binary search for the first pair after it, the upper bound of #14, and step one slot to the left. If no pair comes before it, the index was never written by then and still holds 0. Picture each index as a row of snapshot columns with a value wherever that snapshot changed it; a query looks at its column and walks left to the nearest value. It is the Time-Based Key-Value Store (#92) with one timeline per index and snapshot ids for times.

```text
calls: set(0, 5)  snap() → 0  set(0, 6)  set(1, 4)  set(0, 8)  get(0, 0) → 5
       snap() → 1  snap() → 2  set(1, 9)  snap() → 3

snap id        0      1      2      3      pairs after the calls
index 0        5      8      ·      ·      [(0, 5), (1, 8)]    8 rewrote 6
index 1        ·      4      ·      9      [(1, 4), (3, 9)]
index 2        ·      ·      ·      ·      []

get(i, s) looks at row i, column s, and walks left to the nearest value
get(0, 2): pairs [(0, 5), (1, 8)], left = 0, right = 2
  mid = 1: snap 1 ≤ 2 → left = 2; the answer is pairs[1] → 8
get(1, 2): pairs [(1, 4), (3, 9)], left = 0, right = 2
  mid = 1: snap 3 > 2 → right = 1;  mid = 0: snap 1 ≤ 2 → left = 1 → 4
get(1, 0): mid = 1: snap 3 > 0 → right = 1;  mid = 0: snap 1 > 0 → right = 0
  left = 0: index 1 was not written by snapshot 0 → 0
```

```pseudo
CLASS SnapshotArray
    FUNCTION Init(length)
        self.history ← empty list         // index → list of (snap_id, value)
        FOR i FROM 0 TO length - 1
            self.history.append(empty list)
        self.snap_id ← 0                  // the id the next Snap returns

    FUNCTION Set(index, val)
        pairs ← self.history[index]
        last ← len(pairs) - 1             // the newest pair, if any
        IF last ≥ 0 AND pairs[last][0] = self.snap_id
            pairs[last] ← (self.snap_id, val)    // same snapshot: rewrite it
        ELSE
            pairs.append((self.snap_id, val))

    FUNCTION Snap()
        self.snap_id ← self.snap_id + 1
        RETURN self.snap_id - 1

    FUNCTION Get(index, snap_id)
        pairs ← self.history[index]
        left ← 0
        right ← len(pairs)
        WHILE left < right                // find the first pair after snap_id
            mid ← floor((left + right) / 2)
            IF pairs[mid][0] ≤ snap_id
                left ← mid + 1            // mid was written by then
            ELSE
                right ← mid               // mid is later: maybe the first
        IF left = 0
            RETURN 0                      // not written by that snapshot
        RETURN pairs[left - 1][1]
```

`set` and `snap` cost `O(1)`, and `get` costs `O(log w)` for an index written in `w` different snapshots. Memory is `O(length + writes)`: it grows with the writes, never with snapshots times length, so a million snapshots of an untouched array cost one counter. Reach for per-index histories when a problem asks for versions, snapshots or a value as of some moment, and copying everything on each version would be too slow. Databases run the same idea at scale as multiversion concurrency control: every write adds a version stamped with a transaction id, and a reader sees the newest version at or before its own snapshot. The classic mistake is a lower-bound search for the first pair whose id is at least `snap_id`: when the index was not written in that very snapshot, it lands on a later write, and `get(1, 2)` above returns 9, written after snapshot 2, instead of 4. The other one is `snap()` returning the incremented counter, which shifts every id by one.

*Practice:* LC 1146 Snapshot Array · LC 981 Time Based Key-Value Store · LC 911 Online Election
