# Find Minimum in Rotated Sorted Array

*LeetCode 153 · Medium · Pattern: Binary search on a rotated sorted array · Reading time ~7 min*

## What the problem is really asking

Someone took a sorted array of distinct numbers, cut it at an unknown point, and swapped the two pieces. `[0,1,2,4,5,6,7]`
might become `[4,5,6,7,0,1,2]`. Return the smallest value, in O(log n).

The smallest value is the first element of the piece that used to be in front. So the real question is: **where is the
cut?** The answer is one value, but finding it means finding one index, the seam.

```text
value
  7 |          *
  6 |       *
  5 |    *
  4 | *
  2 |                   *
  1 |                *
  0 |             *
    +-----------------------
      0  1  2  3  4  5  6   idx
      high ramp    low ramp
                 ^ seam: the minimum
```

Two rising ramps, with a cliff between them. Every value on the high ramp is larger than every value on the low ramp.
That is what makes this tractable: the array is not sorted, but it is two sorted runs in a known relationship.

## Do it by hand first

Look at `[4, 5, 6, 7, 0, 1, 2]` and point at the minimum. Your eye scanned for the place where the numbers *drop*. A
drop happens exactly once (or never, if the rotation put everything back in order).

Now do it with a blindfold, allowed to ask for one value at a time. Ask for the last value: 2. Any value bigger than 2
must be on the high ramp, because the low ramp ends at 2 and only climbs to get there. Any value at most 2 is on the low
ramp. So "is this value bigger than the last one?" tells you which ramp you are standing on:

```text
nums           4   5   6   7   0   1   2
> last (2)?    T   T   T   T   F   F   F
               high ramp       low ramp
                               ^ first F = minimum
```

A T...T F...F row again. Your hand kept track of one comparison partner, the right end, and the border between "high
ramp" and "low ramp".

## The first honest attempt

Scan for the smallest value, or scan for the drop `nums[i] > nums[i+1]`. Both are O(n).

The repeated work: once you see that `nums[3] = 7` is bigger than the last element, you know indices 0..3 are all on the
high ramp. The scan visits them one by one anyway.

```text
scan:  4 -> 5 -> 6 -> 7 -> 0
       each step re-confirms "still on the high ramp",
       a fact that one look at index 3 already proved for 0..3
```

## The turning point

**Claim: comparing `nums[mid]` with `nums[hi]` tells you whether the minimum is strictly right of mid, or at mid or to
its left.**

- `nums[mid] > nums[hi]`: mid is on the high ramp, the cliff is somewhere between mid and hi. The minimum is strictly
  right of mid: `lo = mid + 1`.
- `nums[mid] <= nums[hi]`: mid is on the low ramp (or the window is one clean ramp). The minimum is at mid or to its
  left. Mid itself may be the minimum, so keep it: `hi = mid`.

This is the half-open style from the background: `while lo < hi`, `lo = mid + 1` on T, `hi = mid` on F. Here hi starts at
`n - 1` rather than n, because the minimum always exists inside the array; there is no "past the end" answer.

Why compare with `nums[hi]` and not the last element of the whole array? You can, and the row of T's and F's is the same.
But note what `hi` is: it only ever moves to a mid that was on the low ramp, so `nums[hi]` is always a low-ramp value,
and "bigger than `nums[hi]`" still means "on the high ramp". Comparing with the moving `hi` keeps the code self-contained.

Why not compare with `nums[lo]`? Because `nums[mid] > nums[lo]` is true in two very different situations: mid is on the
high ramp with lo, or the whole window is already sorted and the minimum is at lo. The left end cannot tell these apart.
The right end can: if the window is sorted, `nums[mid] <= nums[hi]` and you correctly move left.

```text
window [4,5,6,7,0,1,2]  mid=7:  7 > 4  -> min is right
window [0,1,2]          mid=1:  1 > 0  -> min is LEFT
same comparison with lo, opposite answers
```

## Watch it work

`nums = [4, 5, 6, 7, 0, 1, 2]`. P is "nums[i] > nums[6] = 2", the ramp label. The code compares with `nums[hi]`, which
gives the same verdict for every mid in the window.

```text
Frame 1: lo=0 hi=6 mid=3
idx      0   1   2   3   4   5   6
nums     4   5   6   7   0   1   2
P        T   T   T   T   F   F   F
         L           M           H
nums[mid]=7 vs nums[hi]=2
```

7 > 2: mid is on the high ramp, so the minimum is in 4..6 and `lo = 4`.

```text
Frame 2: lo=4 hi=6 mid=5
idx      0   1   2   3   4   5   6
nums     4   5   6   7   0   1   2
P        T   T   T   T   F   F   F
                         L   M   H
nums[mid]=1 vs nums[hi]=2
```

1 <= 2: mid is on the low ramp. The minimum is at index 5 or before it, so `hi = 5`.

```text
Frame 3: lo=4 hi=5 mid=4
idx      0   1   2   3   4   5   6
nums     4   5   6   7   0   1   2
P        T   T   T   T   F   F   F
                       L/M   H
nums[mid]=0 vs nums[hi]=1
```

The comparison partner moved to `nums[5] = 1`, still a low-ramp value. 0 <= 1, so `hi = 4`.

```text
Frame 4: lo=4 hi=4
idx      0   1   2   3   4   5   6
nums     4   5   6   7   0   1   2
P        T   T   T   T   F   F   F
                       L/H
```

The window has one cell. Return `nums[4] = 0`.

In every frame, every index left of `lo` was a high-ramp T, `hi` sat on a low-ramp F, and the seam lay in `[lo, hi]`.

## Why it is correct

Label each index T if it is on the high ramp and F if on the low ramp. Rotation guarantees all T's come first, and the
minimum is the first F (if the array was not rotated at all, there are no T's and the first F is index 0). The invariant
is "the first F lies in `[lo, hi]`, and `nums[hi]` is an F value". It holds initially: the last element is always on the
low ramp. If `nums[mid] > nums[hi]`, mid is T, so the first F is beyond mid. Otherwise mid is F, so the first F is at or
before mid, and setting `hi = mid` keeps hi on an F. The window strictly shrinks because `lo <= mid < hi`. At `lo == hi`
the single remaining cell is the first F: the minimum.

## Cost

Time O(log n): one halving search. Space O(1).

## Variations you will meet

- **Duplicates allowed (LeetCode 154).** When `nums[mid] == nums[hi]` you cannot tell which ramp mid is on (`[1,1,1,0,1]`
  vs `[1,0,1,1,1]`). Shrink by one, `hi -= 1`, which is safe because the value at hi still exists at mid. The worst case
  degrades to O(n), and no algorithm can do better on all-equal-but-one inputs.
- **How many times was it rotated?** The index of the minimum is the rotation count.
- **Search for a target in the rotated array.** Either find the seam first and then binary search the correct ramp, or do
  it in one pass by checking which half is sorted. That is the next problem.

## What to carry forward

A rotated array is two sorted runs, and "bigger than the right end?" labels each cell's run with T...TF...F; the seam is
the first F. The next problem searches for a target instead of the seam, and asks a different question at each mid: which
half is the clean ramp?
