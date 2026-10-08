## Sorting

> Sorting buys you **order**, and order makes the next step cheap: equal items sit together, neighbours become comparable, two pointers can squeeze from both ends, binary search can jump. **Selection** is sorting's lazy cousin: to find the k-th item, partition once and throw away the half that cannot contain it.

[Binary Search](11_Binary_Search.ipynb#topic-binary-search) searched a landscape that flips once, from False to True, and [Two Pointers](06_Two_Pointers.ipynb#topic-two-pointers) squeezed a sorted array from both ends; sorting is what creates the order both of them need. This section builds that order, and when only one position of it matters, the k-th item, it finds that position without sorting everything.

**Reach for it when** the problem gets easy "if only the input were sorted": pairs or triples with a target sum, merging intervals, scheduling, greedy by size or deadline. Reach for it too when the problem asks for the **k-th smallest or largest** or the **top k**, asks to count pairs that are **out of order**, as in "how many smaller numbers to my right", or has small integer values you could **count** instead of compare.

### The picture

Two motions carry the whole section. Merge sort splits until every piece is trivially sorted and merges sorted halves on the way up; a partition sweeps once and drops its pivot into the slot it will have in the sorted list:

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

A comparison sort must tell apart all n! possible orders, and each comparison at best halves what is still possible, so in the worst case it needs about log₂(n!) ≈ n log n comparisons. Merge sort reaches that bound: log n levels of splitting, and n items merged on each level.

Quicksort with a random pivot splits near the middle on average, so it also has about log n levels. With an unlucky pivot, the smallest or the largest every time, it has n levels and costs O(n²). **Quickselect** keeps only one side: n + n/2 + n/4 + ... < 2n, so it is O(n) on average. Sorting everything to read one position wastes the work of ordering two halves it then ignores.

**Counting sort** never compares two items. It uses each value as an array index, so it runs in O(n + k) for values in a range of size k, and it beats n log n when k is small.

The interview question is rarely "implement a sort"; it is "find the k-th" or "the top k", and you are expected to know four ways to answer it and what each costs:

| Approach | Time | Extra space | Mutates? | Stream? | Say it when |
|---|---|---|---|---|---|
| `sorted(a)[-k]` | O(n log n) | O(n) | no | no | first answer, always |
| size-k min-heap ([Heaps](16_Heaps.ipynb#topic-heaps)) | O(n log k) | O(k) | no | yes | k ≪ n, or the data arrives over time |
| quickselect (below) | O(n) average, O(n²) worst | O(1) in place | yes | no | "can you beat n log n?" |
| bucket by count ([Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets)) | O(n) | O(n) | no | no | the keys are small integers (frequencies ≤ n) |

### From idea to code

**The idea in one sentence:** *merge: two sorted piles become one by repeatedly taking the smaller top item; partition: one sweep splits the items into "small" and "big" around a pivot, and the pivot lands in its final slot; quickselect: partition, then keep only the side that holds the index you want.*

Merge comes first. **State** is two sorted piles with a read head in each, `i` and `j`, plus the output `out`, and **Definition** says that `left[i]` and `right[j]` are the next untaken items of their piles. **Invariant** holds that `out` is sorted and no item in it is bigger than an untaken one. **Step** moves the smaller front item into `out`, the left one on ties, `if left[i] <= right[j]:`, and advances that head.

A plain merge has no **Record** per item, because `out` itself is the answer; counting inversions records `cross += len(left) - i` when the right pile wins. **Init** is `i = j = 0` and `out = []`. **Return** is `out + left[i:] + right[j:]`: when the loop stops, one pile is empty, and the rest of the other is sorted and larger than everything in `out`.

The template sorts a list: `[5, 2, 4, 6, 1, 3]` → `[1, 2, 3, 4, 5, 6]`. `merge` joins two sorted piles, `[2, 4, 5]` and `[1, 3, 6]`, by repeatedly taking the smaller front item. `merge_sort` splits the list at `mid = len(a) // 2`, sorts each half with the same call, and merges the results, `merge(merge_sort(a[:mid]), merge_sort(a[mid:]))`, which is exactly the tree in the picture.

<!-- cell -->

```python
def merge(left, right):
    out, i, j = [], 0, 0                     # STATE + INIT: left[i], right[j] = the next untaken item of each pile
    # INVARIANT: out is sorted and <= every untaken item
    while i < len(left) and j < len(right):
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

<!-- cell -->

**Try it**
- Delete `+ left[i:] + right[j:]`: `merge([2, 4, 5], [1, 3, 6])` loses the 6. The loop stops as soon as one pile is empty.
- See stability: compare only the first field (`left[i][0] <= right[j][0]`) and run `merge_sort([(2, "a"), (1, "b"), (2, "c"), (1, "d")])`: `[(1, 'b'), (1, 'd'), (2, 'a'), (2, 'c')]`, ties in input order. Now make it `<`: `[(1, 'd'), (1, 'b'), (2, 'c'), (2, 'a')]`, every tie flipped.
- Add `print(a)` as the first line of `merge_sort` and watch the splits of `[5, 2, 4, 6, 1, 3]` (11 lines, left half first): the call tree from the picture.

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

def quick_sort(nums):
    a = list(nums)

    def sort_range(lo, hi):
        if lo < hi:
            p = random_partition(a, lo, hi)
            sort_range(lo, p - 1)            # p is final: it never moves again
            sort_range(p + 1, hi)

    sort_range(0, len(a) - 1)
    return a
```

<!-- cell -->

```python
print(quick_sort([3, 1, 2, 1]))  # [1, 1, 2, 3]
```

<!-- cell -->

### Trace partitioning

<!-- cell -->

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
```

<!-- cell -->

```python
trace_partition([5, 2, 4, 6, 1, 3])
```

<!-- cell -->

```python
random.seed(1)

cases = [[], [7], [2, 2, 2], [1, 2, 3, 4], [4, 3, 2, 1], [0, -5, 3, -5],
         [random.randint(-50, 50) for _ in range(200)]]

for sort_fn in (merge_sort, quick_sort):
    for case in cases:
        assert sort_fn(case) == sorted(case), (sort_fn.__name__, case)

assert merge([], [1]) == [1] and merge([], []) == []

print("edge cases pass")
```

<!-- cell -->

**Try it**
- Read the `ValueError`: with `k = 0` the target index is 3, every pivot lands left of it, `lo` climbs past `hi`, and `random.randint(3, 2)` fails. Say "I assume 1 ≤ k ≤ n" out loud, or check it and raise a clear error.
- Check that the input survives: `data = [3, 1, 2]`, then `kth_largest(data, 1)`, then `data` is still `[3, 1, 2]` because the function copies it.
- Try `quick_sort([5] * 3000)`: `RecursionError`, even with random pivots (all-equal input is trap 2). Then try `quick_sort_hoare([5] * 3000)` from the second pass of the Variations below.

<!-- cell -->

### Variations

Each variation below changes one thing: how the partition splits, what the order compares, or what the sorted order is used for. The table is the overview; the paragraphs after it take the main ones in order.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Quickselect** (k-th, top k) | partition, then continue on ONE side only | Kth Largest Element in an Array (215), K Closest Points to Origin (973): the k points nearest to (0, 0) |
| **Three-way partition** | three regions `< pivot`, `== pivot`, `> pivot`; equal items finish in one pass | Sort Colors (75): sort 0s, 1s and 2s in place; quicksort on many duplicates |
| **Sort as preprocessing** | sort once in O(n log n), then a linear sweep: two pointers, greedy, merge neighbours | 3Sum (15): every unique triplet that sums to 0; Merge Intervals (56): merge the overlapping ranges; Meeting Rooms II (253): the fewest rooms that hold every meeting; Non-overlapping Intervals (435): the fewest removals that leave no overlap |
| **Custom order** | `key=` when each item has its own rank; `cmp_to_key` when the order depends on the pair | Sort Array by Increasing Frequency (1636): rarer values first, ties by the bigger value; Largest Number (179) |
| **Bucket by value** | a small integer key indexes an array instead of being compared ([Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets)) | Top K Frequent Elements (347): the k most frequent values; Maximum Gap (164): the largest gap between neighbours in sorted order, in O(n) |
| **Selection with a heap** | a size-k min-heap: O(n log k), works on a stream ([Heaps](16_Heaps.ipynb#topic-heaps)) | Kth Largest Element in a Stream (703): the k-th largest after each new number |
| *Second pass:* **Hoare partition** | two pointers walk inward and swap a misplaced pair; returns a split point, not the pivot's slot | quicksort with fewer swaps, safe on duplicates |
| *Second pass:* **Count while merging** | total inversions: `+= len(left) - i` when the right pile wins. Per element: merge `(value, index)` pairs; when a LEFT item is placed, add `j`, the right items already placed (smaller and later) | Count of Smaller Numbers After Self (315): for each item, how many later items are smaller |
| *Second pass:* **Count, then merge** | the condition is not the merge order (`a > 2b`), so first sweep a second pointer over the two sorted halves to count, then merge | Reverse Pairs (493): the pairs i < j with `nums[i] > 2 · nums[j]` |

The first row is the template itself. K Closest Points to Origin is quickselect on squared distances with target index k − 1: once the pivot lands there, the k points up to it are the answer, in any order. [Heaps](16_Heaps.ipynb#topic-heaps) solves it with a size-k max-heap instead, which also works on a stream.

The next variation repairs Lomuto's weakness with equal items. A **three-way partition** keeps `< pivot` at the front, `> pivot` at the back, and lets the items equal to the pivot collect in the middle, so a run of duplicates is finished in one pass. Sort Colors, which sorts an array of 0s, 1s and 2s in place, is exactly this with pivot 1: `[2, 0, 2, 1, 1, 0]` → `[0, 0, 1, 1, 2, 2]`. It is the Dutch flag loop of [Two Pointers](06_Two_Pointers.ipynb#topic-two-pointers), run around any pivot value.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Call it with a pivot that is in no item, `three_way_partition([3, 1, 2], 5)`: every item is < pivot, it returns `(3, 2)` (lt > gt, an empty middle block) and the list keeps its order, `[3, 1, 2]`.
- Change `while i <= gt` to `while i < gt` and run `three_way_partition([1, 0], 1)`: nothing moves, and the list stays `[1, 0]`. The last unseen item is never looked at.
- Run `three_way_partition([5, 5, 5], 5)`: `(0, 2)`. Everything is in the middle block, so a quicksort built on it is done in one pass.

<!-- cell -->

**Sort as preprocessing** needs no new code. One O(n log n) sort often turns an O(n²) search into a linear sweep: two pointers squeeze a sorted array, as in 3Sum in [Two Pointers](06_Two_Pointers.ipynb#topic-two-pointers), and intervals sorted by start can only overlap their neighbours, as in Merge Intervals in [Intervals & Sweep Line](17_Intervals_and_Sweep_Line.ipynb#topic-intervals-and-sweep-line). Meeting Rooms II sorts by start and keeps a heap of end times; Non-overlapping Intervals sorts by end and greedily keeps the earliest finisher.

A **custom order** comes next. A `key` works whenever each item has a rank of its own, as [Python Toolkit](03_Python_Toolkit.ipynb#topic-python-toolkit) shows, and tuples compare field by field, so a tuple key sorts by several levels and negating a number flips just that level. Sort Array by Increasing Frequency asks to sort values by how often they occur, rarer first, with ties broken by the bigger value first: `[1, 1, 2, 2, 2, 3]` → `[3, 1, 1, 2, 2, 2]`. The rank of x is the tuple `(freq[x], -x)`.

<!-- cell -->

```python
def frequency_sort(nums):                    # LeetCode 1636: rarer values first, ties -> bigger value first
    freq = Counter(nums)
    return sorted(nums, key=lambda x: (freq[x], -x))


print(frequency_sort([1, 1, 2, 2, 2, 3]), frequency_sort([2, 3, 1, 3, 2]))   # [3, 1, 1, 2, 2, 2] [1, 3, 3, 2, 2]
```

<!-- cell -->

**Try it**
- Change the key to `(freq[x], x)`: in the second list, ties now put the smaller value first, `[1, 2, 2, 3, 3]`.
- Use `key=lambda x: -freq[x]` alone: the second list becomes `[2, 3, 3, 2, 1]`, most frequent first with ties in input order (stability).
- Predict `frequency_sort([4, 4, 6, 6, 5])` before running it: `[5, 6, 6, 4, 4]`.

<!-- cell -->

Largest Number asks to arrange non-negative integers so that their concatenation is the largest number, returned as a string: `[3, 30, 34, 5, 9]` → `"9534330"`, `[10, 2]` → `"210"`, `[0, 0]` → `"0"`. No number has a rank of its own here, because the order depends on the pair: x goes before y when `x + y > y + x` as strings, so `"3"` goes before `"30"`, since 330 beats 303.

When the order depends on the pair, you need `cmp_to_key`: the comparator returns a negative number for "x first", a positive one for "y first", and 0 otherwise. Sort the numbers as strings with it and join them. Then guard the all-zeros case, which would otherwise come out as `"00"`.

<!-- cell -->

```python
def largest_number(nums):                    # 179: the order depends on the PAIR, x + y vs y + x
    def cmp(x, y):
        if x + y > y + x:
            return -1                        # negative: x goes first
        if x + y < y + x:
            return 1                         # positive: y goes first
        return 0
    s = "".join(sorted(map(str, nums), key=cmp_to_key(cmp)))
    return "0" if s[0] == "0" else s         # [0, 0] -> "0", not "00"


print(largest_number([3, 30, 34, 5, 9]), largest_number([10, 2]), largest_number([0, 0]))   # 9534330 210 0
```

<!-- cell -->

**Try it**
- Replace the body of `cmp` with `return x + y > y + x` and run `largest_number([10, 2])`: `"102"` instead of `"210"`, and no error. A bool is never negative, so no item ever goes first and the sort keeps the input order (trap 9).
- Delete the zeros guard and run `largest_number([0, 0])`: `"00"`.
- Try plain reverse string order, `"".join(sorted(map(str, [3, 30, 34, 5, 9]), reverse=True))`: `"9534303"` instead of `"9534330"`. As strings `"30"` beats `"3"`, so 30 goes first, yet 303 loses to 330.
- Swap `-1` and `1` in `cmp`: `largest_number([3, 30, 34, 5, 9])` becomes the *smallest* arrangement, `"3033459"`.

<!-- cell -->

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Hoare's partition comes first, because it repairs what Lomuto gets wrong on equal items: `quick_sort([5] * 3000)` needs 3000 levels of recursion, since every 5 joins the small side, and raises `RecursionError`. Two pointers walk towards each other, each stopping at an item on the wrong side, and swap the pair. On equal items both pointers stop at every step and meet in the middle, so the split stays balanced. The function returns a split point, not the pivot's final slot.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Run `quick_sort_hoare([5] * 3000)`: no `RecursionError` this time; the recursion is only 13 levels deep.
- Recurse on `sort_range(lo, p - 1)` as if `p` were final: `quick_sort_hoare([5, 2, 4, 6, 1, 3])` returns `[2, 3, 1, 4, 5, 6]`. Hoare's `p` is a boundary, and `a[p]` still needs sorting with its side.
- Use `pivot = a[hi]` instead of the middle and rerun the cell: `RecursionError`. The smallest case is `[1, 2]`: the split comes back as `[0..1]` and `[2..1]`, so the left call repeats forever.

<!-- cell -->

Counting inversions is the second. An inversion is a pair i < j with `nums[i] > nums[j]`: `[2, 4, 1, 3, 5]` has 3, the pairs (2, 1), (4, 1) and (4, 3). Merge sort finds them all while it merges. When the right pile wins, its item jumps ahead of every item still waiting in the left pile, and each of those is an inversion:

```text
left = [2, 4]     right = [1, 3, 5]
take 1 (right): it jumps over 2 and 4  -> len(left) - i = 2 - 0 = 2 inversions
take 2 (left)
take 3 (right): it jumps over 4 only   -> len(left) - i = 2 - 1 = 1 inversion
```

<!-- cell -->

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

<!-- cell -->

**Try it**
- Replace `cross += len(left) - i` with `cross += 1`: `[2, 4, 1, 3, 5]` gives 2 instead of 3. The 1 jumps over two items but was counted once.
- Change `<=` to `<` and run `count_inversions([1, 1])`: 1, but equal items are not out of order.
- Turn it into Count of Smaller Numbers After Self (315): sort `(value, index)` pairs, keep `counts = [0] * n`, and when a LEFT pair is placed, add `j`, the right pairs already placed, which are smaller and later, to `counts[its index]`; left-overs from the left pile get `j` too. `[5, 2, 6, 1]` gives `[2, 1, 1, 0]`; the Fenwick version is in [Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets).

<!-- cell -->

Reverse Pairs asks for the number of pairs i < j with `nums[i] > 2 · nums[j]`: `[1, 3, 2, 3, 1]` → 2. That condition is not the order the merge uses, so count before merging. With both halves sorted, a pointer into the right half only ever moves forward as the left item grows, and each left item adds the right items the pointer has passed. Then merge as usual.

<!-- cell -->

### The rest of the family

This part is a reference, not a second pass. You will rarely type these sorts in an interview, but each has a "why" an interviewer may ask about, and the table answers it at a glance:

| Sort | The idea | Time (average / worst) | Extra space | Stable? | Use it when |
|---|---|---|---|---|---|
| Insertion | grow a sorted prefix; slide each new item left into place | O(n²) / O(n²); O(n) if nearly sorted | O(1) | yes | tiny or nearly sorted input |
| Merge | split in halves, merge two sorted lists | O(n log n) / O(n log n) | O(n) | yes | stability, linked lists, counting inversions |
| Quick | partition around a pivot, recurse on both sides | O(n log n) / O(n²) | O(log n) stack on average | no | in place, fast in practice; the base of quickselect |
| Heap | build a max-heap, swap the max to the end, repeat | O(n log n) / O(n log n) | O(1) | no | in place with a guaranteed worst case |
| Counting | tally each value, emit values in order | O(n + k) | O(k) | yes, when records are placed by prefix sums | small integer range k |
| Bucket | spread values over buckets by range, sort each, concatenate | O(n) expected / O(n²) | O(n) | if the inner sort is | evenly spread values; "bucket by frequency" ([Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets)) |
| Python `sorted` | Timsort: a merge sort that first finds the runs already sorted in the data | O(n log n); O(n) if already sorted | O(n) | yes | always, unless asked to implement one |

Insertion sort works like sorting playing cards in your hand: it grows a sorted prefix and slides each new item left into place, so `[5, 2, 4]` becomes `[2, 5, 4]` and then `[2, 4, 5]`. Heap sort repeatedly takes the max. It builds a max-heap inside the array itself, with the children of `i` at `2i + 1` and `2i + 2`, swaps the max to the end, and shrinks the heap by one.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Count the shifts in `insertion_sort` (add a counter inside the `while`): 0 for `list(range(1000))`, 499,500 for `list(range(1000, 0, -1))`. Same code, O(n) versus O(n²).
- In `heap_sort`, print `a` right after the build loop: `[6, 5, 4, 2, 1, 3]`. The max is on top; the rest is only "heap ordered", not sorted.
- Delete the two lines that pick the bigger child (always use the left one): `heap_sort([1, 2, 3])` returns `[1, 3, 2]`. Sifting down must swap with the *bigger* child, or the smaller child ends up above a bigger one.

<!-- cell -->

Counting sort uses each value as an address instead of comparing. `[3, -1, 2, -1, 0, 3]` holds values from −1 to 3, so five counters, one per possible value, are enough, and walking them in order emits `[-1, -1, 0, 2, 3, 3]`. Shifting each value by the minimum gives the negative values a slot, and the cell checks all three sorts against `sorted` on 200 random lists.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Drop the shift (use `counts[x]` and `out += [offset] * c`) and rerun: the random check stops with `IndexError`, because a value larger than the range indexes past the end of `counts`. Worse, `counting_sort([3, -1, 2])` raises nothing and returns `[2, 3, 4]`: the negative index `counts[-1]` quietly counted the -1 in the last slot.
- Run `counting_sort([1_000_000, 0])`: correct, but it allocates a million counters for two numbers. The cost is the value range, not the length.
- Run `counting_sort([1.5, 2])`: `TypeError`. Counting sort needs integer keys, because a value becomes a list index.

<!-- cell -->

### Say it in the interview

> "Sorting everything is O(n log n) and gives me far more than I need: I only care about one position. One partition around a random pivot puts the pivot in its final slot in O(n) and tells me which side the answer is on, so I continue on that side only: n + n/2 + ... is under 2n, O(n) on average, O(n²) in the worst case if every pivot is unlucky. If they want a guaranteed bound or the data arrives as a stream, a size-k min-heap gives O(n log k)."

While coding, point at the partition's region comments (`a[lo..i] <= pivot`) and say why the pivot's index is final. For "sort first" problems, say the trade explicitly: "O(n log n) to sort buys me an O(n) sweep instead of O(n²) pairs."

### Self-check

1. Why is quickselect O(n) on average while quicksort is O(n log n)?
<details><summary>Answer</summary>Both partition in linear time, but quicksort recurses into both sides (n work on each of about log n levels), while quickselect continues into one side only, whose size halves on average: n + n/2 + n/4 + ... is less than 2n.</details>

2. What does Lomuto partition do with `[7, 7, 7, 7]`, and what is the fix?
<details><summary>Answer</summary>Every item is ≤ the pivot, so all of them join the "small" region and the pivot lands at the end: one side is empty, the next call has n − 1 items, and the whole sort is O(n²) and n levels deep. A three-way partition puts all the 7s in the middle block in one pass; Hoare's partition also splits equal items evenly.</details>

3. You need the top 10 of a million scores that keep arriving. Which of the four top-k approaches, and why not quickselect?
<details><summary>Answer</summary>A size-10 min-heap: O(log 10) per new score and O(10) memory, and its root is always the 10th best so far. Quickselect needs the whole array in memory and rearranges it; it answers one query on a fixed array, not a stream.</details>

4. When counting inversions, why add `len(left) - i` at the moment the right pile wins?
<details><summary>Answer</summary>The left items <code>left[i:]</code> are all still waiting and all bigger than <code>right[j]</code> (the left pile is sorted and <code>left[i]</code> already lost the comparison). Each of them came earlier in the original array, so each forms one inversion with <code>right[j]</code>.</details>
