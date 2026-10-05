# Search in Rotated Sorted Array

*LeetCode 33 · Medium · Pattern: Binary search on a rotated sorted array · Reading time ~7 min*

## The problem

A sorted array of distinct integers was rotated at an unknown pivot. Return the index of target, or -1, in O(log n).

```text
Example: nums = [4,5,6,7,0,1,2], target = 0 returns 4; target =
  3 returns -1.
```

## What the problem is really asking

The same rotated array as the previous problem: a sorted list of distinct values, cut at an unknown point with the two
pieces swapped. Now find a given target and return its index, or -1. In O(log n).

```text
idx      0   1   2   3   4   5   6   7   8
nums     6   7   8   0   1   2   3   4   5
         high run   |  low run
target 2 -> 5      target 9 -> -1
```

The answer is an index. The difficulty: plain binary search compares the target with `nums[mid]` and assumes "smaller
means left". In a rotated array that is false. Target 2 is smaller than `nums[0] = 6` and yet it is far to the right.

## Do it by hand first

Look for 2 by hand. You probably notice two runs: 6, 7, 8 and then 0 to 5. You ask "which run could hold a 2?" The high
run spans 6..8, so no. The low run spans 0..5, so yes. Then you search inside the low run as normal.

The key move your hand made was to describe a sorted run by its two endpoints. A sorted stretch from value a to value b
contains the target only if `a <= target <= b`, and you know that from two lookups, without reading the middle.

That suggests a two-pass algorithm: find the seam with the previous problem, then binary search whichever run the target's
value fits. It works and is O(log n). But there is a one-pass version that never looks for the seam, and the idea behind
it shows up again in harder problems.

## The first honest attempt

Linear scan for the target: O(n).

The waste: at each probe you have enough information to throw away a whole half, but a scan throws away one cell.

```text
scan for 2:  6  7  8  0  1  2
             x  x  x  x  x  ^
after seeing 6 at idx 0 and 5 at idx 8 you already know
idx 0..2 (values 6..8) cannot hold 2. The scan checks them.
```

## The turning point

**Claim: whatever mid you pick, at least one of the halves `[lo, mid]` and `[mid, hi]` is a clean sorted ramp, and you can
tell which with one comparison.**

The cliff, if it lies inside the window at all, is in exactly one half. The other half has no cliff, so it is sorted, and
its smallest value is its left end and its largest is its right end.

```text
cliff in the left half:          cliff in the right half:
 lo        mid        hi          lo        mid        hi
  8  0  1   2  3  4  5             3  4  5   6  7  0  1
  [ messy ] [ clean  ]             [ clean ] [ messy  ]
  nums[lo] > nums[mid]             nums[lo] <= nums[mid]
```

So at every probe:

1. If `nums[mid] == target`, done.
2. If `nums[lo] <= nums[mid]`, the left half is the clean ramp. If `nums[lo] <= target < nums[mid]`, the target is in it:
   `hi = mid - 1`. Otherwise it can only be in the right half: `lo = mid + 1`.
3. Else the right half is the clean ramp. If `nums[mid] < target <= nums[hi]`, go right: `lo = mid + 1`. Otherwise go left:
   `hi = mid - 1`.

Why always test the *clean* half? Because only for a sorted stretch can you decide membership from the endpoints. The
messy half contains a cliff, so its endpoints say nothing about what is between them. If the target is not in the clean
half, it must be in the messy one, by elimination.

The `<=` in `nums[lo] <= nums[mid]` matters when the left half is a single cell (lo == mid). That cell is trivially
sorted, and with a strict `<` you would wrongly treat the right half as the sorted one. On `[3, 1]` searching for 1, the
strict version goes left and returns -1.

There is a monotone predicate hiding here too. For a target that exists at position p, the question "is the target right
of index i?" is T for i < p and F from p on. You never evaluate it directly; the sorted-half test is a way to compute it at
mid using only endpoints.

## Watch it work

`nums = [6, 7, 8, 0, 1, 2, 3, 4, 5]`, target 2 (at index 5). Row `run` marks the high (H) and low (L) runs. Row P is
"target is right of i", the hidden predicate the search effectively evaluates at each mid.

```text
Frame 1: lo=0 hi=8 mid=4 nums[mid]=1
idx      0   1   2   3   4   5   6   7   8
nums     6   7   8   0   1   2   3   4   5
run      H   H   H   L   L   L   L   L   L
P        T   T   T   T   T   F   F   F   F
         L               M               H
```

`nums[0] = 6 > 1`, so the left half has the cliff and `[1, 2, 3, 4, 5]` on the right is clean. 2 fits in (1, 5], so the
target is right of mid: `lo = 5`.

```text
Frame 2: lo=5 hi=8 mid=6 nums[mid]=3
idx      0   1   2   3   4   5   6   7   8
nums     6   7   8   0   1   2   3   4   5
run      H   H   H   L   L   L   L   L   L
P        T   T   T   T   T   F   F   F   F
                             L   M       H
```

`nums[5] = 2 <= 3`: the left half `[2, 3]` is clean. 2 fits in [2, 3), so `hi = 5`.

```text
Frame 3: lo=5 hi=5 mid=5 nums[mid]=2
idx      0   1   2   3   4   5   6   7   8
nums     6   7   8   0   1   2   3   4   5
run      H   H   H   L   L   L   L   L   L
P        T   T   T   T   T   F   F   F   F
                         L/M/H
```

`nums[5] == 2`. Return 5.

In each frame exactly one half was clean, and the target-membership test on that half gave the same verdict as the hidden
row P. The window never lost the target. The search never located the seam at index 3; it did not need to.

## Why it is correct

Invariant: if the target exists, its index is in `[lo, hi]`. At each step the window `[lo, hi]` is a contiguous piece of
a rotated sorted array, so it contains at most one cliff, and one of `[lo, mid]`, `[mid, hi]` is sorted. The test
`nums[lo] <= nums[mid]` identifies a sorted left half correctly: with distinct values, a left half containing the cliff
would have `nums[lo] > nums[mid]`. For a sorted half, `endpoint_low <= target <= endpoint_high` is exactly membership.
If the target is in the sorted half we keep that half; if not, it is either absent or in the other half. Either way the
invariant survives, and the window strictly shrinks because both updates step past mid.

## Cost

Time O(log n): one closed-window binary search with O(1) extra work per probe. Space O(1).

The two-pass version (find the seam, then search one run) is also O(log n), about twice the probes.

## Variations you will meet

- **Duplicates allowed (LeetCode 81).** With `nums[lo] == nums[mid] == nums[hi]` you cannot tell which half is clean
  (`[1, 1, 1, 3, 1]`). Shrink both ends by one and continue. Worst case O(n).
- **Two-pass via the seam.** Find the minimum's index s with the previous problem; then search `[0, s-1]` if
  `target >= nums[0]`, else `[s, n-1]`. Easier to get right under pressure, same complexity.
- **Return a boolean only.** Same algorithm.
- **Rotated with a known rotation count k.** Map a virtual sorted index i to the real index `(i + k) % n` and run ordinary
  binary search, the same virtual-index trick as the 2D matrix.

## What to carry forward

At every mid, one half is a clean ramp you can judge from its two endpoints; test that half and fall back to the other by
elimination. The next problem drops the target altogether: it asks only which way is uphill, and the predicate becomes a
slope sign.
