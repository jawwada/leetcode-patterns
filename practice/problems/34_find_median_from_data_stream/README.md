# Find Median from Data Stream (LeetCode 295)

**Area:** heap · **Difficulty:** Medium-Hard · **Key operations:** push into the max-heap low, move its max to the min-heap high, rebalance sizes, read the roots

## Problem

Numbers arrive one at a time. After each arrival report the median of everything seen so far: the middle value for an odd count, the mean of the two middle values for an even count. The practice script takes the whole stream as a list and returns the list of medians after each addition.

## Example

```
stream   5     15     1     3     8
sorted   5   5 15   1 5 15   1 3 5 15   1 3 5 8 15
median   5.0  10.0   5.0     4.0        5.0
```

## Brute force

Append each number to a list, sort it, read the middle element(s).

O(n log n) per addition (or O(n) with `bisect.insort`), O(n) space. The wasted work: the full sorted order of *both* halves is rebuilt or maintained, although only the boundary between the lower half and the upper half ever matters.

## From brute force to optimal

The median is determined by the **maximum of the lower half** and the **minimum of the upper half**. The internal order of each half is irrelevant. Keep the lower half in a max-heap and the upper half in a min-heap; each exposes exactly the one element we need at its root.

Insertion: push the new number into `low`, then move `low`'s maximum across to `high`. That guarantees every element of `low` is at most every element of `high` (the new number has been "filtered" through the seam). If `high` is now bigger than `low`, move `high`'s minimum back. Both heaps stay within one of each other in size, with `low` holding the extra element when the count is odd. Each step is O(log n); reading the median is O(1).

## Intuition

Split the numbers into a small half and a large half so that every small number is at most every large number and the halves differ in size by at most one. The median lives at the seam: the biggest small number and the smallest large number. Picture two triangles touching apex to apex along a horizontal line: the left one (max-heap) has its apex at the largest small number, the right one (min-heap) its apex at the smallest large number. A new number drops into the left triangle; its apex is flicked across the seam so the seam stays ordered; if the right triangle got too heavy, its apex is flicked back. The seam *is* the median.

## Walkthrough

`low` is drawn with its stored negatives undone, so it reads as the actual numbers with the maximum first; `high` reads with the minimum first.

```
add 5    push into low           low [5]       | high []
         move low's max to high  low []        | high [5]
         high bigger: rebalance  low [5]       | high []          median 5.0   (odd: max(low))

add 15   push into low           low [15, 5]   | high []
         move low's max to high  low [5]       | high [15]        median (5 + 15) / 2 = 10.0

add 1    push into low           low [5, 1]    | high [15]
         move low's max to high  low [1]       | high [5, 15]
         high bigger: rebalance  low [5, 1]    | high [15]        median 5.0

add 3    push into low           low [5, 1, 3] | high [15]
         move low's max to high  low [3, 1]    | high [5, 15]     median (3 + 5) / 2 = 4.0

add 8    push into low           low [8, 1, 3] | high [5, 15]
         move low's max to high  low [3, 1]    | high [5, 15, 8]
         high bigger: rebalance  low [5, 1, 3] | high [8, 15]     median 5.0
```

The seam after the last step: `max(low) = 5`, `min(high) = 8`; the count is odd and `low` has the extra element, so the median is 5.

## Steps

1. `low = []` (max-heap via negated values), `high = []` (min-heap).
2. For each `x`: `heappush(low, -x)`.
3. `heappush(high, -heappop(low))`: the largest of the small side crosses the seam.
4. If `len(high) > len(low)`: `heappush(low, -heappop(high))`.
5. Median: if `len(low) > len(high)` it is `-low[0]`; otherwise `(-low[0] + high[0]) / 2`.

## Complexity

O(log n) per addition (two or three heap operations), O(1) per median read, O(n) space for the two heaps.

## Pitfalls

- **Forgetting to negate when a value crosses heaps.** `low` stores `-x`; moving a popped value into `high` without flipping its sign puts negatives into `high` and every median comes out with the wrong sign (`[1, 2]` reports -1.5).
- **Rebalancing with `>=` instead of `>`.** Equal sizes are allowed; rebalancing them makes `low` always one bigger, so even counts read a single root (`[1, 2]` reports 2.0).
- **Reading a single root with `>=`.** The symmetric slip on the median read: an even count reports `max(low)` alone (`[1, 2]` reports 1.0).
- **Floor division `//` in the mean.** `(1 + 2) // 2` is 1, not 1.5.
- **Pushing directly into whichever heap "looks right"** (`x < low[0]` tests) without the cross-seam move. Edge cases on empty heaps multiply; the push-then-move pattern needs no special cases.
