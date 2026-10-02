# Sliding Window
*13 problems · Reading time ~14 min*

## Why this chapter exists

A large family of interview questions asks something about a *contiguous* piece of a sequence: the longest stretch with some property, the shortest stretch that reaches some total, every stretch of a fixed length, or how many stretches qualify. The naive answer is to try every start and every end, which is O(n^2) pieces and often O(n) work per piece. The sliding window is the observation that neighbouring pieces overlap almost completely, so you can move from one to the next by adding one element on the right and removing one on the left, never rebuilding from scratch.

The thirteen problems fall into a handful of families:

- **Running summary sweeps** (Best Time to Buy and Sell Stock): the "window" is everything before today, and you only need one number about it.
- **Shortest window that is good enough** (Minimum Size Subarray Sum, Minimum Window Substring): grow until the window qualifies, then shrink while it still does.
- **Longest window that stays legal** (Longest Substring Without Repeating Characters, Max Consecutive Ones III, Fruit Into Baskets, Longest Repeating Character Replacement): grow freely, shrink only when a rule breaks.
- **Fixed-size windows compared by counts** (Permutation in String, Substring with Concatenation of All Words): the width never changes; you compare a frequency table against a target.
- **Counting windows** (Subarrays with K Different Integers): turn "exactly K" into "at most K minus at most K-1".
- **Windows that need more than a counter** (Sliding Window Maximum, Shortest Subarray with Sum at Least K, Sliding Window Median): the summary cannot be updated with plus and minus, so we carry a monotonic deque or a pair of heaps.

## What it is

Start from the data. An array lives in memory as consecutive cells, each addressed by an index. A window is nothing more than two indices into that array, `L` and `R`, and the cells between them, inclusive.

```text
index:    0    1    2    3    4    5    6
        +----+----+----+----+----+----+----+
nums:   |  2 |  3 |  1 |  2 |  4 |  3 |  5 |
        +----+----+----+----+----+----+----+
                   ^              ^
                   L              R
window = nums[L..R] = [1, 2, 4]    length = R - L + 1 = 3
```

The window itself is never copied. What the technique stores alongside the two indices is a **summary** of the cells inside: a running sum, a count of zeros, a dictionary of character counts, the last position each character was seen. The summary is the whole trick. It must answer the question "is this window good?" in O(1), and it must be cheap to update when one cell enters on the right or leaves on the left.

```text
state carried by every sliding-window loop

   +-----------+     +-----------+     +------------------+
   | L (int)   |     | R (int)   |     | summary          |
   | left edge |     | right edge|     | sum / counts /   |
   +-----------+     +-----------+     | last-seen map    |
                                       +------------------+
   plus: best (the answer so far)
```

There are two shapes of window. A **fixed** window has width `k` and both edges move together: every step adds `nums[R]` and drops `nums[R-k]`. A **variable** window lets `R` advance one cell per iteration and lets `L` advance as many cells as needed to restore a rule. In both shapes, neither edge ever moves left. That single fact is why the total work is O(n): `R` makes n moves, `L` makes at most n moves, and each move costs O(1) summary work.

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| Extend right (`R += 1`, add `nums[R]` to summary) | O(1) | one counter or map update |
| Shrink left (remove `nums[L]`, `L += 1`) | O(1) | the inverse update |
| Test validity | O(1) | read the summary, not the window |
| Read length | O(1) | `R - L + 1` |
| Whole sweep | O(n) amortised | each index enters once and leaves once |
| Window max/min | O(1) amortised | needs a monotonic deque, not a counter |
| Window median | O(log k) | needs two heaps, not a counter |

Extend right, on a sum summary:

```text
before:  [ 2  3  1 ] 2  4        sum = 6
           L     R
after:   [ 2  3  1  2 ] 4        sum = 6 + 2 = 8
           L        R
```

Shrink left, on the same summary:

```text
before:  [ 2  3  1  2 ] 4        sum = 8
           L        R
after:     2 [ 3  1  2 ] 4       sum = 8 - 2 = 6
              L     R
```

Shrink with a count map: removing a character decrements its count, and when a count reaches zero the key is deleted so that `len(map)` still means "number of distinct values in the window".

```text
window "aab" -> drop 'a'        window "ab" -> drop 'a'
counts {a:2, b:1}               counts {a:1, b:1}
     -> {a:1, b:1}                   -> {b:1}   (key a deleted)
```

The amortised O(n) bound is worth drawing once, because it is the reason the whole chapter exists. Plot each step as a dot at `(R, L)`. Both coordinates only increase, so the path is a staircase that can take at most n steps right and n steps up.

```text
 L
 6 |                         *
 4 |                  * * * *
 2 |          * * * * *
 0 | * * * * *
   +--------------------------- R
     0 1 2 3 4 5 6 7 8 9
 path length <= 2n: L never goes back down
```

## The invariant

Every variable-window solution protects one sentence: **after the inner loop finishes, the window `[L, R]` is the best legal window that ends at `R`** (the longest legal one, or for "shortest" problems, the shortest one that still qualifies has just been recorded). Everything else follows. Because every window ends at some `R`, and we visit every `R`, the best window overall must be one we looked at.

The invariant only works when the rule is **monotone under shrinking**: if a window is legal, every window inside it is legal too (for "at most" rules), or if a window qualifies, every window containing it qualifies too (for "at least" rules with positive numbers). That monotonicity is what lets `L` move in one direction only.

Here is a legal and an illegal state for "no repeated characters":

```text
LEGAL                            ILLEGAL
 s:  a  b  c  b  d                s:  a  b  c  b  d
        [b  c] b                     [a  b  c  b]
         L  R                         L        R
 counts {b:1, c:1}               counts {a:1, b:2, c:1}
 every count <= 1                b has count 2 -> must shrink
```

The illegal state is allowed to exist for an instant, right after `R` advances. The inner loop's only job is to push `L` until the window is legal again.

## How to picture it

Picture a caterpillar on a branch. Its head is `R`, its tail is `L`. The head reaches forward one leaf at a time. If the body becomes too heavy, too varied, or breaks a rule, the tail pulls in until the body is fine again. The caterpillar never walks backwards. You record its length at every moment and keep the best.

```text
time 1   ====>               head moves
         L   R
time 2   =======>            head moves again
         L      R
time 3      ====>            rule broke: tail catches up
            L   R
time 4      =======>         head moves on
            L      R
```

For fixed windows, picture a rigid frame of width `k` slid along a ruler: one cell falls off the back each time one appears at the front.

For the hard problems at the end, picture the same caterpillar carrying a backpack: a deque of candidate maxima that stays sorted, or two piles (a max-heap of the small half and a min-heap of the big half) that stay balanced. The window still moves the same way. Only the summary got heavier.

## Signals in a problem statement

Point here:

- "contiguous subarray", "substring", "consecutive", "window of size k".
- "longest ... such that", "shortest ... such that", "minimum length ... with sum at least".
- "at most k distinct", "at most k replacements / flips / zeros".
- "contains all characters of", "is a permutation / anagram of", "every window of size k".
- All values positive (for sum problems) — this is what makes the sum monotone in each edge.
- n up to 10^5 or 10^6, so O(n^2) is too slow but O(n) or O(n log n) fits.

Point elsewhere:

- "subsequence" (not contiguous) usually means DP or greedy, not a window.
- Sum problems with **negative numbers** or zeros and "exactly equals target": use prefix sums with a hash map; the window rule is no longer monotone.
- "Shortest subarray with sum at least k" **with negatives**: prefix sums plus a monotonic deque (problem 12 in this chapter).
- "k-th largest in the whole array", or anything about non-adjacent elements: heaps or selection.
- Pairs from both ends of a sorted array: two pointers moving toward each other, a sibling of this chapter.

## Python toolbox

`collections.Counter` and `defaultdict(int)` are the usual summary. Delete zero counts so `len()` means distinct values:

```python
from collections import Counter, defaultdict, deque
count = defaultdict(int)
count[x] += 1
count[y] -= 1
if count[y] == 0:
    del count[y]          # keep len(count) == distinct
```

`Counter` equality ignores zero entries only if you remove them; for a fixed 26-letter alphabet, a list `[0] * 26` compared with `==` is fast and avoids that trap.

`deque` gives O(1) at both ends, which the monotonic-deque problems need:

```python
dq = deque()              # holds indices, values decreasing
while dq and nums[dq[-1]] <= x:
    dq.pop()              # smaller values can never be max
dq.append(i)
if dq[0] <= i - k:
    dq.popleft()          # front index left the window
```

`heapq` is a min-heap only. For a max-heap push negatives. It cannot delete an arbitrary item, so the median problem uses lazy deletion: remember what should be gone and discard it when it reaches the top.

`enumerate` hands you `R` and the value together: `for right, x in enumerate(nums):`. Use `float("inf")` as the "no answer yet" sentinel for minimum-length problems and convert it to 0 at the end.

## Mistakes people make

1. **`if` where `while` is needed when shrinking.** One new element can require several removals; write `while invalid:`.
2. **Recording the answer before the window is legal.** Update `best` after the shrink loop for "longest" problems, inside it for "shortest" ones.
3. **Not deleting zero counts.** `len(count)` stays inflated; always `del` at zero.
4. **Moving `L` backwards with a stale index.** With a last-seen map, guard `last[ch] >= L`, or use `L = max(L, last[ch] + 1)`.
5. **Off-by-one length.** The window `[L, R]` has length `R - L + 1`, not `R - L`.
6. **Applying the positive-number window to arrays with negatives.** Shrinking no longer lowers the sum; switch to prefix sums.
7. **Returning the sentinel.** `inf` must become `0` when no window qualified.
8. **Rebuilding the summary each step.** Calling `sum(nums[L:R+1])` or `max(window)` inside the loop quietly returns you to O(nk).
9. **Comparing count maps that contain zeros.** `{a:1, b:0} != {a:1}` for plain dicts; delete zeros or use fixed arrays.
10. **Updating the summary in the wrong order.** In the stock problem, compute today's profit before lowering the minimum to today.

## The journey ahead

1. **Best Time to Buy and Sell Stock** — the window in its simplest form: the left edge is a single remembered number, the running minimum.
2. **Minimum Size Subarray Sum** — the first true two-pointer window: grow until heavy enough, shrink while still heavy, with a running sum.
3. **Longest Substring Without Repeating Characters** — flips the goal to "longest legal", and shows `L` can jump using a last-seen map.
4. **Max Consecutive Ones III** — "at most k bad items": the summary shrinks to one counter, and the reframing from flips to windows is the lesson.
5. **Fruit Into Baskets** — "at most k distinct": the summary becomes a count map whose size is the rule.
6. **Longest Repeating Character Replacement** — validity depends on the most frequent letter, and a stale maximum turns out to be harmless.
7. **Permutation in String** — fixed width, compare two frequency tables, track how many letters already match.
8. **Substring with Concatenation of All Words** — fixed window over word-sized steps, run once per offset.
9. **Minimum Window Substring** — shortest window that covers a multiset, with a "formed" counter so validity is O(1).
10. **Subarrays with K Different Integers** — counting instead of optimising: exactly K = at most K minus at most K-1.
11. **Sliding Window Maximum** — the summary can no longer be a counter; a monotonic deque keeps candidates.
12. **Shortest Subarray with Sum at Least K** — negatives break the window, so slide over prefix sums with a monotonic deque.
13. **Sliding Window Median** — two heaps with lazy deletion as the summary; the hardest bookkeeping in the chapter.
