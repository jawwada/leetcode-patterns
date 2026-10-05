# Sorting

Sorting is the one algorithm family every interviewer assumes you can write on a whiteboard, and it is where the three ideas that power everything else first show up: an invariant on a region of the array (insertion, selection, heap sort), divide and conquer (merge sort, quick sort), and trading comparisons for indexing when you know the value range (counting and bucket sort). In Python you call `sorted` or `list.sort` (Timsort); the skill being drilled here is choosing a key, knowing what stability buys you, and being able to write the classic algorithms cleanly when asked.

## The algorithms side by side

| Algorithm | Best | Average | Worst | Extra space | Stable | When it wins |
|---|---|---|---|---|---|---|
| insertion sort | O(n) | O(n^2) | O(n^2) | O(1) | yes | tiny or nearly sorted input; the inner loop of Timsort and bucket sort |
| merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | yes | guaranteed bound, linked lists, external sorting, when stability matters |
| quick sort (Lomuto, last-element pivot) | O(n log n) | O(n log n) | O(n^2) on sorted input | O(log n) stack | no | in-place and cache friendly; randomize the pivot to dodge the worst case |
| heap sort | O(n log n) | O(n log n) | O(n log n) | O(1) | no | guaranteed bound with no extra memory |
| counting sort | O(n + k) | O(n + k) | O(n + k) | O(n + k) | yes (prefix-sum version) | small non-negative ints, k = max value; also a radix-sort digit pass |
| bucket sort | O(n) | O(n) | O(n^2) all in one bucket | O(n) | yes, if buckets are sorted stably | floats spread evenly over a known range |
| Timsort (`sorted`) | O(n) | O(n log n) | O(n log n) | O(n) | yes | the default; merge sort that exploits existing runs |

Comparison sorts cannot beat O(n log n) in the worst case; counting and bucket sort escape the bound by never comparing two elements, at the price of needing to know the value range.

## Drawn example: insertion sort of [5, 2, 4, 6, 1, 3]

The sorted prefix is left of the bar. Each round takes the first unsorted element and shifts bigger prefix elements right until its slot opens.

```
start   [5 | 2 4 6 1 3]
i=1     take 2: 5 > 2 shift      [2 5 | 4 6 1 3]
i=2     take 4: 5 > 4 shift      [2 4 5 | 6 1 3]
i=3     take 6: nothing to shift [2 4 5 6 | 1 3]
i=4     take 1: 6 5 4 2 shift    [1 2 4 5 6 | 3]
i=5     take 3: 6 5 4 shift      [1 2 3 4 5 6 |]
```

## Drawn example: merge sort of the same array

```
            [5 2 4 6 1 3]
           /             \
      [5 2 4]           [6 1 3]
      /     \           /     \
    [5]   [2 4]       [6]   [1 3]
          /   \             /   \
        [2]   [4]         [1]   [3]

merge [2]+[4] -> [2 4]          merge [1]+[3] -> [1 3]
merge [5]+[2 4] -> [2 4 5]      merge [6]+[1 3] -> [1 3 6]
merge [2 4 5]+[1 3 6] -> [1 2 3 4 5 6]
```

Every level of the tree touches n elements once and there are log n levels.

## Stability, and why it matters

A stable sort keeps equal keys in their input order. That is what makes a two-pass sort work: sort by the minor key first, then by the major key, and the minor order survives within each major group. In Python the one-pass equivalent is a tuple key, with a minus sign to flip a numeric field: `key=lambda r: (r.dept, -r.salary)`. Quick sort and heap sort are not stable because they swap elements across long distances; insertion and merge sort are stable as long as you shift or take the right element only on a STRICT comparison.

## The invariants to say out loud

- Insertion: "a[:i] is sorted; I slide a[i] left until the element before it is <= it."
- Merge: "both runs are sorted; the smaller head is the next output, left wins ties."
- Quick sort (Lomuto): "a[lo..i] <= pivot, a[i+1..j-1] > pivot, pivot sits at hi; at the end it swaps to i+1, its final place."
- Heap sort: "a[:end] is a max-heap and a[end:] is sorted and bigger than everything in the heap."
- Counting: "counts[v] is how many times v occurs; walking counts in index order is the sorted output."
- Bucket: "the bucket index int(x * n) is monotone in x, so sorted buckets concatenate into a sorted whole."

## Exercises

| File | Drills |
|---|---|
| `01_insertion_sort.py` | the sorted-prefix invariant: shift bigger elements right, drop the key into the gap |
| `02_merge_sort.py` | split in half, recurse, two-pointer merge taking the left on ties, append the leftovers of BOTH runs |
| `03_quick_sort.py` | Lomuto partition with the last element as pivot, final swap to `i + 1`, recurse on both sides |
| `04_heap_sort.py` | max-heapify, swap root with the end, sift down inside the shrunk heap |
| `05_counting_and_bucket_sort.py` | sorting by indexing: counts array of size max+1; n buckets by `int(x * n)`, sorted and concatenated |
| `06_python_sort_keys_and_stability.py` | tuple keys, `-field` for mixed directions, two stable passes with the minor key first |
