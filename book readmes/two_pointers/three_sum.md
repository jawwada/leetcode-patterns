# 3Sum
*LeetCode 15 · Medium · Pattern: Sort + fixed element + converging two pointers · Reading time ~8 min*

## The problem

Given an integer array nums, return all unique triplets [a, b, c] with a + b + c == 0; the result must not contain
duplicate triplets.

```text
Example: nums = [-1, 0, 1, 2, -1, -4] -> [[-1, -1, 2], [-1, 0,
  1]].
```

## What the problem is really asking

Given an unsorted integer array, list every distinct triplet of values `[a, b, c]`, taken from three different positions, with `a + b + c == 0`. "Distinct" is about values: `[-1, 0, 1]` and `[0, -1, 1]` are the same triplet and must appear once, even if the array contains several `-1`s that could produce it.

The answer is a list of value triplets, not indices. Two things make it hard: the search space is n^3 triples, and the duplicate rule means a naive search produces the same triplet many times.

```text
nums = [ -1 | 0 | 1 | 2 | -1 | -4 ]

  -1 + 0 + 1  = 0   (positions 0,1,2)
  -1 + 0 + 1  = 0   (positions 4,1,2)  same values!
  -1 + -1 + 2 = 0   (positions 0,4,3)

answer: [[-1, -1, 2], [-1, 0, 1]]
```

## Do it by hand first

Sort the numbers first; it is how anyone would start with pen and paper.

```text
 [ -4  -1  -1   0   1   2 ]
```

Now pick the first number as a commitment: "the triplet starts with -4". The other two must sum to 4. The largest pair available is `1 + 2 = 3`, so -4 is hopeless. Commit to -1 instead: the other two must sum to 1. That is Two Sum II on the rest, `[-1, 0, 1, 2]` with target 1, and you find `-1 + 2` and `0 + 1`. Commit to the second -1: but you just did "-1 first", so anything it finds is a repeat. Skip. Commit to 0: you need two numbers summing to 0 from `[1, 2]`; none.

What your hand tracked: one committed anchor, and a two-pointer search on what lies to its right. Also a rule: never commit to the same value twice in a row.

## The first honest attempt

Three nested loops over `i < j < k`, test the sum, and put the sorted triplet into a set to remove repeats. O(n^3) time.

There are two kinds of waste. First, once `i` and `j` are fixed, the needed third value is known exactly, `-(nums[i] + nums[j])`, yet a whole loop searches for it. Second, duplicate triplets are built over and over just to be thrown away by the set.

```text
fixed i, j  ->  need c = -(a + b)
k loop:     scans all k > j for c
            (a hash set finds it in O(1),
             a sorted suffix lets pointers
             find all (b, c) pairs in O(n))
```

A hash-set version is O(n^2), which is the right complexity, but deduplicating with a set of tuples is clumsy, and an interviewer will ask for the cleaner argument.

## The turning point

**Claim: after sorting, 3Sum is n separate copies of Two Sum II, and duplicates become adjacent, so skipping them is a comparison with a neighbour.**

Sorting buys two things at once.

1. **A two-pointer search for each anchor.** Fix `nums[i]`. On the sorted suffix to its right, put `L = i + 1` and `R = n - 1`. If `nums[i] + nums[L] + nums[R]` is negative, every pair using `nums[L]` with anything left of `R` is also negative, so `L += 1`. If positive, `R -= 1`. This is the Two Sum II row-and-column elimination with target `-nums[i]`.

2. **Local deduplication.** Equal values sit next to each other, so:
   - Skip anchor `i` if `nums[i] == nums[i - 1]`. Every triplet it could start was already found by the previous anchor, whose suffix is a superset of this one's.
   - After recording a hit, move **both** `L` and `R` inward, then keep moving `L` while it equals the value just used, and `R` likewise. A second triplet with the same anchor and the same `nums[L]` would need the same `nums[R]`, so it would be a repeat.

```text
anchor dedup compares with the PREVIOUS cell:

  [ -4 | -1 | -1 | 0 | 1 | 2 ]
          i=1  i=2
  i=1 runs (finds [-1,-1,2], which needs both -1s)
  i=2 skipped: nums[2] == nums[1]

comparing with the NEXT cell would skip i=1
and lose [-1, -1, 2]
```

One more early exit: if `nums[i] > 0`, every value to its right is also positive, so no later anchor can reach zero. Stop.

## Watch it work

`nums` sorted: `[-4, -1, -1, 0, 1, 2]` (indices 0 to 5).

Frame 1. Anchor `i = 0` (-4). `L = 1`, `R = 5`: `-4 - 1 + 2 = -3 < 0`, so `L` moves.

```text
  [ -4 | -1 | -1 |  0 |  1 |  2 ]
     i    L                   R
  sum -3 < 0 -> L += 1
```

Frame 2. Still `i = 0`. Sums are `-3`, `-2`, `-1` as `L` walks 2, 3, 4; all negative. `L` reaches `R`; no triplet starts with -4.

```text
  [ -4 | -1 | -1 |  0 |  1 |  2 ]
     i                       LR
  anchor -4 exhausted, 0 found
```

Frame 3. Anchor `i = 1` (-1). `L = 2`, `R = 5`: `-1 - 1 + 2 = 0`. Record `[-1, -1, 2]`. Move both: `L = 3`, `R = 4`; neither equals the value just used, so no skipping.

```text
  [ -4 | -1 | -1 |  0 |  1 |  2 ]
          i    L              R
  sum 0 -> record [-1,-1,2]
```

Frame 4. `L = 3`, `R = 4`: `-1 + 0 + 1 = 0`. Record `[-1, 0, 1]`. Move both; `L = 4 > R = 3`, done with this anchor.

```text
  [ -4 | -1 | -1 |  0 |  1 |  2 ]
          i         L    R
  sum 0 -> record [-1,0,1]
```

Frame 5. Anchor `i = 2` is -1 again: `nums[2] == nums[1]`, skip it entirely.

```text
  [ -4 | -1 | -1 |  0 |  1 |  2 ]
               i  (same as i=1: skip)
```

Frame 6. Anchor `i = 3` (0). `L = 4`, `R = 5`: `0 + 1 + 2 = 3 > 0`, `R` moves to 4 and meets `L`. The anchor loop ends (it stops at `n - 3`).

```text
  [ -4 | -1 | -1 |  0 |  1 |  2 ]
                    i    L    R
  sum 3 > 0 -> R -= 1, pointers meet
  result: [[-1,-1,2], [-1,0,1]]
```

Across all frames, each anchor ran an independent Two Sum II on its suffix, and no triplet was produced twice.

## Why it is correct

Completeness: take any zero-sum triplet of values `a <= b <= c` in the sorted array. Consider the **first** index `i` holding value `a`. That anchor is not skipped (the skip only fires on later copies). The suffix after `i` contains `b` and `c` at some positions, and Two Sum II's invariant guarantees the pointer walk does not discard any index belonging to a matching pair before finding a pair with these values. The clone-skipping after a hit only discards positions whose values equal ones just used, which would reproduce a triplet already recorded.

Uniqueness: two recorded triplets with the same anchor value would require the same anchor index (later copies are skipped). Within one anchor, after recording `(b, c)`, both pointers move past every copy of `b` and `c`, and since `b` determines `c`, no later pair can have the same `b`.

## Cost

- Time: O(n^2). Sorting is O(n log n); each of up to n anchors runs an O(n) pointer walk.
- Space: O(1) extra beyond the output (Python's sort uses O(n) internally).

Brute force with a set: O(n^3). Hash-set per anchor: O(n^2) time but O(n) space and messier dedup.

## Variations you will meet

- **3Sum Closest (LeetCode 16)**: no dedup needed; track the sum with the smallest `|sum - target|` and move pointers by the sign of `sum - target`.
- **4Sum (LeetCode 18)**: two nested anchors, each with its own `nums[x] == nums[x - 1]` skip, then the pointer walk. O(n^3). In general kSum is k - 2 nested loops around Two Sum II.
- **3Sum Smaller (LeetCode 259)**: count triplets with sum below target. When the sum is too small, all `R - L` pairs with this `L` count at once; add them and move `L`.
- **Count triplets with duplicates allowed (3Sum With Multiplicity, LeetCode 923)**: dedup is replaced by combinatorics on value counts.

## What to carry forward

Reduce the dimension: fix one element and the rest is the previous problem; sorting both enables the pointer walk and turns deduplication into "compare with your neighbour". The next problem keeps the converging walk but has no sorted order at all; the monotone fact that justifies each move comes from geometry instead.
