# Sliding Window Median

*LeetCode 480 · Hard · Pattern: Two heaps with lazy deletion · Reading time ~13 min*

## What the problem is really asking

Slide a window of width `k` across `nums` and report the median of every window. For odd `k` the median is the middle value once the window is sorted; for even `k` it is the average of the two middle values, which can be a fraction.

```text
nums = [1, 3, -1, -3, 5, 3, 6, 7]    k = 3
        0  1   2   3  4  5  6  7

window        sorted        median
1  3 -1      -1  1  3        1
3 -1 -3      -3 -1  3       -1
-1 -3 5      -3 -1  5       -1
-3  5 3      -3  3  5        3
5  3  6       3  5  6        5
3  6  7       3  6  7        6

answer: [1, -1, -1, 3, 5, 6]
```

This is the same array and the same window as the classic example for Sliding Window Maximum, and the comparison is the point. The maximum is an *extreme*: an element that is beaten once is useless forever, which is why a monotone deque worked. The median is a *rank*. An element that is not the median now can become the median later, from either side, depending on what arrives and what leaves. Nothing can be thrown away early. We need a structure that keeps every element, knows which ones are in the lower half and which in the upper half, and supports deleting the element that slides out.

## Do it by hand first

To find a median by hand you sort the window. When the window slides, you would not re-sort from scratch. You would take your sorted list, cross out the number that left, and write the new one in its place.

```text
window [3,-1,-3] -> [-1,-3,5]:  3 leaves, 5 arrives

sorted window:  -3  -1   3          median -1

cross out 3:    -3  -1   .
insert 5:       -3  -1   5          median -1
                     ^ middle
```

Your eyes only ever looked at the **middle** of the list. Everything far below or far above the middle mattered only as a count: "one number below, one above". That is the seed. We do not need the whole sorted order. We need a lower half whose largest element is visible, an upper half whose smallest element is visible, and the sizes of the two halves.

## The first honest attempt

For each of the `n - k + 1` windows, copy it, sort it, and read the middle. That is `O(n · k log k)`.

The repeated work: consecutive windows differ by one element out and one in, but each sort rebuilds the order of all `k` elements.

```text
win 0: sort [1, 3, -1]        -> [-1, 1, 3]
win 1: sort [3, -1, -3]       -> [-3, -1, 3]
                  ^^^^^ 3 and -1 were already
                        in order last time
```

A better honest attempt keeps one sorted list and edits it with `bisect`: binary search to find where the leaving value is and remove it, binary search to insert the new one. The median is then a direct index. The searches are `O(log k)`, but inserting into or deleting from the middle of a Python list shifts elements, which is `O(k)`. So the total is `O(n · k)`. Better constants, same shape. To go further we have to stop maintaining the full order.

## The turning point

**Claim: the median only depends on the boundary between the lower half and the upper half, and an element buried inside a half never affects that boundary, so it can be deleted lazily, as long as each half's size is tracked logically.**

Two ideas are combined here.

**Idea 1: two heaps.** Split the window into `small`, the lower half, kept as a max-heap, and `large`, the upper half, kept as a min-heap. Keep `small` the same size as `large` or one bigger. Then for odd `k` the median is the top of `small`, and for even `k` it is the average of the two tops. A heap is a complete binary tree stored in an array: index 0 is the root, the children of index `i` are `2i+1` and `2i+2`. In Python, `heapq` is min-only, so `small` stores negated values.

```text
window [-3, 5, 3]:

small (max-heap)            large (min-heap)
   top: 3                      top: 5
    /
  -3
array: [-3, 3]  (negated)    array: [5]
values: 3, -3

all of small <= 3 <= 5 <= all of large
median (k odd) = top of small = 3
```

Inserting is `O(log k)`: push onto `small` if the value is at most `small`'s top, otherwise onto `large`, then move one top across if the sizes drift apart. For a stream where elements only arrive, that is the whole story (Find Median from Data Stream).

**Idea 2: lazy deletion.** A heap can only remove its top. The element leaving the window may be buried anywhere inside. But look at what a buried element does to the median: nothing. The median reads tops only. So instead of removing it, record it in a `delayed` counter ("one copy of value `x` is dead"), and decrement the *live* size of the half it belongs to. Whenever a dead value surfaces at a top (because it was the top already, or because something above it was popped or moved), pop it then. This is called pruning.

Which half does the leaving value belong to? Compare it with the top of `small`: if `x <= top(small)`, it is in the lower half; otherwise the upper half. Equal values are interchangeable, so if copies of the same value sit in both halves it does not matter which copy we declare dead.

Two rules make the corpses harmless:

- **Balance by live counts, not array lengths.** The arrays include dead entries; `small_n` and `large_n` count only live ones. If we balanced by `len(small)`, a heap full of corpses would look big and the median would be read from the wrong place.
- **Every top is always live.** After any operation that changes a top (a pop, a move across, a deletion of the top value), prune that heap. Then reading the median never touches a dead value.

```text
small array with a corpse inside:

      5            values: 5, -3, 3
     / \           -3 is dead (delayed[-3] = 1)
   -3   3          live count small_n = 2
   (x)             top 5 is live -> median safe
```

Each value is pushed once and popped once, either when it is moved across, or when it surfaces dead. The work per slide is a few `O(log k)` heap operations.

## Watch it work

`nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`. Heaps are shown by their values in array order; `(x)` marks a dead value. Live counts in brackets.

Frame 1: first window.

```text
window [1, 3, -1]
add 1 -> small        add 3 -> large (3 > 1)
add -1 -> small (-1 <= 1)
small: 1, -1   [2]     large: 3   [1]
median = top(small) = 1
```

`small` is one bigger than `large`, which is the shape we want for odd `k`.

Frame 2: i = 3, add -3, remove 1.

```text
add -3 -> small: 1,-1,-3 [3]  too big
  move top 1 across  -> large: 1, 3 [2]
remove 1: 1 > top(small) = -1 -> large side
  1 is large's top -> pruned at once
small: -1, -3 [2]     large: 3   [1]
median = -1
```

The leaving value happened to be a top, so it was deleted for real, not lazily.

Frame 3: i = 4, add 5, remove 3.

```text
add 5 -> large: 3, 5 [2]
remove 3: on large side, it is the top
  -> pruned at once
small: -1, -3 [2]     large: 5   [1]
median = -1
```

Again the departing value was a top, so no corpse is left behind.

Frame 4: i = 5, add 3, remove -1.

```text
add 3 -> large (3 > -1): 3, 5 [2]
remove -1: top of small -> pruned
  small: -3 [1] < large [2] -> move 3 to small
small: 3, -3  [2]     large: 5   [1]
median = 3
```

After deleting the old top, the halves were unbalanced by live count, so the smallest upper value moved down.

Frame 5: i = 6, add 6, remove -3, the first corpse.

```text
add 6 -> large: 5, 6 [2]
remove -3: -3 <= top(small) = 3 -> small side
  -3 is NOT the top -> delayed[-3] = 1
  small_n = 1 < large_n = 2 -> move 5 down
small: 5, -3(x), 3  [2]    large: 6  [1]
median = 5
```

The value `-3` stays physically inside `small`, but the live count already ignores it, and the median is read from the live top 5.

Frame 6: i = 7, add 7, remove 5.

```text
add 7 -> large: 6, 7 [2]
remove 5: top of small -> pruned
  small: 3, -3(x) [1] < [2] -> move 6 down
small: 6, -3(x), 3  [2]    large: 7  [1]
median = 6
```

The corpse is still buried and never surfaced; it cost nothing. The final answer is `[1, -1, -1, 3, 5, 6]`.

Across the frames, every live value in `small` was at most every live value in `large`, the live counts satisfied `small_n == large_n` or `small_n == large_n + 1`, and both tops were always live.

## Why it is correct

Three invariants hold after every `add`, `remove` and `rebalance`.

1. **Membership.** The live values in `small` and `large` together are exactly the current window (as a multiset), and `delayed` counts exactly the dead entries still physically in the heaps.
2. **Order.** Every live value in `small` is at most every live value in `large`.
3. **Balance and live tops.** `small_n` is `large_n` or `large_n + 1`, and neither heap has a dead value on top.

From these, the top of `small` is the largest of the lower `ceil(k/2)` values and the top of `large` is the smallest of the rest, which is exactly the median definition.

Each step preserves them. `add` places the value on the correct side of `small`'s live top, so order holds; `rebalance` moves a top across, which keeps order because a top is the boundary value. `remove` uses the same comparison to decide the side, so it decrements the correct live count; equal values on both sides are interchangeable, so whichever copy gets marked dead the live multiset is right. Every operation that can expose a new top is followed by a prune, so live tops hold. A dead value buried below a live top is never read, so it cannot affect the answer.

## Cost

- Time `O(n log n)` in the worst case, usually described as `O(n log k)`: each value is pushed once and popped at most once, each at the cost of `O(log` heap size`)`. Heaps hold `k` live values plus corpses that have not surfaced yet; corpses are bounded by `n`, and in practice the heaps stay near `k`.
- Space `O(n)` in the worst case for the same reason (corpses may linger), `O(k)` for the live data.

The two levels before it: sort every window `O(n · k log k)`, and a bisect-maintained sorted list `O(n · k)`. With a balanced sorted container (for example `sortedcontainers.SortedList`) you get `O(n log k)` with real deletions and much simpler code, but it is not in the standard library.

## Variations you will meet

- **Find Median from Data Stream (LeetCode 295).** Only arrivals, so no lazy deletion at all: just the two heaps and the balance rule.
- **Sliding window k-th smallest, or any percentile.** Same two heaps, but keep `small` at a live size of `p`, not half. The boundary between the heaps is then the `p`-th smallest.
- **Sliding Window Maximum, seen from here.** You could solve it with a single heap and lazy deletion too, in `O(n log n)`. The monotone deque wins there because a max can discard dominated values; a median cannot.
- **Any heap whose entries can expire or be cancelled.** Whenever items in a heap can become invalid while buried, the same rule applies: mark them, keep a true count elsewhere, and discard them only when they reach the top.

## What to carry forward

When a window needs an order statistic, split it into two heaps at the boundary you care about, balance them by live counts, and let departing values die quietly until they reach a top. That closes the chapter. You can now recognise the three questions every window problem asks: what the window must satisfy (fixed width, at most a budget, covering a target, exactly `k`), whether that condition is monotone or must be rebuilt from monotone pieces, and which summary you keep (a sum, a histogram with a shortfall counter, a deque of undominated candidates, or two heaps with lazy deletion). Faced with a new window problem, answer those three in that order and the algorithm usually writes itself.
