---
rank: 106
slug: random_pick_with_weight
---

Given an array of positive weights, design `pick_index()`, which returns index `i` with probability `w[i] / total`, where `total` is the sum of the weights. With `w = [1, 3, 2]` the total is `6`, so index `0` should come up one time in six, index `1` three times in six and index `2` two times in six.

The brute force fills a bag with `w[i]` copies of every index and draws a uniform slot from it, which costs memory proportional to the total weight, hopeless when a single weight is a billion. The bag never needs to exist. Lay the weights end to end on a number line from `1` to `total`, so that index `i` owns a segment of exactly `w[i]` consecutive integers: index `0` owns `1`, index `1` owns `2` to `4`, index `2` owns `5` and `6`. The prefix sums `[1, 4, 6]` are the right ends of the segments, and because every weight is positive they strictly increase. A pick draws an integer target uniformly from `1` to `total` and asks which segment contains it, which is the first index whose prefix sum is at least the target. That question is the lower bound of #14 asked of the prefix sums, so building costs one pass and every pick costs one binary search.

The probability argument is a count. Each of the `total` targets is drawn with chance `1 / total`, and index `i` owns `w[i]` of them, so it is returned with chance `w[i] / total`, exactly as asked. The draw and the comparison must agree on where a segment ends: with targets `1` to `total` and the test `prefix[i] ≥ target`, the target equal to `prefix[i]` is the last one index `i` owns.

```text
w = [1, 3, 2]     prefix = [1, 4, 6]     total = 6
target      1 │  2   3   4 │  5   6     RandomInt(1, 6): each has chance 1/6
owner       0 │  1   1   1 │  2   2     index i owns w[i] targets in a row
chance    1/6 │     3/6    │   2/6      prefix[i] is the last target i owns

LowerBound(5): the first i with prefix[i] ≥ 5
   lo   hi   mid   prefix[mid]   < 5?   move
    0    3    1        4         yes    lo ← 2     segments 0 and 1 end below 5
    2    3    2        6         no     hi ← 2     segment 2 reaches 5: keep it
    2    2   window empty: return 2

60000 picks after random.seed(7):   0 → 9986    1 → 30002    2 → 20012
expected 60000 × w[i] / 6:             10000        30000        20000
```

```pseudo
CLASS WeightedPicker
    FUNCTION Init(w)
        self.prefix ← empty list              // prefix[i] = w[0] + … + w[i]
        running ← 0
        FOR EACH weight IN w
            running ← running + weight
            self.prefix.append(running)
        self.total ← running

    FUNCTION LowerBound(target)               // first i with prefix[i] ≥ target
        lo ← 0
        hi ← len(self.prefix)                 // half-open [lo, hi)
        WHILE lo < hi
            mid ← floor((lo + hi) / 2)
            IF self.prefix[mid] < target
                lo ← mid + 1                  // mid's whole range lies below
            ELSE
                hi ← mid                      // mid's range reaches target
        RETURN lo

    FUNCTION PickIndex()
        target ← RandomInt(1, self.total)     // uniform over 1..total
        RETURN self.LowerBound(target)
```

Building the prefix sums costs `O(n)` time and space, and each pick costs `O(log n)` for the binary search. Reach for it whenever items must be chosen in proportion to a weight, a count or a capacity: Random Point in Non-overlapping Rectangles weights each rectangle by the number of integer points it holds and then picks a point inside the chosen one uniformly, and Random Pick with Blacklist draws a uniform rank among the allowed numbers and finds the number with that rank, again by binary search. With real-valued weights, draw `random() × total` and search for the first prefix sum strictly greater than it. When the weights change between picks, a Fenwick tree or the segment tree of #107 keeps the prefix sums current in `O(log n)` per update; when they arrive as a stream, the weighted reservoir of #131 picks in one pass without storing them. The classic mistake is a draw that disagrees with the comparison: `RandomInt(0, total - 1)` with the test `≥` hands index `0` the extra target `0` and takes target `6` away from index `2`, so `[1, 3, 2]` comes out as `2/6`, `3/6`, `1/6`, which the frequency check in the Python book catches.

*Practice:* LC 528 Random Pick with Weight · LC 497 Random Point in Non-overlapping Rectangles · LC 710 Random Pick with Blacklist
