---
rank: 4
slug: longest_consecutive_sequence
---

Given an unsorted array of integers, return the length of the longest run of consecutive values, values that climb by exactly 1 from one to the next, wherever they sit in the array. In `[100, 4, 200, 1, 3, 2]` the answer is `4`, the run `1, 2, 3, 4`.

Sorting lines the runs up, and one scan that counts steps of exactly 1 and skips repeats finds the longest, `O(n log n)` in all. The linear solution throws the order away and keeps only membership. Put every value in a hash set; then any value can ask in `O(1)` whether its neighbor is present, and a run can be traced by stepping up one value at a time. Stepping up from every value would retrace the same run over and over, `n + (n - 1) + ... + 1` steps on `1, 2, ..., n`, which is `O(n²)`. The fix is to walk only from the start of a run, a value `num` whose left neighbor `num - 1` is missing. Every other value sits inside a run whose start will count it.

Picture the values as dots on a number line. Each dot looks once at the spot to its left. A dot with an empty spot on its left is the bottom of a run, and only that dot walks right, step by step, until the next spot is empty. Each value is therefore visited at most twice, once when the loop tests it as a possible start and once when the walk from its run's start steps onto it, so the work stays linear however the runs are laid out. Duplicates collapse in the set, and negative values need nothing special, since `num - 1` and `num + 1` behave the same below zero.

```text
number line   ●──●──●──●   …   ●   …   ●
              1  2  3  4      100     200
start?        ✓  ✗  ✗  ✗       ✓       ✓      ✓ when num - 1 is not in the set

the loop visits the set in its own order
  num   num - 1 in set?   action                  length   best
    1         no          walk 1 → 2 → 3 → 4        4        4
    2         yes         skip                               4
    3         yes         skip                               4
  100         no          walk 100                  1        4
    4         yes         skip                               4
  200         no          walk 200                  1        4
12 lookups in all: two per distinct value
```

```pseudo
FUNCTION LongestConsecutive(nums)
    values ← set(nums)                     // O(1) lookups; duplicates collapse
    best ← 0
    FOR EACH num IN values                 // the set, so each start walks once
        IF num - 1 IN values
            CONTINUE                       // inside a run: its start counts it
        length ← 1
        WHILE num + length IN values
            length ← length + 1            // one more step up the run
        best ← max(best, length)
    RETURN best
```

Building the set and visiting each value at most twice give `O(n)` time, and the set takes `O(n)` space. Reach for this pattern when a problem asks for consecutive values rather than consecutive positions and wants to beat a sort: the set turns "is my neighbor here?" into one lookup, and the start test makes each run be counted exactly once. Union-Find (#41) solves the same problem by joining each `x` with `x + 1`, with more machinery and no gain. The classic mistake is looping over `nums` instead of the set. Every copy of a start then walks its whole run again, so 5,000 copies of `1` in front of the run `1, 2, ..., 5000` cost about 25 million steps instead of 5,000.

*Practice:* LC 128 Longest Consecutive Sequence · LC 298 Binary Tree Longest Consecutive Sequence · LC 2501 Longest Square Streak in an Array
