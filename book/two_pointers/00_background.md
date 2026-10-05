# Two Pointers
*10 problems · Reading time ~22 min*

## The chapter

Two indices that move through an array or string in a disciplined way, inward from both ends, or as a reader and a
writer, or one per input. This chapter teaches the arguments that let a pointer move without ever needing to look
back: sorted order, in-place partition invariants, and the shorter-side-loses rule for geometric problems.

Problems, in reading order:

1. [Valid Palindrome](valid_palindrome.md) · Easy
2. [Move Zeroes](move_zeroes.md) · Easy
3. [Squares of a Sorted Array](squares_of_a_sorted_array.md) · Easy
4. [Remove Duplicates from Sorted Array II](remove_duplicates_from_sorted_array_ii.md) · Medium
5. [Sort Colors](sort_colors.md) · Medium
6. [Two Sum II - Input Array Is Sorted](two_sum_ii_input_array_is_sorted.md) · Medium
7. [3Sum](three_sum.md) · Medium
8. [Container With Most Water](container_with_most_water.md) · Medium
9. [Trapping Rain Water](trapping_rain_water.md) · Hard
10. [Wildcard Matching](wildcard_matching.md) · Hard

## Why this chapter exists

Many array and string questions have an obvious answer that looks at every pair of positions: every left end with every right end, every reader with every writer, every candidate wall with every other wall. That is n(n-1)/2 pairs, and for n = 10^5 it is five billion of them. Two pointers is the observation that, in a surprising number of problems, a single comparison between two positions tells you that an entire row of those pairs is useless. You throw that row away and never look at it again. Do that n times and you have scanned the whole pair space in O(n).

The ten problems in this chapter fall into four families:

- **Mirror checks** (Valid Palindrome): two indices walk inward from both ends and compare what they find.
- **In-place compaction and partition** (Move Zeroes, Remove Duplicates from Sorted Array II, Sort Colors): a reader scans everything while a writer marks where the next kept element belongs.
- **Searching a sorted pair space** (Squares of a Sorted Array, Two Sum II, 3Sum): sorted order tells you which end to discard after each comparison.
- **Geometric "the shorter side loses" arguments** (Container With Most Water, Trapping Rain Water): no sorting at all, but the shorter of two walls provably cannot do better, so its pointer moves.

The last problem, Wildcard Matching, puts one pointer on each of two different strings and adds a single saved bookmark. It shows how far the "never look back further than you must" idea stretches.

## What it is

Start with memory. An array is a row of consecutive cells, each with an index. A pointer here is not a memory address; it is just an integer index into that row. The technique keeps two (occasionally three) such integers and a tiny amount of extra state, and moves the integers according to a rule.

```text
index:    0    1    2    3    4    5    6
        +----+----+----+----+----+----+----+
nums:   |  1 |  3 |  4 |  6 |  8 | 11 | 15 |
        +----+----+----+----+----+----+----+
          ^                             ^
          L                             R
state: L = 0, R = 6  (two ints, O(1) space)
```

There are three geometries. Learn to draw all three, because the first thing you do with a new problem is decide which one it is.

**Geometry 1: converging from both ends.** `L` starts at the left end, `R` at the right end, and each step moves exactly one of them one cell inward. The loop ends when they meet. The region outside `[L, R]` is finished: either checked or proven useless.

```text
step 0:  [ a  b  c  d  e  f  g ]
           L                 R
step 1:  [ a  b  c  d  e  f  g ]
           L              R          R moved in
step 2:  [ a  b  c  d  e  f  g ]
              L           R          L moved in
         \__/              \__/
       settled            settled
```

**Geometry 2: reader and writer, same direction.** Both indices start at the left. The reader `r` advances every step and looks at one element. The writer `w` advances only when the reader finds something worth keeping, and that element is copied or swapped into slot `w`. The writer never passes the reader.

```text
         0   1   2   3   4   5   6
       [ 5 | 7 | 9 | x | x | 4 | 2 ]
                     ^       ^
                     w       r
       \___________/ \_____/ \___/
          kept,        junk   not yet
          final               read
```

**Geometry 3: fast and slow.** Two indices move in the same direction at different speeds or with a fixed lag. The best-known form is Floyd's cycle check on a linked list (the hare moves two nodes per step, the tortoise one). In arrays it appears as a slow index that trails a fast one and looks a fixed distance back, as in Remove Duplicates II, where the slow writer compares against the cell two behind it.

```text
linked list, speeds 2 and 1:

  [1]->[2]->[3]->[4]->[5]->[6]
             ^         ^
           slow      fast
  after one step: slow at [4], fast past [6]

array, slow trails fast, look-back of 2:

  [ 1 | 1 | 2 | 2 | 2 | 3 ]
            ^       ^
        slow-2     fast   compare nums[fast]
                          with nums[slow-2]
```

Some problems combine geometries. Sort Colors runs a reader with two writers, one growing from each end. Trapping Rain Water converges like Geometry 1 but each pointer also carries a running maximum. Wildcard Matching runs a pointer on each of two strings in lockstep and keeps one bookmark that only moves forward.

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| Read `nums[L]`, `nums[R]` | O(1) | array indexing |
| Move one pointer inward | O(1) | one integer increment |
| Swap two cells | O(1) | tuple assignment, no shifting |
| Write `nums[w] = nums[r]` | O(1) | overwrite, nothing moves |
| Look back `nums[w - k]` | O(1) | fixed offset into finished region |
| Whole converging sweep | O(n) | the gap `R - L` shrinks by one each step |
| Whole reader/writer sweep | O(n) | reader makes n steps, writer at most n |
| Sort first (when allowed) | O(n log n) | buys the monotone order the moves need |

The two expensive alternatives the technique replaces are worth drawing too, because each problem's brute force uses one of them.

Deleting from the middle of a Python list shifts the whole tail left. Doing it k times is O(nk):

```text
del nums[1]:
  before [ 4 | 0 | 5 | 0 | 6 ]
  after  [ 4 | 5 | 0 | 6 ]     <- 3 cells moved one slot left
```

Overwriting at the writer instead moves each kept element exactly once:

```text
nums[w] = nums[r]:
  [ 4 | 0 | 5 | 0 | 6 ]      w=1, r=2
        ^   ^
        w   r
  [ 4 | 5 | 5 | 0 | 6 ]      one cell written, w -> 2
```

A swap is the writer's tool when the discarded values must survive (Move Zeroes keeps its zeros, Sort Colors keeps every colour):

```text
swap(nums[w], nums[r]):  [ 1 | 0 | 0 | 3 ]  w=1, r=3
                     ->  [ 1 | 3 | 0 | 0 ]  zero carried to r
```

## The invariant

Every two-pointer algorithm protects one sentence:

**Everything the pointers have already passed is settled: either its contribution to the answer is recorded, or it has been proven unable to contribute.**

The second half, "proven unable", is the whole game. Here is the argument that makes converging pointers O(n), drawn for Two Sum II on the sorted array `[1, 3, 4, 6, 8, 11]` with target 10. Each cell of the grid is one pair `(i, j)` with `i < j`. The letters say which pointer move eliminated the cell.

```text
 value:          3    4    6    8   11
 j:              1    2    3    4    5
 i=0 (1)         B    B    B    B    A
 i=1 (3)              D    D    C    A
 i=2 (4)                   *    C    A
 i=3 (6)                        C    A
 i=4 (8)                             A

 A: (0,5) sum 12 > 10 -> every pair with 11 is too big
 B: (0,4) sum  9 < 10 -> every pair with 1 is too small
 C: (1,4) sum 11 > 10 -> every pair with 8 is too big
 D: (1,3) sum  9 < 10 -> every pair with 3 is too small
 *: (2,3) sum 10 = target
```

Four comparisons killed fourteen pairs. Each move removes a whole row or a whole column, and there are only n rows and n columns. That is the O(n) argument, and it only works because of a **monotone property**: in a sorted array, if `1 + 11` is too big then `3 + 11`, `4 + 11`, and every other partner of 11 is bigger still. Sorted order is one such property. The other one you will meet is geometric: in Container With Most Water, the shorter wall limits the height, so any container that keeps the shorter wall and is narrower **can never do better**. Different problems, same shape of argument: one comparison, one whole line of candidates gone.

For reader/writer problems the invariant is about regions. A legal state of Move Zeroes and an illegal one:

```text
legal (w=2, r=4):
  [ 1 | 3 | 0 | 0 | 12 ]
  \_____/ \_____/ \__/
   kept    zeros  unread

illegal:
  [ 1 | 0 | 3 | 0 | 12 ]   w=2, r=4
        ^
   a zero inside the "kept" prefix: the writer
   advanced past a slot it never filled
```

If you can say, before writing any code, what each region between the pointers contains, the loop body almost writes itself: it is whatever restores that description after the reader takes one step.

## How to picture it

Carry two pictures.

The first is the **pair grid with a staircase**. The brute force fills the whole upper triangle; converging pointers start in the top-right corner and walk down or left, one row or column per step, until they hit the answer or fall off the diagonal. Whenever you are unsure whether your pointer rule is safe, ask: "when I move this pointer, which row or column am I deleting, and why is everything in it hopeless?"

```text
          j=1  j=2  j=3  j=4  j=5
   i=0     .    .    .    o <- S      S: start (0, n-1)
                          |
   i=1          .    o <- o    .      <-: R -= 1
                     |                 |: L += 1
   i=2               *    .    .       *: answer
   i=3                    .    .
   i=4                         .
```

The second is the **conveyor belt** for reader/writer problems: the reader is a scanner moving at constant speed, the writer is a stamping machine behind it, and the gap between them is scrap. The array to the left of the writer is the finished product, already in its final place.

## Advanced patterns

The basic geometries get you through the Easy and most Medium problems. The Hard end of the chapter, and the interview follow-ups that come after a Medium, need a sharper toolkit. Each pattern below is a reusable argument, not just a loop shape. Learn the argument and you can rebuild the loop on the spot.

### 1. Discard the weaker side

**When it shows up**: you choose a pair of positions, the score of a pair depends on the *smaller* (or weaker) of the two plus the distance between them, and the input is not sorted. "Two lines", "two walls", "maximise min(...) times width".

**The intuition**: put the pointers at the two ends, so the width is as large as it will ever be. Now look at the weaker side, say the shorter wall at `L`. Every other pair that uses `L` has a partner strictly inside, so it is narrower, and its height is still capped by `h[L]` no matter how tall the partner is. So the current pair is the best pair `L` will ever be part of. You record it and delete `L`'s whole row of the pair grid. The stronger side gets no such guarantee (a taller partner might appear inside), so it must stay. On a tie, both rows are dead, and moving either pointer is safe. This is the "exchange" shape of proof: any pair you skip is dominated by one you already scored.

```text
 h:  [ 1 | 8 | 6 | 2 | 5 | 4 | 8 | 3 | 7 ]
       L                               R
 score(L, R) = min(1, 7) * 8 = 8
 any (L, j) with j < R:
     width  < 8
     height <= h[L] = 1        -> score < 8
 row of L is dead: record 8, then L += 1
```

**Where you'll use it**: Container With Most Water directly; Trapping Rain Water reuses the same "the shorter side is the one we can decide about" move. Beyond the chapter: Boats to Save People (LeetCode 881), where the heaviest person is the "weaker" side that must leave now.

### 2. Settle a cell with a borrowed bound

**When it shows up**: the answer is a sum over cells, and each cell's value depends on a quantity from **both** sides (the tallest bar to the left and to the right, the best price before and after). The obvious fix is two prefix arrays and O(n) space; the follow-up asks for O(1).

**The intuition**: a cell's value usually needs only the *smaller* of its two side quantities. You do not need to know the exact right maximum to know it is at least the bar `R` currently stands on. So if the left running max is no larger than `h[R]`, the left side is provably the binding one, and the cell under `L` can be settled right now and forever. The rule "always move the pointer on the shorter bar" keeps that comparison true: every bar either pointer has passed is no taller than the taller of the two current bars. You are borrowing a lower bound from the far side instead of computing the far side's exact value.

```text
 h:  [ 3 | 0 | 2 | 0 | 4 | 1 | 2 ]
           L           R
 leftMax = 3 (bars 0..1)    h[R] = 4
 true right max at L >= h[R] = 4 >= leftMax
 water at L = leftMax - h[L] = 3 - 0 = 3   settled
 (rightMax is only 2 here, and it does not matter)
```

**Where you'll use it**: Trapping Rain Water. Beyond the chapter, Trapping Rain Water II (LeetCode 407) keeps the idea "settle from the lowest boundary inward" but needs a min-heap, because a 2D boundary has no single "other end".

### 3. k-sum reduction: fix one, two-pointer the rest

**When it shows up**: "find all triplets (or quadruplets) that sum to a target", values may repeat, and the output must not contain duplicates.

**The intuition**: sort once. Then fixing the smallest element of the triple (the anchor at `i`) turns the rest into Two Sum II on the suffix `i+1..n-1` with target `-nums[i]`, which is a single O(n) staircase walk. n anchors times O(n) gives O(n^2), against O(n^3) for all triples. Sorting buys a second gift: duplicates become neighbours, so deduplication is a local check instead of a set of tuples. Skip an anchor equal to the previous anchor (it would find exactly the same pairs), and after a hit move both pointers, then step `L` past clones of the value just used. The same reduction stacks: 4Sum fixes two anchors and costs O(n^3); k-sum fixes k-2.

```text
 index:     0    1    2    3    4    5
 sorted: [ -4 | -1 | -1 |  0 |  1 |  2 ]
 anchor i=1 (-1), pair target = 1
 step 1:         i    L              R   -1 + 2 = 1  hit
 step 2:         i         L    R        0 + 1 = 1  hit
 anchor i=2 is -1 again: same suffix pairs -> skip
 found: [-1,-1,2]  [-1,0,1]
```

**Where you'll use it**: 3Sum, built on Two Sum II. Beyond: 4Sum (LeetCode 18) and 3Sum Closest (LeetCode 16), where you track the best distance instead of stopping on equality.

### 4. Three-way partition (Dutch national flag)

**When it shows up**: only a few distinct key classes (three colours, "less than / equal to / greater than a pivot"), in place, one pass.

**The intuition**: keep four regions with three pointers: zeros in `[0, lo)`, ones in `[lo, mid)`, unknown in `[mid, hi]`, twos in `(hi, n-1]`. Each step looks at `a[mid]`, the first unknown cell, and shrinks the unknown region by exactly one. A 0 is swapped to `lo`; what comes back is a 1 that `mid` has already seen (or the same cell), so both advance. A 2 is swapped to `hi`; what comes back is **unexamined**, so only `hi` moves and `mid` looks again. A 1 is already in place. The loop ends when the unknown region is empty: `mid > hi`.

```text
 regions after 3 steps on [2,0,2,1,1,0]:

   [ 0 | 0 | 2 | 1 | 1 | 2 ]
     \___/   \_________/ \_/
     zeros    unknown    twos
             ^       ^
            lo      hi
            mid
 a[mid]=2: swap with a[hi], hi -= 1, mid stays
```

**Where you'll use it**: Sort Colors. Beyond: the 3-way partition inside quickselect (Kth Largest Element, LeetCode 215) that stops long runs of equal keys from causing O(n^2), and Wiggle Sort II (LeetCode 324).

### 5. Writer with a look-back of k

**When it shows up**: a sorted array, in place, "each value may appear at most k times", or more generally "keep x unless the last few kept items forbid it".

**The intuition**: the writer's output prefix is itself sorted. So if the value k cells behind the writer equals the incoming `x`, then everything between those cells also equals `x`, which means `x` already appears k times in the output. One comparison replaces a counter. The crucial detail is that the look-back reads the **output** (`a[w - k]`), not the input: the output is the certified region, while the input around the reader may already have been overwritten. The first k values are always kept.

```text
 k = 2, input [1,1,1,2,2,3], reader at x = 2 (index 3)

   [ 1 | 1 | 1 | 2 | 2 | 3 ]
     ^       ^   ^
   w - 2     w   reader
 a[w-2] = 1 != 2 -> write: a[w] = 2, w += 1
 (the third 1 was refused because a[w-2] was 1)
```

**Where you'll use it**: Remove Duplicates from Sorted Array II (k = 2); Move Zeroes uses the same writer with a simpler keep-test, "x is non-zero". Beyond: Remove Duplicates from Sorted Array (LeetCode 26) is k = 1.

### 6. Two sequences, merge-like, often from the back

**When it shows up**: two sorted runs must be combined, or one sequence must be matched against another in order. Sometimes the two runs are hidden inside one array, as in Squares of a Sorted Array, where the negatives form a run sorted by absolute value from the left and the positives one from the right.

**The intuition**: each pointer marks the frontier of its own sequence, and each step consumes the better frontier element, so each element is touched once: O(n + m). When the output lives in the same buffer as an input, fill it **from the back** with the largest element first. The free space sits at the back, and the back writer can never overtake an unread element: the slots it writes are either empty or already consumed. In Squares the same trick appears because the largest square is guaranteed to be at one of the two ends, while the smallest could be anywhere in the middle.

```text
 merge [1,3,5,_,_,_] with [2,4,6], writing from the back

   a: [ 1 | 3 | 5 | _ | 5 | 6 ]
            ^       ^
            i       k     (i = 1, k = 3)
   b: [ 2 | 4 | 6 ]
            ^
            j             (j = 1)
 a[i]=3 vs b[j]=4 -> a[k] = 4, j -= 1, k -= 1
```

(Here 6 and 5 have already been placed, and the 3 is the next `a` value to compare.)

**Where you'll use it**: Squares of a Sorted Array (two hidden runs, filled from the back), and Wildcard Matching (one pointer on the text, one on the pattern). Beyond: Merge Sorted Array (LeetCode 88) and Is Subsequence (LeetCode 392).

### 7. Greedy matching with one backtrack bookmark

**When it shows up**: matching one sequence against another where some token can absorb a variable amount (`*` in a glob pattern), and the exhaustive answer would be a recursion tree or a 2D DP table.

**The intuition**: match greedily with the star eating nothing at first. Remember only the **latest** star and the text position where its stretch currently ends (`match`). On a mismatch, do not reconsider every earlier choice; let the latest star eat one more character and retry the rest of the pattern from just after it. This is safe because the greedy reaches each star at the leftmost text position any matching could reach it, and from a leftmost position the latest star can imitate any other solution by eating more. Earlier stars are dominated, so the bookmark only ever moves right, and the whole recursion tree folds into two pointers plus one integer.

```text
 s = "abcab", p = "a*ab"          star = 1 (p[1])

   s: [ a | b | c | a | b ]      p: [ a | * | a | b ]
                ^                             ^
                i = 2, match = 2              j = 2
 p[2]='a' vs s[2]='c': mismatch
 -> star eats one more: match = 3, i = 3, j = 2
 then 'a'='a', 'b'='b': matched
```

**Where you'll use it**: Wildcard Matching. Beyond: the same "remember only the latest choice point" idea fails for Regular Expression Matching (LeetCode 10), because `a*` cannot imitate an arbitrary earlier star. Knowing when the dominance argument fails is as useful as knowing the pattern.

## Signals in a problem statement

- "sorted array", "non-decreasing order": pairs can be pruned by comparing a sum or difference with a target.
- "in place", "O(1) extra space", "return the new length k": reader/writer compaction.
- "keep the relative order": the writer must copy or swap forward, never sort.
- "palindrome", "reads the same forwards and backwards": mirror pointers from both ends.
- "pair", "triplet", "two lines", "two numbers that sum to": converging pointers, possibly after sorting.
- "only values 0, 1, 2" or "partition around a pivot": a reader with writers at both ends.
- "container", "trapped", "between two walls": the shorter-side argument.
- "linked list", "cycle", "middle node": fast and slow at speeds 2 and 1.

Counter-signals:

- Unsorted input where the answer needs **original indices** (classic Two Sum): sorting destroys them, so use a hash map.
- "Contiguous subarray with sum/count property": that is a sliding window, the cousin chapter. Its two pointers move the same direction and bound a window; here the region between pointers usually is not the answer.
- Negative numbers with a "subarray sum" condition: neither pointer rule is monotone; reach for prefix sums.
- "All subsets", "all orderings": the answer is exponential, so no pruning of a pair grid helps; that is backtracking.

## Python toolbox

The language gives you very little here, and that is the point: the technique is a handful of integers.

```python
l, r = 0, len(a) - 1
while l < r:                      # converging template
    ...                           # move exactly one side
    l += 1                        # or r -= 1

a[w], a[r] = a[r], a[w]           # swap without a temp

ch.isalnum(); ch.lower()          # filters for string problems

a.sort()                          # in place, O(n log n), stable
for w in range(n - 1, -1, -1):    # fill an output from the back
    ...

a[:] = a[:k]                      # truncate the same list
```

Two Python details bite. `a = a[:k]` rebinds a local name and does not change the caller's list; `a[:] = ...` does. And `del a[i]` inside a loop is O(n) per call and shifts every index after `i` under your loop variable.

## Mistakes people make

1. **Moving the wrong pointer.** In Container With Most Water you must move the shorter wall. Fix: before coding, say which line of candidates the move deletes and why it is hopeless.
2. **`while l < r` versus `while l <= r`.** Squares of a Sorted Array and Sort Colors need the last element handled, so they use `<=` (or a for-loop over output slots). Fix: ask whether the meeting cell still needs work.
3. **Skip loops that run off the end.** `while not s[l].isalnum(): l += 1` crashes on `".,"`. Fix: guard every inner skip with `l < r`.
4. **Advancing the reader after swapping with the right writer.** In Sort Colors the value swapped in from the right is unexamined. Fix: on a 2, decrement `high` and leave `mid` alone.
5. **Looking back into the input instead of the output.** Remove Duplicates II compares with `nums[write - 2]`, not `nums[read - 2]`. Fix: the look-back must point into the region you have already certified.
6. **Deduplicating 3Sum with `nums[i] == nums[i + 1]`.** That skips the first of two equal anchors and loses `[-1, -1, 2]`. Fix: compare with `nums[i - 1]`.
7. **Forgetting to move both pointers after a hit.** In 3Sum, moving only one side after recording a triplet either loops forever or re-finds the same pair. Fix: move both, then skip clones.
8. **Filling the output from the wrong end.** In Squares of a Sorted Array the smallest square is in the middle, not at an end. Fix: write the largest first, from the back.
9. **Adding negative water.** In Trapping Rain Water, subtracting before updating the running max can go negative. Fix: update the max first, then add `max - height`.
10. **Sorting when indices matter.** Fix: if the answer is "the original positions", sort pairs of `(value, index)` or use a hash map.

## The journey ahead

The ten problems climb from "two indices and one comparison" to "two indices, one bookmark and a dominance proof". Each one keeps something from the problem before it and adds exactly one new idea.

### Warm-up: one walk, one rule

**Valid Palindrome.** The puzzle looks too easy to be one: compare a string with its reverse. The catch is that punctuation and case do not count, so building a cleaned copy costs O(n) extra space, and the interviewer will ask you to drop it. Two mirror pointers that skip junk on their own side do the comparison in place. This is the converging geometry at its simplest: every step settles one pair of mirror cells for good.

**Move Zeroes.** Now the pointers walk the same way. The naive move is to delete each zero and append it, which shifts the tail every time and costs O(n^2). A reader that looks at everything and a writer that only advances on a kept value do it in one pass. The new idea is the region picture (kept, junk, unread), and the swap that carries the zeros backward instead of overwriting them.

**Squares of a Sorted Array.** Squaring breaks the sorted order, because a large negative becomes a large square. Sorting again works but wastes the order you were given. The question to ask is where the largest square can be: only at one of the two ends. So the converging pointers return, but now they **produce output**, filling a result from the back. It is the first taste of the merge-from-the-back pattern.

### Writers with memory

**Remove Duplicates from Sorted Array II.** At most two copies of each value, in place. A counter of "how many of this value have I kept" works, but it is fiddly at value boundaries. The new idea is that the writer can ask its own output: if the cell two behind the writer already holds this value, a third copy is not allowed. The look-back into the certified region replaces the counter, and the same line handles any k.

**Sort Colors.** Three values, one pass, no counting sort. One writer is no longer enough, so a second writer grows from the right end, and the reader sits between them. The puzzle is the asymmetry: after a swap with the left writer the reader advances, but after a swap with the right writer it must look again. That asymmetry is the whole Dutch flag invariant, with four regions kept straight by three pointers.

### Pruning the pair grid

**Two Sum II.** Sorted input, find the pair with a given sum. The brute force checks all n^2/2 pairs. The question is why moving one pointer per comparison never skips the answer, and the answer is the staircase picture: each comparison deletes a whole row or column of pairs. This is where the chapter's central argument is made explicit.

**3Sum.** Triples instead of pairs, unsorted input, and no duplicate triples in the output. Fixing one element turns the rest into Two Sum II, so the new idea is the reduction: sort, anchor, run the staircase on the suffix. Sorting earns its keep twice, because duplicates become neighbours and the dedup becomes "skip if equal to the previous one".

**Container With Most Water.** Same pair grid, but the input is **not** sorted, so the monotone fact must come from somewhere else. It comes from geometry: the shorter wall caps the height, and every other partner is closer, so the shorter wall's row is dead. The new idea is the discard-the-weaker-side proof, which needs no sorting at all.

### The Hard end

**Trapping Rain Water.** Instead of choosing one best pair, every cell holds water, and each cell's level depends on the tallest bars on **both** sides. Two prefix-max arrays give O(n) space; the challenge is O(1). The shorter-side argument from Container returns with a twist: the bar under the far pointer is a lower bound on the far side's maximum, which is enough to settle the near cell immediately.

**Wildcard Matching.** Pointers on two different strings, and a `*` that can swallow any run of text. The natural solution is a recursion over how much each star eats, or a 2D DP table. The question a curious person asks is: when a match fails, which earlier choice do I really need to revisit? The answer is "only the latest star", and that dominance fact collapses the search into two pointers and one bookmark that only moves forward. It is the chapter's argument in its most general form.
