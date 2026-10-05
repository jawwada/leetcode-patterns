# Binary Search

*16 problems · Reading time ~24 min*

## The chapter

Binary search finds the position where a yes/no answer flips, in logarithmic time, whenever every yes comes before
every no. This chapter teaches the one loop that never goes off by one, then applies it to exact lookups, boundaries,
rotated and mountain arrays, and finally to searching the answer space itself when the input is not sorted at all.

Problems, in reading order:

1. [Binary Search](binary_search.md) · Easy
2. [Search Insert Position](search_insert_position.md) · Easy
3. [Find First and Last Position of Element in Sorted Array](find_first_and_last_position.md) · Medium
4. [Search a 2D Matrix](search_2d_matrix.md) · Medium
5. [Find Minimum in Rotated Sorted Array](find_min_rotated_sorted_array.md) · Medium
6. [Search in Rotated Sorted Array](search_rotated_sorted_array.md) · Medium
7. [Find Peak Element](find_peak_element.md) · Medium
8. [Find in Mountain Array](find_in_mountain_array.md) · Hard
9. [Koko Eating Bananas](koko_eating_bananas.md) · Medium
10. [Magnetic Force Between Two Balls](magnetic_force_between_two_balls.md) · Medium
11. [Split Array Largest Sum](split_array_largest_sum.md) · Hard
12. [Maximum Running Time of N Computers](maximum_running_time_of_n_computers.md) · Hard
13. [Kth Smallest Number in Multiplication Table](kth_smallest_number_in_multiplication_table.md) · Hard
14. [Find K-th Smallest Pair Distance](find_kth_smallest_pair_distance.md) · Hard
15. [Maximum Average Subarray II](maximum_average_subarray_ii.md) · Hard
16. [Median of Two Sorted Arrays](median_of_two_sorted_arrays.md) · Hard

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

## Advanced patterns

The template above never changes. What changes in the harder problems is *what you search over* and *how you evaluate
one probe*. The six ideas below are what the second half of this chapter leans on. Each one is a way of manufacturing a
T...TF...F row where none is visible.

### 1. Minimize the maximum, maximize the minimum

**When it shows up.** The statement asks you to arrange things (cut an array into k pieces, place m balls, ship within
d days) so that the worst piece is as good as possible: "the largest sum is as small as possible", "the smallest gap is as
large as possible".

**The intuition.** Optimizing over every arrangement is hopeless: there are exponentially many ways to cut an array. But
if somebody hands you the answer and asks "can every gap be at least g?", a greedy pass decides it: put the first ball at
the first stall, then each next ball at the first stall at least g away. Placing a ball as early as allowed never hurts
later balls, so the greedy fits as many balls as any arrangement can. So stop optimizing and start *checking*. The
direction of the row tells you which end you want. For "maximize the minimum gap", a bigger g is harder, so the row is
T...T F...F and the answer is the last T. For "minimize the largest piece", a bigger cap is easier, so the row is
F...F T...T and the answer is the first T. The answer is always a value some real arrangement reaches: at the flip,
the greedy's tightest gap (or fullest piece) equals the guess exactly, otherwise the neighbouring guess would also work.

```text
stalls at 1 2 3 4 7, m = 3 balls, greedy check for gap g

coord :  1  2  3  4  5  6  7
stall :  *  *  *  *  .  .  *
g = 3 :  B  .  .  B  .  .  B     3 balls placed  -> T
g = 4 :  B  .  .  .  .  .  B     2 balls placed  -> F

g      :  1  2  3  4  5  6
balls  :  5  3  3  2  2  2
fits?  :  T  T  T  F  F  F
                ^ last T = 3, the largest minimum gap
```

**Where you'll use it.** Koko Eating Bananas, Magnetic Force Between Two Balls, Split Array Largest Sum. Beyond the
chapter: Capacity To Ship Packages Within D Days (LeetCode 1011).

### 2. A feasibility check that is a formula, not a simulation

**When it shows up.** The check has no obvious left-to-right greedy, because resources can be moved around freely over
time (batteries swapped between computers, workers that can switch tasks) and simulating schedules looks endless.

**The intuition.** Find a counting bound that every schedule must obey, then prove the bound is also enough. Running n
computers for t minutes needs `n * t` battery-minutes. A battery cannot sit in two computers in the same minute, so over
t minutes it contributes at most `min(b, t)`, no matter how large b is. That clamp is the whole insight. The condition
`sum(min(b, t)) >= n * t` is necessary, and a wrap-around packing shows it is sufficient, so the check is one line of
arithmetic. The tempting shortcut `sum // n` ignores the clamp and is wrong whenever one battery is huge: it pretends a
single battery can power two machines at once.

```text
n = 2 computers, batteries [10, 1, 1]
tempting answer: sum // n = 12 // 2 = 6

t   clamped min(b, t)   total   need n*t   can?
1   1 + 1 + 1             3        2        T
2   2 + 1 + 1             4        4        T
3   3 + 1 + 1             5        6        F
6   6 + 1 + 1             8       12        F
                    last T = 2, not 6
```

**Where you'll use it.** Maximum Running Time of N Computers; the hours count in Koko Eating Bananas is the same kind of
closed-form check. Beyond the chapter: Minimum Time to Complete Trips (LeetCode 2187).

### 3. K-th smallest by counting

**When it shows up.** "Find the k-th smallest" over a set far too large to list (all `m * n` cells of a multiplication
table, all `n(n-1)/2` pairwise distances), but with enough structure to count quickly how many members are at most v.

**The intuition.** You cannot ask "what value sits at rank k?" because the sorted list does not exist. Ask the reverse:
"what rank does value v reach?" That is `count(v)`, the number of members `<= v`, and it never decreases as v grows. So
`count(v) >= k` reads F...F T...T over v, and the first T is the k-th smallest. The search probes values that are not in
the set at all, and that is fine: count only jumps at real members, so the first T always lands on one. The new work in
each problem is the counting engine, a per-row formula `min(n, v // i)` for the table, a forward-only two-pointer sweep
over a sorted array for distances. The cost is log(value range) times one count, and it does not depend on k at all,
which is why this beats a heap that would pop k times.

```text
2 x 3 table        sorted bag: 1 2 2 3 4 6      k = 4
  1  2  3
  2  4  6

v          :  1  2  3  4  5  6
count(<=v) :  1  3  4  5  5  6    (5 is not in the table:
>= 4 ?     :  F  F  T  T  T  T     a flat step)
                    ^ first T = 3, the 4th smallest
```

**Where you'll use it.** Kth Smallest Number in Multiplication Table, Find K-th Smallest Pair Distance. Beyond the
chapter: Kth Smallest Element in a Sorted Matrix (LeetCode 378).

### 4. Real-valued answers: fix the guess, then subtract it

**When it shows up.** The objective is a ratio or an average ("largest average of a subarray of length at least k"), and
the answer is a real number accepted within a tolerance such as 1e-5.

**The intuition.** Averages do not decompose: the best average of the left half and of the right half tell you little
about the best average overall, so no scan-and-extend recurrence works. Fixing a guess x changes that. "Some subarray
has average at least x" is the same as "some subarray of `(v - x)` values has sum at least 0", and sums are what prefix
sums are built for: with `P` the prefix sums of the shifted values, you need `P[j] >= min(P[0..j-k])` for some j. The
guess is monotone (reaching x means reaching anything smaller), so the row over the real line is T...T F...F. On reals
there is no "next integer", so both updates go *to* mid (`lo = mid` on T, `hi = mid` on F) and the loop runs a fixed
number of halvings rather than testing float equality.

```text
nums = [4, 0, 6], k = 2          true answer 10/3 = 3.33

guess x = 3     shifted [1, -3, 3]
  P   = 0   1   -2   1
  j=3 : P3 = 1 >= min(P0, P1) = 0       -> T, lo = 3

guess x = 3.5   shifted [0.5, -3.5, 2.5]
  P   = 0   0.5   -3   -0.5
  j=2 : -3   < min(P0)     = 0
  j=3 : -0.5 < min(P0, P1) = 0          -> F, hi = 3.5
```

**Where you'll use it.** Maximum Average Subarray II. Beyond the chapter: Minimize Max Distance to Gas Station
(LeetCode 774).

### 5. Searching a cut across two arrays

**When it shows up.** You need the median, or any k-th element, of the union of two sorted arrays, in logarithmic time,
without merging them.

**The intuition.** The lower half of the union is a prefix of A plus a prefix of B, because anything before a small
element in its own sorted array is also small. If the lower half has `half` elements and i of them come from A, then
`j = half - i` come from B, so the whole search is over one number, i. A cut is valid when the two cross comparisons
hold: `A[i-1] <= B[j]` and `B[j-1] <= A[i]`. When the second fails you took too few from A and must move i right; when
the first fails you took too many and must move i left. "Too many" is false and then true as i grows, so it is a
monotone row again, with the valid cut sitting at the flip. Search the shorter array so j always stays inside B, and
treat missing neighbours at the ends as `-inf` and `+inf`.

```text
A = [1, 3, 8]   B = [2, 4, 5, 9, 10]   half = 4

i=1, j=3   A: 1 | 3 8          B[j-1] = 5 > A[i] = 3
           B: 2 4 5 | 9 10     too few from A -> i up
i=2, j=2   A: 1 3 | 8          3 <= 5 and 4 <= 8
           B: 2 4 | 5 9 10     valid cut
median = (max(3, 4) + min(8, 5)) / 2 = 4.5
```

**Where you'll use it.** Median of Two Sorted Arrays. Beyond the chapter: the k-th element of two sorted arrays, which is
the same search with `half` replaced by k.

### 6. Broken order: trust the clean half, or find the seam first

**When it shows up.** The array was sorted and then damaged in one controlled way: rotated (one cliff) or shaped like a
mountain (one summit). Often the statement adds a read budget or an O(log n) demand.

**The intuition.** One cliff can sit in at most one half, so at every mid at least one of `[lo, mid]` and `[mid, hi]` is a
clean sorted ramp, and `nums[lo] <= nums[mid]` tells you which. A range check like `nums[lo] <= target < nums[mid]` is
only trustworthy on a clean ramp, so make it there: if the target is inside the clean range, go into that half,
otherwise go into the other one, whatever it looks like. The other strategy is to find the seam first (the minimum of a
rotated array, the summit of a mountain, each a first-F search) and then run ordinary sorted searches on each piece.
That composition is how Find in Mountain Array fits in 100 reads: one summit search plus two slope searches, the left
slope first so a hit there is automatically the smaller index. Duplicates are the one thing that breaks the clean-half
test: when `nums[lo] == nums[mid] == nums[hi]` you cannot tell the halves apart and must shrink by one, which makes the
worst case O(n).

```text
idx :  0  1  2  3  4  5  6        target = 6
val :  4  5  6  7  0  1  2

round 1: lo=0 mid=3 hi=6   4 <= 7: left [4..7] clean
         4 <= 6 < 7, inside clean range    -> hi = 2
round 2: lo=0 mid=1 hi=2   4 <= 5: left [4..5] clean
         6 not in [4, 5)                   -> lo = 2
round 3: lo=2 mid=2 hi=2   val[2] = 6      -> found 2
```

**Where you'll use it.** Find Minimum in Rotated Sorted Array, Search in Rotated Sorted Array, Find in Mountain Array.
Beyond the chapter: Search in Rotated Sorted Array II (LeetCode 81), which adds duplicates.

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

The order follows one thread: first learn to trust the template on plain sorted data, then keep the template and change
what the row of T's and F's is made of, until in the last problem the candidates are not values at all but places to cut.

### Warm-up: one sorted array

**Binary Search.** The plain lookup: is the target in a sorted array, and where? It looks too easy to teach anything, but
it is where you prove to yourself that the closed window `[lo, hi]` never loses the target and always shrinks. Every later
problem quietly relies on that argument.

**Search Insert Position.** Now the target may be missing, and you must say where it would go. The equality check stops
being useful, and the question becomes a border: the first index where `nums[i] < target` turns false. The new idea is
that the answer can be n, one past the end, which is why the half-open window starts with `hi = n`.

**Find First and Last Position of Element in Sorted Array.** With duplicates, finding *a* copy is easy and finding the
run is the trap: stepping outwards from a hit costs O(n) on an array of identical values. The new idea is that both ends
of the run are borders, `lower(t)` and `lower(t + 1) - 1`, so one helper written once gives both.

**Search a 2D Matrix.** A grid sorted row after row is secretly one sorted list. The new idea is that the candidates do
not have to be stored in a list: a flat index `0 .. m*n - 1` is enough, and `divmod(mid, n)` folds it back into a cell.

### Broken order: rotations and slopes

**Find Minimum in Rotated Sorted Array.** The array is sorted except for one cliff, and you want the bottom of the cliff.
There is no target to compare with, so what do you compare mid against? The right end: values above it belong to the
high ramp. This is the first predicate that compares the array with itself.

**Search in Rotated Sorted Array.** Same array, but now a target. The naive move, comparing the target with mid, fails
because the array is not sorted across the cliff. The new idea is the clean-half test: at least one half is a sorted
ramp, and only there can you trust a range check.

**Find Peak Element.** No sortedness at all, and the predicate "is it rising to the right?" really does flip back and
forth. Why can binary search still work? Because following an uphill slope must end at a peak before the wall, so each
halving keeps some peak inside. The new idea is that you need an invariant that keeps *an* answer, not a globally
monotone row.

**Find in Mountain Array.** Now the array is hidden behind a `get` with a budget of 100 reads, and you need the smallest
index of a target on a mountain. It combines the last two ideas: a summit search, then an ascending and a descending
search. The new ideas are composing searches, searching in the order that gives the smaller index first, and caching
reads to stay in budget.

### Searching the answer

**Koko Eating Bananas.** Nothing here is sorted, yet the answer, a speed, sits in a range where "fast enough" switches on
once and stays on. This is the jump the whole chapter turns on: the candidates are values of the answer, and one probe
is an O(n) count of hours.

**Magnetic Force Between Two Balls.** "Maximize the minimum gap" sounds like it needs a search over placements. A guessed
gap turns it into a greedy check, and the row now runs T...T F...F, so the answer is the *last* T. The new idea is
handling the last-T direction without an infinite loop.

**Split Array Largest Sum.** The mirror image: minimize the largest piece. The greedy check counts pieces under a cap,
and the subtle point is phrasing it as "at most k pieces", which is monotone, instead of "exactly k", which is not. The
range `[max(nums), sum(nums)]` has to be argued, not guessed.

**Maximum Running Time of N Computers.** Here no greedy simulation is obvious, because batteries can be swapped any
minute. The new idea is a check that is a formula: clamp each battery at t and compare the total with `n * t`, with a
packing argument that proves the formula is enough.

### Counting and continuous answers

**Kth Smallest Number in Multiplication Table.** Up to `9 * 10^8` cells, so you cannot sort them. The new idea is to
search over values and turn each guessed value into a rank with a per-row count; the first value whose count reaches k
is the answer, even though many probed values are not in the table.

**Find K-th Smallest Pair Distance.** The same value-to-rank search, but the set is all pairwise distances. The new piece
is the counting engine: after sorting (allowed, because a distance does not care about order), a forward-only two-pointer
sweep counts pairs within d in O(n).

**Maximum Average Subarray II.** The answer is a real number and the objective is an average, which no scan can extend.
The new idea is to subtract the guess from every element so "average at least x" becomes "some sum at least 0", decided
by prefix minima, and to run the search on reals with a fixed number of halvings.

### The Hard end: searching a cut

**Median of Two Sorted Arrays.** The candidates are no longer values or positions but cut points: how many elements of
the shorter array go into the lower half. Everything from the chapter meets here: a monotone failure test ("too many from
A"), sentinels at the ends, choosing the shorter array to search, and an invariant that keeps the valid cut inside the
window. It runs in O(log min(m, n)) without merging anything.
