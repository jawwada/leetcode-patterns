## Sorting & Selection

> Sorting buys you **order**, and order makes the next step cheap: equal items sit together, neighbours become comparable, two pointers can squeeze from both ends, binary search can jump. **Selection** is sorting's lazy cousin: to find the k-th item, partition once and throw away the half that cannot contain it.

**Reach for it when** the problem gets easy "if only the input were sorted" (pairs or triples with a target sum, merging intervals, scheduling, greedy by size or deadline), asks for the **k-th smallest/largest** or the **top k**, asks to count pairs that are **out of order** ("how many smaller numbers to my right"), or the values are small integers you could **count** instead of compare.

**In this repo:** sorting has no topic folder. Its building blocks are `practice/simple/basics/sorting/01_insertion_sort.py`, `02_merge_sort.py`, `03_quick_sort.py`, `04_heap_sort.py`, `05_counting_and_bucket_sort.py` and `06_python_sort_keys_and_stability.py`, and the problems it cracks live in the sections of their main technique (listed at the end of this section). In an interview you call `sorted()`; you implement a sort only when asked, or when you need to change its inner loop (quickselect, counting inversions).

### The picture

```text
MERGE SORT: split until trivial, then merge sorted halves on the way up

             [5 2 4 6 1 3]
            /             \
        [5 2 4]         [6 1 3]          log n levels of splitting
        /    \          /    \
     [5]   [2 4]     [6]   [1 3]
        \    /          \    /
        [2 4 5]         [1 3 6]          every level merges n items in total
            \             /
             [1 2 3 4 5 6]

PARTITION (quicksort, quickselect): one sweep puts the pivot in its FINAL slot

   [5 2 4 6 1 3]        pivot = 3 (the last item)
   [2 1] 3 [6 5 4]      everything left of 3 is <= 3, everything right is > 3
         ^ index 2 is final: quicksort recurses on BOTH sides;
           quickselect only on the side that holds the index it wants
```

Why it is fast:

- A comparison sort must tell apart all n! possible orders, and each comparison at best halves what is still possible, so in the worst case it needs about log2(n!) ≈ n log n comparisons. Merge sort reaches that bound: log n levels, n work per level.
- Quicksort with a random pivot splits near the middle on average, so it also has about log n levels. With an unlucky pivot (the smallest or largest every time) it has n levels: O(n²).
- **Quickselect** keeps only one side: n + n/2 + n/4 + ... < 2n, so O(n) on average. Sorting everything to read one position wastes the work of ordering the two halves it then ignores.
- **Counting sort** never compares two items: it uses each value as an array index, so it runs in O(n + k) for values in a range of size k and beats n log n when k is small.

**Top k, four ways.** The interview question is rarely "implement a sort"; it is "find the k-th" or "the top k", and you are expected to know the trade-offs:

| Approach | Time | Extra space | Mutates? | Stream? | Say it when |
|---|---|---|---|---|---|
| `sorted(a)[-k]` | O(n log n) | O(n) | no | no | first answer, always |
| size-k min-heap ([Heaps](#s13)) | O(n log k) | O(k) | no | yes | k ≪ n, or the data arrives over time |
| quickselect (below) | O(n) average, O(n²) worst | O(1) in place | yes | no | "can you beat n log n?" |
| bucket by count ([Arrays & Hashing](#s03)) | O(n) | O(n) | no | no | the keys are small integers (frequencies ≤ n) |

### From idea to code

**The idea in one sentence:** *merge: two sorted piles become one by repeatedly taking the smaller top item; partition: one sweep splits the items into "small" and "big" around a pivot, and the pivot lands in its final slot; quickselect: partition, then keep only the side that holds the index you want.*

Before typing, answer the seven questions for the piece you are about to write:

| Decision | Merge (merge sort, inversions) | Partition (Lomuto) | Quickselect (k-th largest) |
|---|---|---|---|
| **State** | two sorted piles, a read head in each (`i`, `j`), the output `out` | the pivot, the end of the "small" region `i`, the scanner `j` | the range `[lo, hi]` still in play |
| **Definition** | `left[i]`, `right[j]` = the next untaken item of each pile | `a[lo..i]` ≤ pivot; `a[i+1..j-1]` > pivot; `a[j..hi-1]` not seen yet | `target = n - k`: the k-th largest sits at index `target` of the sorted order |
| **Invariant** | `out` is sorted and ≤ every untaken item | the three regions above hold, with the pivot parked at `a[hi]` | target's slot lies in `[lo, hi]`: everything left of `lo` is ≤ the answer, everything right of `hi` is ≥ it |
| **Step** | the smaller front item joins `out` (the left one on ties); advance that head | if `a[j]` ≤ pivot: `i += 1`, swap `a[i]` and `a[j]` | partition `[lo, hi]`: one sweep fixes `a[p]` in its final slot |
| **Record** | nothing per item for a plain merge (`out` is the answer); for inversions, `cross += len(left) - i` when the right pile wins | after the sweep, swap the pivot into `i + 1`, its final slot | the answer is known when `p == target`; otherwise keep only the side that holds `target` (the fix) |
| **Init** | `i = j = 0`, `out = []` | `pivot = a[hi]` (a random item swapped there), `i = lo - 1` | `lo, hi = 0, n - 1` |
| **Return** | `out + left[i:] + right[j:]`: one pile is empty, the other's rest is the largest and already sorted | the pivot's index `i + 1` | `a[p]` when `p == target` |

The same ideas, sentence by sentence:

| In words | In code |
|---|---|
| "split in half" | `mid = len(a) // 2` |
| "sort each half, then merge them" | `merge(merge_sort(a[:mid]), merge_sort(a[mid:]))` |
| "take the smaller front item, the left pile on ties" | `if left[i] <= right[j]:` |
| "add whatever is left over" | `out + left[i:] + right[j:]` |
| "pick a random pivot" | `r = random.randint(lo, hi)` then `a[r], a[hi] = a[hi], a[r]` |
| "grow the small region by one" | `i += 1` then `a[i], a[j] = a[j], a[i]` |
| "the pivot lands in its final slot" | `a[i + 1], a[hi] = a[hi], a[i + 1]` |
| "k-th largest = position n − k in ascending order" | `target = len(nums) - k` |
| "keep only the side that holds the target" | `lo = p + 1` if `p < target`, else `hi = p - 1` |

The merge template:

```python
def merge(left, right):
    out, i, j = [], 0, 0                     # STATE + INIT: left[i], right[j] = the next untaken item of each pile
    while i < len(left) and j < len(right):  # INVARIANT: out is sorted and <= every untaken item
        if left[i] <= right[j]:              # <= : the left pile wins ties -> stable
            out.append(left[i])              # STEP: the smaller front item joins out
            i += 1
        else:
            out.append(right[j])             # STEP (counting inversions: RECORD len(left) - i here)
            j += 1
    return out + left[i:] + right[j:]        # RETURN: one pile is empty; the other's rest is sorted and largest


def merge_sort(a):
    if len(a) <= 1:                          # 0 or 1 items: already sorted
        return list(a)
    mid = len(a) // 2
    return merge(merge_sort(a[:mid]), merge_sort(a[mid:]))


print(merge([2, 4, 5], [1, 3, 6]), merge_sort([5, 2, 4, 6, 1, 3]))   # [1, 2, 3, 4, 5, 6] [1, 2, 3, 4, 5, 6]
```

**Try it**
- Delete `+ left[i:] + right[j:]`: `merge([2, 4, 5], [1, 3, 6])` loses the 6. The loop stops as soon as one pile is empty.
- See stability: compare only the first field (`left[i][0] <= right[j][0]`) and run `merge_sort([(2, "a"), (1, "b"), (2, "c"), (1, "d")])`: `[(1, 'b'), (1, 'd'), (2, 'a'), (2, 'c')]`, ties in input order. Now make it `<`: `[(1, 'd'), (1, 'b'), (2, 'c'), (2, 'a')]`, every tie flipped.
- Add `print(a)` as the first line of `merge_sort` and watch the splits of `[5, 2, 4, 6, 1, 3]` (11 lines, left half first): the call tree from the picture.

The partition template, and the two algorithms built on it:

```python
def partition(a, lo, hi):
    """Lomuto: pivot = a[hi]. Afterwards the pivot sits at its final sorted index, which is returned."""
    pivot, i = a[hi], lo - 1                 # STATE + INIT: a[lo..i] <= pivot (empty so far)
    for j in range(lo, hi):                  # INVARIANT: a[i+1..j-1] > pivot, a[j..hi-1] not seen yet
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]          # STEP: a[j] joins the small region
    a[i + 1], a[hi] = a[hi], a[i + 1]        # RECORD: the pivot lands right after the small region
    return i + 1                             # RETURN its final index


def random_partition(a, lo, hi):
    r = random.randint(lo, hi)               # random pivot: sorted input can't hurt us
    a[r], a[hi] = a[hi], a[r]
    return partition(a, lo, hi)


def quick_sort(nums):
    a = list(nums)

    def sort_range(lo, hi):
        if lo < hi:
            p = random_partition(a, lo, hi)
            sort_range(lo, p - 1)            # p is final: it never moves again
            sort_range(p + 1, hi)

    sort_range(0, len(a) - 1)
    return a


def kth_largest(nums, k):
    a, target = list(nums), len(nums) - k    # target = index of the k-th largest in ascending order
    lo, hi = 0, len(a) - 1                   # STATE + INIT: target's final slot lies in [lo, hi]
    while True:
        p = random_partition(a, lo, hi)      # STEP: one sweep fixes a[p] in its final slot
        if p == target:
            return a[p]                      # RETURN: the pivot landed exactly on the target
        if p < target:
            lo = p + 1                       # FIX: keep only the side that holds target
        else:
            hi = p - 1                       # FIX: keep only the side that holds target


random.seed(0)
print(quick_sort([3, 1, 2, 1]), kth_largest([3, 2, 1, 5, 6, 4], 2), kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))   # [1, 1, 2, 3] 5 4
```

**Try it**
- Use `target = k - 1` instead: `kth_largest([3, 2, 1, 5, 6, 4], 2)` returns 2, the 2nd *smallest*. Say the direction out loud before you type the index.
- In `quick_sort`, use `partition` instead of `random_partition` and sort `list(range(3000))`: `RecursionError`. On sorted input the last item is always the max, so one side is empty and the recursion is n levels deep.
- Change `sort_range(lo, p - 1)` to `sort_range(lo, p)` and rerun the cell: `RecursionError` on `[3, 1, 2, 1]`. Once a range holds just the two 1s, the pivot lands at `hi` every time, so `[lo, p]` never shrinks.
- Print `lo, hi, p` at the end of each round in `kth_largest`: the range only ever shrinks towards `target`, and nothing outside it is touched again.

### Watch it work

The partition sweep, one line per item seen, then quickselect narrowing its range (a fixed last-item pivot here, so the run is repeatable):

```python
def trace_partition(nums):
    a, hi = list(nums), len(nums) - 1
    pivot, i = a[hi], -1
    print(f"pivot = {pivot}")
    for j in range(hi):
        seen = a[j]
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
        print(f"  j={j} sees {seen}:  small {a[:i + 1]}  big {a[i + 1:j + 1]}  unseen {a[j + 1:hi]}")
    a[i + 1], a[hi] = a[hi], a[i + 1]
    print(f"  pivot goes to index {i + 1}: {a}")


def trace_quickselect(nums, k):
    a, target = list(nums), len(nums) - k
    lo, hi = 0, len(a) - 1
    print(f"k={k}: looking for index {target} of the sorted order")
    while True:
        p = partition(a, lo, hi)
        print(f"  range [{lo}..{hi}]: pivot {a[p]} lands at {p}  {a}")
        if p == target:
            return a[p]
        lo, hi = (p + 1, hi) if p < target else (lo, p - 1)


trace_partition([5, 2, 4, 6, 1, 3])
print(trace_quickselect([3, 2, 1, 5, 6, 4], 2))
```

**Try it**
- Run `trace_partition([1, 2, 3, 4, 5])`: every item is "small" and the pivot stays at the end. One side is empty: that is the shape of the O(n²) worst case.
- Run `trace_partition([3, 3, 3, 3])`: all equal items pile into "small", same problem. The three-way partition below fixes it.
- Run `trace_quickselect([1, 2, 3, 4, 5, 6], 6)` (the smallest of sorted input): six rounds, and the range shrinks by only one item per round, because the last item is always the largest one left. A random pivot avoids that bad luck.

### Where it goes wrong

1. **A fixed pivot on sorted input.** The last item is always the max, the recursion goes n deep: O(n²) time and `RecursionError` around n = 1000. Swap a random item into `hi` first.
2. **Many equal items with Lomuto.** Every item ≤ pivot goes left, so all-equal input is O(n²) even with random pivots. Use a three-way partition (or Hoare's).
3. **The k-th largest index.** In ascending order it is `n - k`, not `k - 1` (that is the k-th smallest).
4. **Recursing on `[lo, p]` after Lomuto.** The pivot is already final: recurse on `p - 1` and `p + 1`. Hoare is the opposite: it returns a split point, so recurse on `[lo, p]` and `[p + 1, hi]`.
5. **`<` instead of `<=` in merge.** Still sorted, but no longer stable, and inversion counts start counting equal pairs.
6. **Forgetting the leftovers** after the merge loop: `out + left[i:] + right[j:]`.
7. **Counting sort with negatives.** Index with `x - min(nums)`; a negative index silently writes into the end of the list.
8. **Mutating the caller's list.** Quickselect rearranges its input; copy first if the original order matters.
9. **A comparator that returns a bool.** `cmp_to_key` needs a negative number for "x first"; `return x + y > y + x` only ever returns True or False (1 or 0), so nothing moves: Largest Number on `[10, 2]` gives `"102"` instead of `"210"`. Return -1, 1 or 0.

### Edge cases to say out loud

Empty list · one item · all equal · already sorted · reverse sorted · negative numbers · duplicates equal to the pivot · `k = 1` (the max) and `k = n` (the min) · `k` outside `1..n` (state the contract).

```python
random.seed(1)
cases = [[], [7], [2, 2, 2], [1, 2, 3, 4], [4, 3, 2, 1], [0, -5, 3, -5],
         [random.randint(-50, 50) for _ in range(200)]]
for sort_fn in (merge_sort, quick_sort):
    for case in cases:
        assert sort_fn(case) == sorted(case), (sort_fn.__name__, case)
assert kth_largest([7], 1) == 7                      # one item
assert kth_largest([2, 2, 2], 2) == 2                # all equal
assert kth_largest([1, 2, 3, 4], 1) == 4             # k = 1 is the max
assert kth_largest([1, 2, 3, 4], 4) == 1             # k = n is the min
assert merge([], [1]) == [1] and merge([], []) == []
try:
    kth_largest([1, 2, 3], 0)                        # k = 0 asks for index 3: past the end
except ValueError as e:
    print("k outside 1..n:", e)                      # k outside 1..n: empty range in randrange(3, 3)
print("edge cases pass")
```

**Try it**
- Read the `ValueError`: with `k = 0` the target index is 3, every pivot lands left of it, `lo` climbs past `hi`, and `random.randint(3, 2)` fails. Say "I assume 1 ≤ k ≤ n" out loud, or check it and raise a clear error.
- Check that the input survives: `data = [3, 1, 2]`, then `kth_largest(data, 1)`, then `data` is still `[3, 1, 2]` because the function copies it.
- Try `quick_sort([5] * 3000)`: `RecursionError`, even with random pivots (all-equal input is trap 2). Then try `quick_sort_hoare([5] * 3000)` from the Variations below.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Quickselect** (k-th, top k) | partition, then continue on ONE side only | Kth Largest Element (215), K Closest Points (973) |
| **Three-way partition** | three regions `< pivot`, `== pivot`, `> pivot`; equal items finish in one pass | Sort Colors (75), quicksort on many duplicates |
| **Hoare partition** (Hard stretch) | two pointers walk inward and swap a misplaced pair; returns a split point, not the pivot's slot | quicksort with fewer swaps, safe on duplicates |
| **Count while merging** (Hard stretch) | total inversions: `+= len(left) - i` when the right pile wins. Per element: merge `(value, index)` pairs; when a LEFT item is placed, add `j`, the right items already placed (smaller and later) | Count of Smaller Numbers After Self (315) |
| **Count, then merge** (Hard stretch) | the condition is not the merge order (`a > 2b`), so first sweep a second pointer over the two sorted halves to count, then merge | Reverse Pairs (493) |
| **Sort as preprocessing** | sort once in O(n log n), then a linear sweep: two pointers, greedy, merge neighbours | 3Sum (15), Merge Intervals (56), Meeting Rooms II (253), Non-overlapping Intervals (435) |
| **Custom order** | `key=` when each item has its own rank; `cmp_to_key` when the order depends on the pair | Sort by Frequency (1636), Largest Number (179) |
| **Bucket by value** | a small integer key indexes an array instead of being compared ([Arrays & Hashing](#s03)) | Top K Frequent Elements (347), Maximum Gap (164) |
| **Selection with a heap** | a size-k min-heap: O(n log k), works on a stream ([Heaps](#s13)) | Kth Largest in a Stream (703) |

**Three-way partition** (Dutch national flag): keep `< pivot` at the front, `> pivot` at the back, and let equal items collect in the middle. Sort Colors is exactly this with pivot 1:

```python
def three_way_partition(a, pivot):
    """In place: [ < pivot | == pivot | > pivot ]. Returns (lt, gt), the inclusive bounds of the
    middle block; lt > gt when no item equals the pivot."""
    lt, i, gt = 0, 0, len(a) - 1             # STATE: a[:lt] < p, a[lt:i] == p, a[i:gt+1] unseen, a[gt+1:] > p
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]        # STEP: a small item joins the front block
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]        # STEP: a big item joins the back block
            gt -= 1                          # do NOT move i: the item swapped in is still unseen
        else:
            i += 1
    return lt, gt                            # RETURN


colors = [2, 0, 2, 1, 1, 0]
print(three_way_partition(colors, 1), colors, three_way_partition([1, 3], 2))   # (2, 3) [0, 0, 1, 1, 2, 2] (1, 0)
```

**Try it**
- Add `i += 1` to the `> pivot` branch and run it on `[1, 2, 0]`: the result is `[1, 0, 2]`. The 0 swapped in from the back was never examined.
- Change `while i <= gt` to `while i < gt` and run it on `[1, 0]`: nothing moves. The last unseen item is never looked at.
- `three_way_partition([5, 5, 5], 5)` returns `(0, 2)`: everything is in the middle block, so a quicksort built on it is done in one pass.

**Hoare partition** (Hard stretch): two pointers walk towards each other, each stopping at an item on the wrong side, and swap them. On equal items both pointers stop at every step and meet in the middle, so the split stays balanced:

```python
def hoare_partition(a, lo, hi):
    pivot = a[(lo + hi) // 2]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < pivot:                  # from the left: find an item that is not small
            i += 1
        j -= 1
        while a[j] > pivot:                  # from the right: find an item that is not big
            j -= 1
        if i >= j:
            return j                         # RETURN: a[lo..j] <= pivot <= a[j+1..hi]
        a[i], a[j] = a[j], a[i]              # STEP: swap the misplaced pair


def quick_sort_hoare(nums):
    a = list(nums)

    def sort_range(lo, hi):
        if lo < hi:
            p = hoare_partition(a, lo, hi)
            sort_range(lo, p)                # p is a split point, NOT the pivot's final slot
            sort_range(p + 1, hi)

    sort_range(0, len(a) - 1)
    return a


print(quick_sort_hoare([5, 2, 4, 6, 1, 3]), quick_sort_hoare([2] * 6))   # [1, 2, 3, 4, 5, 6] [2, 2, 2, 2, 2, 2]
```

**Try it**
- Run `quick_sort_hoare([5] * 3000)`: no `RecursionError` this time; the recursion is only 13 levels deep.
- Recurse on `sort_range(lo, p - 1)` as if `p` were final: `quick_sort_hoare([5, 2, 4, 6, 1, 3])` returns `[2, 3, 1, 4, 5, 6]`. Hoare's `p` is a boundary, and `a[p]` still needs sorting with its side.
- Use `pivot = a[hi]` instead of the middle and rerun the cell: `RecursionError`. The smallest case is `[1, 2]`: the split comes back as `[0..1]` and `[2..1]`, so the left call repeats forever.

**Count while merging** (Hard stretch; inversions = pairs `i < j` with `nums[i] > nums[j]`). When the right pile wins, its item jumps ahead of every item still waiting in the left pile, and each of those is an inversion:

```text
left = [2, 4]     right = [1, 3, 5]
take 1 (right): it jumps over 2 and 4  -> len(left) - i = 2 - 0 = 2 inversions
take 2 (left)
take 3 (right): it jumps over 4 only   -> len(left) - i = 2 - 1 = 1 inversion
```

```python
def count_inversions(nums):
    """Pairs i < j with nums[i] > nums[j], counted during a merge sort."""
    def sort_count(a):
        if len(a) <= 1:
            return list(a), 0
        mid = len(a) // 2
        left, inv_left = sort_count(a[:mid])
        right, inv_right = sort_count(a[mid:])
        out, i, j, cross = [], 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
                cross += len(left) - i       # RECORD: right[j] jumps ahead of every untaken left item
        return out + left[i:] + right[j:], inv_left + inv_right + cross

    return sort_count(nums)[1]


print(count_inversions([2, 4, 1, 3, 5]), count_inversions([5, 4, 3, 2, 1]), count_inversions([1, 1]))   # 3 10 0
```

**Try it**
- Replace `cross += len(left) - i` with `cross += 1`: `[2, 4, 1, 3, 5]` gives 2 instead of 3. The 1 jumps over two items but was counted once.
- Change `<=` to `<` and run `count_inversions([1, 1])`: 1, but equal items are not out of order.
- Turn it into Count of Smaller Numbers After Self (315): sort `(value, index)` pairs, keep `counts = [0] * n`, and when a LEFT pair is placed, add `j` (the right pairs already placed: smaller and later) to `counts[its index]`; left-overs from the left pile get `j` too. `[5, 2, 6, 1]` gives `[2, 1, 1, 0]`.

**Sort as preprocessing.** One O(n log n) sort often turns an O(n²) search into a linear sweep: two pointers squeeze a sorted array (3Sum, in [Two Pointers](#s05)), and intervals sorted by start can only overlap their neighbours (Merge Intervals, in [Intervals](#s14)).

**Custom order**: a `key` works whenever each item has a rank of its own. When the order depends on the *pair*, as in Largest Number, you need `cmp_to_key` ([Python Toolkit](#s02)).

```python
def frequency_sort(nums):                    # LeetCode 1636: rarer values first, ties -> bigger value first
    freq = Counter(nums)
    return sorted(nums, key=lambda x: (freq[x], -x))


print(frequency_sort([1, 1, 2, 2, 2, 3]), frequency_sort([2, 3, 1, 3, 2]))   # [3, 1, 1, 2, 2, 2] [1, 3, 3, 2, 2]
```

**Try it**
- Change the key to `(freq[x], x)`: in the second list, ties now put the smaller value first, `[1, 2, 2, 3, 3]`.
- Use `key=lambda x: -freq[x]` alone: the second list becomes `[2, 3, 3, 2, 1]`, most frequent first with ties in input order (stability).
- Predict `frequency_sort([4, 4, 6, 6, 5])` before running it: `[5, 6, 6, 4, 4]`.

### The rest of the family

You will rarely type these in an interview, but each has a "why" worth knowing:

| Sort | The idea | Time (average / worst) | Extra space | Stable? | Use it when |
|---|---|---|---|---|---|
| Insertion | grow a sorted prefix; slide each new item left into place | O(n²) / O(n²); O(n) if nearly sorted | O(1) | yes | tiny or nearly sorted input |
| Merge | split in halves, merge two sorted lists | O(n log n) / O(n log n) | O(n) | yes | stability, linked lists, counting inversions |
| Quick | partition around a pivot, recurse on both sides | O(n log n) / O(n²) | O(log n) stack on average | no | in place, fast in practice; the base of quickselect |
| Heap | build a max-heap, swap the max to the end, repeat | O(n log n) / O(n log n) | O(1) | no | in place with a guaranteed worst case |
| Counting | tally each value, emit values in order | O(n + k) | O(k) | yes, when records are placed by prefix sums | small integer range k |
| Bucket | spread values over buckets by range, sort each, concatenate | O(n) expected / O(n²) | O(n) | if the inner sort is | evenly spread values; "bucket by frequency" ([Arrays & Hashing](#s03)) |
| Python `sorted` | Timsort: a merge sort that first finds the runs already sorted in the data | O(n log n); O(n) if already sorted | O(n) | yes | always, unless asked to implement one |

**Insertion sort** works like sorting playing cards in your hand; **heap sort** is "repeatedly take the max", with the heap living inside the array itself (children of `i` at `2i+1`, `2i+2`):

```python
def insertion_sort(nums):
    a = list(nums)
    for i in range(1, len(a)):
        key, j = a[i], i - 1                 # a[:i] is sorted; slide a[i] left into place
        while j >= 0 and a[j] > key:         # only strictly bigger items move: stable
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def heap_sort(nums):
    a = list(nums)

    def sift_down(i, size):                  # push a[i] down until it is >= both children
        while 2 * i + 1 < size:
            c = 2 * i + 1
            if c + 1 < size and a[c + 1] > a[c]:
                c += 1                       # c = the bigger child
            if a[c] <= a[i]:
                return
            a[i], a[c] = a[c], a[i]
            i = c

    for i in range(len(a) // 2 - 1, -1, -1):   # build a max-heap, last parent first: O(n)
        sift_down(i, len(a))
    for end in range(len(a) - 1, 0, -1):     # swap the max to the end, then shrink the heap
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
    return a


print(insertion_sort([5, 2, 4, 6, 1, 3]), heap_sort([5, 2, 4, 6, 1, 3]))   # [1, 2, 3, 4, 5, 6] [1, 2, 3, 4, 5, 6]
```

**Try it**
- Count the shifts in `insertion_sort` (add a counter inside the `while`): 0 for `list(range(1000))`, 499,500 for `list(range(1000, 0, -1))`. Same code, O(n) versus O(n²).
- In `heap_sort`, print `a` right after the build loop: `[6, 5, 4, 2, 1, 3]`. The max is on top; the rest is only "heap ordered", not sorted.
- Delete the two lines that pick the bigger child (always use the left one): `heap_sort([1, 2, 3])` returns `[1, 3, 2]`. Sifting down must swap with the *bigger* child, or the smaller child ends up above a bigger one.

**Counting sort** uses each value as an address instead of comparing:

```python
def counting_sort(nums):                     # small integer range: count instead of compare
    if not nums:
        return []
    lo = min(nums)
    counts = [0] * (max(nums) - lo + 1)      # one slot per possible value
    for x in nums:
        counts[x - lo] += 1                  # shift by lo so negative values get a slot
    out = []
    for offset, c in enumerate(counts):      # walk the values in increasing order
        out += [lo + offset] * c
    return out


random.seed(2)
for _ in range(200):
    data = [random.randint(-9, 9) for _ in range(random.randint(0, 12))]
    assert insertion_sort(data) == heap_sort(data) == counting_sort(data) == sorted(data), data
print(counting_sort([3, -1, 2, -1, 0, 3]))   # [-1, -1, 0, 2, 3, 3]
```

**Try it**
- Drop the shift (use `counts[x]` and `out += [offset] * c`) and rerun: the random check stops with `IndexError`, because a value larger than the range indexes past the end of `counts`. Worse, `counting_sort([3, -1, 2])` raises nothing and returns `[2, 3, 4]`: the negative index `counts[-1]` quietly counted the -1 in the last slot.
- Run `counting_sort([1_000_000, 0])`: correct, but it allocates a million counters for two numbers. The cost is the value range, not the length.
- `counting_sort([1.5, 2])` raises `TypeError`: counting sort needs integer keys, because a value becomes a list index.

### Say it in the interview

> "Sorting everything is O(n log n) and gives me far more than I need: I only care about one position. One partition around a random pivot puts the pivot in its final slot in O(n) and tells me which side the answer is on, so I continue on that side only: n + n/2 + ... is under 2n, O(n) on average, O(n²) in the worst case if every pivot is unlucky. If they want a guaranteed bound or the data arrives as a stream, a size-k min-heap gives O(n log k)."

While coding, point at the partition's region comments (`a[lo..i] <= pivot`) and say why the pivot's index is final. For "sort first" problems, say the trade explicitly: "O(n log n) to sort buys me an O(n) sweep instead of O(n²) pairs."

### Where sorting shows up in this repo

Sorting has no topic folder, so this section adds no rows to the A-Z problem finder. These problems are mapped (and taught) in the sections of their main technique, but sorting or selection is the step that cracks them:

| Problem | Where | The sorting step |
|---|---|---|
| Kth Largest Element in an Array | `heap/kth_largest_element_in_an_array.py` | quickselect: partition, keep the side holding index n − k |
| K Closest Points to Origin | `heap/k_closest_points_to_origin.py` · `practice/simple/32_k_closest_points_to_origin.py` | a size-k max-heap on distance; quickselect on distance for O(n) average |
| Sort Colors | `two_pointers/sort_colors.py` | three-way partition around 1 |
| Count of Smaller Numbers After Self | `arrays_hashing/count_of_smaller_numbers_after_self.py` | merge `(value, index)` pairs; a placed left item gains `j`, the right items already placed |
| Reverse Pairs | `arrays_hashing/reverse_pairs.py` | count `a > 2b` with a second pointer over the two sorted halves, then merge |
| Maximum Gap | `arrays_hashing/maximum_gap.py` | pigeonhole buckets: the largest gap never sits inside one bucket |
| Top K Frequent Elements | `arrays_hashing/top_k_frequent_elements.py` | bucket sort by frequency (1..n) |
| 3Sum | `two_pointers/three_sum.py` · `practice/simple/06_three_sum.py` | sort, fix one number, two pointers on the rest; duplicates become neighbours |
| Merge Intervals | `intervals/merge_intervals.py` · `practice/simple/48_merge_intervals.py` | sort by start: overlapping intervals become neighbours |
| Meeting Rooms II | `intervals/meeting_rooms_ii.py` · `practice/simple/49_meeting_rooms_ii.py` | sort by start, min-heap of end times |
| Non-overlapping Intervals | `intervals/non_overlapping_intervals.py` | sort by end, greedily keep the earliest finisher |

### Self-check

1. Why is quickselect O(n) on average while quicksort is O(n log n)?
<details><summary>Answer</summary>Both partition in linear time, but quicksort recurses into both sides (n work on each of about log n levels), while quickselect continues into one side only, whose size halves on average: n + n/2 + n/4 + ... is less than 2n.</details>

2. What does Lomuto partition do with `[7, 7, 7, 7]`, and what is the fix?
<details><summary>Answer</summary>Every item is ≤ the pivot, so all of them join the "small" region and the pivot lands at the end: one side is empty, the next call has n − 1 items, and the whole sort is O(n²) (and n levels deep). A three-way partition puts all the 7s in the middle block in one pass; Hoare's partition also splits equal items evenly.</details>

3. You need the top 10 of a million scores that keep arriving. Which of the four top-k approaches, and why not quickselect?
<details><summary>Answer</summary>A size-10 min-heap: O(log 10) per new score and O(10) memory, and its root is always the 10th best so far. Quickselect needs the whole array in memory and rearranges it; it answers one query on a fixed array, not a stream.</details>

4. When counting inversions, why add `len(left) - i` at the moment the right pile wins?
<details><summary>Answer</summary>The left items <code>left[i:]</code> are all still waiting and all bigger than <code>right[j]</code> (the left pile is sorted and <code>left[i]</code> already lost the comparison). Each of them came earlier in the original array, so each forms one inversion with <code>right[j]</code>.</details>
