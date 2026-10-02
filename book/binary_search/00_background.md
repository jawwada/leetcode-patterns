# Binary Search

*16 problems · Reading time ~16 min*

## Why this chapter exists

Binary search is usually introduced as "find a number in a sorted array". That is the smallest thing it does. The real
skill is this: whenever you can ask a yes/no question about a position, and every "yes" comes before every "no", you can
find the place where the answer flips in about `log2(n)` questions. For a million positions that is 20 questions. For a
range of values up to a billion it is 30.

The sixteen problems in this chapter are all that one skill, wearing different clothes:

- **Exact lookup in sorted data.** Is the target here, and where (binary search, search a 2D matrix).
- **Boundaries.** Not "is it here" but "where does the run of small values end" (search insert position, first and last
  position).
- **Two sorted runs glued together.** A rotated array is sorted except for one cliff; find the cliff or search around it
  (find minimum in rotated array, search in rotated array).
- **Slopes instead of values.** Compare a cell with its right neighbour, and the sign of the slope tells you which way a
  peak lies (find peak element, find in mountain array).
- **Binary search on the answer.** The array is not sorted at all, but the answer is a number, and "can I do it with value
  x?" is monotone in x (Koko, magnetic balls, split array, running time of computers).
- **Counting below a guess.** To find the k-th smallest of a huge implicit set, guess a value and count how many items are
  at most that value (multiplication table, smallest pair distance).
- **A real-valued answer.** Search over a continuous range and stop at a precision (maximum average subarray II).
- **Searching a cut, not a value.** Choose how many elements of one array go left of the median line (median of two
  sorted arrays).

## What it is

Start with the only picture you need. Line up the candidate positions left to right. Next to each one write the answer to
a yes/no question `P(i)`. Binary search works whenever that row looks like this:

```text
index:   0   1   2   3   4   5   6   7
P(i):    T   T   T   T   F   F   F   F
                         ^
                 first F = the answer
```

All the T's come first, all the F's after. Nothing else is required: not sortedness, not distinct values, not even an
array. Sortedness is just one common way to get such a row. If `nums` is sorted and `P(i)` is `nums[i] < target`, the row
is T's (too small) followed by F's (big enough), and the first F is exactly where the target is or would go.

```text
nums:    1   3   4   6   8   9  11  14      target = 8
P(i):    T   T   T   T   F   F   F   F      P(i) = nums[i] < 8
                         ^
                 first F = index 4 (nums[4] == 8)
```

The state the technique maintains is two indices, `lo` and `hi`, with a promise: the first F lies in the half-open range
`[lo, hi)` or is `hi` itself if everything left of `hi` is T. Start with `lo = 0` and `hi = n`. The value `hi = n` stands
for "after the last cell", which is the honest answer when every cell is T (the target is larger than everything).

```text
         lo                                  hi
         v                                   v
index:   0   1   2   3   4   5   6   7   |   8
P(i):    ?   ?   ?   ?   ?   ?   ?   ?   |  (past the end)
         <------- first F is somewhere in here, or at 8 ------->
```

Probe the middle. If `P(mid)` is T, then mid and everything left of it is T (that is what monotone means), so the first F
is strictly right of mid: `lo = mid + 1`. If `P(mid)` is F, mid might be the first F, or the first F is further left:
`hi = mid`. Here is the whole template; every problem in the chapter is a variation of these six lines.

```text
lo, hi = 0, n
while lo < hi:
    mid = (lo + hi) // 2
    if P(mid): lo = mid + 1  # T: answer right of mid
    else:      hi = mid      # F: mid may be the answer
return lo                    # lo == hi == first F (or n)
```

**Why it cannot loop forever.** Inside the loop `lo < hi`, so `mid = (lo + hi) // 2` satisfies `lo <= mid < hi`. The
floor division rounds down, so mid can equal lo but never hi. Then `lo = mid + 1` makes lo strictly bigger, and
`hi = mid` makes hi strictly smaller. The gap `hi - lo` shrinks by at least one every round, and in fact roughly halves.
A shrinking non-negative integer must reach zero. When it does, `lo == hi`, and the promise says the first F is there.

A useful by-product: because mid is always strictly less than hi, the template never evaluates `P(n)`. You never index
`nums[n]`, even though `hi` starts at n.

**Lower bound and upper bound.** Two predicates cover almost every lookup in a sorted array:

```text
nums:          2   4   4   4   7   9
index:         0   1   2   3   4   5   (6 = end)

nums[i] <  4:  T   F   F   F   F   F   first F = 1  lower_bound
nums[i] <= 4:  T   T   T   T   F   F   first F = 4  upper_bound

run of 4s = [lower_bound, upper_bound - 1] = [1, 3]
count of 4s = upper_bound - lower_bound = 3
```

Lower bound is "first index whose value is at least x". Upper bound is "first index whose value is greater than x". The
run of copies of x lives between them. If they are equal, x is absent and both point to where x would be inserted.

**Binary search on the answer.** Now throw the array away. Suppose the question is "what is the slowest eating speed
that finishes all bananas in h hours?" The positions are no longer indices; they are candidate speeds 1, 2, 3, ... up to
the largest pile. Ask `P(k)` = "is speed k too slow?" Too slow at speed k means too slow at every smaller speed, so the
row is T's then F's again:

```text
speed k:   1   2   3   4   5   6   7   8   ...  max
too slow:  T   T   T   F   F   F   F   F   ...   F
                       ^
               first F = minimum speed that works
```

The template does not care that the positions are speeds. It needs a range `[lo, hi)` of candidates and a predicate that
you can evaluate at any candidate, usually by a greedy simulation in O(n). Total cost: O(n log(range)).

**Rotated arrays as two sorted runs.** `[4, 5, 6, 7, 0, 1, 2]` is a sorted array cut and swapped. Draw height against
index and you see two rising ramps with a cliff between them. Every element of the left ramp is larger than every element
of the right ramp, so `P(i)` = "nums[i] > nums[last]" is T on the high ramp and F on the low ramp: monotone again, and its
first F is the minimum.

```text
value
  7 |          *
  6 |       *
  5 |    *
  4 | *
  2 |                               *
  1 |                         *
  0 |                   *
    +--------------------------------- index
      0  1  2  3        4     5     6
P:    T  T  T  T        F     F     F     P = nums[i] > nums[6]
```

**Peaks as slope sign.** For "find any peak", ask `P(i)` = "nums[i] < nums[i+1]", that is, "is the ground rising to the
right of i?" The row is not monotone in general (T F T T F...), but it has a weaker property that is enough: if `P(mid)`
is T, a peak exists strictly to the right; if it is F, a peak exists at mid or to the left. The window keeps a peak
inside it, which is all the template needs.

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| One probe (evaluate `P(mid)`) on a sorted array | O(1) | one comparison |
| Exact lookup / lower bound / upper bound | O(log n) | window halves per probe |
| Find the cliff of a rotated array | O(log n) | compare mid with the right end |
| Find a peak | O(log n) | follow the rising slope |
| Binary search on an answer range of size R | O(log R) probes | the range halves |
| One feasibility probe on the answer | usually O(n) | greedy pass over the input |
| Whole "search on the answer" | O(n log R) | probes times probe cost |
| `bisect_left` / `bisect_right` | O(log n) | the same template in C |
| Insert into a Python list at a found index | O(n) | elements shift right |

The probe itself, drawn for `P(i) = nums[i] < 8` on the eight-element array above:

```text
 idx  0  1  2  3  4  5  6  7  8
 P    T  T  T  T  F  F  F  F  (end)

round 1: lo=0 hi=8 mid=4   P(4): 8<8 F  -> hi=4
      L           M           H
round 2: lo=0 hi=4 mid=2   P(2): 4<8 T  -> lo=3
      L     M     H
round 3: lo=3 hi=4 mid=3   P(3): 6<8 T  -> lo=4
               LM H
end:  lo=4 hi=4 -> answer 4        L = lo, M = mid, H = hi
```

Three probes for eight cells. Each probe cut the window in half and never threw away the first F.

The closed-interval cousin is the "exact lookup" form some solutions in this chapter use. It keeps `[lo, hi]` inclusive,
loops `while lo <= hi`, returns early on equality, and moves `lo = mid + 1` or `hi = mid - 1`. It terminates for the
same reason: both updates move a bound past mid, so the window loses at least one cell per round. It ends with `lo > hi`
(empty window, target absent) and at that moment `lo` is the lower bound.

```text
closed  [lo, hi]:  while lo <= hi   lo = mid+1   hi = mid-1
half-open [lo,hi): while lo <  hi   lo = mid+1   hi = mid
```

Never mix the columns. `while lo <= hi` with `hi = mid` loops forever when `lo == hi == mid`.

## The invariant

Everything rests on one sentence:

**Everything left of `lo` is known T, everything at or right of `hi` is known F (or past the end), and the cells in
between are unknown.**

```text
legal state:
 idx  0  1  2  3  4  5  6  7 | 8
      T  T  T  ?  ?  ?  F  F |
               lo       hi
      known T  unknown  known F
```

Each probe turns the unknown middle cell into known and pushes a bound to it. When the unknown zone is empty, `lo` sits on
the first F. Here is a state that breaks the promise:

```text
illegal state (after a wrong "hi = mid - 1"):
 idx  0  1  2  3  4  5  6  7 | 8
      T  T  T  T  F  F  F  F |
      lo       hi
                  ^ the first F (4) is now outside [lo, hi)
```

If `P(mid)` was F at mid = 4 and you set `hi = mid - 1 = 3`, the window `[0, 3)` no longer contains the answer. The loop
will still finish and return something, just the wrong thing. Every off-by-one bug in binary search is a moment where an
update throws away a cell that could still be the answer.

That gives you the discipline for writing any update. Ask of each branch: "is mid itself still a possible answer?" If
yes, the bound moves *to* mid. If no, it moves *past* mid. Then check that the loop condition and the mid rounding make
progress with that pair of updates.

There is one asymmetric case to remember. If you are looking for the *last* T (the largest speed that is still valid,
the largest gap that still fits all balls), the natural updates are `lo = mid` (mid is T, keep it) and `hi = mid - 1`.
With floor division, `lo = mid` can leave lo unchanged when `hi = lo + 1`, and you loop forever. Round mid up instead:
`mid = (lo + hi + 1) // 2`. Or keep the standard template and return `first F - 1`.

## How to picture it

Carry the row of T's and F's. Every problem in this chapter, before you write a line, should be redrawn as:

```text
candidates:  c0  c1  c2  c3  c4  c5  c6  c7
P(c):         T   T   T   T   F   F   F   F
              <--- lo moves right    hi moves left --->
                          they meet on the first F
```

Then ask three questions:

1. What are the candidates? Indices of an array, flat positions of a grid, speeds, distances, times, or how many elements
   of one array go left of a cut.
2. What is P, and why does one T imply every candidate to its left is T? This is the proof of correctness; if you cannot
   say it, binary search is not justified.
3. Is the answer the first F, or the last T? (They are neighbours; pick one and stay with it.)

For the answer-search problems, the picture is a number line of values rather than array cells, and the cost of looking
at one cell is a whole simulation. For peaks, the picture is a landscape and P is "uphill to the right", and you always
walk toward higher ground.

## Signals in a problem statement

- "sorted", "non-decreasing", "rotated sorted", "each row sorted and the first of each row exceeds the last of the
  previous": a lookup or boundary search.
- "must run in O(log n)" or a budget of very few reads (100 calls to `get`): binary search almost certainly.
- "first", "last", "leftmost", "insert position", "smallest index such that": a boundary, not an exact match.
- "minimum possible maximum", "maximum possible minimum", "smallest speed / capacity / time such that": binary search on
  the answer with a greedy check.
- "k-th smallest" over an implicit set too large to list (all pairs, an m x n table): binary search on the value and count
  how many are at most the guess.
- Answer is a real number, "within 1e-5": binary search on a continuous range with a fixed number of iterations.
- Huge numeric bounds (values up to 1e9, n up to 1e5): log of the range is about 30, so O(n * 30) fits.
- Counter-signal: "contiguous subarray with sum/count property" and no monotone yes/no over a value usually means sliding
  window or prefix sums.
- Counter-signal: you need *all* matches, or the data changes between queries with inserts: consider a heap, a balanced
  structure, or a hash map.
- Counter-signal: the predicate goes T F T F with no structure (unlike peaks). Then halving can throw away the answer.

## Python toolbox

`bisect` implements exactly the two bounds:

```python
from bisect import bisect_left, bisect_right
a = [2, 4, 4, 4, 7, 9]
bisect_left(a, 4)    # 1: first index with a[i] >= 4
bisect_right(a, 4)   # 4: first index with a[i] >  4
bisect_left(a, 5)    # 4: where 5 would be inserted
```

Since Python 3.10 both take `key=`, and both accept any object with `len` and indexing, including `range`. That gives a
one-line binary search on the answer: search for the first candidate where the predicate flips to True.

```python
def feasible(k): ...          # monotone: F F F T T T
lo, hi = 1, 10**9
ans = bisect_left(range(lo, hi + 1), True, key=feasible) + lo
```

The `key` is applied to elements, not to the search value, so pass `True` (the value you look for) unconverted.
`insort` inserts and keeps a list sorted, but costs O(n) for the shift. For real-valued answers, loop a fixed number of
times instead of comparing floats:

```python
lo, hi = -1e4, 1e4
for _ in range(60):            # 2^-60 of the range: plenty
    mid = (lo + hi) / 2
    if ok(mid): lo = mid
    else:       hi = mid
```

Python integers never overflow, so `(lo + hi) // 2` is safe. In Java or C++ write `lo + (hi - lo) / 2`.

## Mistakes people make

1. `while lo <= hi` paired with `hi = mid`: when `lo == hi` the window never shrinks. Fix: `while lo < hi` with `hi = mid`.
2. `hi = mid - 1` when mid could be the answer (first F, minimum of a rotated array, a peak). Fix: move to mid, not past it.
3. `lo = mid` with floor division: infinite loop on a two-cell window. Fix: `mid = (lo + hi + 1) // 2`, or restate as
   first-F search.
4. Starting `hi = n - 1` when "insert at the end" is a valid answer. Fix: `hi = n` for boundary searches.
5. Reading `nums[lo]` after a boundary search without checking `lo < n` and `nums[lo] == target`. Fix: guard both.
6. Expanding linearly from a found index to find the run of duplicates: O(n) on `[x, x, ..., x]`. Fix: two bound searches.
7. In a rotated array, comparing mid with `nums[lo]` to find the minimum: ambiguous when `[lo, hi]` is already sorted.
   Fix: compare with `nums[hi]`.
8. On the answer range, a bad `hi`: too small excludes the answer (Koko with `hi = max(piles) - 1`). Fix: make `hi` a
   value you can prove is feasible.
9. Using a predicate that is not monotone ("can be done with exactly k parts" instead of "at most k"). Fix: phrase the
   check so feasibility is inherited by every larger (or smaller) candidate.
10. `divmod(mid, m)` instead of `divmod(mid, n)` when flattening a grid. Fix: divide by the row length.

## The journey ahead

1. **Binary Search**: the closed-interval exact lookup; the window halves and the target never leaves it.
2. **Search Insert Position**: "where would it go" turns lookup into a boundary, the first F of `nums[i] < target`.
3. **Find First and Last Position**: two boundaries, lower and upper bound, from one half-open template.
4. **Search a 2D Matrix**: the candidates are virtual positions; `divmod` folds a flat index back into the grid.
5. **Find Minimum in Rotated Sorted Array**: the predicate compares with the right end instead of a target.
6. **Search in Rotated Sorted Array**: at every mid one half is a clean ramp; decide by testing that half.
7. **Find Peak Element**: the predicate is a slope sign and is only locally monotone, but a peak stays in the window.
8. **Find in Mountain Array**: compose three searches (peak, ascending, descending) under a call budget.
9. **Koko Eating Bananas**: the first binary search on the answer; the candidates are speeds, P is a greedy count.
10. **Magnetic Force Between Two Balls**: maximize a minimum, so the answer is the last T; greedy placement as the check.
11. **Split Array Largest Sum**: minimize a maximum; the same greedy check counts pieces.
12. **Maximum Running Time of N Computers**: the check is a clever capped sum instead of a simulation.
13. **Kth Smallest Number in Multiplication Table**: binary search on a value, the check counts entries at most the guess.
14. **Find K-th Smallest Pair Distance**: the same counting idea, the count done by two pointers on a sorted array.
15. **Maximum Average Subarray II**: the answer is real; subtract the guess and test a prefix-sum condition.
16. **Median of Two Sorted Arrays**: the candidates are cut positions in the shorter array, P compares across the cut.
