# Online Majority Element In Subarray

*LeetCode 1157 · Hard · Pattern: Value -> sorted positions + randomized sampling with bisect verification · Reading time ~11 min*

## What the problem is really asking

You get an array once. Then many queries arrive, each naming a subarray `arr[left..right]` and a threshold. Return the
element that occurs at least `threshold` times inside that subarray, or -1 if none does. The problem promises
`2 * threshold > right - left + 1`: the threshold is more than half the subarray's length. So any answer is a strict
majority, and there can be at most one.

The answer is a single value or -1. What makes it hard is "online": queries cover arbitrary ranges, there are up to
10^4 of them on an array of up to 2·10^4, and counting every element of every range is too slow.

```text
arr:    1  1  2  2  1  1
index:  0  1  2  3  4  5

query(0,5,4): [1 1 2 2 1 1]  1 appears 4 times      -> 1
query(0,3,3): [1 1 2 2]      best is 2 times < 3    -> -1
query(2,3,2):     [2 2]      2 appears 2 times      -> 2
```

## Do it by hand first

Look at `query(0,5,4)` on paper. You would not tally every value. You would glance at the range, see a lot of 1s, and
then count the 1s to confirm: four of them, threshold four, done. The glance proposed a candidate; the count verified it.

The verifying count is itself something you can speed up. If, before any query, you wrote down for each value the list
of positions where it appears, counting a value inside `[left, right]` becomes "how many of my positions fall in this
window?"

```text
positions by value:
  1 -> [0, 1, 4, 5]
  2 -> [2, 3]

count of 1 in [0,5]: positions 0,1,4,5 all inside -> 4
count of 2 in [0,3]: positions 2,3 inside          -> 2
```

Since each list is sorted, "how many fall in the window" is two binary searches. Your hand kept two things: a cheap
way to guess a candidate, and a value-to-positions index to check it. That is the whole design.

## The first honest attempt

For each query, build a counter over `arr[left..right]` and take the most common element. That is O(length) per query,
O(n · q) in total, around 2·10^8 at the limits.

A slightly smarter brute force runs Boyer-Moore voting over the range to get one candidate in O(1) space, then counts
it. Still O(length) per query.

The repeated work is the same elements being read over and over by overlapping queries, all to find one value:

```text
query(0,5): reads 1 1 2 2 1 1
query(0,3): reads 1 1 2 2        <- re-reads 4 cells
query(2,3): reads     2 2        <- re-reads 2 cells

every query re-tallies values it has seen before,
mostly to rule out values that cannot be the answer
```

Counting all values to find the single dominant one is overkill. If you could produce a good candidate cheaply, a
two-bisect check would finish the job.

## The turning point

**Claim: if a value fills more than half of the range, a uniformly random position in the range lands on it with
probability greater than 1/2, so 20 random samples all miss it with probability less than 2^-20.**

That claim splits the problem into "guess" and "check".

**The check is exact and cheap.** Build `pos[v]` = sorted list of indices where `arr[i] == v`, once, in O(n). Then the
number of occurrences of v in `[left, right]` is

```text
count(v) = bisect_right(pos[v], right)
         - bisect_left(pos[v], left)
```

`bisect_left(pos[v], left)` counts positions strictly before `left`; `bisect_right(pos[v], right)` counts positions
at or before `right`. The difference is the positions inside the window. O(log n).

```text
pos[1] = [0, 1, 4, 5],  window [0, 3]
          ^  ^  |
          in in  out
bisect_left(.., 0)  = 0     (none before 0)
bisect_right(.., 3) = 2     (0 and 1 are <= 3)
count = 2 - 0 = 2
```

**The guess is a coin with good odds.** Pick a random index i in `[left, right]` and take `v = arr[i]`. If a majority
element exists, it occupies more than half the slots, so `P(v is the majority) > 1/2`. Check v. If it meets the
threshold, return it. Otherwise sample again.

```text
range of length 6, majority 1 occupies 4 slots:
  [1 1 2 2 1 1]
   *   *   * *    4 of 6 slots hit the answer
  each sample: P(miss) = 2/6 < 1/2
  20 samples:  P(all miss) < (1/2)^20 ~ 1e-6
```

Three properties make this safe.

1. **No false answers.** Every returned value passed an exact count, so if the method returns v, v really meets the
   threshold.
2. **No false -1 when there is no majority.** If nothing meets the threshold, every check fails, and after 20 tries
   the answer -1 is correct.
3. **The only error** is returning -1 when a majority exists but all 20 samples missed it: probability under one in a
   million per query.

Why is this "being big makes you easy to find" idea so effective here? Because the threshold condition is exactly the
condition that makes sampling work. A plurality that is only 30% of the range would need more samples; a strict
majority needs a constant number. The randomness is in how fast the answer is found, not in whether a returned answer
is correct.

The solution file seeds its random generator so runs are reproducible, and samples with `randint(left, right)`,
which includes both ends. (Python's `randrange(left, right)` excludes `right`, a classic off-by-one.)

There is a deterministic alternative: a segment tree whose nodes store a Boyer-Moore (candidate, count) pair. Two
pairs merge by cancelling: same candidate adds counts, different candidates subtract and the larger survives. A range
query merges O(log n) nodes to produce one candidate, which is then verified with the same bisect count. That gives
O(log^2 n) per query with no randomness, at the cost of more code.

## Watch it work

`arr = [1, 1, 2, 2, 1, 1]`. The samples below are the ones the seeded generator in the solution actually draws.

Frame 1: build the index.

```text
arr:   1  1  2  2  1  1
idx:   0  1  2  3  4  5

pos[1] = [0, 1, 4, 5]
pos[2] = [2, 3]
```

One pass, each index appended to its value's list, so the lists are born sorted.

Frame 2: `query(0, 5, 4)`, first two samples miss.

```text
sample idx 3 -> v = 2
  pos[2] = [2,3]: right(5)=2 - left(0)=0 -> 2 < 4  miss
sample idx 3 -> v = 2
  same count 2 < 4                                 miss
```

Here `right(x)` is shorthand for `bisect_right(pos[v], x)` and `left(x)` for `bisect_left(pos[v], x)`. Two of six
slots hold 2, and the sampler happened to land there twice. Each miss costs only two bisects.

Frame 3: third sample hits.

```text
sample idx 0 -> v = 1
  pos[1] = [0,1,4,5]: right(5)=4 - left(0)=0 -> 4 >= 4
return 1
```

The check confirms the candidate exactly; we stop at the first success.

Frame 4: `query(0, 3, 3)`, no majority exists.

```text
window [0,3]: 1 1 2 2
count(1) = right(3)=2 - left(0)=0 = 2 < 3
count(2) = right(3)=2 - left(0)=0 = 2 < 3
samples drawn: 2,3,3,2,3,2,1,1,2,1,0,2,1,2,0,0,2,3,0,2
every sample is 1 or 2, every check fails
after 20 samples -> return -1
```

All twenty samples fail because there is nothing to find, and -1 is correct.

Frame 5: `query(2, 3, 2)`.

```text
window [2,3]: 2 2
sample idx 3 -> v = 2
  pos[2] = [2,3]: right(3)=2 - left(2)=0 -> 2 >= 2
return 2
```

A range that is entirely one value is found on the first try with certainty.

Across frames, `pos` never changed (the array is static), and every returned value had passed an exact count. The only
thing that varied was how many guesses a query took.

## Why it is correct

The invariant is static: `pos[v]` is the sorted list of indices holding v, so the bisect difference is exactly the
number of occurrences of v in the window. That makes each check exact.

If the query returns some v, v passed the check, so v occurs at least `threshold` times. Since the threshold is more
than half the window, v is the unique valid answer.

If a majority element m exists, each sample independently equals m with probability `p > 1/2`. The method fails only if
all 20 samples miss, probability `(1 - p)^20 < 2^-20`. When m does not exist, no check can pass, and -1 is returned,
which is correct. So the algorithm is always correct when it returns a value, and correct with probability above
`1 - 10^-6` when it returns -1. For a deterministic guarantee, use the segment tree of Boyer-Moore pairs.

## Cost

- Build: O(n) time and O(n) space for the position lists.
- Query: at most t = 20 samples, each O(1) to draw plus O(log n) to verify: O(t log n), effectively O(log n).
- Deterministic alternative: O(n) build for the segment tree, O(log n) merge plus O(log n) verify per query.

Compared with O(length) per query for counting, this removes the dependence on the range length entirely.

## Variations you will meet

- **Majority Element (LeetCode 169) and Majority Element II (229).** One fixed array, one query. Boyer-Moore voting
  finds the candidate in O(1) space; the version for more than n/3 keeps two candidates.
- **Count occurrences of x in a range, many queries.** Exactly the bisect count on `pos[x]` with no sampling. This is
  the same "sorted list per key, bisect" trick as Time Based Key-Value Store.
- **Threshold not above half.** Sampling loses its guarantee: an element filling 10% of the range needs about 200
  samples for the same error. Then use frequency-based structures (sqrt decomposition, Mo's algorithm offline).
- **Updates to the array.** Position lists must support insert and delete (sorted containers), and the segment tree of
  Boyer-Moore pairs supports point updates naturally.

## What to carry forward

Guess cheaply, verify exactly: a strict majority is hit by a random sample more than half the time, and a value's
sorted position list turns "how many in this range" into two bisects. The next problem, Design Movie Rental System,
keeps the theme of many queries over a changing collection, but now the question is "top five cheapest", and the
tool is heaps whose stale entries are discarded lazily by version stamp.
