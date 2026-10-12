# Next Greater Element II

*LeetCode 503 · Medium · Pattern: Monotonic stack · Reading time ~7 min*

## The problem

nums is circular: after the last element comes the first. For every index return the first strictly greater value
found by walking forward (wrapping around), or -1 if none exists.

```text
Example: nums = [1,2,1] -> [2,-1,2]; nums = [1,2,3,4,3] ->
  [2,3,4,-1,4].
```

## What the problem is really asking

For every position in an array, find the first value to its right that is strictly larger. The twist: the array is a circle. After the last element you continue at the first. If you go all the way around and nothing is larger, the answer is -1.

The answer is an array of values (not distances, this time). Compared to Daily Temperatures, the only new thing is the wrap-around, and the whole problem is about handling it without paying for it.

```text
nums = [3, 1, 4, 2, 1]   arranged on a circle:

          3 (i=0)
       /          \
  1 (i=4)        1 (i=1)
     |              |
  2 (i=3) ----- 4 (i=2)

walk clockwise: 0 -> 1 -> 2 -> 3 -> 4 -> 0 -> ...
answer = [4, 4, -1, 3, 3]
```

Index 3 (value 2) looks right, sees 1, then wraps to index 0 and finds 3. Index 2 (value 4) is the maximum; nothing on the whole circle beats it, so -1.

## Do it by hand first

Copy the array twice in a row on paper, so the circle becomes a straight line twice as long. Now "walk forward with wrap-around" is just "walk forward" on the doubled line.

```text
doubled:  3  1  4  2  1 | 3  1  4  2  1
index:    0  1  2  3  4 | 0  1  2  3  4
                         ^ wrap point
for i=3 (value 2): 1 ... 3   -> answer 3
for i=4 (value 1): 3          -> answer 3
```

Now do it the Daily Temperatures way: walk the doubled line once, keeping a note of the positions still waiting for something bigger. Your note again stays sorted, biggest first, and each new value crosses off the smaller waiting entries at the end of the note. The second copy of the array only matters for the entries still waiting at the wrap point: it gives them a second look at the start of the array. The thing your hand tracked is the same descending list of waiting indices as before, plus one more lap.

## The first honest attempt

For each `i`, step `k = 1 .. n-1`, look at `nums[(i + k) % n]`, stop at the first larger value. O(n^2) time, O(1) extra space.

The waste is the same shape as before, made worse by the circle. A long descending stretch is re-walked from each of its members, and every one of them may have to go all the way around to the start to find its answer.

```text
nums = [5, 4, 3, 2, 1]
from 4: 3 2 1 | 5          4 steps
from 3:   2 1 | 5          3 steps
from 2:     1 | 5          2 steps
from 1:       | 5          1 step
            ~~~~~~
the same tail "... 1 | 5" is walked again and again;
one look at 5 would answer all four at once
```

## The turning point

**Claim: the indices still waiting for an answer always hold non-increasing values, so a new value resolves exactly a run at the top of a stack; and a second pass that only pops is enough to handle the wrap-around.**

The first half is Daily Temperatures exactly. If a later waiting index had a bigger value than an earlier waiting index, it would have answered the earlier one when it arrived. So the waiting indices form a descending staircase, and a newcomer pops (and answers) every step smaller than itself.

The second half is the new idea. After one pass over the array, the stack holds exactly the indices that found nothing bigger to their right *within the array*. Their remaining hope lies in the wrap: the values at indices `0, 1, 2, ...` from the start. So walk the array a second time and run the same popping loop, but push nothing. Pushing would be pointless: every index already had its turn to wait, and putting it on the stack again would only create duplicates.

Why does one extra lap suffice? An index `j` can look forward at most `n - 1` positions on the circle. The first lap covers everything to its right; the second lap covers everything from 0 up to `j - 1` (and beyond, harmlessly). Every position on the circle has been offered to `j`.

Each index is pushed once (first lap) and popped at most once (either lap). Two laps of O(n) is O(n).

## Watch it work

`nums = [3, 1, 4, 2, 1]`. The staircase beside the array lists the stack bottom-first, bar length equal to the value.

Frame 1 — lap 1, `i = 0, 1`: nothing smaller to pop; both pushed.

```text
lap 1   i:  0  1  2  3  4
     nums:  3  1  4  2  1
               ^ i=1
staircase:
  i0 3 |###
  i1 1 |#              <- top
ans: [-1, -1, -1, -1, -1]
```

Frame 2 — lap 1, `i = 2` (value 4) floods both steps.

```text
lap 1   i:  0  1  2  3  4
     nums:  3  1  4  2  1
                  ^ i=2
pop i1 (1 < 4): ans[1] = 4
pop i0 (3 < 4): ans[0] = 4
staircase:
  i2 4 |####           <- top
ans: [4, 4, -1, -1, -1]
```

Frame 3 — lap 1, `i = 3, 4`: both smaller, both wait.

```text
lap 1   i:  0  1  2  3  4
     nums:  3  1  4  2  1
                        ^ i=4
staircase:
  i2 4 |####
  i3 2 |##
  i4 1 |#              <- top
```

End of lap 1: three indices have found nothing to their right.

Frame 4 — lap 2, `i = 0` (value 3) answers the wrap.

```text
lap 2   i:  0  1  2  3  4
     nums:  3  1  4  2  1
            ^ i=0  (no push in lap 2)
pop i4 (1 < 3): ans[4] = 3
pop i3 (2 < 3): ans[3] = 3
stop at i2 (4 >= 3)
staircase:
  i2 4 |####           <- top
ans: [4, 4, -1, 3, 3]
```

Frame 5 — lap 2, `i = 1..4`: no value exceeds 4.

```text
staircase:
  i2 4 |####           <- never popped
ans: [4, 4, -1, 3, 3]
```

The maximum keeps its default -1.

Throughout, the staircase descended from bottom to top, every answer was written exactly once at the moment of popping, and lap 2 only ever shrank the stack.

## Why it is correct

**Order invariant.** In lap 1 we push `i` only after popping everything smaller, so the stack stays non-increasing. Lap 2 only pops, and popping from the top of a sorted stack leaves it sorted.

**A popped element's answer is fixed at pop time.** Suppose index `j` is popped by position `p` (in lap 1 or lap 2). Every position the circle visits between `j` and `p` was processed while `j` sat on the stack. Any of them with a value larger than `nums[j]` would have popped `j` first, because the loop pops from the top down and everything above `j` is no larger than `nums[j]`. So `nums[p]` is the first larger value walking forward from `j`, and writing it now is final.

**An element never popped has no answer.** After the two laps, an index `j` still on the stack has been offered every other position on the circle (lap 1 gave it the right side, lap 2 the left side), and none popped it. Since anything above `j` is no larger, a bigger value would have cleared them and reached `j`. So nothing on the circle is bigger, and -1 is right. In practice only copies of the maximum survive.

## Cost

Time O(n): each index is pushed once in lap 1 and popped at most once across both laps; the two `for` loops add 2n iterations.

Space O(n): a strictly decreasing array leaves all indices stacked after lap 1.

The brute force is O(n^2) time, O(1) space.

## Variations you will meet

- **Index arithmetic instead of two loops.** Loop `i` from 0 to `2n - 1`, use `nums[i % n]`, and push only while `i < n`. Same algorithm; one loop.
- **Next Greater Element I** (LeetCode 496). Queries come from a subset array; run the stack on `nums2` once, record answers in a dict keyed by value, then look up each query.
- **Distance instead of value on a circle.** Store `(p - j) mod n`; the `mod` handles the wrap automatically.
- **Next smaller on a circle.** Flip the comparison; the staircase rises from bottom to top instead.

## What to carry forward

A circular "next greater" is a straight one walked twice: the first lap builds the staircase, the second lap only knocks steps down. Answers are still written once, at pop time.

The next problem keeps the staircase but hides it: cars on a road, sorted by position, where "being caught" plays the role of being popped.
