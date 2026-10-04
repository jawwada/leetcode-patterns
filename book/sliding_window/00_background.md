# Sliding Window
*13 problems · Reading time ~22 min*

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

## Advanced patterns

Everything above gets you through the Medium problems: two edges, a summary updated with plus and minus, a `while` loop that restores the rule. The Hard problems in this chapter keep that skeleton and change one of three things: what the summary is, what "valid" means, or what the window slides over. The seven patterns below are those changes. Each is small on its own; the skill is recognising which one a problem is asking for.

### 1. The window that never shrinks

**When it shows up**: you want the *longest* legal window, and checking legality exactly is awkward (it needs a maximum that is expensive to keep up to date as elements leave).

**The intuition**: once you have found a legal window of width `W`, you never care about any window narrower than `W` again. So when the window turns illegal, there is no reason to shrink it below `W`: move `L` by exactly one step (an `if`, not a `while`), which slides the window at its current width instead of shrinking it. The width is now a ratchet: it only grows, and it grows only when the newly added element genuinely proves a wider legal window exists. This is what lets Longest Repeating Character Replacement keep a stale `max_freq` that never decreases: a too-large `max_freq` can make an illegal window look legal, but only at a width already proven achievable, so the answer is never corrupted. At the end, the answer is simply the final width.

```text
"AABABBA", k = 1, rule: width - max_freq <= k
s:      A  A  B  A  B  B  A
R=3:   [A  A  B  A]            width 4, max_freq 3, legal
R=4:      [A  B  A  B]         5 - 3 > 1: slide, stay 4
R=5:         [B  A  B  B]      slid again; B:3, legal
R=6:            [A  B  B  A]   slid; true max 2, stale 3
"ABBA" is illegal but only 4 wide, already proven
width never drops: answer = final width = 4
```

**Where you'll use it**: Longest Repeating Character Replacement (essential), Max Consecutive Ones III (as the tidy final form). Beyond the chapter: Longest Subarray of 1's After Deleting One Element (1493).

### 2. A "matched" counter instead of comparing tables

**When it shows up**: validity means "the window contains a target multiset" (covers it, or equals it), and comparing two count tables at every step would cost O(alphabet) or O(m) each time.

**The intuition**: keep one table `need[c]` that starts as the target counts and is decremented when `c` enters the window and incremented when it leaves. Alongside it keep one integer: how many required items are still `missing` (or, for exact matching, how many letters currently match). The integer changes only at the moment a count *crosses* a threshold: `need[c]` going from 1 to 0 fills a real gap, going from 0 to -1 is just surplus. So every entry and exit costs O(1), and "is the window valid?" becomes `missing == 0`. A negative `need[c]` also tells the shrink loop something useful: that copy of `c` is spare, so `L` can drop it without losing coverage.

```text
t = "ABC", s = "ADOBEC...", missing starts at 3
R  char  need A B C   others     missing
0   A         0 1 1               2   gap filled
1   D         0 1 1   D:-1        2   surplus, no change
3   B         0 0 1   D,O:-1      1   gap filled
5   C         0 0 0   D,O,E:-1    0   window covers t
shrink: front A has need 0 -> not spare -> stop
```

**Where you'll use it**: Minimum Window Substring (the `missing` counter), Permutation in String (match count over 26 letters, or array equality), Substring with Concatenation of All Words (the "no word over budget and m tiles" check). Beyond the chapter: Find All Anagrams in a String (438).

### 3. Fixed-stride windows: one sweep per offset

**When it shows up**: the items you slide over are not single characters but fixed-length chunks (words of length `L`), so the natural window moves `L` characters at a time.

**The intuition**: a window starting at index `i` sees chunk boundaries at `i, i+L, i+2L, ...`. Two starts that differ by a multiple of `L` see the *same* boundaries, so there are only `L` distinct chunkings of the string, one per offset `0..L-1`. On one offset the string is simply a list of whole words, and the problem collapses to an ordinary counting window over that list, with every chunk read once. Running `L` such sweeps reads each character about once per offset, which is O(n · L) in character work instead of re-slicing every start from scratch. The general lesson: when the step is bigger than one, split the start positions into residue classes and slide inside each class.

```text
s = barfoofoobarthefoobarman, words = bar foo the
offset 0 tiles: bar foo foo bar the foo bar man
                 0   1   2   3   4   5   6   7
after tile 2:  [bar foo foo]     foo is over budget (2 > 1)
shrink:                [foo]     drop bar, drop foo
grow to tile 4:        [foo bar the]   3 tiles, hit
                        start = 2 * 3 = 6
```

**Where you'll use it**: Substring with Concatenation of All Words. The same residue-class idea appears whenever a window steps by a fixed stride.

### 4. Exactly K = at most K minus at most K-1

**When it shows up**: you must *count* windows with *exactly* K of something (distinct values, odd numbers, ones), and the valid starts for a given right end form a band with two moving edges rather than one.

**The intuition**: "exactly K" is not monotone: shrinking a window with K distinct values can drop it to K-1, and growing it can push it to K+1, so there is no single `L` to maintain. "At most K" *is* monotone, and for each right end `R` the valid starts form one unbroken run `L..R`, so you add `R - L + 1` windows at once. Every window with at most K either has exactly K or at most K-1, and those groups do not overlap, so subtracting two one-edged counts leaves the two-edged band. Two passes of the simple window replace one pass of a complicated one. The counting line `total += R - L + 1` is the second half of the trick: it counts all windows ending at `R`, not one.

```text
nums = [1, 2, 1, 2, 3], K = 2
R                 0  1  2  3  4   total
atMost(2) adds    1  2  3  4  2    12
atMost(1) adds    1  1  1  1  1     5
exactly(2)        0  1  2  3  1     7
```

**Where you'll use it**: Subarrays with K Different Integers. Beyond the chapter: Count Number of Nice Subarrays (1248), Binary Subarrays With Sum (930).

### 5. Monotonic deque for the window maximum or minimum

**When it shows up**: the summary is the max (or min) of the window, which cannot be "un-added" when an element leaves: if the maximum leaves, a counter has no idea what the new maximum is.

**The intuition**: an element that is older *and* no larger than a newer one can never be the maximum again, because every future window containing the old one also contains the new one. Throw such elements away the moment they are beaten. The survivors, read front to back, are strictly decreasing in value and increasing in index: a staircase. New elements pop the back while they are at least as big; the front leaves when its index falls out of the window; the front is always the maximum. Each index is pushed once and popped at most once, so the whole sweep is O(n) even though one step can pop many. For a minimum, flip the comparison; for "max minus min within a limit", run both deques side by side.

```text
nums = [5, 3, 4, 1, 2], k = 3, deque holds indices
i=2: 4 arrives, pops 3 (3 <= 4)
     deque idx [0, 2]  values [5, 4]   max 5
i=3: 1 arrives, appended; front idx 0 <= 3-3 expires
     deque idx [2, 3]  values [4, 1]   max 4
     window [3, 4, 1]: staircase 4 > 1
```

**Where you'll use it**: Sliding Window Maximum. Beyond the chapter: Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit (1438), with one max-deque and one min-deque.

### 6. Prefix sums plus a monotonic deque when values go negative

**When it shows up**: a sum condition ("sum at least K", shortest such subarray) on an array that contains negative numbers, so adding an element can lower the sum and the basic window's monotonicity is gone.

**The intuition**: rewrite every subarray sum as a difference of prefix sums, `P[j] - P[i]`, and think of each index `i` as a candidate *start*. A start is attractive when its prefix is low and it is recent. If a later start has a prefix no higher than an earlier one, the earlier one is dominated forever: pop it from the back. If the front start already works for the current end `j`, record `j - i` and pop it from the front, since any later end would only give a longer answer. The surviving starts have strictly increasing prefix sums, and both deque ends only move forward: it is a sliding window over prefix indices, where `L` advances because a start is used up rather than because a sum got too big.

```text
nums = [2, -1, 3, -4, 6], K = 4
P    = [0, 2, 1, 4, 0, 6]     (P index 0..5)
j=2: P=1 pops index 1 (P=2 >= 1)  deque [0, 2]
j=3: P=4, 4 - P[0] = 4 >= K  -> length 3, pop 0
     deque [2, 3]   prefixes [1, 4]
j=4: P=0 pops 3 and 2           deque [4]
j=5: 6 - P[4] = 6 >= K  -> length 1 (the [6])
```

**Where you'll use it**: Shortest Subarray with Sum at Least K. Beyond the chapter: Max Value of Equation (1499) keeps a deque of best starts in the same way with a different score.

### 7. Two heaps with lazy deletion

**When it shows up**: the summary is an order statistic of the window (the median, or more generally "the boundary between the lower and upper part"), and elements must leave as well as arrive.

**The intuition**: the median depends only on the boundary between the lower half (a max-heap) and the upper half (a min-heap), so you only ever need the two tops. A heap cannot remove a buried element, but a buried element does not affect the tops, so leave it there: record it in a `delayed` counter, decrease the live size of the half it belongs to, and pop it only when it surfaces at a top. Two disciplines make the corpses harmless: balance the halves by *live* counts, never by array length, and prune a heap whenever its top may have changed, so every top you read is alive. Each value is pushed once and popped once, so each slide costs O(log k) amortised.

```text
nums = [5, 1, 4, 2, 8, 3, 9], k = 3, window [8, 3, 9]
small (max-heap)          large (min-heap)
      8                        9
     / \
    3   2(x)                live: small 2, large 1
   /                        dead: 1 and 2 (delayed)
  1(x)                      median = top of small = 8
array (values): [8, 3, 2, 1]
```

**Where you'll use it**: Sliding Window Median. Beyond the chapter: Find Median from Data Stream (295) is the same two heaps without deletion.

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

The thirteen problems are ordered so that each one changes exactly one thing about the previous one: the goal, the rule, the summary, or what the window slides over. By the end, the window loop itself has not changed at all; what you carry inside it has grown from one number to two heaps.

### Warm-up: one edge, one number

**Best Time to Buy and Sell Stock.** The puzzle looks like pairs (a buy day and a later sell day), and the naive answer tries all of them. The insight is that for each sell day only one buy day matters, the cheapest one so far, so the whole left edge collapses into a single running minimum. It teaches the idea every later problem leans on: do not store the window, store the one fact about it you need.

### Variable windows: grow, break, repair

**Minimum Size Subarray Sum.** Now both edges move. The tension is that a window can be "too light" or "good enough", and you want the shortest good one; the trap is restarting the sum for every start. Because all values are positive, growing only raises the sum and shrinking only lowers it, which is precisely what allows `L` to chase `R` without ever stepping back. This is the first real two-pointer window and the first `while` shrink loop.

**Longest Substring Without Repeating Characters.** The goal flips from "shortest that qualifies" to "longest that stays legal", which moves where you record the answer. The new trick is that `L` does not have to crawl: a last-seen map lets it jump straight past the previous copy of the repeated character, as long as you never let it jump backwards to a stale position.

**Max Consecutive Ones III.** On the surface it is about flipping zeros, which invites you to simulate flips. Reframe it: a run of ones after at most `k` flips is just a window containing at most `k` zeros. The summary shrinks to one counter, and the lesson is the reframing itself, turning an "edit" question into a "window rule" question.

**Fruit Into Baskets.** A story problem that hides "longest window with at most 2 distinct values". The summary becomes a count map, and the rule is its size, which only works if you delete keys whose count reaches zero. It is the template you will reuse, with a different limit, inside the Hard counting problem later.

**Longest Repeating Character Replacement.** The rule now depends on the most frequent letter in the window, and keeping an exact maximum while letters leave looks expensive. The surprise is that you never need to lower it: a window that only grows or slides, never shrinks, makes a stale maximum harmless. This is the first problem where the window's width, rather than its contents, is the thing you protect.

### Fixed windows: matching a target

**Permutation in String.** "Does any rearrangement of `s1` appear in `s2`?" sounds like generating permutations. It is really "does any window of width `len(s1)` have the same letter counts", and sliding a fixed window changes just two counts per step. The left edge loses its freedom entirely; it is chained to the right edge.

**Substring with Concatenation of All Words.** The same matching question, but the letters are whole words and the window steps a word at a time. The puzzle is where the word boundaries are; the answer is that there are only `L` possible chunkings, one per starting offset, so you run the previous problem's window once per offset over a list of words. It also shows how an over-budget word pushes `L` and how an unknown word resets the window entirely.

**Minimum Window Substring.** The shortest window that *covers* a multiset, not one that equals it. Comparing tables at every step is the naive cost; the fix is a single `missing` counter that changes only when a count crosses zero, so validity is O(1). It combines the shrink loop of Minimum Size Subarray Sum with the count tables of the last two problems, and it is the classic interview Hard for that reason.

### The Hard end: when plus and minus are not enough

**Subarrays with K Different Integers.** For the first time you count windows instead of finding the best one, and "exactly K distinct" refuses to be monotone. The way out is set arithmetic: count windows with at most K, subtract those with at most K-1, and each count is the Fruit Into Baskets loop plus the line that adds `R - L + 1` windows at once.

**Sliding Window Maximum.** The summary is now a maximum, and when the maximum leaves, no counter can tell you the next one. The new idea is dominance: an older, smaller element can never win again, so discard it, and the survivors form a decreasing staircase in a deque. It is the first summary that is a data structure rather than a number.

**Shortest Subarray with Sum at Least K.** Minimum Size Subarray Sum again, but with negative numbers, which breaks the reason that window worked. The rescue is to slide over prefix sums instead of values and to reuse the dominance idea from the previous problem on candidate starts. It is the chapter's best demonstration that a "window" is a pair of forward-only pointers, whatever they point into.

**Sliding Window Median.** The heaviest summary of all: the middle of a window that both gains and loses elements. Two heaps give the middle in O(1), but heaps cannot delete from the inside, so you delete lazily and track live sizes. Every earlier lesson is here in some form: a fixed window, a summary that must be updated on both ends, and the discipline of only ever reading values that are known to be current.
