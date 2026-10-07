## Binary Search

> Every binary search answers one question: **where does a yes/no answer flip?** Line the candidates up so the answers read `F F F F T T T T`, keep a window that always contains the first `T`, and look at the middle: one look throws away half the window.

**Reach for it when** the input is sorted, or sorted in pieces (rotated, a mountain, a matrix whose rows continue each other); when the problem demands O(log n); or when it asks for the **minimum X such that ...** or the **maximum X such that ...** and making X bigger only ever makes the condition easier (or only harder): that is binary search on the answer. Also "the k-th smallest" in something too big to list, when you can *count* how many items are ≤ v quickly.

**In this repo:** `binary_search/` (16 problems) · bank: `practice/simple/18_search_in_rotated_sorted_array.py`, `practice/simple/19_koko_eating_bananas.py`, `practice/simple/20_split_array_largest_sum.py` · basics: `practice/simple/basics/searches/01_binary_search_variants.py`, `practice/simple/basics/searches/02_binary_search_on_answer.py`, `practice/simple/basics/matrices/04_search_2d_matrix_staircase.py`

### The picture

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

**Why it is fast:** a linear scan learns about one cell per look. But in `F F F T T T`, a `T` in the middle tells you that every cell to its right is `T` too, and an `F` tells you every cell to its left is `F`. So each look settles half of the remaining candidates: a million candidates need 20 looks, a billion need 30. Notice what binary search really needs: not sorted *data*, but a *question* whose answers are sorted. That is why it also works on rotated arrays, on peaks, and on the answer itself.

**Why it is correct:** the window always contains the first `T`: every candidate left of `lo` is known to be `F`, and `hi` is known to be `T` (or is past the end). A probe keeps both facts true on either branch, and every probe makes the window smaller, so the loop ends with `lo == hi` sitting on the first `T`.

### From idea to code

**The idea in one sentence:** *write `ok(x)`, which is False for small x and True from some point on; keep `[lo, hi]` so that the first True is always inside; test the middle and move the side that the test proves.*

| Decision | Binary-search answer |
|---|---|
| **State / Definition** | two integers: the first True lies in `[lo, hi]`. `hi` itself is never tested: it is one past the last candidate, or a value already known to be True |
| **Invariant** | every candidate left of `lo` is F; `hi` is T (or past the end); the window shrinks every step |
| **Step** | probe `mid = (lo + hi) // 2`: `if ok(mid): hi = mid` (mid might be the first T, keep it) `else: lo = mid + 1` (mid is F, drop it) |
| **Fix** | none: each probe moves one side and keeps the invariant by itself |
| **Record** | never during the loop: when `lo == hi` the window has shrunk onto the answer |
| **Init** | `lo` = the smallest candidate; `hi` = the fallback answer: one past the largest (`len(nums)`), or a value that surely works |
| **Return** | `lo`; then turn "no True at all" (`lo == len(nums)`, or `nums[lo] != target`) into `-1` |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "the answer is somewhere from lo up to hi" | `lo, hi = 0, len(nums)` |
| "something is still untested" | `while lo < hi:` |
| "look in the middle" | `mid = (lo + hi) // 2` (rounds down, so `lo <= mid < hi`) |
| "mid works, so the first one that works is mid or earlier" | `hi = mid` |
| "mid fails, so the first one that works is after mid" | `lo = mid + 1` |
| "the first one that works" | `return lo` |
| "is the target really there?" | `lo < len(nums) and nums[lo] == target` |
| "the last one that works" | the first one that fails, minus 1 |

The template, then the same loop with the question passed in (`first_true`), so that every later problem is just "write `ok`". Exact search, which can stop the moment it finds the target, is where the closed `lo <= hi` window fits naturally:

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

**Try it**
- Change `hi = mid` to `hi = mid - 1` in `lower_bound` and run `lower_bound([1, 5], 4)`: 0 instead of 1. Mid *was* the first True, and you threw it away.
- Predict what `while lo <= hi` would do in `lower_bound([1, 5], 4)`: once `lo == hi == 1`, mid is 1, `ok(1)` is True, and `hi = mid` changes nothing, so it loops forever. (If you run it, interrupt the kernel.)
- Print `lo, hi` at the top of the loop in `search(nums, 4)`: `0 6`, `0 2`, `2 2`. The window holds 7, then 3, then 1 candidate, and the loop stops when `lo` passes `hi`.
- Compare with the library: `bisect.bisect_left(nums, 4)` is 3, the same as `lower_bound`, and `bisect.bisect_right(nums, 3)` is 3, the first index with a value `> 3`.

**The recipe: never edit the loop.** Every problem in this section is four decisions around `first_true`:

1. Write `ok(x)` so the candidates read F…F T…T. For a *maximum*, search the first False and subtract 1.
2. Check it out loud: "if `ok(x)` is True, is `ok(x + 1)` True too?"
3. `lo` = the smallest candidate; `hi` = the fallback answer, returned when nothing in `[lo, hi)` is True: `len(nums)` for "none", or a value that surely works (`max(piles)`).
4. `i = first_true(lo, hi, ok)`, and check `i < len(nums)` before reading `nums[i]`.

Two views of the same window help: the answer is one of `lo..hi`, the untested cells are `lo..hi-1`, and the loop runs while something is untested. In Python you rarely write the loop for a sorted list: `bisect.bisect_left(a, x)` is `lower_bound`, `bisect.bisect_right(a, x)` is the first index `> x`, and on Python 3.10+ `lo + bisect.bisect_left(range(lo, hi), True, key=ok)` equals `first_true(lo, hi, ok)` (more in [Python Toolkit](#s02)). In an interview, say you'd use `bisect`, write the loop if asked, and use `bisect` as your tester.

The loop styles you will meet, and why none of them hangs:

| Style | Loop | Moves | Why it ends | Use it for |
|---|---|---|---|---|
| **first True** (the template) | `while lo < hi` | `hi = mid` / `lo = mid + 1` | `mid < hi` (rounded down), so `hi = mid` still shrinks the window | boundaries, the minimum that works, rotations, peaks; the maximum as "first False − 1" |
| **closed window** | `while lo <= hi` | `lo = mid + 1` / `hi = mid - 1` | both moves skip `mid` | exact match, returning as soon as you find it |
| **record-and-skip** | `while lo <= hi` | `if ok(mid): ans, hi = mid, mid - 1`, else `lo = mid + 1` | both moves skip `mid` | fine if it is your habit; start `ans` at the "none" value |
| **last True** | `while lo < hi`, `mid = (lo + hi + 1) // 2` | `lo = mid` / `hi = mid - 1` | `mid > lo` (rounded up), so `lo = mid` still shrinks the window | recognise it in other code; "first False − 1" avoids it |

Never mix them: `while lo <= hi` with `hi = mid` loops forever once `lo == hi` and `ok(mid)` is True, and `lo = mid` with a rounded-down `mid` loops forever once `hi == lo + 1` and `ok(mid)` is True.

### Watch it work

Each row is one probe. The window `[lo, hi)` shows its letters, everything already settled is a dot, and `[ ]` marks mid:

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

**Try it**
- Trace `x = 13`, bigger than everything: every probe is F, `lo` walks up to 7 = `len(nums)`, and the last line says there is no T at all ("insert at the very end").
- Trace `x = 0`, smaller than everything: every probe is T and `hi` walks down to 0.
- Trace `x = 3`: there are two 3s, and the search lands on the first one, index 1.
- On `list(range(1000))`, count the loop rounds of `lower_bound` for every x from -1 to 1000: never more than 10, because 2¹⁰ = 1024.

### Where it goes wrong

1. **`hi = mid - 1` in the first-True loop.** If mid *is* the first True, you just threw the answer away: `lower_bound([1, 5], 4)` returns 0 instead of 1. Only a test that proves "mid is wrong" may skip mid.
2. **Mixing the loop styles.** `while lo <= hi` with `hi = mid` never ends once `lo == hi` and `ok(mid)` is True. `lo = mid` with `mid = (lo + hi) // 2` never ends when `hi == lo + 1` and `ok(mid)` is True. Rule: `lo = mid` needs `mid = (lo + hi + 1) // 2`.
3. **`hi = len(nums) - 1` when "nothing qualifies" is possible.** Search Insert Position on `[1, 3, 5, 6]` with target 7 must return 4, which only exists if `hi` starts at `len(nums)`.
4. **A question that isn't monotone.** Binary search never complains; it quietly returns garbage. Before coding, say out loud: "if `ok(x)` is True, is `ok(x + 1)` True too?" (Koko: a faster speed never needs more hours.)
5. **Bad bounds on the answer.** `lo` must be a real candidate and `hi` must surely work. Koko's speed starts at 1 (speed 0 divides by zero) and `max(piles)` always works. Split Array's cap starts at `max(nums)`: with a smaller cap, the greedy count goes wrong (`[1, 4, 4]`, k = 3 would answer 1).
6. **Rotated arrays: `<` instead of `<=`.** In the classic one-pass search, `nums[lo] <= nums[mid]` needs the `=` when `lo == mid` (two items left): with `<`, `[3, 1]` never finds the 1.
7. **Integer moves on real numbers.** On a real-valued answer, `lo = mid + 1` jumps right over the answer. Move `lo = mid` / `hi = mid`, and stop after a fixed number of rounds (50 to 100) or once `hi - lo` is tiny.
8. **Midpoints in other languages.** In Java or C++, `/` truncates toward zero, so with negative bounds `(lo + hi) / 2` rounds *up* and `hi = mid` can stall, and `lo + hi` can overflow. `lo + (hi - lo) / 2` fixes both. Python's `//` floors, so `first_true(-10, -2, ok)` is fine.
9. **A T…T F…F question fed to `first_true`.** It returns garbage without complaint: in `max_min_gap` below, passing `fits` instead of `not fits` gives 6 instead of 3 for `[1, 2, 3, 4, 7]`, m = 3. For a maximum, search the first False and subtract 1.
10. **Reading `nums[lo]` unchecked.** When nothing qualifies, `lo == len(nums)`: `lower_bound([1, 3], 5)` is 2, and `nums[2]` raises `IndexError`. Check `lo < len(nums)` first.
11. **Duplicates break the rotated questions.** With repeats, `nums[i] <= nums[-1]` no longer separates the two runs: `find_min_rotated([1, 1, 0, 1])` returns 1 (the minimum is 0), and `search_rotated([1, 0, 1, 1, 1], 0)` returns -1. The follow-ups (154, 81) shrink `hi -= 1` when `nums[mid] == nums[hi]`, which costs O(n) in the worst case.
12. **"The last copy is `lower_bound(x + 1) - 1`" only works for integers.** For `[1.0, 1.5, 1.5, 2.0]` and x = 1.5 it gives 3 instead of 2. The general form is "the first index with `nums[i] > x`, minus 1" (`bisect_right(nums, x) - 1`).

### Edge cases to say out loud

Empty array · one element · target below everything / above everything · all equal · duplicates (the first copy or the last?) · two elements (where infinite loops show up) · the answer at index 0 or at `len(nums)`.

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

**Try it**
- Predict, then add: `assert lower_bound([1, 2, 2, 2, 3], 3) == 4`.
- The *last* copy of x is the first index with `nums[i] > x`, minus one. With `a = [2, 2, 2]`, assert `first_true(0, len(a), lambda i: a[i] > 2) - 1 == 2`.
- `first_true(5, 5, ok)` has an empty range and returns 5 without calling `ok`. Check it with `ok = lambda x: 1 / 0`: no `ZeroDivisionError`.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Exact match** | closed window, return on `==` | 704 |
| **Lower / upper bound** | `ok = nums[i] >= x` or `nums[i] > x`; all copies of x sit in `[lower, upper)` | 35, 34 |
| **Rotated array** | `ok(i) = nums[i] <= nums[-1]` finds the drop; then search the one run that can hold the target | 153, 33 |
| **A question about neighbours** | `ok` compares `nums[i]` with another cell: the next one, its pair partner, the cell k ahead | 162, 540, 658 |
| **2D matrix** | rows continue each other: position k is cell `divmod(k, cols)` | 74 (240 uses a staircase walk instead) |
| **On the answer, minimise** | the candidates are answers; `ok = feasible(x)`, often one greedy pass | 875, 410 |
| **The same code, a different `ok`** | ship within days, smallest divisor, make m bouquets, minimum time for trips | 1011, 1283, 1482, 2187 |
| **On the answer, maximise** | the last True = the first False − 1 | 1552, 2141 |
| **Mountain** | find the peak, then a normal search on each side | 1095 |
| **K-th smallest by counting** | `ok(v) = count(items <= v) >= k` | 668, 719; 378 counts with a staircase, in [Matrices](#s21) |
| **Real numbers** | `lo = mid` / `hi = mid`, a fixed number of rounds | 644 |
| **Cut two sorted arrays** | binary search how many items of the shorter array go left | 4 |
| **A key's history** | `bisect_right(times, t) - 1` is the latest entry at or before t | 981, in [Design](#s24) |
| **Weighted random pick** | the first prefix sum ≥ a random ticket | 528, in [Prefix Sums](#s04) |

**Rotated arrays** (153, 33): a rotated array is two sorted runs with a drop between them. Compare every value with the *last* one: the left run is all bigger, the right run all smaller or equal. That is `F F F F T T T`, and the first T is the minimum, also called the drop. To search, find the drop first; then the target can only live in one run (the right run if `target <= nums[-1]`, the left run otherwise), and that run is plain sorted. The classic one-pass version is shown too, because interviewers know it: at least one half around `mid` is a sorted run, so test whether the target lies inside that half's range.

```text
nums      4  5  6  7  0  1  2
<= 2 ?    F  F  F  F  T  T  T        the first T (index 4) is the minimum, and the rotation count
```

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

**Try it**
- In `find_min_rotated`, compare with `nums[0]` instead of `nums[-1]` and run `[1, 2, 3]`: 3 instead of 1. An unrotated array reads `T F F` against its first value, which is not F…F T…T.
- Print `drop, lo, hi` in `search_rotated([4, 5, 6, 7, 0, 1, 2], 0)`: `4 4 7`, the right run. For target 5 it is `4 0 4`, the left run.
- In `search_rotated_classic`, change `<=` to `<` in `nums[lo] <= nums[mid]` and run `([3, 1], 1)`: -1 instead of 1.
- Feed duplicates to both versions: `search_rotated([1, 0, 1, 1, 1], 0)` and `search_rotated_classic([1, 0, 1, 1, 1], 0)` both return -1 (trap 11).

**A question about neighbours** (162, 540, 658): `ok` doesn't have to compare `nums[i]` with a target; it can compare it with another cell. Find Peak asks "am I going downhill?" (`nums[i] > nums[i + 1]`). Over a whole array that question is not F…F T…T, yet `first_true` still lands on a peak: each probe keeps a climb into the window and a descent out of it (`lo == 0 or nums[lo - 1] < nums[lo]`, and `hi == n - 1 or nums[hi] > nums[hi + 1]`), and a one-cell window with both is a peak. Single Element in a Sorted Array compares each cell with its pair partner `i ^ 1`; K Closest Elements compares the two ends of a window of size k starting at `s`.

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

**Try it**
- With `a = [1, 2, 1, 3, 5, 6, 4]`, print `[a[i] > a[i + 1] for i in range(6)]`: `F T F F F T`, not F…F T…T, yet `find_peak(a)` returns 5, a peak.
- Run `find_peak([1, 2, 3, 4, 5])`: 4. No probe is True, so the fallback `hi = n - 1` comes back, and the last item is a peak because the array ends in −∞.
- With `a = [1, 1, 2, 3, 3, 4, 4, 8, 8]`, print `[a[i] != a[i ^ 1] for i in range(8)]`: `F F T T T T T T`. Before the single element, pairs start at even indices; from it on, they are shifted by one.
- In `find_closest_elements`, change `<=` to `<` and rerun the first call: `[2, 3, 4, 5]`. On a tie (1 and 5 are both 2 away from 3) the problem wants the smaller elements.

**2D matrix** (74): when each row starts after the previous one ends, the rows glued end to end form one sorted list of `rows * cols` items. Don't build it: position k of that list lives at row `k // cols`, column `k % cols`. (When rows and columns are only sorted separately, as in 240, the glued list isn't sorted; walk a staircase from the top-right corner instead, dropping a row or a column per step: O(m + n).)

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

**Try it**
- Use `rows` instead of `cols` in `cell` (`k // rows`, `k % rows`) and run `search_matrix(grid, 60)`: `IndexError`, because row `9 // 3 = 3` doesn't exist.
- Print `[grid[k // 4][k % 4] for k in range(12)]`: one sorted list, exactly what the search walks over.
- Run `search_matrix([[1, 4], [2, 5]], 2)`: `False`, although 2 is there. Those rows don't continue each other, so the glued list `[1, 4, 2, 5]` isn't sorted: that shape needs the staircase walk.
- Predict `search_matrix([[1]], 1)` and `search_matrix([[]], 1)`: `True` and `False`.

**Binary search on the answer** (875, 410, 1552, 2141): when the problem asks for the *minimum* X that works and a bigger X only makes things easier, don't construct the answer: guess it, and check the guess. The candidates are the possible answers, and `ok(x)` is a quick feasibility check, often one greedy pass. The recipe's decisions for three classics:

| Decision | Koko (875) | Split Array (410) | Magnetic Force (1552) |
|---|---|---|---|
| **Candidates** | speeds `1 .. max(piles)` | caps `max(nums) .. sum(nums)` | gaps `1 .. span` (span = last − first position) |
| **ok** | `hours(k) <= h` | `pieces(cap) <= k` | `not fits(d)` |
| **Monotone because** | a faster speed never needs more hours | a bigger cap never needs more pieces | a bigger gap never fits more balls |
| **hi (fallback)** | `max(piles)`: always works | `sum(nums)`: one piece always works | `span + 1`: never fits |
| **Return** | `first_true(...)` | `first_true(...)` | `first_true(...) - 1` |

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

**Try it**
- Print Koko's landscape: `[sum((p + k - 1) // k for p in [3, 6, 7, 11]) <= 8 for k in range(1, 12)]` reads three `False`s, then `True` from k = 4 on.
- Replace the ceiling `(p + k - 1) // k` with `p // k` and rerun: 3 instead of 4. Eating 7 bananas at 3 per hour takes 3 hours, not `7 // 3 = 2`.
- Start Split Array's search at 0 instead of `max(nums)` and run `split_array([1, 4, 4], 3)`: 1 instead of 4. Below the biggest number the greedy count still says "3 pieces", but every piece holding a 4 breaks the cap.
- Capacity To Ship Packages (1011) is this same function: predict `split_array(list(range(1, 11)), 5)` before running (15).

**Maximise** (1552, 2141): now the landscape reads `T T T F F F` ("this gap still fits", "this many minutes still works"). Don't flip the loop: search the first False and subtract 1.

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


def max_run_time(n, batteries):              # 2141: can all n computers run for t minutes?
    fails = lambda t: sum(min(b, t) for b in batteries) < n * t   # a battery gives at most t minutes
    return first_true(1, sum(batteries) // n + 1, fails) - 1


print(max_min_gap([1, 2, 3, 4, 7], 3), max_min_gap([5, 4, 3, 2, 1, 1000000000], 2))   # 3 999999999
print(max_run_time(2, [3, 3, 3]), max_run_time(2, [1, 1, 1, 1]))                      # 4 2
```

**Try it**
- Pass `fits` instead of `not fits` and run `max_min_gap([1, 2, 3, 4, 7], 3)`: 6 instead of 3. A T…T F…F question fed to `first_true` gives garbage (trap 9).
- Print the landscape of `max_run_time(2, [3, 3, 3])`: `[sum(min(3, t) for _ in range(3)) < 2 * t for t in range(1, 6)]` is `F F F F T`. The first failure is t = 5, so the answer is 4.
- Why is `sum(batteries) // n + 1` a safe fallback? Running n computers that long needs more battery-minutes than exist, so it always fails.
- Predict `max_min_gap([1, 2, 3, 4, 7], 2)` and `max_min_gap([1, 2, 3, 4, 7], 5)` before running: 6 (the two ends) and 1.

**Harder variations (second pass).** Mountain arrays, k-th smallest by counting, real-valued answers and the median of two arrays come up less often; read them once the first pass feels easy.

**Mountain** (1095): a mountain has exactly one peak, so "am I going downhill?" *is* F…F T…T there. Find the peak, then binary search each sorted side. Search the rising side first: it holds the smaller index.

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

**Try it**
- Search the falling side first and run `([1, 2, 3, 4, 5, 3, 1], 3)`: 5 instead of 2. Both are 3s, but the problem asks for the smaller index.
- Predict `find_in_mountain([1, 5, 2], 5)` and `find_in_mountain([1, 5, 2], 2)`: 1 (the peak itself) and 2 (on the falling side).
- Print `peak` and `i` for `([1, 2, 3, 4, 5, 3, 1], 3)`: 4 and 2. Three searches of about log₂ n probes each stay far below the 100-call budget.

**K-th smallest by counting** (668, 719): the k-th smallest value is the smallest v with at least k items ≤ v. So you never list the items; you only *count* those ≤ v, and binary search v. Counting is cheap thanks to structure: row i of a multiplication table is `i, 2i, ..., n·i`, so it has `min(n, v // i)` entries ≤ v; in a sorted array, the pairs at distance ≤ d are counted with a sliding window. The result always occurs in the data: the count only grows at values that occur, so the first v where it reaches k is one of them.

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

**Try it**
- Print the counts of the 3 × 3 table: `[sum(min(3, v // i) for i in range(1, 4)) for v in range(1, 10)]` is `[1, 3, 5, 6, 6, 8, 8, 8, 9]`. The first v with a count ≥ 5 is 3, and the count doesn't grow at 5 because 5 isn't in the table.
- Remove the `min(n, ...)` and run `kth_in_mult_table(2, 3, 6)`: 4 instead of 6. Row 1 has only 3 entries, but `4 // 1` counts 4 of them.
- List the pair distances of `[1, 6, 1]` by hand (0, 5, 5), then check `kth_pair_distance([1, 6, 1], k)` for k = 1, 2, 3: 0, 5, 5.
- Predict `kth_pair_distance([1, 1, 1], 2)`: 0. Duplicates give distance 0, which is why the search starts at 0.

**Real numbers** (644): with a real-valued answer there is no "next candidate", so `first_true` and `mid + 1` don't apply: move `lo = mid` or `hi = mid`, and stop after a fixed number of rounds. Each round halves the gap, so 50 rounds shrink it by 2⁵⁰ ≈ 10¹⁵. The check for Maximum Average Subarray II is a trick worth keeping: *a window's average is ≥ x exactly when the sum of (value − x) over it is ≥ 0*, and "does some window of length ≥ k have a sum ≥ 0" is one pass over prefix sums.

```python
def avg_at_least(nums, k, x):                # does some window of length >= k average >= x?
    prefix, lowest = [0.0], math.inf
    for v in nums:
        prefix.append(prefix[-1] + v - x)    # average >= x  <=>  the sum of (v - x) is >= 0
    for j in range(k, len(nums) + 1):
        lowest = min(lowest, prefix[j - k])  # the best start at least k items before j
        if prefix[j] >= lowest:
            return True
    return False


def max_average(nums, k):                    # 644
    lo, hi = min(nums), max(nums)            # every average lies between these
    for _ in range(50):                      # each round halves [lo, hi]
        mid = (lo + hi) / 2
        if avg_at_least(nums, k, mid):
            lo = mid                         # mid is reachable: the answer is >= mid
        else:
            hi = mid
    return lo


print(round(max_average([1, 12, -5, -6, 50, 3], 4), 5), round(max_average([5], 1), 5))   # 12.75 5.0
```

**Try it**
- With `nums = [1, 12, -5, -6, 50, 3]`, print `avg_at_least(nums, 4, 12.75)` and `avg_at_least(nums, 4, 12.76)`: `True`, then `False`. That flip is the answer.
- Add `print(hi - lo)` before the `return`: about 5e-14. The starting gap of 56 was halved 50 times.
- Change `range(50)` to `range(10)` and print the raw result: about 12.70, because after 10 halvings the window is still 56 / 1024 ≈ 0.055 wide.
- Run `round(max_average([1, 12, -5, -6, 50, 3], 1), 5)`: 50.0, a window of one item. The length rule is what makes the problem hard.

**Median of two sorted arrays** (4): don't merge. The median splits all m + n items into a left half of `half = (m + n + 1) // 2` items and a right half. The left half is a prefix of `a` (i items) plus a prefix of `b` (`half - i` items), so the whole problem is choosing i. Taking one more item from `a` can only raise `a`'s right edge and lower `b`'s left edge, so "the last item of `b`'s left part ≤ the first item of `a`'s right part" reads F..F T..T in i, and its first True is the cut where everything on the left is ≤ everything on the right.

```text
a:  1  3 | 8  9            i = 2 items from a                     half = (4 + 5 + 1) // 2 = 5
b:  2  4  5 | 7  10        j = half - i = 3 items from b
left = {1, 3, 2, 4, 5}, right = {8, 9, 7, 10}:  max(left) = 5 <= 7 = min(right), so the median is 5
```

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

**Try it**
- Remove the swap and run `find_median([1, 2, 3, 4, 5], [6])`: `IndexError`. With the longer array on the cut side, `half - i - 1` points past the end of `b`.
- Print `i, j` for the example in the picture: 2 and 3.
- In `find_median([1, 2], [3, 4])` the cut is `i = 2, j = 0`: all of `b` is on the right, so its left edge is the `-math.inf` stand-in. Print `left, right` to see 2 and 3.
- Predict `find_median([1, 1, 1], [1, 1])`: 1.0. Equal values are fine because the test uses `<=`.

### Say it in the interview

> "The brute force tries every speed from 1 upward and checks each one: O(max · n). But the check is monotone: if speed k finishes in time, every faster speed does too. So the answers look like F F F T T T, and I'll binary search for the first T between 1 and max(piles). That's O(n log max) time and O(1) space."

Then point at three things while you code: the definition of `ok` and why it is monotone; the invariant ("the first True is in `[lo, hi]`, and `hi` is known to work"); and why `hi = mid` keeps mid while the loop still ends (`mid < hi`). Likely follow-ups and your answers:

- *Why is max(piles) enough?* At that speed every pile takes one hour, and `h` is at least the number of piles.
- *A tighter lower bound?* `ceil(sum(piles) / h)`: any slower speed can't eat everything in h hours, even before rounding each pile up.
- *How many checks for values up to 10⁹?* About 30, since 2³⁰ ≈ 10⁹.
- *What if `h < len(piles)`?* No speed works, because every pile needs at least an hour; say so and return -1 (the problem rules it out).

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Binary Search | `binary_search/binary_search.py` | closed window `[lo, hi]` with `while lo <= hi`; both moves skip mid |
| Capacity To Ship Packages Within D Days | `practice/simple/basics/searches/02_binary_search_on_answer.py` | first capacity in [max(w), sum(w)] whose greedy day count fits within days |
| Find First and Last Position of Element in Sorted Array | `binary_search/find_first_and_last_position.py` | first = the first index ≥ target; last = the first index > target, minus 1 (for integers, lb(target + 1) − 1) |
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
