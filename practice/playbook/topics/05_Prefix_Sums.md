## Prefix Sums

> Write down the running total at every position once; then the sum of any stretch is the difference of two totals, like the distance between two towns read off a car's odometer. Questions about subarrays become questions about *pairs of totals*, and a list or a dict answers those in O(1).

[Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets) kept a notebook of what the walk had seen, keyed by what a later item would ask, and asked it before writing. Prefix sums put one new thing in that notebook, the running total, and "which stretches sum to k?" becomes Two Sum on those totals.

**Reach for it when** a problem asks about sums, products, counts or parities (odd or even) of *contiguous* stretches: many range-sum queries on one array, "count or longest subarrays with sum k", especially with negatives, where a [Sliding Window](07_Sliding_Window.ipynb#topic-sliding-window) fails, "product of everything except me", "equal number of 0s and 1s", "add v to every element in [l, r]" over and over, the sum of a rectangle in a grid, or a random pick weighted by sizes.

**In this repo:** `arrays_hashing/subarray_sum_equals_k.py`, `arrays_hashing/product_of_array_except_self.py`, `arrays_hashing/max_consecutive_ones.py` · bank: `practice/simple/05_subarray_sum_equals_k.py`, `practice/simple/03_product_of_array_except_self.py` · basics: `practice/simple/basics/bits/03_xor_tricks_single_number_missing_number.py` (why xor can be "subtracted") · the same idea elsewhere: `intervals/my_calendar_iii.py` (difference array, [Intervals & Sweep Line](16_Intervals_and_Sweep_Line.ipynb#topic-intervals-and-sweep-line)), `bit_manipulation/find_longest_awesome_substring.py` (prefix parity mask, taught below), `greedy/super_washing_machines.py` (prefix-sum flow), `greedy/maximum_subarray.py` (running sum, [Greedy](17_Greedy.ipynb#topic-greedy)), `design/range_sum_query_2d_mutable.py` (2D range sums with updates, [Design Problems](00_Topic_Index.ipynb#s24))

### The picture

Think of the totals as **fence posts between the items**: post `P[k]` stands just before item k and holds the sum of everything to its left.

```text
posts:     P0    P1    P2    P3    P4    P5
            |  3  |  1  | -2  |  4  |  1  |
totals:     0     3     4     2     6     7          P[k] = sum of the first k items

the items between two posts sum to (right post) - (left post):
items 1..3 = 1 + (-2) + 4 = 3 = P4 - P1 = 6 - 3
```

Items `l..r` sit between post `l` and post `r + 1`; that is where the famous `+ 1` comes from.

Why it is fast: the brute force adds the same items again for every (start, end) pair. Prefix sums do the adding once, in O(n); after that every range costs one subtraction.

The second half of the trick turns "for every start" into a dict lookup. To count stretches that sum to k, walk the posts from left to right and ask at each one: *how many earlier posts hold my total minus k?*

```text
k = 3       totals:  0   3   4   2   6   7
                     P0  P1  P2  P3  P4  P5

at P1 (3): look for 0   -> P0      items 0..0  = [3]
at P4 (6): look for 3   -> P1      items 1..3  = [1, -2, 4]
at P5 (7): look for 4   -> P2      items 2..4  = [-2, 4, 1]          3 stretches in one pass
```

The lookup never needs the totals to be in order, so negative numbers are fine. A sliding window would need the sum to grow every time the window grows.

### From idea to code

**The idea in one sentence:** *carry the running total as you walk; a stretch ending here sums to `total - (an earlier total)`, so a question about stretches becomes a question about one earlier total, which a list (by position) or a dict (by value) answers instantly.*

**Two Sum, term by term.** Subarray Sum Equals K looks up `total - k` where Two Sum ([Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets)) looks up `target - v`, and it *counts* instead of returning. The seed `{0: 1}` is post P0, the empty prefix, already in the notebook before the first item.

The seven decisions follow. The **State** is the running `total`, or the whole table `P` when the queries come later; to count stretches, add `posts[t]`, how many earlier posts hold the total `t`. The **Definition** is `P[k] = nums[0] + ... + nums[k-1]`, so `P[0] = 0` and `sum(nums[l..r]) = P[r + 1] - P[l]`. The **Invariant** holds between the query and the store: `total == P[j + 1]`, and `posts` holds exactly the earlier posts `P[0..j]`.

A **Step** is `total += x`, and the new total joins `posts` only after the query. The **Record** comes before that store, `found += posts.get(total - k, 0)`, so the current post cannot pair with itself. **Init** is `total = 0` and `posts = {0: 1}`, because the empty prefix is a real post, needed by every stretch that starts at index 0. The **Return** is `found`, 0 when nothing matched, or `P[r + 1] - P[l]` for each query.

**From the question to the code.** Most prefix-sum questions are this one loop with four knobs: what each item adds to the total, what you look up, what the dict stores, and its seed. The knobs come in three families, by what the dict stores.

Counting stores how many posts hold each total and seeds `{0: 1}`. Subarray Sum Equals K (560), the number of stretches with sum k, adds `x` and looks up `total - k`. Subarray Sums Divisible by K (974), the number of stretches whose sum is a multiple of k, adds `x` but keeps the total `% k`, and looks up the same remainder. Count Number of Nice Subarrays (1248), the number of stretches with exactly k odd numbers, adds `x % 2` and looks up `total - k`.

Longest stores the first index of each total and seeds `{0: -1}`. Maximum Size Subarray Sum Equals k (325), the longest stretch with sum k, adds `x` and looks up `total - k`. Contiguous Array (525), the longest stretch with as many 0s as 1s, adds `+1` for a 1 and `-1` for a 0, and looks up the same total. Continuous Subarray Sum (523), a stretch of length 2 or more whose sum is a multiple of k, keeps the total `% k` like 974 and needs `j - first >= 2`.

The longest family also runs on parities, with a bit mask as the total. Find the Longest Substring Containing Vowels in Even Counts (1371) flips a vowel's bit at each vowel and looks up the same mask. Find Longest Awesome Substring (1542), the longest stretch of digits that can be rearranged into a palindrome, keeps a 10-bit mask of digit parities and looks up the same mask or one that differs in exactly one bit, 11 lookups at each end.

Shortest stores the last index of each total, overwriting, with the same seed `{0: -1}`; the shortest stretch with sum k adds `x` and looks up `total - k`. When the dict stores indices, name each post by the item it follows: after item `j` the post is called `j`, and the empty prefix is called `−1`. The stretch after post `i` up to item `j` then has length `j − i`.

Two templates follow: a table for range queries, and the running total plus a dict for counting. Range Sum Query - Immutable (303) asks for the sum of `nums[l..r]` for many pairs (l, r), so "the total of the first k items" is `P[k]`, built item by item below or all at once as `P = [0] + list(accumulate(nums))`, and "the sum of items l..r, both included" is `P[r + 1] - P[l]`.

Subarray Sum Equals K asks how many contiguous subarrays sum to k, negatives allowed: `[3, 1, -2, 4, 1], k = 3 → 3`, the three stretches of the picture. "How many stretches ending here sum to k" is `posts.get(total - k, 0)`, "the empty prefix counts" is `posts = {0: 1}`, and "remember this post" is `posts[total] = posts.get(total, 0) + 1`, after the query. It is [From Idea to Code](02_Idea_to_Code.ipynb#topic-idea-to-code)'s `subarray_sum` with a plain dict and the picture's names.

<!-- cell -->

```python
def prefix_table(nums):
    P = [0] * (len(nums) + 1)                # STATE + INIT: P[k] = sum of the first k items; P[0] = 0
    for k, x in enumerate(nums):
        P[k + 1] = P[k] + x                  # STEP: one more item on the running total
    return P


def range_sum(P, l, r):                      # RETURN: sum of nums[l..r], both ends included
    return P[r + 1] - P[l]


def count_subarrays_with_sum(nums, k):
    posts = {0: 1}                           # STATE + INIT: total -> how many posts hold it; the empty prefix
    total = found = 0
    for x in nums:
        total += x                           # STEP: total = sum of everything up to and including x
        found += posts.get(total - k, 0)     # RECORD: each earlier post holding total - k starts a k-sum
        posts[total] = posts.get(total, 0) + 1   # STEP: this post joins AFTER the query
    return found                             # RETURN


P = prefix_table([3, 1, -2, 4, 1])
print(P, range_sum(P, 1, 3))                           # [0, 3, 4, 2, 6, 7] 3
print(count_subarrays_with_sum([3, 1, -2, 4, 1], 3))   # 3
```

<!-- cell -->

**Try it**
- Keep a *set* of totals instead of counts (`posts = {0}`, `found += (total - k) in posts`, `posts.add(total)`) and run `count_subarrays_with_sum([0, 0, 0], 0)`: 3 instead of 6. Equal totals are different starts, and each one is a separate answer.
- Predict `count_subarrays_with_sum([1, 2, 3], 3)` and name each stretch's earlier post (2: `[1, 2]` pairs with P0, `[3]` with P2).
- Predict `range_sum(P, 0, 4)` and `range_sum(P, 2, 2)` before running them (7, the whole array, and −2, a single item).

<!-- cell -->

### Watch it work

The trace counts the stretches of `[3, 1, -2, 4, 1]` that sum to 3, the three from the picture. Each line is one item, and `posts` is shown *before* the current post is stored, so every hit on a line is an earlier post that starts a stretch ending at that item.

<!-- cell -->

```python
def trace_count(nums, k):
    posts, total, found = {0: 1}, 0, 0
    for j, x in enumerate(nums):
        total += x
        hits = posts.get(total - k, 0)
        found += hits
        print(f"j={j}  x={x:>2}  total={total:>2}  look for {total - k:>2}: {hits} hit(s)  found={found}   posts={posts}")
        posts[total] = posts.get(total, 0) + 1
    return found


print(trace_count([3, 1, -2, 4, 1], 3))   # 3
```

<!-- cell -->

**Try it**
- Run `trace_count([0, 0, 0], 0)`: the hits are 1, 2 and 3, for a total of 6. Every pair of equal totals is one zero-sum stretch.
- Run `trace_count([1, -1, 1, -1], 0)` and match each hit to the earlier post it pairs with (4 stretches in all).
- Predict the answer before running `trace_count([3, 1, -2, 4, 1], 4)` (3: `[3, 1]`, `[4]` and `[1, -2, 4, 1]`).

<!-- cell -->

### Where it goes wrong

1. **The empty prefix, and the order of the two dict lines.** Both are [From Idea to Code](02_Idea_to_Code.ipynb#topic-idea-to-code) lessons: without `{0: 1}`, `[3]` with k = 3 gives 0; storing before the query makes `[1]` with k = 0 give 1.
2. **Off by one in ranges.** `sum(nums[l..r]) = P[r + 1] - P[l]`. `P[r] - P[l]` leaves out item r: items 1..3 of the picture give −1 instead of 3. `P[r + 1] - P[l - 1]` adds item l − 1, and at l = 0, `P[-1]` silently reads the *last* total.
3. **First, last, or how many?** Counting stores how many posts hold each total. *Longest* keeps the **first** index (store only when absent, in its own `if`, not an `else`); *shortest* keeps the **last** (always overwrite). Contiguous Array asks for the longest stretch with as many 0s as 1s; overwriting there turns `[0, 1, 0, 1]` into 2 instead of 4.
4. **Including yourself in a left-right pass.** Product of Array Except Self gives every index the product of all the *other* numbers. Multiply `nums[i]` into the running product *after* stamping `out[i]`, in both passes; otherwise `[1, 2, 3, 4]` gives `[24, 48, 72, 96]`. And skip division: it fails on zeros.
5. **Ragged 2D borders.** Without a border, the index −1 at row 0 or column 0 wraps around to the far side instead of meaning zero: built in an R × C table, `[[1, 2], [3, 4]]` reaches a total of 7 instead of 10. Give the table an extra zero row and column, `(R + 1) × (C + 1)`; then no `if r > 0` cases are needed and the build is `cell + up + left - up_left`.
6. **Difference array: one slot short, or the wrong end.** `diff[r + 1] -= v` needs `n + 1` slots, or an update that ends at the last index raises `IndexError`. For half-open ranges `[start, end)` the −v goes at `end` itself: treating `end` as included makes `[10, 20)` and `[20, 30)` overlap at 20.

### Edge cases to say out loud

Empty input · one item equal to k · `k = 0` · all zeros (many overlapping answers) · negatives · the whole array is the answer · no answer at all. The asserts below run each case through the two templates.

<!-- cell -->

```python
assert count_subarrays_with_sum([], 0) == 0
assert count_subarrays_with_sum([3], 3) == 1               # needs the {0: 1} seed
assert count_subarrays_with_sum([1], 0) == 0               # query before store
assert count_subarrays_with_sum([0, 0, 0], 0) == 6         # all 6 stretches
assert count_subarrays_with_sum([1, -1, 1, -1], 0) == 4    # negatives are fine
assert count_subarrays_with_sum([1, 2, 3], 7) == 0         # no answer
assert prefix_table([]) == [0]                             # one post, no items
assert range_sum(prefix_table([5]), 0, 0) == 5
print("edge cases pass")
```

<!-- cell -->

**Try it**
- Predict `count_subarrays_with_sum([0], 0)` before running it (1: the single 0 pairs with the empty prefix).
- Predict, then add: `assert count_subarrays_with_sum([1, 2, 3], 6) == 1` (only the whole array).
- A negative k works too: predict `count_subarrays_with_sum([-1, -1, 1], -2)` (1: the first two items).

<!-- cell -->

### Variations

Every variation keeps the running value and changes what it feeds: a dict, an output array, a grid, a list of changes or a binary search. The table is the overview.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Range sum queries** | build `P` once; each query is `P[r + 1] - P[l]` | Range Sum Query - Immutable (303) |
| **The dict recipes** | change what an item adds, what you look up and what the dict stores (the three families above) | Subarray Sum Equals K (560), Maximum Size Subarray Sum Equals k (325), Contiguous Array (525), Subarray Sums Divisible by K (974), Continuous Subarray Sum (523), Count Number of Nice Subarrays (1248), Find the Longest Substring Containing Vowels in Even Counts (1371), Find Longest Awesome Substring (1542) |
| **Left-right passes** | carry a running value from each side. 238 stamps before multiplying (never include yourself); 42 includes the bar in its max, so `min(L, R) - h` is never negative | Product of Array Except Self (238); Trapping Rain Water (42): the water a row of bars holds after rain |
| **Running value that resets** | carry `run`; a wall resets it to 0; record the max inside the run | Max Consecutive Ones (485): the longest run of 1s |
| **2D prefix sums** | `(R + 1) × (C + 1)` table; a rectangle is four corners, inclusion–exclusion | Range Sum Query 2D - Immutable (304): the sum of any rectangle, many times over; Number of Submatrices That Sum to Target (1074): how many rectangles sum to a target |
| **Difference array** | range update: `diff[l] += v`, `diff[r + 1] -= v` (half-open: at `end`); one prefix sum rebuilds the values | Range Addition (370): many "add v on l..r", then the final array; Corporate Flight Bookings (1109): the seats booked on each flight; Car Pooling (1094): does the car ever exceed its capacity; My Calendar III (732): the most bookings that overlap at once |
| **Prefix sums + binary search** | positive weights make the totals increasing, so `bisect` finds whose ticket was drawn | Random Pick with Weight (528): an index drawn in proportion to its weight |

**Longest instead of count; remainders instead of totals.** The first variation keeps the loop and changes what the dict stores. Maximum Size Subarray Sum Equals k asks for the *longest* stretch with sum k: `[1, -1, 5, -2, 3], k = 3 → 4`, the stretch `[1, -1, 5, -2]`. Keep the *first* index of each total, because the earliest start gives the longest stretch: a hit measures `j - first[total - k]`, and a total is stored only the first time it shows up.

Contiguous Array, the longest stretch with as many 0s as 1s, is the same function with every 0 turned into −1 and k = 0. Subarray Sums Divisible by K counts the stretches whose sum is a multiple of k: `[4, 5, 0, -2, -3, 1], k = 5 → 7`. Two posts with the same remainder are a multiple of k apart, so `count_divisible` keeps the total as a remainder and looks up that remainder itself; everything else is the counting template.

<!-- cell -->

```python
def longest_with_sum(nums, k):               # 325; 525 is this on +1 / -1 with k = 0
    first = {0: -1}                          # STATE + INIT: total -> FIRST post (item index) holding it
    total = best = 0
    for j, x in enumerate(nums):
        total += x                           # STEP
        if total - k in first:               # RECORD: the earliest post that leaves exactly k
            best = max(best, j - first[total - k])
        if total not in first:               # STEP: store the first time only, and NOT as an else
            first[total] = j
    return best


def count_divisible(nums, k):                # 974: stretches whose sum is divisible by k
    posts = {0: 1}                           # STATE + INIT: remainder -> how many posts hold it
    total = found = 0
    for x in nums:
        total = (total + x) % k              # STEP: Python's % stays in 0..k-1 for k > 0, even for negatives
        found += posts.get(total, 0)         # RECORD: equal remainders, so the difference is a multiple of k
        posts[total] = posts.get(total, 0) + 1
    return found


print(longest_with_sum([1, -1, 5, -2, 3], 3))                                        # 4  ([1, -1, 5, -2])
print(longest_with_sum([1 if b else -1 for b in [0, 1, 1, 0, 1, 1, 1, 0]], 0))       # 4  (525: [0, 1, 1, 0])
print(count_divisible([4, 5, 0, -2, -3, 1], 5))                                      # 7
```

<!-- cell -->

**Try it**
- Turn the second `if` into an `else` and run `longest_with_sum([1, -1, 1], 1)`: 1 instead of 3. On the miss at index 1 the `else` overwrote the empty prefix's `-1`, which the whole array needed.
- Always overwrite (`first[total] = j` with no `if`) and run `longest_with_sum([-1, 1, -1, 1], 0)`: 2 instead of 4. That is the rule for *shortest*, not longest.
- Drop `% k` in `count_divisible` and run it on `[5, 5]` with k = 5: 0 instead of 3.

<!-- cell -->

**Left-right passes and running values.** Next, the running value is not stored in a dict at all: a stamp from the left and a stamp from the right meet in one output array. Product of Array Except Self asks, for each index, for the product of all the other numbers, without division: `[1, 2, 3, 4] → [24, 12, 8, 6]`. "Everything except me" is everything to my left times everything to my right, and both parts are running products.

```text
nums           1    2    3    4
left part      1    1    2    6        product of everything left of i
right part    24   12    4    1        product of everything right of i
out           24   12    8    6        left part * right part
```

Trapping Rain Water (42) asks how much water the bars of a histogram hold after rain: `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] → 6`. Its first solution has the same shape with running *maxima*, each including the bar itself so that the water `min(L, R) - h` is never negative; [Two Pointers](06_Two_Pointers.ipynb#topic-two-pointers) then removes the arrays.

A running value can also reset. Max Consecutive Ones asks for the longest run of 1s in a 0/1 array: `[1, 1, 0, 1, 1, 1] → 3`, and every 0 is a wall that no run crosses. In the code, `product_except_self` stamps the left products on the way out and multiplies in the right products on the way back; `max_consecutive_ones` counts up on a 1, records the best inside the run, and drops to 0 on a 0.

<!-- cell -->

```python
def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    left = 1                                 # STATE: product of nums[0..i-1]
    for i in range(n):
        out[i] = left                        # RECORD: stamp first ...
        left *= nums[i]                      # STEP: ... then include nums[i] for the indices after it
    right = 1                                # STATE: product of nums[i+1..n-1]
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out


def max_consecutive_ones(nums):
    run = best = 0                           # STATE: run = length of the run of 1s ending at this item
    for x in nums:
        if x == 1:
            run += 1                         # STEP
            best = max(best, run)            # RECORD inside the run, so a run at the very end counts
        else:
            run = 0                          # STEP: a 0 is a wall, no run crosses it
    return best


print(product_except_self([1, 2, 3, 4]))          # [24, 12, 8, 6]
print(product_except_self([-1, 1, 0, -3, 3]))     # [0, 0, 9, 0, 0]
print(max_consecutive_ones([1, 1, 0, 1, 1, 1]))   # 3
```

<!-- cell -->

**Try it**
- Swap the two lines inside *both* loops of `product_except_self` (multiply first, then stamp) and run `[1, 2, 3, 4]`: `[24, 48, 72, 96]`. Every index now includes itself.
- Run `product_except_self([0, 0, 2])`: `[0, 0, 0]`, with no special case for zeros (dividing a total product would crash here).
- In `max_consecutive_ones`, move `best = max(best, run)` into the `else` branch (above `run = 0`) and run `[0, 1, 1, 1]`: 0 instead of 3. The last run never meets a 0, so it is never recorded.

<!-- cell -->

**2D prefix sums.** The next variation lifts the fence posts into two dimensions. Range Sum Query 2D - Immutable (304) asks for the sum of any rectangle of a grid, many times over. `P[r][c]` is the sum of the rectangle above and to the left of the crossing of post row r and post column c, and any rectangle is the big one, minus the strip above, minus the strip to the left, plus the corner that was subtracted twice.

```text
                 post c1      post c2+1
                    |              |
              A     |      B       |
  post r1   --------+--------------+       rect = P[r2+1][c2+1]     (A + B + C + rect)
              C     |     rect     |            - P[r1][c2+1]       (A + B)
  post r2+1 --------+--------------+            - P[r2+1][c1]       (A + C)
                                                + P[r1][c1]         (A, which was subtracted twice)
```

So `prefix_2d` builds a table one row and one column bigger than the grid, each cell being the grid cell plus the total above plus the total to the left minus the overlap, and `rect_sum` combines four corners of that table.

<!-- cell -->

```python
def prefix_2d(grid):
    R, C = len(grid), len(grid[0])
    P = [[0] * (C + 1) for _ in range(R + 1)]    # STATE + INIT: P[r][c] = sum of grid[0..r-1][0..c-1]; zero border
    for r in range(R):
        for c in range(C):
            P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]   # STEP: cell + up + left - overlap
    return P


def rect_sum(P, r1, c1, r2, c2):             # RETURN: cells r1..r2 x c1..c2, corners included
    return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]


grid = [[3, 0, 1],
        [5, 6, 3],
        [1, 2, 0]]
P2 = prefix_2d(grid)
print(rect_sum(P2, 1, 1, 2, 2))   # 11  (6 + 3 + 2 + 0)
print(rect_sum(P2, 0, 0, 2, 2))   # 21  (the whole grid)
```

<!-- cell -->

**Try it**
- Print `P2` row by row: the first row and the first column are all zeros. That border is why neither function needs an `if r > 0` check.
- Drop `- P[r][c]` from the build and rerun: `rect_sum(P2, 0, 0, 2, 2)` becomes 52 instead of 21. The shared corner is added twice at every cell, and the error snowballs.
- Predict `rect_sum(P2, 2, 0, 2, 2)` (the bottom row: 3) and `rect_sum(P2, 1, 0, 1, 0)` (a single cell: 5).

<!-- cell -->

**Difference array.** The reverse trick comes next: instead of reading range sums, apply range updates. Range Addition (370) applies many updates "add v to every index in l..r" and asks for the final array. Record only where a change *starts*, `+v` at l, and where it *stops*, `-v` at r + 1; one prefix sum at the end rebuilds every value. Corporate Flight Bookings (1109), bookings of seats on the flights first..last, is the same with flights as indices.

Car Pooling (1094) has trips `(passengers, from, to)` and asks whether the car's capacity ever overflows; My Calendar III (732, in [Intervals & Sweep Line](16_Intervals_and_Sweep_Line.ipynb#topic-intervals-and-sweep-line)) asks for the largest number of bookings that overlap at one moment. Both put the trick on a timeline of half-open ranges `[start, end)`: +p at each start, −p at each end itself, with p = 1 for a booking, and the running sum is the load at that moment.

```text
add +2 on 1..3:    diff   0  +2   0   0  -2   0        running sum ->   0  2  2  2  0
```

`apply_range_adds` touches two slots per update, then walks once adding up the changes.

<!-- cell -->

```python
def apply_range_adds(n, updates):            # updates: (l, r, v) = add v to every index in l..r
    diff = [0] * (n + 1)                     # STATE + INIT: one extra slot, so diff[r + 1] exists for r = n - 1
    for l, r, v in updates:
        diff[l] += v                         # STEP: from l on, everything is v higher ...
        diff[r + 1] -= v                     # ... and from r + 1 on, back to normal
    out, running = [], 0
    for i in range(n):
        running += diff[i]                   # the prefix sum of the changes is the value at i
        out.append(running)
    return out                               # RETURN


print(apply_range_adds(5, [(1, 3, 2), (2, 4, 3), (0, 1, -1)]))   # [-1, 1, 5, 5, 3]
```

<!-- cell -->

**Try it**
- Print `diff` before the rebuild loop: `[-1, 2, 4, 0, -2, -3]`. Each update touched only two slots.
- Make `diff = [0] * n` and run `apply_range_adds(5, [(2, 4, 3)])`: `IndexError`, because the update ends at the last index and `diff[r + 1]` falls off the end.
- Feed two half-open bookings `[10, 20)` and `[20, 30)` as `(10, 20, 1)` and `(20, 30, 1)` with n = 31: the maximum is 2, yet they never overlap. Pass `end - 1` instead (`(10, 19, 1)`, `(20, 29, 1)`) and it is 1.

<!-- cell -->

**Prefix xor / parity mask.** The last dict recipe swaps + for xor. Parity means odd or even, and xor is addition where 1 + 1 = 0, so it tracks parity. Find the Longest Substring Containing Vowels in Even Counts (1371) asks for the longest substring in which every vowel appears an even number of times: `"eleetminicoworoep" → 13`. Give each vowel one bit, and the running mask says which vowels have appeared an odd number of times so far.

Two equal masks mean that every vowel appeared an even number of times in between: the "first index of each total" trick again, with masks as the totals. So `longest_even_vowels` flips the vowel's bit at each letter and measures back to the first post that held the same mask.

<!-- cell -->

```python
def longest_even_vowels(s):                  # longest substring where every vowel count is even (1371)
    bit = {v: 1 << i for i, v in enumerate("aeiou")}
    first = {0: -1}                          # STATE + INIT: mask -> first post holding it; empty prefix at -1
    mask = best = 0
    for j, ch in enumerate(s):
        mask ^= bit.get(ch, 0)               # STEP: flip this vowel's parity; other letters change nothing
        if mask in first:
            best = max(best, j - first[mask])   # RECORD: same parities at both ends, even counts between
        else:
            first[mask] = j
    return best


print(longest_even_vowels("eleetminicoworoep"))   # 13
print(longest_even_vowels("bcbcbc"))              # 6
```

<!-- cell -->

**Try it**
- Print `j, ch, f"{mask:05b}"` at each step for `"abca"`: the a-bit turns on at index 0 and off at index 3, so mask 0 comes back and the whole string (length 4) counts.
- Run `longest_even_vowels("leetcodeisgreat")`: 5 (`"leetc"`, which has two e's).
- Allow one odd vowel, the rule of 1542 below: also look up `mask ^ b` for every vowel bit `b` (`for b in bit.values(): if mask ^ b in first: best = max(best, j - first[mask ^ b])`). `longest_even_vowels("eae")` goes from 0 to 3.

<!-- cell -->

Find Longest Awesome Substring (1542) asks for the longest stretch of digits that can be rearranged into a palindrome, `"3242415" → 5`, since `"24241"` rearranges into `"24142"`, and a palindrome allows at most one digit with an odd count. So the same loop keeps a 10-bit mask of digit parities, and a stretch works when its two end masks are equal or differ in exactly one bit: each end makes 11 lookups into the dict of first positions.

**Prefix sums + binary search.** The last variation uses the order of the totals instead of a dict. Random Pick with Weight (528) asks to pick index i with probability `w[i] / sum(w)`; with `w = [1, 3, 6]`, index 2 comes up six times in ten. Give index i a block of `w[i]` tickets on the number line 1..total. The running totals mark where each block ends, and with positive weights they increase, so `bisect` finds the block a random ticket falls in.

```text
w = [1, 3, 6]    P = [1, 4, 10]
tickets:   1 | 2 3 4 | 5 6 7 8 9 10
index:     0 |   1   |      2
```

`WeightedPicker` stores the running totals, draws a ticket between 1 and the last total, and `bisect_left` returns the first index whose total reaches the ticket.

<!-- cell -->

```python
class WeightedPicker:                        # 528: pick i with probability w[i] / sum(w)
    def __init__(self, w):
        self.P = list(accumulate(w))         # STATE: index i owns tickets P[i-1]+1 .. P[i]

    def pick(self):
        x = random.randint(1, self.P[-1])    # draw a ticket 1..total
        return bisect.bisect_left(self.P, x) # RETURN: the first index whose running total reaches x


random.seed(0)
picker = WeightedPicker([1, 3, 6])
print(sorted(Counter(picker.pick() for _ in range(10000)).items()))   # [(0, 1011), (1, 3009), (2, 5980)]  (about 1 : 3 : 6)
```

<!-- cell -->

**Try it**
- Use `bisect_right` and see where each ticket goes for `w = [1, 3]`: `[bisect.bisect_right([1, 4], x) for x in range(1, 5)]` is `[1, 1, 1, 2]`, so ticket 4 lands on index 2, which does not exist; `bisect_left` gives `[0, 1, 1, 1]`.
- Give some items weight 0: `WeightedPicker([0, 5, 0])` only ever returns 1, because indices 0 and 2 own no tickets.
- Draw from `random.randint(0, self.P[-1])` (ticket 0 included): index 0 now owns 2 tickets out of 11 instead of 1 out of 10.

<!-- cell -->

### Say it in the interview

> "Brute force tries every start and end: O(n²) even with a running sum. A subarray sum is a difference of two prefix sums, so this is Two Sum on the running totals: for each end I need the number of earlier prefix sums equal to the current one minus k. A dict of prefix-sum counts, seeded with {0: 1} for the empty prefix, answers that in O(1) on average. One pass, O(n) time and O(n) space, and it works with negatives, unlike a sliding window."

Then point at the seed ("the empty prefix, for subarrays that start at index 0") and at the order of the two dict lines: query first, then store. Follow-ups to have ready:

- *Values change between queries?* A Fenwick tree keeps prefix sums with O(log n) updates ([Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets) builds one over values, [Design Problems](00_Topic_Index.ipynb#s24) one in 2D).
- *Longest instead of how many? Return the subarray itself?* Store the first index of each total; the stretch is `first[total - k] + 1 .. j`.
- *Number of Submatrices That Sum to Target (1074)?* Fix a pair of rows, collapse the columns between them into one array, and run this dict: O(R²·C).
- *Maximum subarray?* The largest `P[j] − (smallest earlier P)`: the buy-and-sell loop of [From Idea to Code](02_Idea_to_Code.ipynb#topic-idea-to-code) run on the totals, which [Greedy](17_Greedy.ipynb#topic-greedy) writes as Kadane.
- *Path Sum III (437), downward paths in a tree that sum to k?* The same dict over root-to-node totals, with `posts[total] -= 1` as the DFS leaves a node.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Max Consecutive Ones | `arrays_hashing/max_consecutive_ones.py` | carry the current run length; a 0 resets it; record the max inside the run so a final run counts |
| Product of Array Except Self | `arrays_hashing/product_of_array_except_self.py` · `practice/simple/03_product_of_array_except_self.py` | out[i] = product left of i × product right of i: one pass each way, stamp before multiplying in |
| Subarray Sum Equals K | `arrays_hashing/subarray_sum_equals_k.py` · `practice/simple/05_subarray_sum_equals_k.py` | Two Sum on the running totals: count earlier totals equal to total − k; seed {0: 1}; query before storing |

### Self-check

1. In what sense is Subarray Sum Equals K "Two Sum on the running totals"?
<details><summary>Answer</summary>A stretch ending at item j sums to k exactly when an earlier post holds <code>total - k</code>, just as Two Sum's partner is <code>target - v</code>. The dict maps a total to how many earlier posts hold it (instead of value to index), and the answer adds up the hits instead of returning the first one. The seed <code>{0: 1}</code> is the empty prefix, already in the notebook.</details>

2. For "longest subarray with sum k", why do you store only the *first* index of each total?
<details><summary>Answer</summary>The stretch runs from just after the earlier post to the current item, so the earlier that post, the longer the stretch. Overwriting with later indices would only ever shorten the answers (that is the rule for <em>shortest</em>).</details>

3. Why does a sliding window fail on "count subarrays with sum k" with negative numbers, while prefix sums + a dict work?
<details><summary>Answer</summary>The window decides to shrink because the sum is too big, which only makes sense if dropping an item lowers the sum. A negative item breaks that, so there is no safe moment to shrink (<code>[1, -1, 1]</code>, k = 1: the window counts 2 of the 3). The dict approach never shrinks anything: it looks up an exact earlier total, which works for any numbers.</details>

4. In a difference array, what does each update touch, and why is `diff` one slot longer than the array?
<details><summary>Answer</summary>Each update touches two slots: <code>+v</code> where the range starts and <code>-v</code> just after it ends, at <code>r + 1</code>. When the range ends at the last index, <code>r + 1 = n</code>, so <code>diff</code> needs n + 1 slots. A prefix sum over <code>diff</code> then rebuilds every value.</details>
