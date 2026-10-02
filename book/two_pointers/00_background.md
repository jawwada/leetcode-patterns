# Two Pointers
*10 problems · Reading time ~14 min*

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

1. **Valid Palindrome** introduces converging pointers in their simplest form: compare mirror cells, skip junk, stop at the first mismatch.
2. **Move Zeroes** introduces the reader/writer geometry and the idea that a swap can carry the discarded values along.
3. **Squares of a Sorted Array** converges again, but now the pointers produce output, and the monotone property (largest absolute value is at an end) decides which side moves.
4. **Remove Duplicates from Sorted Array II** adds the fast/slow look-back: the slow writer checks its own output two cells back instead of counting.
5. **Sort Colors** uses three pointers: one reader and two writers growing from opposite ends, with four regions to keep straight.
6. **Two Sum II** makes the pruning argument explicit: each comparison against the target deletes a row or column of the pair grid.
7. **3Sum** wraps Two Sum II in an outer loop after sorting and shows how sorted order also makes deduplication a local check.
8. **Container With Most Water** drops sorting and replaces it with a geometric monotone fact: the shorter wall can never be part of a better pair.
9. **Trapping Rain Water** reuses that fact with running maxima, so each pointer step settles one cell's water permanently.
10. **Wildcard Matching** closes the chapter with pointers on two strings and a single bookmark, justified by a dominance argument: the most recent `*` can do anything an earlier one could.
