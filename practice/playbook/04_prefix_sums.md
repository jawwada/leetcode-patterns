## Prefix Sums

> Write down the running total at every position once; then the sum of any stretch is the difference of two totals, like the distance between two towns read off a car's odometer. Questions about subarrays become questions about *pairs of totals*, and a list or a dict answers those in O(1).

**Reach for it when** a problem asks about sums (or products, counts, parities) of *contiguous* stretches: many range-sum queries, "count / longest subarrays with sum k" (especially with negatives, where a [Sliding Window](#s06) fails), "product of everything except me", "equal number of 0s and 1s", "add v to every element in [l, r]" over and over, the sum of a rectangle in a grid, or a random pick weighted by sizes.

**In this repo:** `arrays_hashing/subarray_sum_equals_k.py`, `arrays_hashing/product_of_array_except_self.py`, `arrays_hashing/max_consecutive_ones.py` · bank: `practice/simple/05_subarray_sum_equals_k.py`, `practice/simple/03_product_of_array_except_self.py` · basics: `practice/simple/basics/bits/03_xor_tricks_single_number_missing_number.py` (why xor can be "subtracted") · the same idea elsewhere: `intervals/my_calendar_iii.py` (difference array, [Intervals & Sweep Line](#s14)), `bit_manipulation/find_longest_awesome_substring.py` (prefix parity mask, [Math, Bits & Geometry](#s22)), `greedy/super_washing_machines.py` (prefix-sum flow), `greedy/maximum_subarray.py` (running sum, [Greedy](#s15)), `design/range_sum_query_2d_mutable.py` (2D range sums with updates, [Design](#s24))

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

**It is Two Sum on the running totals.** Subarray Sum Equals K looks up `total - k` where [Two Sum](#s03) looks up `target - v`, and it *counts* instead of returning. The seed `{0: 1}` is post P0, the empty prefix, already in the notebook before the first item.

| Decision | Prefix-sum answer |
|---|---|
| **State**: what must I remember? | the running `total` (or the whole table `P` when the queries come later); for counting, `posts[t]` = how many earlier posts hold total `t` |
| **Definition**: what exactly does each variable mean? | `P[k] = nums[0] + ... + nums[k-1]` (so `P[0] = 0`), and then `sum(nums[l..r]) = P[r + 1] - P[l]` |
| **Invariant**: what is true at the end of every step? | after the query and before the store: `total == P[j + 1]`, and `posts` holds exactly the earlier posts `P[0..j]` |
| **Step**: how does one item change the state? | `total += x`; then, after the query, add `total` to `posts` |
| **Record**: when is the answer updated? | `found += posts.get(total - k, 0)`, *before* storing the current post |
| **Init**: starting values | `total = 0` and `posts = {0: 1}`: the empty prefix is a real post, needed by stretches that start at index 0 |
| **Return**: what comes back, and for "not found"? | `found` (0 when nothing matched), or `P[r + 1] - P[l]` for each query |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "the total of the first k items" | `P[k]`; the whole table at once: `P = [0] + list(accumulate(nums))` |
| "the sum of items l..r, both included" | `P[r + 1] - P[l]` |
| "the running total so far" | `total += x` |
| "a stretch ending here sums to k" | `total - k in posts` |
| "how many such stretches" | `posts.get(total - k, 0)` |
| "the empty prefix counts" | `posts = {0: 1}` |
| "remember this post" | `posts[total] = posts.get(total, 0) + 1`, after the query |

**From the question to the code.** Most prefix-sum questions are this one loop with four knobs: what each item adds to the total, what you look up, what the dict stores, and its seed.

| Question | Each item adds | Look up | Dict stores | Seed |
|---|---|---|---|---|
| count stretches with sum k (560) | `x` | `total - k` | posts per total | `{0: 1}` |
| longest stretch with sum k (325) | `x` | `total - k` | first index per total | `{0: -1}` |
| shortest stretch with sum k | `x` | `total - k` | last index per total | `{0: -1}` |
| as many 0s as 1s (525) | `+1` or `-1` | the same total | first index | `{0: -1}` |
| count sums divisible by k (974) | `x`, keep `% k` | the same remainder | posts per remainder | `{0: 1}` |
| a multiple of k, length ≥ 2 (523) | `x`, keep `% k` | the same remainder; a hit needs `j - first >= 2` | first index | `{0: -1}` |
| exactly k odd numbers (1248) | `x % 2` | `total - k` | posts per total | `{0: 1}` |
| every vowel an even number of times (1371) | flip the vowel's bit | the same mask | first index | `{0: -1}` |
| at most one digit odd (1542) | flip the digit's bit | the same mask, or one bit flipped | first index | `{0: -1}` |

When the dict stores indices, name each post by the item it follows: after item `j` the post is called `j`, and the empty prefix is called `−1`. The stretch after post `i` up to item `j` then has length `j − i`.

Two templates: a table for range queries, and the running total plus dict for counting. The second is [From Idea to Code](#s01)'s `subarray_sum` with a plain dict and the picture's names. Its RECORD comes before the last STEP, so the current post can never pair with itself.

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

**Try it**
- Keep a *set* of totals instead of counts (`posts = {0}`, `found += (total - k) in posts`, `posts.add(total)`) and run `count_subarrays_with_sum([0, 0, 0], 0)`: 3 instead of 6. Equal totals are different starts, and each one is a separate answer.
- Predict `count_subarrays_with_sum([1, 2, 3], 3)` and name each stretch's earlier post (2: `[1, 2]` pairs with P0, `[3]` with P2).
- Predict `range_sum(P, 0, 4)` and `range_sum(P, 2, 2)` before running them (7, the whole array, and −2, a single item).

### Watch it work

Each line is one item; `posts` is shown *before* the current post is stored.

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

**Try it**
- Run `trace_count([0, 0, 0], 0)`: the hits are 1, 2 and 3, for a total of 6. Every pair of equal totals is one zero-sum stretch.
- Run `trace_count([1, -1, 1, -1], 0)` and match each hit to the earlier post it pairs with (4 stretches in all).
- Predict the answer before running `trace_count([3, 1, -2, 4, 1], 4)` (3: `[3, 1]`, `[4]` and `[1, -2, 4, 1]`).

### Where it goes wrong

1. **The empty prefix, and the order of the two dict lines.** Both are [From Idea to Code](#s01) lessons: without `{0: 1}`, `[3]` with k = 3 gives 0; storing before the query makes `[1]` with k = 0 give 1.
2. **Off by one in ranges.** `sum(nums[l..r]) = P[r + 1] - P[l]`. `P[r] - P[l]` leaves out item r; `P[r + 1] - P[l - 1]` adds item l − 1 (and at l = 0, `P[-1]` silently reads the *last* total).
3. **First, last, or how many?** Counting stores how many posts hold each total. *Longest* keeps the **first** index (store only when absent, in its own `if`, not an `else`); *shortest* keeps the **last** (always overwrite). Overwriting in a "longest" question turns Contiguous Array on `[0, 1, 0, 1]` into 2 instead of 4.
4. **Sliding window with negatives.** A window that shrinks while its sum is above k counts 2 on `[1, -1, 1]` with k = 1; the answer is 3 (`[1]`, `[1]` and `[1, -1, 1]`). Dropping an item can raise the sum, so the window cannot tell when to stop.
5. **Including yourself in a left-right pass.** In Product Except Self, multiply `nums[i]` into the running product *after* stamping `out[i]`, in both passes; otherwise `[1, 2, 3, 4]` gives `[24, 48, 72, 96]`. And skip division: it fails on zeros.
6. **Ragged 2D borders.** Give the 2D table an extra zero row and column, `(R + 1) × (C + 1)`; then no `if r > 0` cases are needed and the build is `cell + up + left - up_left`.
7. **Difference array: one slot short, or the wrong end.** `diff[r + 1] -= v` needs `n + 1` slots, or an update that ends at the last index raises `IndexError`. For half-open ranges `[start, end)` the −v goes at `end` itself: treating `end` as included makes `[10, 20)` and `[20, 30)` overlap at 20.

### Edge cases to say out loud

Empty input · one item equal to k · `k = 0` · all zeros (many overlapping answers) · negatives · the whole array is the answer · no answer at all.

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

**Try it**
- Predict `count_subarrays_with_sum([0], 0)` before running it (1: the single 0 pairs with the empty prefix).
- Predict, then add: `assert count_subarrays_with_sum([1, 2, 3], 6) == 1` (only the whole array).
- A negative k works too: predict `count_subarrays_with_sum([-1, -1, 1], -2)` (1: the first two items).

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Range sum queries** | build `P` once; each query is `P[r + 1] - P[l]` | 303 |
| **The dict recipes** | change what an item adds, what you look up and what the dict stores (the table above) | 560, 325, 525, 974, 523, 1248, 1371, 1542 |
| **Left-right passes** | carry a running value from each side. 238 stamps before multiplying (never include yourself); 42 includes the bar in its max, so `min(L, R) - h` is never negative | 238, 42 |
| **Running value that resets** | carry `run`; a wall resets it to 0; record the max inside the run | 485 |
| **2D prefix sums** | `(R + 1) × (C + 1)` table; a rectangle is four corners, inclusion–exclusion | 304, 1074 |
| **Difference array** | range update: `diff[l] += v`, `diff[r + 1] -= v` (half-open: at `end`); one prefix sum rebuilds the values | 370, 1109, 1094, 732 |
| **Prefix sums + binary search** | positive weights make the totals increasing, so `bisect` finds whose ticket was drawn | 528 |

**Longest instead of count; remainders instead of totals.** For the longest stretch, keep the *first* index where each total appeared: the earliest start gives the longest stretch. Contiguous Array (525) is this with every 0 turned into −1 and k = 0. For "divisible by k", two posts with the same remainder are a multiple of k apart.

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

**Try it**
- Turn the second `if` into an `else` and run `longest_with_sum([1, -1, 1], 1)`: 1 instead of 3. On the miss at index 1 the `else` overwrote the empty prefix's `-1`, which the whole array needed.
- Always overwrite (`first[total] = j` with no `if`) and run `longest_with_sum([-1, 1, -1, 1], 0)`: 2 instead of 4. That is the rule for *shortest*, not longest.
- Drop `% k` in `count_divisible` and run it on `[5, 5]` with k = 5: 0 instead of 3.

**Left-right passes and running values.** "Everything except me" is (everything to my left) × (everything to my right), and both parts are running products: one pass from the left stamps the left part into `out`, one pass from the right multiplies in the right part. Trapping Rain Water's first solution has the same shape with running *maxima*, each including the bar itself so the water `min(L, R) - h` is never negative; the [Two Pointers](#s05) section then removes the arrays. A running value can also reset: Max Consecutive Ones carries the length of the current run of 1s, and every 0 is a wall that sends it back to 0.

```text
nums           1    2    3    4
left part      1    1    2    6        product of everything left of i
right part    24   12    4    1        product of everything right of i
out           24   12    8    6        left part * right part
```

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

**Try it**
- Swap the two lines inside *both* loops of `product_except_self` (multiply first, then stamp) and run `[1, 2, 3, 4]`: `[24, 48, 72, 96]`. Every index now includes itself.
- Run `product_except_self([0, 0, 2])`: `[0, 0, 0]`, with no special case for zeros (dividing a total product would crash here).
- In `max_consecutive_ones`, move `best = max(best, run)` into the `else` branch (above `run = 0`) and run `[0, 1, 1, 1]`: 0 instead of 3. The last run never meets a 0, so it is never recorded.

**2D prefix sums.** `P[r][c]` is the sum of the rectangle above and to the left of the crossing of post row r and post column c. Any rectangle is the big one, minus the strip above, minus the strip to the left, plus the corner that was subtracted twice.

```text
                 post c1      post c2+1
                    |              |
              A     |      B       |
  post r1   --------+--------------+       rect = P[r2+1][c2+1]     (A + B + C + rect)
              C     |     rect     |            - P[r1][c2+1]       (A + B)
  post r2+1 --------+--------------+            - P[r2+1][c1]       (A + C)
                                                + P[r1][c1]         (A, which was subtracted twice)
```

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

**Try it**
- Print `P2` row by row: the first row and the first column are all zeros. That border is why neither function needs an `if r > 0` check.
- Drop `- P[r][c]` from the build and rerun: `rect_sum(P2, 0, 0, 2, 2)` becomes 52 instead of 21. The shared corner is added twice at every cell, and the error snowballs.
- Predict `rect_sum(P2, 2, 0, 2, 2)` (the bottom row: 3) and `rect_sum(P2, 1, 0, 1, 0)` (a single cell: 5).

**Difference array.** The reverse trick: to add v to a whole range many times, record only where the change *starts* (`+v` at l) and where it *stops* (`-v` at r + 1). One prefix sum at the end rebuilds every value. Car Pooling (1094) and My Calendar III (732, in [Intervals & Sweep Line](#s14)) use it on a timeline of half-open trips `[start, end)`: +1 at each start, −1 at each end itself, and the running sum is how many trips overlap at that moment.

```text
add +2 on 1..3:    diff   0  +2   0   0  -2   0        running sum ->   0  2  2  2  0
```

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

**Try it**
- Print `diff` before the rebuild loop: `[-1, 2, 4, 0, -2, -3]`. Each update touched only two slots.
- Make `diff = [0] * n` and run `apply_range_adds(5, [(2, 4, 3)])`: `IndexError`, because the update ends at the last index and `diff[r + 1]` falls off the end.
- Feed two half-open bookings `[10, 20)` and `[20, 30)` as `(10, 20, 1)` and `(20, 30, 1)` with n = 31: the maximum is 2, yet they never overlap. Pass `end - 1` instead (`(10, 19, 1)`, `(20, 29, 1)`) and it is 1.

**Prefix xor / parity mask.** Xor is addition where 1 + 1 = 0, so it tracks *parity*. Give each vowel one bit; the running mask says which vowels have appeared an odd number of times so far. Two equal masks mean every vowel appeared an even number of times in between: the "first index of each total" trick again, with masks as the totals. [Math, Bits & Geometry](#s22) applies it to digits, where one odd digit is allowed (1542).

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

**Try it**
- Print `j, ch, f"{mask:05b}"` at each step for `"abca"`: the a-bit turns on at index 0 and off at index 3, so mask 0 comes back and the whole string (length 4) counts.
- Run `longest_even_vowels("leetcodeisgreat")`: 5 (`"leetc"`, which has two e's).
- Allow one odd vowel, the 1542 rule: also look up `mask ^ b` for every vowel bit `b` (`for b in bit.values(): if mask ^ b in first: best = max(best, j - first[mask ^ b])`). `longest_even_vowels("eae")` goes from 0 to 3.

**Prefix sums + binary search.** To pick index i with probability `w[i] / sum(w)`, give index i a block of `w[i]` tickets on the number line 1..total. The running totals mark where each block ends, and with positive weights they increase, so `bisect` finds the block a random ticket falls in.

```text
w = [1, 3, 6]    P = [1, 4, 10]
tickets:   1 | 2 3 4 | 5 6 7 8 9 10
index:     0 |   1   |      2
```

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

**Try it**
- Use `bisect_right` and see where each ticket goes for `w = [1, 3]`: `[bisect.bisect_right([1, 4], x) for x in range(1, 5)]` is `[1, 1, 1, 2]`, so ticket 4 lands on index 2, which does not exist; `bisect_left` gives `[0, 1, 1, 1]`.
- Give some items weight 0: `WeightedPicker([0, 5, 0])` only ever returns 1, because indices 0 and 2 own no tickets.
- Draw from `random.randint(0, self.P[-1])` (ticket 0 included): index 0 now owns 2 tickets out of 11 instead of 1 out of 10.

### Say it in the interview

> "Brute force tries every start and end: O(n²) even with a running sum. A subarray sum is a difference of two prefix sums, so this is Two Sum on the running totals: for each end I need the number of earlier prefix sums equal to the current one minus k. A dict of prefix-sum counts, seeded with {0: 1} for the empty prefix, answers that in O(1) on average. One pass, O(n) time and O(n) space, and it works with negatives, unlike a sliding window."

Then point at the seed ("the empty prefix, for subarrays that start at index 0") and at the order of the two dict lines: query first, then store. Follow-ups to have ready:

- *Values change between queries?* A Fenwick tree keeps prefix sums with O(log n) updates ([Arrays & Hashing](#s03) builds one over values, [Design](#s24) one in 2D).
- *Longest instead of how many? Return the subarray itself?* Store the first index of each total; the stretch is `first[total - k] + 1 .. j`.
- *Count submatrices with sum k (1074)?* Fix a pair of rows, collapse the columns between them into one array, and run this dict: O(R²·C).
- *Maximum subarray?* The largest `P[j] − (smallest earlier P)`: the buy-and-sell loop of [From Idea to Code](#s01) run on the totals, which [Greedy](#s15) writes as Kadane.
- *Downward paths in a tree that sum to k (437)?* The same dict over root-to-node totals, with `posts[total] -= 1` as the DFS leaves a node.

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
