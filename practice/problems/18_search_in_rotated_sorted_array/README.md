# Search in Rotated Sorted Array (LeetCode 33)

**Area:** binary search · **Difficulty:** Medium · **Key operations:** compute mid, decide which half is sorted, test target against the sorted half, move lo or hi

## Problem

An array of distinct integers was sorted ascending and then rotated at an unknown pivot (`[0,1,2,4,5,6,7]` may become `[4,5,6,7,0,1,2]`). Given the rotated array and a `target`, return the index of `target`, or -1 if it is not present. The algorithm must run in O(log n).

## Example

```
nums   = [4, 5, 6, 7, 0, 1, 2]
target = 0
answer = 4
```

`target = 3` gives -1.

## Brute force

Scan the array from left to right and return the first index holding `target`.

O(n) time, O(1) space. The wasted work: at every probe we are standing inside one of two sorted runs and could discard an entire half, but a scan discards one element at a time.

## From brute force to optimal

A rotated sorted array is two ascending runs with one "cliff" between them. Pick any `mid`. The cliff falls in only one of the halves `[lo..mid]` or `[mid..hi]`, so the *other* half is a plain sorted array whose minimum and maximum are its endpoints.

That gives an O(1) test. If `nums[lo] <= nums[mid]`, the left half is sorted; the target is in it exactly when `nums[lo] <= target < nums[mid]`. Otherwise the right half is sorted; the target is in it exactly when `nums[mid] < target <= nums[hi]`. Either way we know which half to keep and discard the other, so the range halves on every step without ever locating the pivot.

## Intuition

Picture two rising ramps with a cliff between them. Whatever `mid` you land on, one of the two halves is a clean ramp, and a clean ramp is described by its two ends. Ask "does the target's height fit on this ramp?" If yes, the target is there. If no, it must be on the messy side, cliff and all. You always interrogate the clean half, because only there can membership be decided from the endpoints alone.

## Walkthrough

`nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`. The carets mark `lo`, `mid`, `hi`.

```
   4   5   6   7   0   1   2
   ^           ^           ^      lo=0 mid=3 hi=6
nums[3] = 7 != 0
nums[lo]=4 <= nums[mid]=7      -> left half [4..7] is sorted
4 <= 0 < 7 ?  no               -> target is in the right half: lo = 4

   4   5   6   7   0   1   2
                   ^   ^   ^      lo=4 mid=5 hi=6
nums[5] = 1 != 0
nums[lo]=0 <= nums[mid]=1      -> left half [0..1] is sorted
0 <= 0 < 1 ?  yes              -> hi = mid - 1 = 4

   4   5   6   7   0   1   2
                   ^              lo=4 mid=4 hi=4
nums[4] = 0 == target          -> return 4
```

For `target = 3`: first step as above, `lo = 4`; then left half `[0..1]` sorted, 3 not in it, `lo = 6`; then `nums[6] = 2`, one-element sorted half, 3 not in `[2..2)`, `lo = 7 > hi` → -1.

## Steps

1. `lo = 0`, `hi = n - 1`. While `lo <= hi`:
2. `mid = (lo + hi) // 2`. If `nums[mid] == target`, return `mid`.
3. If `nums[lo] <= nums[mid]` (left half sorted): if `nums[lo] <= target < nums[mid]` then `hi = mid - 1`, else `lo = mid + 1`.
4. Else (right half sorted): if `nums[mid] < target <= nums[hi]` then `lo = mid + 1`, else `hi = mid - 1`.
5. Return -1.

## Complexity

O(log n) time: an ordinary binary search with an O(1) test per step. O(1) space.

## Pitfalls

- **`<` instead of `<=` when testing which half is sorted.** With two elements `mid == lo`, so `nums[lo] < nums[mid]` is false and the one-element left half is misjudged as unsorted; `[3, 1]` with target 1 returns -1.
- **Excluding the left endpoint.** `nums[lo] < target` sends a target equal to `nums[lo]` to the wrong half; target 4 in the example returns -1.
- **Excluding the right endpoint.** `target < nums[hi]` sends a target equal to `nums[hi]` the wrong way; `[5, 1, 3]` with target 3 returns -1.
- **Testing the unsorted half.** The membership test is only valid on the sorted half; on the half with the cliff the endpoints say nothing about what lies between.
- **Duplicates.** This reasoning needs distinct values; with duplicates `nums[lo] == nums[mid]` is ambiguous (LeetCode 81 handles that by shrinking one step).
