# Kth Largest Element in an Array

*LeetCode 215 · Medium · Pattern: Quickselect (partition, recurse one side) · Reading time ~8 min*

## What the problem is really asking

You get an unsorted array and a number k. Return the value that would sit at position k (counting from the top, 1-based)
if the array were sorted from largest to smallest. Duplicates count as separate positions, so in `[5, 5, 4]` the 2nd
largest is 5, not 4.

The answer is one value. The phrase "without fully sorting" in the statement is the real question: can you find the value
that belongs at one position without paying to put every other value in its place?

It helps to translate "k-th largest" into an index you can point at. In ascending order the k-th largest sits at index
`n - k`.

```text
nums = [7, 1, 9, 4, 3, 8, 2]   n = 7, k = 3

ascending:  1  2  3  4  7  8  9
index:      0  1  2  3  4  5  6
                        ^
                  target = n - k = 4  -> answer 7
```

## Do it by hand first

Imagine the seven numbers on index cards. You do not want to sort all seven. Pick one card, say 2, and split the others
into two piles: smaller than 2 on the left, the rest on the right.

```text
left (< 2)   pivot   right (>= 2)
  [1]         2      [7, 9, 4, 3, 8]
index 0     index 1   indices 2..6
```

Now 2 sits at its true sorted position, index 1, because exactly one card is smaller. You wanted index 4. Index 4 is not
in the left pile and is not the pivot, so it is in the right pile. You never need to look at the left pile again, and
you never needed to sort it. Repeat inside the right pile with a new pivot.

What your hand tracked: a live segment `[lo .. hi]` that is guaranteed to contain index 4, and one pivot's final position
per round. That is the seed of quickselect.

## The first honest attempt

Sort and read index `n - k`. It is O(n log n) and correct. A candidate who knows heaps (the previous problem) will also
offer: push everything into a min-heap of size k, then read the root. That is O(n log k), better when k is small.

Both still do work that nobody asked for. Draw what the full sort establishes:

```text
sorted:  1  2  3  4 | 7 | 8  9
         ^^^^^^^^^^   ^   ^^^^
         order of     |   order of these two:
         these four:  |   also never used
         never used   answer
```

The sort carefully decides that 1 comes before 2 and 3 comes before 4, and that 8 comes before 9. None of that changes the
answer. The size-k heap similarly keeps its k members in heap order the whole time, which is cheaper but still more than
needed when the array is fixed and fully in memory.

## The turning point

**Claim: one partition pass tells you, in O(n), which side of the pivot contains the answer, so you can discard the other
side forever.**

Partitioning around a pivot value puts every smaller element to its left and every other element to its right, and then
drops the pivot into the gap at index p. At that point the pivot is exactly where a full sort would put it, because
exactly p elements are smaller. Compare p with the target:

- `p == target`: the pivot is the answer. Stop.
- `p < target`: the answer is among the larger elements. Keep `[p+1 .. hi]`.
- `p > target`: the answer is among the smaller ones. Keep `[lo .. p-1]`.

Quicksort would recurse into both sides. Quickselect recurses into one. If the pivot lands near the middle, the live
segment halves each round, and the total work is `n + n/2 + n/4 + ... < 2n`, which is O(n).

The catch is the pivot. If you always take the last element and the array is already sorted, every pivot is the
maximum, the segment shrinks by one per round, and you pay `n + (n-1) + ... = O(n^2)`. Choosing the pivot at random
removes any input that is reliably bad: the expected size of the kept side is at most about 3n/4, so the geometric sum
still converges and the expected time is O(n).

The partition itself (Lomuto style) keeps one pointer `store`: everything before `store` is known to be smaller than the
pivot. A scan pointer `i` walks the segment; whenever `nums[i]` is smaller than the pivot, swap it to `store` and advance
`store`. At the end, swap the pivot (parked at `hi`) into `store`. That index is p.

This is the problem in the chapter where the heap is not the best tool. It is placed here on purpose: when all the data
is present at once and you need one rank, partitioning wins. When data streams in, or k is tiny and n is huge and you can
only afford O(k) memory, the size-k heap wins.

## Watch it work

`nums = [7, 1, 9, 4, 3, 8, 2]`, k = 3, target = 4. The code picks a random pivot; for this trace assume it picks the
last element of the segment each time (the result is the same with any pivot, only the number of rounds changes).

```text
Frame 1: lo=0 hi=6, pivot = nums[6] = 2, store = 0
idx    0  1  2  3  4  5  6
nums [ 7, 1, 9, 4, 3, 8, 2 ]
       ^store            ^pivot
```

The live segment is the whole array, and the target index 4 is inside it.

```text
Frame 2: scan i=0..5; only 1 < 2 -> swap to store=0
nums [ 1, 7, 9, 4, 3, 8, 2 ]   store = 1
then swap pivot into store:
nums [ 1, 2, 9, 4, 3, 8, 7 ]   p = 1
       <  ^p  >= ...............
```

The pivot 2 is now at its final index 1. Since p = 1 < target 4, the answer is to the right.

```text
Frame 3: lo=2 hi=6, pivot = nums[6] = 7, store = 2
idx    0  1  2  3  4  5  6
nums [ 1, 2, 9, 4, 3, 8, 7 ]
       dead  ^store      ^pivot
```

Indices 0 and 1 are discarded without ever being ordered relative to each other beyond what one pass did.

```text
Frame 4: scan i=2..5
i=2: 9 not < 7
i=3: 4 < 7 -> swap(2,3)  [1,2,4,9,3,8,7]  store=3
i=4: 3 < 7 -> swap(3,4)  [1,2,4,3,9,8,7]  store=4
i=5: 8 not < 7
```

Two values smaller than the pivot were gathered to the front of the segment, leaving `store` at 4.

```text
Frame 5: swap pivot into store=4
idx    0  1  2  3  4  5  6
nums [ 1, 2, 4, 3, 7, 8, 9 ]
             <    ^p  >=
p = 4 == target -> return 7
```

The pivot landed exactly on the target slot. Notice `4, 3` on its left are still out of order, and nobody cares.

Across the frames, the target index was always inside `[lo .. hi]`, and each pivot that was placed never moved again.
The segment shrank from 7 slots to 5, then the second pivot hit the target.

## Why it is correct

The loop keeps one invariant: **the element that belongs at index `target` in sorted order lies in `nums[lo .. hi]`, and
every element left of `lo` is no larger than every element in the segment, and every element right of `hi` is no smaller.**

Initially `lo = 0, hi = n - 1`, so it holds trivially. A partition of `[lo .. hi]` around pivot value x places x at p with
`nums[lo .. p-1] < x <= nums[p+1 .. hi]`. Combined with the outer invariant, exactly p elements of the whole array are
placed before the pivot in a valid sorted order, so x is the sorted element at index p. If p equals the target we are
done. If p is less, the target's element is strictly right of p, and moving `lo` to `p+1` keeps the invariant. The
symmetric case moves `hi`. Every round shrinks the segment by at least one (the pivot itself), so the loop ends, and when
`lo == hi` the single remaining slot must be the target.

## Cost

- **Quickselect:** O(n) expected time, because with a random pivot the kept side shrinks geometrically in expectation.
  O(n^2) worst case if every random pivot is terrible, which is vanishingly unlikely. O(1) extra space, because the loop
  is iterative and partitions in place.
- **Size-k min-heap:** O(n log k) time, deterministic, and O(k) space. It does not modify the input and works on a
  stream.
- **Sort:** O(n log n) time.

## Variations you will meet

- **"Do not modify the input."** Quickselect rearranges the array. Either copy it (O(n) space) or use the size-k heap.
- **Guaranteed linear time.** Median-of-medians chooses a pivot that is provably near the middle, giving O(n) worst case.
  Interviewers rarely want it coded, but they like to hear that it exists.
- **Many duplicates.** With a two-way partition, an array of equal values still makes progress (the pivot moves out of
  the segment each round) but can degrade toward quadratic. A three-way partition (`< x`, `== x`, `> x`) handles it: if
  the target index falls in the middle band, return x at once.
- **Top k elements, not just the k-th.** After quickselect stops at the target, everything from the target index to the
  end is the k largest, unordered. K Closest Points can use this trick on distances.

## What to carry forward

Partition places one element in its final sorted slot and tells you which side the target is on; follow only that side.
The next problem returns to the size-k heap, but the club now keeps the k smallest distances, so its bouncer is the
farthest point and the heap must become a max-heap.
