# Search Insert Position

*LeetCode 35 · Easy · Pattern: Binary search for a boundary (lower / upper bound) · Reading time ~5 min*

## The problem

Given a sorted array of distinct integers and a target, return the index of target if present, otherwise the index
where it would be inserted to keep the array sorted, in O(log n).

```text
Example: nums = [1,3,5,6], target = 5 -> 2; target = 2 -> 1;
  target = 7 -> 4.
```

## What the problem is really asking

Sorted distinct integers and a target. If the target is present, return its index. If not, return the index where it
would have to be inserted to keep the array sorted. In O(log n).

That sounds like two questions, but it is one: **the first index whose value is at least the target.** If the target is
present, that index holds it. If it is absent, that index holds the first larger value, which is exactly the slot the
target would push to the right. And if everything is smaller, the answer is n, one past the end.

```text
idx      0   1   2   3   4   5   6  | 7
nums     1   3   5   6   8  10  12  | (end)
target 5  -> 2   (found)
target 7  -> 4   (7 would go before 8)
target 13 -> 7   (past the end)
```

The answer is always an index in `0..n`. That last option, n, is the trap.

## Do it by hand first

Target 7. You glance at the list and your eye goes to "where do the numbers stop being smaller than 7?" 1, 3, 5, 6 are
smaller; 8 is not. The answer is the position of 8.

Your hand did not look for 7. It looked for a *border* between "too small" and "big enough".

```text
nums     1   3   5   6 | 8  10  12
         too small     | big enough
                       ^ insert here, index 4
```

Keep that word. Almost every later problem in this chapter is a border search over some yes/no question.

## The first honest attempt

Scan from the left and return the first index whose value is at least the target; return n if none is. O(n).

The repeated work is the same as in the previous problem. After seeing `nums[3] = 6 < 7`, you already know indices 0, 1,
2 are smaller too; the scan checked them anyway. And on the right side, as soon as you see one value at least 7 you know
all values after it are also at least 7.

## The turning point

**Claim: "is nums[i] smaller than target?" is T on a prefix and F on the suffix, and the answer is the first F.**

The previous problem stopped as soon as it hit an equal value. Here an equal value is not special: it is just the first F
when it exists. So drop the equality check and search for the border directly. Each probe answers "which side of the
border is mid on?":

- `nums[mid] >= target` (F): mid is a candidate. Remember it, `ans = mid`, and look left for an earlier F with
  `hi = mid - 1`.
- `nums[mid] < target` (T): mid and everything left of it is too small. `lo = mid + 1`.

The solution keeps the closed window `[lo, hi]` from the previous problem and adds a variable `ans`, initialised to n. If
no probe ever sees an F, `ans` stays n: insert at the end. The F's we record only get further left, because every later
probe is inside a window that lies left of the last recorded F.

When the loop ends, `lo` itself equals `ans`, so the half-open template from the background chapter (`hi = n`,
`hi = mid` on F) needs no `ans` at all. Either form works.

## Watch it work

`nums = [1, 3, 5, 6, 8, 10, 12]`, target 7. P is "nums[i] < 7". The border is between index 3 and 4.

```text
Frame 1: lo=0 hi=6 mid=3 ans=7
idx      0   1   2   3   4   5   6
nums     1   3   5   6   8  10  12
P        T   T   T   T   F   F   F
         L           M           H
```

6 is too small (T), so indices 0..3 are dead: `lo = 4`. `ans` is still 7, meaning "end of array".

```text
Frame 2: lo=4 hi=6 mid=5 ans=7
idx      0   1   2   3   4   5   6
nums     1   3   5   6   8  10  12
P        T   T   T   T   F   F   F
                         L   M   H
```

10 is big enough (F): record `ans = 5`, and look for an earlier F with `hi = 4`.

```text
Frame 3: lo=4 hi=4 mid=4 ans=5
idx      0   1   2   3   4   5   6
nums     1   3   5   6   8  10  12
P        T   T   T   T   F   F   F
                     L/M/H
```

8 is also big enough: `ans = 4`, `hi = 3`.

```text
Frame 4: lo=4 hi=3 ans=4  -> window empty, return 4
P        T   T   T   T   F   F   F
                     H   L
                         ^ ans
```

The window is empty, and `lo`, `ans` and the border all sit on index 4.

In every frame, `ans` was either n or the leftmost F seen so far, and the true border was inside `[lo, hi]` or equal to
`ans`.

## Why it is correct

The predicate `nums[i] < target` is monotone on a sorted array: if it holds at i it holds at every smaller index. So
the cells form T...T F...F, and the answer is the first F (or n). The invariant is: every index below `lo` is T, every
index above `hi` is F, and `ans` is the smallest index above `hi` that is known F (or n if none). Each branch keeps that
true. When the window is empty, `lo = hi + 1`, so the cells below `lo` are T and the cells from `lo` up are F; `ans` is
then exactly `lo`, the first F.

## Cost

Time O(log n): one halving search. Space O(1): three integers.

## Variations you will meet

- **Duplicates allowed.** "First index with value >= target" still works and returns the leftmost copy. That is the
  lower bound, and the next problem uses it.
- **Insert after equal copies** (upper bound). Change the test to `nums[mid] > target`, giving the first index strictly
  greater. `bisect_right` in Python.
- **Python one-liner.** `bisect.bisect_left(nums, target)` is exactly this function.
- **Sqrt(x), first bad version.** The candidates are numbers or versions, but the border question is the same.

## What to carry forward

Stop looking for the target; look for the border where "too small" turns into "big enough", and remember that the border
can be one past the end. The next problem needs two borders, one for each end of a run of equal values.
