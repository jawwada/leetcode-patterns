## Binary Search

> Every binary search answers one question: **where does a yes/no answer flip?** Line the candidates up so the answers read `F F F F T T T T`, keep a window that always contains the first `T`, and look at the middle: one look throws away half the window.

**Reach for it when** the input is sorted, or sorted in pieces: a rotated array, a mountain, a matrix whose rows continue each other. The same holds when the problem demands O(log n).

Reach for it above all when the problem asks for the **minimum X such that ...** or the **maximum X such that ...** and a bigger X only ever makes the condition easier, or only ever harder. That is binary search on the answer, and it needs no sorted data at all. It also finds "the k-th smallest" in something too big to list, as long as you can *count* the items ≤ v quickly.

### The picture

Binary search does not care about the numbers themselves. It cares about the answers to one question about them, and those answers form a landscape with a single flip:

```text
nums      1    3    3    5    8    9   12       question: the first index with nums[i] >= 4
index     0    1    2    3    4    5    6
ok(i)     F    F    F    T    T    T    T       the boolean landscape: it flips exactly once
                         ^
                         the answer is the first T

look at index 3: T  ->  the answer is 3 or further left: indices 4, 5, 6 are settled
look at index 1: F  ->  the answer is right of 1: indices 0 and 1 are settled
look at index 2: F  ->  only index 3 is left, so it is the answer
```

A linear scan learns about one cell per look. In `F F F T T T`, a `T` in the middle says that every cell to its right is `T` too, and an `F` says that every cell to its left is `F`, so each look settles half of the remaining candidates. A million candidates need 20 looks, a billion need 30.

Notice what the search really needs: not sorted *data*, but a *question* whose answers are sorted, False up to some point and True from then on. A question with that shape is called monotone. That is why binary search also works on rotated arrays, on peaks, and on the answer itself.

It is correct because the window always contains the first `T`. Every candidate left of `lo` is known to be `F`, and `hi` is known to be `T` or is past the end. A probe keeps both facts true on either branch, and every probe makes the window smaller, so the loop ends with `lo == hi` sitting on the first `T`.

### From idea to code

**The idea in one sentence:** *write `ok(x)`, which is False for small x and True from some point on; keep `[lo, hi]` so that the first True is always inside; test the middle and move the side that the test proves.*

The picture dictates the seven decisions. **State** is two integers, `lo` and `hi`, and **Definition** says what they mean in one sentence: the first True lies in `[lo, hi]`. **Invariant** is the fact that holds every time the loop comes round: every candidate left of `lo` is False, `hi` is True or past the end, and the window is smaller than last time. **Init** sets this up: `lo` on the smallest candidate, `hi` on the fallback answer, which is never tested because it is one past the last candidate or a value already known to work.

**Step** probes the middle, `mid = (lo + hi) // 2`: if `ok(mid)` is True, mid might be the first True and `hi = mid` keeps it; if not, `lo = mid + 1` drops it. Each probe keeps the invariant by itself, so there is no **Fix**, and **Record** waits for `lo == hi`, the window shrunk onto the answer. **Return** is `lo`, and the caller turns "no True at all" into −1 by checking `lo == len(nums)` or `nums[lo] != target`.

Read the template as those sentences. `lo, hi = 0, len(nums)` says the answer is one of `lo..hi`, with `len(nums)` meaning "none"; the cells still untested are `lo..hi-1`, and `while lo < hi` runs while one is left. `mid = (lo + hi) // 2` rounds down, so `lo <= mid < hi`: `nums[mid]` always exists, and `hi = mid` still shrinks the window. `return lo` is the first one that works, and the last one that works is the first one that fails, minus 1.

The cell holds two problems and one helper. Search Insert Position asks where a target sits in a sorted array, or where it would be inserted: `[1, 3, 5, 6]` with target 2 → 1, with target 7 → 4. That is `lower_bound`, the first index whose value is ≥ x, with `len(nums)` meaning "after everything". The helper `first_true` is the same loop with the question passed in, so that every later problem is only "write `ok`".

Binary Search itself asks for the index of a target in a sorted array of distinct values, or −1: `[-1, 0, 3, 5, 9, 12]` with target 9 → 4. It may stop the moment it finds the target, and that is where the closed window `[lo, hi]`, with both ends still candidates, fits naturally.

<!-- cell -->

```python
def lower_bound(nums, x):
    """The first index i with nums[i] >= x, or len(nums) if every value is smaller."""
    lo, hi = 0, len(nums)                    # STATE + INIT: the first True lies in [lo, hi]
    while lo < hi:                           # something is still untested
        mid = (lo + hi) // 2                 # rounds down: lo <= mid < hi, so nums[mid] exists
        if nums[mid] >= x:
            hi = mid                         # STEP (True): the first True is mid or left of it
        else:
            lo = mid + 1                     # STEP (False): the first True is right of mid
    return lo                                # RECORD + RETURN: lo == hi is the answer


def first_true(lo, hi, ok):
    """The first x in [lo, hi) with ok(x) True, or hi if there is none (ok reads F..F T..T)."""
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def search(nums, target):                    # exact match (704): a closed window [lo, hi]
    lo, hi = 0, len(nums) - 1                # STATE + INIT: if target is present, it is in nums[lo..hi]
    while lo <= hi:                          # lo == hi is still one candidate
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid                       # RECORD + RETURN: found at a probe
        if nums[mid] < target:
            lo = mid + 1                     # STEP: both moves skip mid,
        else:
            hi = mid - 1                     # STEP: so the window shrinks every time
    return -1                                # RETURN: the window is empty


nums = [1, 3, 3, 5, 8, 9, 12]
print(lower_bound(nums, 3), lower_bound(nums, 4), lower_bound(nums, 13))   # 1 3 7
print(first_true(0, len(nums), lambda i: nums[i] > 3))                     # 3  (the first value > 3)
print(search(nums, 8), search(nums, 4))                                    # 4 -1
```

<!-- cell -->

**Try it**
- Change `hi = mid` to `hi = mid - 1` in `lower_bound` and run `lower_bound([1, 5], 4)`: 0 instead of 1. Mid *was* the first True, and you threw it away.
- Change `while lo < hi` to `while lo <= hi` in `lower_bound`, with a guard, `steps = 0` before the loop and `steps += 1; assert steps < 50` inside it, and rerun the cell: the assert fires on the first call. Trace the smallest case, `lower_bound([1, 5], 4)`: once `lo == hi == 1`, mid is 1, `nums[1] >= 4` is True, and `hi = mid` changes nothing, forever.
- Print `lo, hi` at the top of the loop in `search(nums, 4)`: `0 6`, `0 2`, `2 2`. The window holds 7, then 3, then 1 candidate, and the loop stops when `lo` passes `hi`.
- Compare with the library: `bisect.bisect_left(nums, 4)` is 3, the same as `lower_bound`, and `bisect.bisect_right(nums, 3)` is 3, the first index with a value `> 3`.

<!-- cell -->

Every problem in this section is four decisions around `first_true`, and the loop itself is never edited. First, write `ok(x)` so the candidates read F…F T…T; for a *maximum*, search the first False and subtract 1. Second, check it out loud: if `ok(x)` is True, is `ok(x + 1)` True too? Third, choose `lo`, the smallest candidate, and `hi`, the fallback answer returned when nothing in `[lo, hi)` is True. Fourth, call `i = first_true(lo, hi, ok)`, and check `i < len(nums)` before reading `nums[i]`.

Find First and Last Position of Element in Sorted Array runs the loop twice. It asks for the first and last index of a target, or `[-1, -1]`: `[5, 7, 7, 8, 8, 10]` with target 8 → `[3, 4]`. The first index is `lower_bound(target)`, the last is the first index with a value `> target`, minus 1, and the target is absent when the first index is past the end or holds another value.

In Python you rarely write the loop for a sorted list. `bisect.bisect_left(a, x)` is `lower_bound`, `bisect.bisect_right(a, x)` is the first index `> x`, and on Python 3.10+ `lo + bisect.bisect_left(range(lo, hi), True, key=ok)` equals `first_true(lo, hi, ok)`; more in [Python Toolkit](03_Python_Toolkit.ipynb#topic-python-toolkit). In an interview, say you would use `bisect`, write the loop if asked, and use `bisect` as your tester.

The loop styles you will meet all end for a reason, and this is the table to look up when you read someone else's search:

| Style | Loop | Moves | Why it ends | Use it for |
|---|---|---|---|---|
| **first True** (the template) | `while lo < hi` | `hi = mid` / `lo = mid + 1` | `mid < hi` (rounded down), so `hi = mid` still shrinks the window | boundaries, the minimum that works, rotations, peaks; the maximum as "first False − 1" |
| **closed window** | `while lo <= hi` | `lo = mid + 1` / `hi = mid - 1` | both moves skip `mid` | exact match, returning as soon as you find it |
| **record-and-skip** | `while lo <= hi` | `if ok(mid): ans, hi = mid, mid - 1`, else `lo = mid + 1` | both moves skip `mid` | fine if it is your habit; start `ans` at the "none" value |
| **last True** | `while lo < hi`, `mid = (lo + hi + 1) // 2` | `lo = mid` / `hi = mid - 1` | `mid > lo` (rounded up), so `lo = mid` still shrinks the window | recognise it in other code; "first False − 1" avoids it |

Never mix them: `while lo <= hi` with `hi = mid` loops forever once `lo == hi` and `ok(mid)` is True, and `lo = mid` with a rounded-down `mid` loops forever once `hi == lo + 1` and `ok(mid)` is True.

### Watch it work

Seeing the window shrink once makes the invariant concrete. The trace below runs `lower_bound` on the picture's array for x = 4 and prints one row per probe: the window `[lo, hi)` shows its letters, every settled cell becomes a dot, and `[ ]` marks mid.

<!-- cell -->

```python
def trace_lower_bound(nums, x):
    bits = ["T" if v >= x else "F" for v in nums]

    def show(label, cells, note=""):
        print((f"{label:<12}" + "".join(f"{c:^5}" for c in cells) + note).rstrip())

    show("nums", nums)
    show(f"nums >= {x}", bits)
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        window = [f"[{b}]" if i == mid else b if lo <= i < hi else "." for i, b in enumerate(bits)]
        if bits[mid] == "T":
            show(f"lo={lo} hi={hi}", window, f"  mid={mid} is T: hi = mid")
            hi = mid
        else:
            show(f"lo={lo} hi={hi}", window, f"  mid={mid} is F: lo = mid + 1")
            lo = mid + 1
    print(f"lo = hi = {lo}: " + ("the first T" if lo < len(nums) else "no T at all (lo = len(nums))"))


trace_lower_bound([1, 3, 3, 5, 8, 9, 12], 4)
```

<!-- cell -->

**Try it**
- Trace `x = 13`, bigger than everything: every probe is F, `lo` walks up to 7 = `len(nums)`, and the last line says there is no T at all ("insert at the very end").
- Trace `x = 0`, smaller than everything: every probe is T and `hi` walks down to 0.
- Trace `x = 3`: there are two 3s, and the search lands on the first one, index 1.
- On `list(range(1000))`, count the loop rounds of `lower_bound` for every x from -1 to 1000: never more than 10, because 2¹⁰ = 1024.

<!-- cell -->

### Where it goes wrong

Binary search is five lines, so nearly every bug is one line off, and each one has a tiny input that shows it.

1. **`hi = mid - 1` in the first-True loop.** If mid *is* the first True, you just threw the answer away: `lower_bound([1, 5], 4)` returns 0 instead of 1. Only a test that proves "mid is wrong" may skip mid.
2. **Mixing the loop styles.** `while lo <= hi` with `hi = mid` never ends once `lo == hi` and `ok(mid)` is True: `lower_bound([1, 5], 4)` spins forever at `lo = hi = 1`. `lo = mid` with `mid = (lo + hi) // 2` never ends when `hi == lo + 1` and `ok(mid)` is True. Rule: `lo = mid` needs `mid = (lo + hi + 1) // 2`.
3. **`hi = len(nums) - 1` when "nothing qualifies" is possible.** Search Insert Position on `[1, 3, 5, 6]` with target 7 must return 4, which only exists if `hi` starts at `len(nums)`.
4. **A question that isn't monotone.** Binary search never complains; it quietly returns garbage. `lower_bound([5, 1, 2, 3], 4)` returns 4, "none", although `nums[0] = 5` qualifies: the unsorted array reads `T F F F`. Before coding, say out loud: "if `ok(x)` is True, is `ok(x + 1)` True too?" For Koko Eating Bananas, the slowest eating speed that finishes every pile within h hours, the answer is yes: a faster speed never needs more hours.
5. **Bad bounds on the answer.** `lo` must be a real candidate and `hi` must surely work. Koko's speed starts at 1: from 0, `min_eating_speed([1], 1)` probes speed 0 and divides by zero. Split Array Largest Sum, which cuts an array into k pieces with the smallest possible largest sum, starts its cap at `max(nums)`: from 0, the greedy count goes wrong, and `[1, 4, 4]` with k = 3 answers 1.
6. **Rotated arrays: `<` instead of `<=`.** In the classic one-pass search, `nums[lo] <= nums[mid]` needs the `=` when `lo == mid`, that is, with two items left: with `<`, `[3, 1]` never finds the 1.
7. **Integer moves on real numbers.** `first_true(0, 2, lambda x: x * x >= 2)` returns 2, the first *integer* whose square reaches 2, while the real answer is √2 ≈ 1.414: `lo = mid + 1` jumps right over it. On a real-valued answer, use `mid = (lo + hi) / 2`, move `lo = mid` or `hi = mid`, and stop after a fixed number of rounds, 50 to 100, or once `hi - lo` is tiny.
8. **A T…T F…F question fed to `first_true`.** It returns garbage without complaint: in `max_min_gap` below, passing `fits` instead of `not fits` gives 6 instead of 3 for `[1, 2, 3, 4, 7]`, m = 3. For a maximum, search the first False and subtract 1.
9. **Reading `nums[lo]` unchecked.** When nothing qualifies, `lo == len(nums)`: `lower_bound([1, 3], 5)` is 2, and `nums[2]` raises `IndexError`. Check `lo < len(nums)` first.
10. **Duplicates break the rotated questions.** With repeats, `nums[i] <= nums[-1]` no longer separates the two runs: `find_min_rotated([1, 1, 0, 1])` returns 1 while the minimum is 0, and `search_rotated([1, 0, 1, 1, 1], 0)` returns -1. Find Minimum in Rotated Sorted Array II (154) and Search in Rotated Sorted Array II (81), the same questions with duplicates allowed, shrink `hi -= 1` when `nums[mid] == nums[hi]`, which costs O(n) in the worst case.

### Edge cases to say out loud

Say them before you type: empty array, one element, target below everything or above everything, all equal, duplicates and whether you want the first copy or the last, two elements, where infinite loops show up, and the answer at index 0 or at `len(nums)`. Then let the asserts say them for you:

<!-- cell -->

```python
assert lower_bound([], 5) == 0
assert lower_bound([5], 4) == 0 and lower_bound([5], 5) == 0 and lower_bound([5], 6) == 1
assert lower_bound([2, 2, 2], 2) == 0                  # duplicates: the FIRST copy
assert lower_bound([1, 3, 5, 6], 7) == 4               # insert position past the end (35)
assert lower_bound([1, 5], 4) == 1                     # two elements: F T
assert search([], 1) == -1 and search([1], 1) == 0 and search([1, 2], 2) == 1
assert first_true(0, 10, lambda x: False) == 10        # no True at all: hi comes back
assert first_true(0, 10, lambda x: True) == 0
assert first_true(0, 10, lambda x: x * x >= 50) == 8   # 7 * 7 = 49 < 50 <= 64 = 8 * 8
print("edge cases pass")
```

<!-- cell -->

**Try it**
- Predict, then add: `assert lower_bound([1, 2, 2, 2, 3], 3) == 4`.
- The *last* copy of x is the first index with `nums[i] > x`, minus one. With `a = [2, 2, 2]`, assert `first_true(0, len(a), lambda i: a[i] > 2) - 1 == 2`.
- `first_true(5, 5, ok)` has an empty range and returns 5 without calling `ok`. Check it with `ok = lambda x: 1 / 0`: no `ZeroDivisionError`.

<!-- cell -->

### Variations

Every variation below keeps the loop and changes only `ok`, `lo` and `hi`. The table is the overview; the paragraphs after it work through each variation with the problems it solves.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Exact match** | closed window, return on `==` | Binary Search (704) |
| **Lower / upper bound** | `ok = nums[i] >= x` or `nums[i] > x`; all copies of x sit in `[lower, upper)` | Search Insert Position (35), Find First and Last Position of Element in Sorted Array (34) |
| **Rotated array** | `ok(i) = nums[i] <= nums[-1]` finds the drop; then search the one run that can hold the target | Find Minimum in Rotated Sorted Array (153), Search in Rotated Sorted Array (33) |
| **A question about neighbours** | `ok` compares `nums[i]` with another cell: the next one, its pair partner, the cell k ahead | Find Peak Element (162), Single Element in a Sorted Array (540), Find K Closest Elements (658) |
| **2D matrix** | rows continue each other: position k is cell `divmod(k, cols)` | Search a 2D Matrix (74); Search a 2D Matrix II (240), whose rows and columns are only sorted separately, walks a staircase instead |
| **On the answer, minimise** | the candidates are answers; `ok = feasible(x)`, often one greedy pass | Koko Eating Bananas (875), Split Array Largest Sum (410) |
| **The same code, a different `ok`** | only `ok` changes: a greedy pass like Split Array's, or a sum of divisions like Koko's | Capacity To Ship Packages Within D Days (1011): the smallest capacity that ships in D days; Smallest Divisor Given a Threshold (1283): the smallest d with the sum of ⌈x / d⌉ at most the threshold; Minimum Number of Days to Make m Bouquets (1482): the first day with m bouquets of k adjacent flowers; Minimum Time to Complete Trips (2187): the least time for the buses to make the trips |
| **On the answer, maximise** | the last True = the first False − 1 | Magnetic Force Between Two Balls (1552): place m balls so that the smallest gap is as large as possible |
| **A key's history** | `bisect_right(times, t) - 1` is the latest entry at or before t | Time Based Key-Value Store (981): a key's value at time t, in [Design Problems](00_Topic_Index.ipynb#s24) |
| **Weighted random pick** | the first prefix sum ≥ a random ticket | Random Pick with Weight (528): an index drawn in proportion to its weight, in [Prefix Sums](05_Prefix_Sums.ipynb#topic-prefix-sums) |
| *Second pass:* **Mountain** | find the peak, then a normal search on each side | Find in Mountain Array (1095): the smallest index of a target in an array that rises, then falls |
| *Second pass:* **Maximise with a capped sum** | t works while `sum(min(b, t)) >= n * t`; the answer is the first failing t − 1 | Maximum Running Time of N Computers (2141): how long n computers run at once on shared batteries |
| *Second pass:* **Real numbers** | `lo = mid` / `hi = mid`, a fixed number of rounds (trap 7) | Maximum Average Subarray II (644): the best average over windows of length ≥ k |
| *Second pass:* **K-th smallest by counting** | `ok(v) = count(items <= v) >= k` | Kth Smallest Number in Multiplication Table (668), Find K-th Smallest Pair Distance (719); Kth Smallest Element in a Sorted Matrix (378) counts with a staircase, in [Matrices](37_Matrices.ipynb#topic-matrices) |
| *Second pass:* **Cut two sorted arrays** | binary search how many items of the shorter array go left | Median of Two Sorted Arrays (4) |

The first variation keeps the data sorted but hides it. Find Minimum in Rotated Sorted Array asks for the smallest value of a sorted array that was rotated: `[3, 4, 5, 1, 2]` → 1. Search in Rotated Sorted Array asks for the index of a target in such an array, or −1: `[4, 5, 6, 7, 0, 1, 2]` with target 0 → 4.

A **rotated array** is two sorted runs with a drop between them. Compare every value with the *last* one: the left run is all bigger, the right run all smaller or equal. That reads `F F F F T T T`, and the first T is the minimum, also called the drop; its index is the rotation count.

```text
nums      4  5  6  7  0  1  2
<= 2 ?    F  F  F  F  T  T  T        the first T (index 4) is the minimum, and the rotation count
```

To search, find the drop first. The target can then live in only one run, the right run if `target <= nums[-1]` and the left run otherwise, and that run is plain sorted. The classic one-pass version follows, because interviewers know it: at least one half around `mid` is a sorted run, so test whether the target lies inside that half's range and move accordingly.

<!-- cell -->

```python
def find_min_rotated(nums):                  # 153: the last index surely works, so hi = n - 1
    return nums[first_true(0, len(nums) - 1, lambda i: nums[i] <= nums[-1])]


def search_rotated(nums, target):            # 33: find the drop, then search the run that can hold target
    n = len(nums)
    drop = first_true(0, n - 1, lambda k: nums[k] <= nums[-1])    # the index of the minimum
    lo, hi = (drop, n) if target <= nums[-1] else (0, drop)       # the right run, or the left run
    i = first_true(lo, hi, lambda k: nums[k] >= target)
    return i if i < hi and nums[i] == target else -1


def search_rotated_classic(nums, target):    # 33 in one pass: one half around mid is sorted
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:            # the left half nums[lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                 # the target is inside it
            else:
                lo = mid + 1
        else:                                # the right half nums[mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


print(find_min_rotated([4, 5, 6, 7, 0, 1, 2]), find_min_rotated([3, 4, 5, 1, 2]), find_min_rotated([1, 2, 3]))   # 0 1 1
print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0), search_rotated([4, 5, 6, 7, 0, 1, 2], 3), search_rotated([4, 5, 6, 7, 0, 1, 2], 5))   # 4 -1 1
print(search_rotated_classic([4, 5, 6, 7, 0, 1, 2], 0), search_rotated_classic([3, 1], 1))   # 4 1
```

<!-- cell -->

**Try it**
- In `find_min_rotated`, compare with `nums[0]` instead of `nums[-1]` and run `[1, 2, 3]`: 3 instead of 1. An unrotated array reads `T F F` against its first value, which is not F…F T…T.
- Print `drop, lo, hi` in `search_rotated([4, 5, 6, 7, 0, 1, 2], 0)`: `4 4 7`, the right run. For target 5 it is `4 0 4`, the left run.
- In `search_rotated_classic`, change `<=` to `<` in `nums[lo] <= nums[mid]` and run `([3, 1], 1)`: -1 instead of 1.
- Feed duplicates to both versions: `search_rotated([1, 0, 1, 1, 1], 0)` and `search_rotated_classic([1, 0, 1, 1, 1], 0)` both return -1 (trap 10).

<!-- cell -->

The next variation changes what `ok` compares. Nothing says it has to compare `nums[i]` with a target: **a question about neighbours** compares it with another cell. Find Peak Element asks for any index whose value is bigger than both neighbours, where the outside of the array counts as −∞: `[1, 2, 1, 3, 5, 6, 4]` → 1 or 5. Its question is "am I going downhill?", `nums[i] > nums[i + 1]`.

Over a whole array that question is not F…F T…T, yet `first_true` still lands on a peak. Each probe keeps a climb into the window and a descent out of it: `lo == 0 or nums[lo - 1] < nums[lo]` stays true, and so does `hi == n - 1 or nums[hi] > nums[hi + 1]`. A one-cell window with both is a peak.

Single Element in a Sorted Array asks for the one value without a twin in a sorted array where every other value appears exactly twice: `[1, 1, 2, 3, 3, 4, 4, 8, 8]` → 2. Its question compares each cell with its pair partner `i ^ 1`, the index with the lowest bit flipped: the pairs match up to the single element and are shifted by one after it.

Find K Closest Elements asks for the k values nearest to x, in sorted order, with the smaller value winning a tie: `[1, 2, 3, 4, 5]` with k = 4 and x = 3 → `[1, 2, 3, 4]`. The answer is a window of k neighbours, so the search runs over its start `s`. Its question compares the window's first item, `arr[s]`, with the first item past its end, `arr[s + k]`: it turns True once the left one is no farther from x, and stays True for every later start.

<!-- cell -->

```python
def find_peak(nums):                         # 162: "am I going downhill?"
    return first_true(0, len(nums) - 1, lambda i: nums[i] > nums[i + 1])


def single_non_duplicate(nums):              # 540: pairs (0,1), (2,3)... match until the single one
    return nums[first_true(0, len(nums) - 1, lambda i: nums[i] != nums[i ^ 1])]


def find_closest_elements(arr, k, x):        # 658: binary search the window's start
    # ok(s): the item leaving on the left is no closer than the one entering on the right
    s = first_true(0, len(arr) - k, lambda s: x - arr[s] <= arr[s + k] - x)
    return arr[s:s + k]


print(find_peak([1, 2, 1, 3, 5, 6, 4]), find_peak([1, 2, 3]))                              # 5 2
print(single_non_duplicate([1, 1, 2, 3, 3, 4, 4, 8, 8]), single_non_duplicate([3, 3, 7, 7, 10, 11, 11]))   # 2 10
print(find_closest_elements([1, 2, 3, 4, 5], 4, 3), find_closest_elements([1, 1, 2, 3, 4, 5], 4, -1))      # [1, 2, 3, 4] [1, 1, 2, 3]
```

<!-- cell -->

**Try it**
- With `a = [1, 2, 1, 3, 5, 6, 4]`, print `[a[i] > a[i + 1] for i in range(6)]`: `F T F F F T`, not F…F T…T, yet `find_peak(a)` returns 5, a peak.
- Run `find_peak([1, 2, 3, 4, 5])`: 4. No probe is True, so the fallback `hi = n - 1` comes back, and the last item is a peak because the array ends in −∞.
- With `a = [1, 1, 2, 3, 3, 4, 4, 8, 8]`, print `[a[i] != a[i ^ 1] for i in range(8)]`: `F F T T T T T T`. Before the single element, pairs start at even indices; from it on, they are shifted by one.
- In `find_closest_elements`, change `<=` to `<` and rerun the first call: `[2, 3, 4, 5]`. On a tie (1 and 5 are both 2 away from 3) the problem wants the smaller elements.

<!-- cell -->

A sorted matrix is the same idea in **two dimensions**. Search a 2D Matrix asks whether a target is in a matrix whose rows are sorted and where each row starts above the previous row's end: `[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]` with target 3 → True. Search a 2D Matrix II asks the same of a matrix whose rows and columns are only sorted separately; it walks a staircase from the top-right corner instead, dropping a row or a column per step, in O(m + n), as in [Matrices](37_Matrices.ipynb#topic-matrices).

Because each row starts after the previous one ends, the rows glued end to end form one sorted list of `rows * cols` items. Don't build it: position k of that list lives at row `k // cols`, column `k % cols`, so `first_true` runs over k and reads each probe straight from the matrix.

<!-- cell -->

```python
def search_matrix(matrix, target):           # 74
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])

    def cell(k):                             # position k of the rows glued end to end
        return matrix[k // cols][k % cols]

    k = first_true(0, rows * cols, lambda k: cell(k) >= target)
    return k < rows * cols and cell(k) == target


grid = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
print(search_matrix(grid, 3), search_matrix(grid, 13), search_matrix(grid, 60))   # True False True
```

<!-- cell -->

**Try it**
- Use `rows` instead of `cols` in `cell` (`k // rows`, `k % rows`) and run `search_matrix(grid, 60)`: `IndexError`, because row `9 // 3 = 3` doesn't exist.
- Print `[grid[k // 4][k % 4] for k in range(12)]`: one sorted list, exactly what the search walks over.
- Run `search_matrix([[1, 4], [2, 5]], 2)`: `False`, although 2 is there. Those rows don't continue each other, so the glued list `[1, 4, 2, 5]` isn't sorted: that shape needs the staircase walk.
- Predict `search_matrix([[1]], 1)` and `search_matrix([[]], 1)`: `True` and `False`.

<!-- cell -->

The most important variation searches **the answer itself**. When the problem asks for the *minimum* X that works and a bigger X only makes things easier, don't construct the answer: guess it, and check the guess. The candidates are the possible answers, and `ok(x)` is a quick feasibility check, often one greedy pass.

Koko Eating Bananas asks for the slowest eating speed k that still finishes every pile within h hours, eating from one pile per hour and at most k bananas from it: `[3, 6, 7, 11]` with h = 8 → 4, because the hours are 1 + 2 + 2 + 3. The candidates are the speeds `1 .. max(piles)`, `ok(k)` is `hours(k) <= h`, and it is monotone because a faster speed never needs more hours. The fallback `max(piles)` always works, one hour per pile, and the answer is `first_true` itself.

Split Array Largest Sum asks to cut the array into k contiguous pieces so that the largest piece sum is as small as possible: `[7, 2, 5, 10, 8]` with k = 2 → 18, the split `[7, 2, 5] | [10, 8]`. The candidates are caps `max(nums) .. sum(nums)`, and `ok(cap)` is `pieces(cap) <= k`, where a greedy pass fills each piece until the next number would overflow it. It is monotone because a bigger cap never needs more pieces, and the fallback `sum(nums)` is one piece, which always works.

<!-- cell -->

```python
def min_eating_speed(piles, h):              # 875: the slowest speed that finishes within h hours
    def ok(k):
        return sum((p + k - 1) // k for p in piles) <= h      # ceil(p / k) hours per pile
    return first_true(1, max(piles), ok)     # max(piles) always works: one hour per pile


def split_array(nums, k):                    # 410: the smallest cap that needs at most k pieces
    def pieces(cap):                         # greedy: fill a piece until x would overflow it
        count, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                count, cur = count + 1, 0
            cur += x
        return count
    return first_true(max(nums), sum(nums), lambda cap: pieces(cap) <= k)


print(min_eating_speed([3, 6, 7, 11], 8), min_eating_speed([30, 11, 23, 4, 20], 5))   # 4 30
print(split_array([7, 2, 5, 10, 8], 2), split_array([1, 2, 3, 4, 5], 2))              # 18 9
```

<!-- cell -->

**Try it**
- Print Koko's landscape: `[sum((p + k - 1) // k for p in [3, 6, 7, 11]) <= 8 for k in range(1, 12)]` reads three `False`s, then `True` from k = 4 on.
- Replace the ceiling `(p + k - 1) // k` with `p // k` and rerun: 3 instead of 4. Eating 7 bananas at 3 per hour takes 3 hours, not `7 // 3 = 2`.
- Start Split Array's search at 0 instead of `max(nums)` and run `split_array([1, 4, 4], 3)`: 1 instead of 4. Below the biggest number the greedy count still says "3 pieces", but every piece holding a 4 breaks the cap.
- Capacity To Ship Packages Within D Days (1011) is this same function: predict `split_array(list(range(1, 11)), 5)` before running (15).

<!-- cell -->

The same two lines, with a different `ok`, solve a whole family. Capacity To Ship Packages Within D Days asks for the smallest ship capacity that delivers the packages, in order, within D days: weights `1 .. 10` and 5 days → 15, and its `ok` is Split Array's greedy pass with days for pieces. Smallest Divisor Given a Threshold asks for the smallest divisor d with the sum of `ceil(x / d)` at most the threshold: `[1, 2, 5, 9]` with threshold 6 → 5, and its `ok` is Koko's.

Minimum Number of Days to Make m Bouquets asks for the first day on which m bouquets of k adjacent bloomed flowers exist: bloom days `[1, 10, 3, 10, 2]` with m = 3 and k = 1 → 3, and its `ok` is one pass over the garden counting bouquets. Minimum Time to Complete Trips asks for the least time in which buses with given round-trip times finish `totalTrips` trips together: `[1, 2, 3]` and 5 trips → 3, because `sum(t // time)` first reaches 5 at t = 3.

Maximising turns the landscape over: now it reads `T T T F F F`, "this gap still fits". Don't flip the loop; search the first False and subtract 1. Magnetic Force Between Two Balls asks to put m balls into baskets at given positions so that the smallest gap between two balls is as large as possible: `[1, 2, 3, 4, 7]` with m = 3 → 3, balls at 1, 4 and 7.

The candidates are gaps `1 .. span`, where span is the last position minus the first. `fits(d)` places greedily, each ball in the first basket at least d past the previous one, and it is monotone because a bigger gap never fits more balls. The fallback `span + 1` never fits, and the answer is `first_true(..., not fits) - 1`.

<!-- cell -->

```python
def max_min_gap(position, m):                # 1552: the largest gap d that still fits m balls
    pos = sorted(position)
    def fits(d):                             # greedy: each ball in the first basket >= d away
        count, last = 1, pos[0]
        for p in pos[1:]:
            if p - last >= d:
                count, last = count + 1, p
        return count >= m
    span = pos[-1] - pos[0]
    return first_true(1, span + 1, lambda d: not fits(d)) - 1      # the last True = the first False - 1


print(max_min_gap([1, 2, 3, 4, 7], 3), max_min_gap([5, 4, 3, 2, 1, 1000000000], 2))   # 3 999999999
```

<!-- cell -->

**Try it**
- Pass `fits` instead of `not fits` and run `max_min_gap([1, 2, 3, 4, 7], 3)`: 6 instead of 3. A T…T F…F question fed to `first_true` gives garbage (trap 8).
- Add `print([fits(d) for d in range(1, span + 1)])` before the final `return` and run `max_min_gap([1, 2, 3, 4, 7], 3)`: three `True`s, then three `False`s. The first False is at d = 4, so the answer is 3.
- Use `pos = position` instead of sorting and run `max_min_gap([7, 1, 4, 2, 3], 3)`: 0 instead of 3. The greedy pass walks the baskets left to right, so they must be in order.
- Predict `max_min_gap([1, 2, 3, 4, 7], 2)` and `max_min_gap([1, 2, 3, 4, 7], 5)` before running: 6 (the two ends) and 1.

<!-- cell -->

Two more searches live in other sections. Time Based Key-Value Store asks for the value a key had at time t, given sets at increasing timestamps; `bisect_right(times, t) - 1` is the latest entry at or before t, in [Design Problems](00_Topic_Index.ipynb#s24). Random Pick with Weight asks for an index drawn with probability proportional to its weight; the first prefix sum ≥ a random ticket is the pick, in [Prefix Sums](05_Prefix_Sums.ipynb#topic-prefix-sums).

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

A **mountain** comes first, because it only glues two searches together. Find in Mountain Array asks for the smallest index holding a target in an array that strictly rises to one peak and then strictly falls, reading at most 100 cells through `get(i)`: `[1, 2, 3, 4, 5, 3, 1]` with target 3 → 2, not 5. A mountain has exactly one peak, so "am I going downhill?" *is* F…F T…T there. Find the peak, then binary search each sorted side, the rising side first because it holds the smaller index.

<!-- cell -->

```python
def find_in_mountain(arr, target):           # 1095 (each arr[i] stands for a get(i) call)
    n = len(arr)
    peak = first_true(0, n - 1, lambda k: arr[k] > arr[k + 1])    # F on the way up, T after
    i = first_true(0, peak + 1, lambda k: arr[k] >= target)       # the rising side first:
    if i <= peak and arr[i] == target:                             # it holds the smaller index
        return i
    j = first_true(peak + 1, n, lambda k: arr[k] <= target)       # the falling side: flip the test
    return j if j < n and arr[j] == target else -1


print(find_in_mountain([1, 2, 3, 4, 5, 3, 1], 3), find_in_mountain([0, 5, 3, 1], 1), find_in_mountain([1, 5, 2], 4))   # 2 3 -1
```

<!-- cell -->

**Try it**
- Search the falling side first and run `([1, 2, 3, 4, 5, 3, 1], 3)`: 5 instead of 2. Both are 3s, but the problem asks for the smaller index.
- Predict `find_in_mountain([1, 5, 2], 5)` and `find_in_mountain([1, 5, 2], 2)`: 1 (the peak itself) and 2 (on the falling side).
- Print `peak` and `i` for `([1, 2, 3, 4, 5, 3, 1], 3)`: 4 and 2. Three searches of about log₂ n probes each stay far below the 100-call budget.

<!-- cell -->

Maximising returns with a sharper check. Maximum Running Time of N Computers asks how long all n computers can run at once when batteries can be swapped between them freely: n = 2 and `[3, 3, 3]` → 4. A battery powers one computer at a time, so in t minutes it gives at most `min(b, t)` minutes, and t fails exactly when `sum(min(b, t)) < n * t`. That failure is monotone in t, `sum(batteries) // n + 1` always fails, and the answer is the first failure minus 1.

<!-- cell -->

```python
def max_run_time(n, batteries):              # 2141: can all n computers run for t minutes?
    fails = lambda t: sum(min(b, t) for b in batteries) < n * t   # a battery gives at most t minutes
    return first_true(1, sum(batteries) // n + 1, fails) - 1


print(max_run_time(2, [3, 3, 3]), max_run_time(2, [1, 1, 1, 1]))   # 4 2
```

<!-- cell -->

**Try it**
- Print the landscape of `max_run_time(2, [3, 3, 3])`: `[sum(min(3, t) for _ in range(3)) < 2 * t for t in range(1, 6)]` is `F F F F T`. The first failure is t = 5, so the answer is 4.
- Drop the `min` and count every battery in full, `sum(batteries) < n * t`, then run `max_run_time(2, [10, 1])`: 5 instead of 1. The 10-minute battery cannot power both computers at once.
- Check the fallback for `max_run_time(2, [3, 3, 3])`: `sum(batteries) // n + 1` is 5, and `sum(min(b, 5) for b in [3, 3, 3]) < 2 * 5` is `True`. Any t above `sum(batteries) // n` needs more battery-minutes than exist, so the fallback always fails.

<!-- cell -->

Real-valued answers have no "next candidate", so `mid + 1` and `first_true` don't apply (trap 7). Maximum Average Subarray II asks for the largest average of a contiguous subarray of length at least k: `[1, 12, -5, -6, 50, 3]` with k = 4 → 12.75, from `[12, -5, -6, 50]`. Binary search the average x with `mid = (lo + hi) / 2` and `lo = mid` or `hi = mid`, for a fixed number of rounds: 50 rounds shrink the gap by 2⁵⁰ ≈ 10¹⁵.

Its check is a trick worth keeping: a window averages at least x exactly when the sum of (value − x) over it is at least 0. "Does some window of length ≥ k have a sum ≥ 0?" is one pass over prefix sums, each prefix compared with the smallest prefix at least k positions earlier.

Counting replaces listing when the **k-th smallest** lives in something too big to write out. The k-th smallest value is the smallest v with at least k items ≤ v, so you never list the items: you *count* those ≤ v and binary search v. The answer always occurs in the data, because the count grows only at values that occur, so the first v where it reaches k is one of them.

Kth Smallest Number in Multiplication Table asks for the k-th smallest entry of the m × n table of products: m = n = 3 with k = 5 → 3. Row i holds `i, 2i, ..., n·i`, so it has `min(n, v // i)` entries ≤ v, one division per row. Kth Smallest Element in a Sorted Matrix (378) asks the same of a matrix with sorted rows and columns, and counts with a staircase in [Matrices](37_Matrices.ipynb#topic-matrices).

Find K-th Smallest Pair Distance asks for the k-th smallest `|nums[i] - nums[j]|` over all pairs: `[1, 3, 1]` with k = 1 → 0. Once the array is sorted, the pairs at distance ≤ d are counted with a sliding window (the window from [Sliding Window](07_Sliding_Window.ipynb#topic-sliding-window)): for each right end, every item from `left` on is close enough to pair with it.

<!-- cell -->

```python
def kth_in_mult_table(m, n, k):              # 668
    def count_le(v):                         # entries <= v; row i holds i, 2i, ..., n*i
        return sum(min(n, v // i) for i in range(1, m + 1))
    return first_true(1, m * n, lambda v: count_le(v) >= k)


def kth_pair_distance(nums, k):              # 719
    nums = sorted(nums)
    def count_le(d):                         # pairs at distance <= d, with a sliding window
        count, left = 0, 0
        for right, x in enumerate(nums):
            while x - nums[left] > d:
                left += 1
            count += right - left            # nums[left..right-1] each pair up with x
        return count
    return first_true(0, nums[-1] - nums[0], lambda d: count_le(d) >= k)


print(kth_in_mult_table(3, 3, 5), kth_in_mult_table(2, 3, 6))            # 3 6
print(kth_pair_distance([1, 3, 1], 1), kth_pair_distance([1, 6, 1], 3))   # 0 5
```

<!-- cell -->

**Try it**
- Print the counts of the 3 × 3 table: `[sum(min(3, v // i) for i in range(1, 4)) for v in range(1, 10)]` is `[1, 3, 5, 6, 6, 8, 8, 8, 9]`. The first v with a count ≥ 5 is 3, and the count doesn't grow at 5 because 5 isn't in the table.
- Remove the `min(n, ...)` and run `kth_in_mult_table(2, 3, 6)`: 4 instead of 6. Row 1 has only 3 entries, but `4 // 1` counts 4 of them.
- List the pair distances of `[1, 6, 1]` by hand (0, 5, 5), then check `kth_pair_distance([1, 6, 1], k)` for k = 1, 2, 3: 0, 5, 5.
- Predict `kth_pair_distance([1, 1, 1], 2)`: 0. Duplicates give distance 0, which is why the search starts at 0.

<!-- cell -->

The last variation binary searches a cut rather than a value. Median of Two Sorted Arrays asks for the median of **two sorted arrays** taken together, in O(log(m + n)): `[1, 3]` and `[2]` → 2.0, `[1, 2]` and `[3, 4]` → 2.5. Don't merge: the median splits all m + n items into a left half of `half = (m + n + 1) // 2` items and a right half, like this:

```text
a:  1  3 | 8  9            i = 2 items from a                     half = (4 + 5 + 1) // 2 = 5
b:  2  4  5 | 7  10        j = half - i = 3 items from b
left = {1, 3, 2, 4, 5}, right = {8, 9, 7, 10}:  max(left) = 5 <= 7 = min(right), so the median is 5
```

The left half is a prefix of `a` with i items plus a prefix of `b` with `half - i` items, so the whole problem is choosing i. Taking one more item from `a` can only raise `a`'s right edge and lower `b`'s left edge, so "the last item of `b`'s left part ≤ the first item of `a`'s right part" reads F…F T…T in i. Its first True is the cut where everything on the left is ≤ everything on the right.

<!-- cell -->

```python
def find_median(a, b):                       # 4
    if len(a) > len(b):
        a, b = b, a                          # cut the SHORTER array, so j stays inside b
    m, n = len(a), len(b)
    half = (m + n + 1) // 2                  # size of the left half
    # i items of a + (half - i) items of b form the left half. As i grows, "the last item of
    # b's left part (b[j-1]) <= the first item of a's right part (a[i])" flips from F to T.
    i = first_true(0, m, lambda c: b[half - c - 1] <= a[c])
    j = half - i
    left = max(a[i - 1] if i > 0 else -math.inf, b[j - 1] if j > 0 else -math.inf)
    if (m + n) % 2:
        return float(left)
    right = min(a[i] if i < m else math.inf, b[j] if j < n else math.inf)
    return (left + right) / 2


print(find_median([1, 3], [2]), find_median([1, 2], [3, 4]), find_median([], [1]))   # 2.0 2.5 1.0
print(find_median([1, 3, 8, 9], [2, 4, 5, 7, 10]))                                  # 5.0
```

<!-- cell -->

**Try it**
- Remove the swap and run `find_median([1, 2, 3, 4, 5], [6])`: `IndexError`. With the longer array on the cut side, `half - i - 1` points past the end of `b`.
- Print `i, j` for the example in the picture: 2 and 3.
- In `find_median([1, 2], [3, 4])` the cut is `i = 2, j = 0`: all of `b` is on the right, so its left edge is the `-math.inf` stand-in. Print `left, right` to see 2 and 3.
- Predict `find_median([1, 1, 1], [1, 1])`: 1.0. Equal values are fine because the test uses `<=`.

<!-- cell -->

### Say it in the interview

Koko is the version most interviewers ask, so the script uses it:

> "The brute force tries every speed from 1 upward and checks each one: O(max · n). But the check is monotone: if speed k finishes in time, every faster speed does too. So the answers look like F F F T T T, and I'll binary search for the first T between 1 and max(piles). That's O(n log max) time and O(1) space."

Then point at three things while you code: the definition of `ok` and why it is monotone; the invariant, "the first True is in `[lo, hi]`, and `hi` is known to work"; and why `hi = mid` keeps mid while the loop still ends, because `mid < hi`.

The follow-ups are predictable. `max(piles)` is enough because at that speed every pile takes one hour, and `h` is at least the number of piles. A tighter lower bound is `ceil(sum(piles) / h)`, since any slower speed cannot eat everything in h hours, even before rounding each pile up. Values up to 10⁹ need about 30 checks, since 2³⁰ ≈ 10⁹. If `h < len(piles)`, no speed works, because every pile needs at least an hour; say so and return -1, although the problem rules it out.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Binary Search | `binary_search/binary_search.py` · `practice/simple/basics/searches/01_binary_search_variants.py` | closed window `[lo, hi]` with `while lo <= hi`; both moves skip mid |
| Capacity To Ship Packages Within D Days | `practice/simple/basics/searches/02_binary_search_on_answer.py` | first capacity in [max(w), sum(w)] whose greedy day count fits within days |
| Find First and Last Position of Element in Sorted Array | `binary_search/find_first_and_last_position.py` | first = first index ≥ target; last = first index > target, minus 1; absent when nums[first] ≠ target |
| Find in Mountain Array | `binary_search/find_in_mountain_array.py` | find the peak with `arr[i] > arr[i+1]`, search the rising side first, then the falling side |
| Find K-th Smallest Pair Distance | `binary_search/find_kth_smallest_pair_distance.py` | binary search the distance d; count pairs ≤ d with a sliding window on the sorted array |
| Find Minimum in Rotated Sorted Array | `binary_search/find_min_rotated_sorted_array.py` | `nums[i] <= nums[-1]` reads F…F T…T; the first T is the minimum |
| Find Peak Element | `binary_search/find_peak_element.py` | first_true on "am I going downhill?"; a climb into the window and a descent out of it survive every probe |
| Koko Eating Bananas | `binary_search/koko_eating_bananas.py` · `practice/simple/19_koko_eating_bananas.py` | the first speed in [1, max(piles)] whose total of ceil(p / k) hours fits in h |
| Kth Smallest Number in Multiplication Table | `binary_search/kth_smallest_number_in_multiplication_table.py` | count entries ≤ v as the sum of min(n, v // i); the first v with count ≥ k |
| Magnetic Force Between Two Balls | `binary_search/magnetic_force_between_two_balls.py` | maximise: the first gap where greedy placement fails, minus 1 |
| Maximum Average Subarray II | `binary_search/maximum_average_subarray_ii.py` | binary search the real-valued average; avg ≥ x iff the sum of (v − x) ≥ 0, via prefix minima |
| Maximum Running Time of N Computers | `binary_search/maximum_running_time_of_n_computers.py` | t minutes work iff the sum of min(b, t) ≥ n·t; the answer is the first failing t, minus 1 |
| Median of Two Sorted Arrays | `binary_search/median_of_two_sorted_arrays.py` | binary search how many items of the shorter array join the left half |
| Search a 2D Matrix | `binary_search/search_2d_matrix.py` | the rows glued end to end are one sorted list; position k is `divmod(k, cols)` |
| Search Insert Position | `binary_search/search_insert_position.py` | lower bound with hi = len(nums), so "after everything" is a possible answer |
| Search in Rotated Sorted Array | `binary_search/search_rotated_sorted_array.py` · `practice/simple/18_search_in_rotated_sorted_array.py` | find the drop (first nums[i] ≤ nums[-1]), then binary search the one run that can hold the target |
| Split Array Largest Sum | `binary_search/split_array_largest_sum.py` · `practice/simple/20_split_array_largest_sum.py` | binary search the cap in [max, sum]; a greedy pass counts the pieces, feasible iff ≤ k |

### Self-check

1. In the first-True loop, why `hi = mid` and not `hi = mid - 1`, and why does that force `while lo < hi`?
<details><summary>Answer</summary><code>ok(mid)</code> being True means mid could itself be the first True, so it must stay in the window. Because mid stays, the loop has to stop when one candidate is left (<code>lo == hi</code>). With <code>lo <= hi</code> it would go on: either it probes the same mid forever (<code>hi = mid</code> changes nothing), or, when <code>hi == len(nums)</code>, it reads past the end.</details>

2. Koko: what makes binary search on the speed legal, and why are the bounds 1 and max(piles)?
<details><summary>Answer</summary>Monotonicity: a faster speed never needs more hours, so the answers read F…F T…T. Speed 1 is the smallest meaningful speed (0 never finishes and divides by zero), and max(piles) always works, because every pile then takes exactly one hour and h is at least the number of piles.</details>

3. You need the *largest* value that works. How do you get it without writing a new loop?
<details><summary>Answer</summary>Its landscape reads T…T F…F, so ask the opposite question: <code>first_true(lo, hi, lambda x: not works(x)) - 1</code>, with <code>hi</code> one past the largest candidate (a value that surely fails). The other way is the round-up loop (<code>mid = (lo + hi + 1) // 2</code> with <code>lo = mid</code>); rounding down there would loop forever when <code>hi == lo + 1</code>.</details>

4. Kth Smallest Number in Multiplication Table returns the first v with count(v) ≥ k. Why is that v guaranteed to be in the table?
<details><summary>Answer</summary>count(v) only increases at values that occur in the table. At the first v with count(v) ≥ k we have count(v − 1) &lt; k, so the count increased at v, so v occurs in the table.</details>
