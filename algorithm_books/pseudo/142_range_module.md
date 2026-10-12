---
rank: 142
slug: range_module
---

Design a module that tracks ranges of numbers as half-open intervals `[left, right)` with `left < right`, which contain `left` but not `right`. `add_range(left, right)` starts tracking every number in the range, `remove_range(left, right)` stops tracking them, and `query_range(left, right)` asks whether every number in the range is tracked right now; the calls interleave in any order. After `add_range(10, 20)` and `remove_range(14, 16)` the module tracks `[10, 14)` and `[16, 20)`, so `query_range(10, 14)` is true, `query_range(13, 15)` is false because 14 is no longer tracked, and `query_range(16, 17)` is true.

The brute force keeps a set of every tracked number and visits each number of the range on every call, `O(right - left)` per call, hopeless when a range spans a billion values. The tracked numbers form blocks on the number line, and a block is fully described by its two ends, so store the blocks: a list of `[start, end)` pairs sorted by start, pairwise disjoint and never touching, because two blocks that touch are really one block. That last rule carries the design. Between any two stored blocks lies a gap of untracked numbers, so a range that is fully tracked sits inside a single block. A query needs only that block, the last one starting at or before `left`, and succeeds exactly when it reaches `right`. The upper-bound search of #14 finds the first block that starts after `left`, and the candidate is the block just before it; if there is none, no tracked number lies at or before `left`.

An add is Insert Interval (#65) with half-open ends. Copy the blocks that end before `left`, absorb every block that starts at or before `right` by stretching the new range to the smaller start and the larger end, then copy the rest. The tests are `end < left` and `start ≤ right`, so a block that merely touches the new range is absorbed too, as `[10, 14)` and `[16, 20)` are when `[14, 16)` is added back. A remove walks the blocks once: a block the range misses survives whole, a block it covers disappears, and a block it cuts keeps its piece left of `left`, its piece right of `right`, or both. A removal never creates touching blocks, because it leaves the gap `[left, right)` between its pieces.

```text
                 5    10   15   20   25   30
add(10, 20)           ├─────────┤             [10, 20)
remove(14, 16)        ├───┤ ├───┤             [10, 14) [16, 20)
add(14, 16)           ├─────────┤             touches both: [10, 20)
add(25, 30)           ├─────────┤    ├────┤   [10, 20) [25, 30)
add(5, 8)        ├──┤ ├─────────┤    ├────┤   [5, 8) [10, 20) [25, 30)

query(13, 15) on [10, 14) [16, 20): lo = 0, hi = 2
  mid = 1: start 16 > 13 → hi = 1
  mid = 0: start 10 ≤ 13 → lo = 1
  [10, 14) is the last block starting ≤ 13, but 14 < 15 → false
query(16, 17): mid = 1: start 16 ≤ 16 → lo = 2; [16, 20) reaches 17 → true
query(8, 10) on the last list: [5, 8) ends at 8 < 10 → false
```

```pseudo
CLASS RangeModule
    FUNCTION Init()
        self.intervals ← empty list     // sorted [start, end), gaps between

    FUNCTION AddRange(left, right)
        merged ← empty list
        i ← 0
        n ← len(self.intervals)
        WHILE i < n AND self.intervals[i][1] < left     // ends before: keep
            merged.append(self.intervals[i])
            i ← i + 1
        WHILE i < n AND self.intervals[i][0] ≤ right    // overlaps or touches
            left ← min(left, self.intervals[i][0])
            right ← max(right, self.intervals[i][1])
            i ← i + 1
        merged.append([left, right])
        WHILE i < n                                     // starts after: keep
            merged.append(self.intervals[i])
            i ← i + 1
        self.intervals ← merged

    FUNCTION RemoveRange(left, right)
        kept ← empty list
        FOR EACH [start, end] IN self.intervals
            IF end ≤ left OR start ≥ right
                kept.append([start, end])       // no overlap: untouched
            ELSE
                IF start < left
                    kept.append([start, left])  // the piece on the left
                IF end > right
                    kept.append([right, end])   // the piece on the right
        self.intervals ← kept

    FUNCTION QueryRange(left, right)
        lo ← 0
        hi ← len(self.intervals)
        WHILE lo < hi                   // first interval starting after left
            mid ← floor((lo + hi) / 2)
            IF self.intervals[mid][0] ≤ left
                lo ← mid + 1
            ELSE
                hi ← mid
        IF lo = 0
            RETURN false                // every interval starts after left
        RETURN self.intervals[lo - 1][1] ≥ right
```

Each update rebuilds the list in `O(n)` for `n` stored blocks and each query costs `O(log n)`; an add creates at most one block and a remove splits at most one, so `n` never exceeds the number of calls. Splicing a Python list shifts its tail anyway, so a binary search would not make the updates sublinear. Under heavy update traffic, a balanced search tree keyed by start (Java's `TreeMap`) finds the affected blocks in `O(log n)`, and since each block is deleted at most once after it is created, updates become amortized `O(log n)`; a segment tree (#107) extended with lazy range assignment is the other heavy-duty answer when the coordinates are known in advance. The signals are ranges added and removed over time, coverage questions on a huge number line, and free/busy or booking designs like #98. The classic mistake is letting touching blocks stay apart, for instance by testing `end ≤ left` in the first loop: adding `[14, 16)` back then copies `[10, 14)` as if it lay wholly before, the list becomes `[10, 14) [14, 20)`, and `query_range(12, 15)` fails although every number in it is tracked.

*Practice:* LC 715 Range Module · LC 57 Insert Interval · LC 352 Data Stream as Disjoint Intervals
