---
rank: 147
slug: count_min_sketch
---

A Count-Min sketch counts the items of a stream approximately, in fixed memory. `add(item, count)` records occurrences and `estimate(item)` returns a count that is never too small and rarely much too large; a size-k heap beside it tracks the k most frequent items, the heavy hitters. With 3 rows of 5 counters, the stream `cat dog cat fish cat dog bird cat dog` gives the estimates 4, 3, 1 and 2, although `bird` came once, and the top two are `cat` and `dog`.

Exact counting needs a hash map entry per distinct item, and a stream of search queries or IP addresses has billions. The sketch is a grid of d rows by w counters, each row with its own hash function: `add` bumps the item's counter in every row, and `estimate` returns the smallest of its d counters. A counter holds the item's count plus the counts of everything that collided with it in that row, never less, so the minimum keeps the least polluted one. A single clean row gives the exact answer; only an item that collides in every row, like `bird`, comes out too large.

Row r reads the item as a number x with a base-31 polynomial hash and sends it to column `((a·x + b) mod p) mod w`, with a and b drawn for that row from a seeded generator, a universal hash family. Two items then share a counter with probability about `1 / w`, so a row overcounts by at most `N / w` on average over a stream of N items, and by more than `e·N / w` with probability at most `1 / e`; the rows are independent, so all d overshoot together with probability at most `e^(-d)`.

The sketch cannot list what it has seen, so the heavy hitters live in the size-k min-heap of Top-K (#19) beside it: a newcomer is pushed with its estimate, and at k + 1 entries the weakest leaves. A leader's count grows while its heap entry stays behind, so entries go stale; a stale entry popped from the top goes back with its current count, and the first fresh entry popped is the true weakest. A dropped item keeps its count in the sketch, so `dog` returns with all of it.

```text
width 5, depth 3, seed 6; stream cat dog cat fish cat dog bird cat dog
columns in rows 0, 1, 2:  cat 1 0 3   dog 1 1 4   fish 4 2 2   bird 4 2 3
         col 0   col 1   col 2   col 3   col 4
row 0      0       7       0       0       2      cat 4 + dog 3 share col 1
row 1      4       3       2       0       0      fish 1 + bird 1 share col 2
row 2      0       0       1       5       3      cat 4 + bird 1 share col 3
estimate(cat)  = min(7, 4, 5) = 4     exact: row 1 is clean
estimate(fish) = min(2, 2, 1) = 1     exact: row 2 is clean
estimate(bird) = min(2, 2, 5) = 2     true 1: a collision in every row

item   est   heap of k = 2, smallest first   what happened
cat     1    (1 cat)
dog     1    (1 cat) (1 dog)
cat     2    (1 cat) (1 dog)                 the entry (1 cat) is now stale
fish    1    (1 fish) (2 cat)                (1 cat) back as (2 cat); drop dog
cat     3    (1 fish) (2 cat)
dog     2    (2 cat) (2 dog)                 dog returns with 2; drop fish
bird    2    (2 cat) (2 dog)                 (2 bird) is the weakest: drop it
cat     4    (2 cat) (2 dog)
dog     3    (2 cat) (2 dog)                 top() = [(4, 'cat'), (3, 'dog')]
```

```pseudo
MOD ← 1000000007                        // a large prime

FUNCTION StringHash(word)
    h ← 0
    FOR EACH ch IN word
        h ← (h * 31 + code(ch)) mod MOD
    RETURN h

CLASS CountMinSketch
    FUNCTION Init(width, depth, seed)
        self.width ← width
        self.depth ← depth
        self.table ← empty list         // depth rows of width counters
        self.a ← empty list             // row r sends x to column
        self.b ← empty list             // ((a[r]·x + b[r]) mod MOD) mod width
        rng ← RandomGenerator(seed)     // the same seed, the same hashes
        FOR row FROM 0 TO depth - 1
            self.table.append(array of width zeros)
            self.a.append(rng.RandomInt(1, MOD - 1))
            self.b.append(rng.RandomInt(0, MOD - 1))

    FUNCTION Columns(item)
        x ← StringHash(item)
        result ← empty list
        FOR row FROM 0 TO self.depth - 1
            h ← (self.a[row] * x + self.b[row]) mod MOD
            result.append(h mod self.width)
        RETURN result

    FUNCTION Add(item, count)
        cols ← self.Columns(item)
        FOR row FROM 0 TO self.depth - 1
            self.table[row][cols[row]] ← self.table[row][cols[row]] + count

    FUNCTION Estimate(item)
        cols ← self.Columns(item)
        best ← self.table[0][cols[0]]
        FOR row FROM 1 TO self.depth - 1
            best ← min(best, self.table[row][cols[row]])
        RETURN best                     // collisions only ever add

CLASS HeavyHitters
    FUNCTION Init(k, width, depth, seed)
        self.k ← k
        self.sketch ← CountMinSketch(width, depth, seed)
        self.counts ← empty map         // leader → estimate when last seen
        self.heap ← empty min-heap      // (estimate, leader), one per leader

    FUNCTION Add(item)
        self.sketch.Add(item, 1)
        estimate ← self.sketch.Estimate(item)
        IF item IN self.counts
            self.counts[item] ← estimate  // its heap entry is now stale
            RETURN
        self.counts[item] ← estimate
        self.heap.push((estimate, item))
        IF len(self.heap) > self.k      // one too many: drop the weakest
            (estimate, weakest) ← self.heap.pop()
            WHILE estimate ≠ self.counts[weakest]  // stale: it grew since
                self.heap.push((self.counts[weakest], weakest))
                (estimate, weakest) ← self.heap.pop()
            self.counts.remove(weakest)

    FUNCTION Top()
        pairs ← empty list
        FOR EACH item IN self.counts
            pairs.append((self.counts[item], item))
        pairs.sort()
        RETURN reverse(pairs)           // largest estimate first
```

Each `add` costs `O(L + d)` for an item of length L, plus `O(log k)` amortized for the heap, since each re-push repairs one earlier update. The memory is `d × w` counters and k leaders, whatever the number of distinct items: in the demo 800 counters find the three heavy words among 3003, and w = 2719 with d = 5 keeps each estimate within 0.1 percent of N with 99 percent probability. Sketches built from the same seed merge by adding their grids cell by cell, so each server counts its own traffic and a collector sums the grids. The signals are counts over a stream too big to store and trending top-k lists; counts that fit in memory deserve the exact heap of #19 or buckets of #61. The classic mistake is one hash for every row: the rows become copies, a collision repeats in all of them, and the minimum is no better than one row.

*Practice:* LC 347 Top K Frequent Elements · LC 692 Top K Frequent Words · LC 1636 Sort Array by Increasing Frequency
