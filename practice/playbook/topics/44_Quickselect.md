## Quickselect

To find the k-th largest value, find sorted index len(nums) − k. Partition once, then keep only the side containing that index. Random pivots give O(n) expected time; the worst case is O(n²). The input contract is 1 ≤ k ≤ len(nums).

<!-- cell -->

Partition, in Lomuto's version, splits one range around a pivot. Its state is the pivot, the end `i` of the "small" region and the scanner `j`. Its definition and its invariant are three regions, `a[lo..i]` ≤ pivot, `a[i+1..j-1]` > pivot and `a[j..hi-1]` not seen yet, with the pivot parked at `a[hi]`. A step looks at `a[j]`, and when it is ≤ pivot, `i += 1` and the swap of `a[i]` and `a[j]` grow the small region by one.

The record comes after the sweep: `a[i + 1], a[hi] = a[hi], a[i + 1]` drops the pivot right after the small region, which is its final slot. Init starts `i = lo - 1`, an empty small region, and takes the pivot from `a[hi]` after `random_partition` has swapped a random item there. The return is the pivot's index, `i + 1`.

Quickselect wraps that partition in a loop over the range `[lo, hi]` still in play, which starts as `0, n - 1`. Its definition rests on `target = len(nums) - k`, the index of the k-th largest in ascending order, and its invariant is that target's slot lies in `[lo, hi]`, with everything left of `lo` ≤ the answer and everything right of `hi` ≥ it.

A step partitions the range, which fixes one pivot in its final slot `p`. When `p == target`, that pivot is the answer; otherwise the **Fix** keeps only the side that holds target, `lo = p + 1` if `p < target`, else `hi = p - 1`.

Kth Largest Element in an Array asks for the k-th largest value of an unsorted array: `[3, 2, 1, 5, 6, 4]` with k = 2 → 5. Sorting answers it in O(n log n), but `kth_largest` only partitions and narrows, O(n) on average. The cell builds it from `partition` and `random_partition`, and `quick_sort` is the same partition recursing into both sides: `[3, 1, 2, 1]` → `[1, 1, 2, 3]`.

<!-- cell -->

```python
def partition(a, lo, hi):
    """Lomuto: pivot = a[hi]. Afterwards the pivot sits at its final sorted index, which is returned."""
    pivot, i = a[hi], lo - 1                 # STATE + INIT: a[lo..i] <= pivot (empty so far)
    # INVARIANT: a[i+1..j-1] > pivot, a[j..hi-1] not seen yet
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]          # STEP: a[j] joins the small region
    a[i + 1], a[hi] = a[hi], a[i + 1]        # RECORD: the pivot lands right after the small region
    return i + 1                             # RETURN its final index

def random_partition(a, lo, hi):
    r = random.randint(lo, hi)               # random pivot: sorted input can't hurt us
    a[r], a[hi] = a[hi], a[r]
    return partition(a, lo, hi)

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
```

<!-- cell -->

```python
print(kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5
```

<!-- cell -->

### Follow only the partition containing the target

<!-- cell -->

```python
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
```

<!-- cell -->

```python
print(trace_quickselect([3, 2, 1, 5, 6, 4], 2))
```

<!-- cell -->

```python
assert kth_largest([7], 1) == 7                      # one item

assert kth_largest([2, 2, 2], 2) == 2                # all equal

assert kth_largest([1, 2, 3, 4], 1) == 4             # k = 1 is the max

assert kth_largest([1, 2, 3, 4], 4) == 1             # k = n is the min

try:
    kth_largest([1, 2, 3], 0)                        # k = 0 asks for index 3: past the end
except ValueError as e:
    print("k outside 1..n:", e)                      # k outside 1..n: empty range in randrange(3, 3)
```
