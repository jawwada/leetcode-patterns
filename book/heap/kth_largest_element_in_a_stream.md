# Kth Largest Element in a Stream

*LeetCode 703 · Easy · Pattern: Size-k heap (keep the k best) · Reading time ~6 min*

## The problem

Design a class initialised with k and a list of scores that then receives new scores one at a time via add(val); after
every add return the k-th largest element seen so far, duplicates counted.

```text
Example: k=3, nums=[4,5,8,2]; add(3)->4, add(5)->5, add(10)->5,
  add(9)->8, add(4)->8.
```

## What the problem is really asking

You are building a scoreboard. It starts with some scores and a number k. After that, scores arrive one at a time, and
after each arrival you must report the k-th largest score seen so far, with duplicates counted separately.

The answer is one number, asked for again and again. One query is trivial; thousands of queries on a growing pile
punish anything that recomputes from scratch.

```text
k = 3, start [4, 5, 8, 2]

sorted high -> low:  8  5  4  2
rank:                1  2  3  4
                           ^ 3rd largest = 4

add(10):            10  8  5  4  2
                           ^ 3rd largest = 5
```

## Do it by hand first

With k = 3 and scores 4, 5, 8, 2, you would circle the three biggest: 8, 5, 4. The answer is the smallest circled one,
4. The 2 can be crossed out for good. Someone calls 3: it loses to the smallest circle, 4, so you ignore it. Someone calls
10: it beats 4, so 10 gets a circle and 4 loses its circle. The new smallest circled number is 5.

```text
circled (top 3)      smallest circled = answer
{8, 5, 4}            4
add 3:  3 < 4        ignore             -> 4
add 10: 10 > 4       circle 10, drop 4  -> {10, 8, 5} -> 5
```

Your hand kept a set of k numbers and knew which one was the weakest. Every decision was one comparison against the
weakest. That is the data structure: a container of k items that always knows its minimum.

## The first honest attempt

Keep every score in a list. On each add, append the new score, sort descending, and return the item at index k-1.

That costs O(n log n) per add, where n is how many scores have arrived, to read one slot.

```text
add(3):  sort [8 5 4 3 2]              read slot 2
add(10): sort [10 8 5 4 3 2]           read slot 2
add(9):  sort [10 9 8 5 4 3 2]         read slot 2
               ^^^^^^ ^^^^^^^
               top 3  re-sorted every time,
                      never read again
```

The tail below the top k is re-sorted on every call, yet nothing in it can ever matter again.

## The turning point

**Claim: only the k largest values seen so far can ever be the answer, and among them we only ever need the smallest.**

If v is outside the current top k, at least k values are at least as big as v. Adds never remove values, so v always
has k values above it and can never be the k-th largest. Discard it the moment it falls out.

The k-th largest is, by definition, the smallest member of the top k. When a value arrives, the only question is "does it
beat the weakest member?". If yes, the weakest is evicted; if no, the newcomer is. Only the weakest is ever involved.

So we need k items with the minimum visible instantly and removable cheaply: a min-heap capped at size k. A min-heap for
large values feels backwards until you see its job: guard the door, and the door is guarded by the weakest member.

Push the new value; if the heap has k+1 items, pop the root; return the root. At construction, heapify and pop down to k.

## Watch it work

k = 3, initial `[4, 5, 8, 2]`, then add 3, 10, 9. Each frame shows the heap as a triangle and as its array.

```text
Frame 1: init. heapify -> [2, 4, 8, 5]; size 4 > 3, pop 2
        4
       / \          array [4, 5, 8]
      5   8         root 4 = 3rd largest
```

Heapify built a min-heap; the extra 2 was popped because only three seats exist.

```text
Frame 2: add(3). push -> [3, 4, 8, 5]; size 4, pop 3
        4
       / \          array [4, 5, 8]
      5   8         return 4
```

3 sifted to the root as the smallest and was evicted at once: it bounced off the club.

```text
Frame 3: add(10). push -> [4, 5, 8, 10]; pop 4
        5
       / \          array [5, 10, 8]
     10   8         return 5
```

10 entered at the bottom and 4 left from the top; the last item, 10, was dropped into the root hole and sank to slot 1.
The apex rose to 5.

```text
Frame 4: add(9). push -> [5, 9, 8, 10]; pop 5
        8
       / \          array [8, 9, 10]
      9   10        return 8
```

9 beat the weakest member 5, so 5 left. The apex rose again, to 8.

After every frame the heap held the three largest values so far, with the smallest at the root. The root never
decreased, because each eviction replaces the minimum with something at least as large.

## Why it is correct

Invariant: after each call, the heap contains the k largest values seen so far (as a multiset), provided at least k values
exist.

Construction keeps the k largest by popping the smallest extras. On add(v): if v is below the root, the pop removes v
itself, correctly, since k values sit at or above it. Otherwise the pop removes the old root, which now has k values at or
above it (the other k-1 members plus v). Either way the invariant survives, and the minimum of the k largest, `heap[0]`,
is the k-th largest. With fewer than k initial items the heap is simply smaller until enough arrive.

## Cost

- Time: O(log k) per add, since the heap never exceeds k+1 items. Construction: O(n) heapify plus O((n - k) log n) pops.
- Space: O(k), because everything below the top k is discarded.

## Variations you will meet

- **k-th smallest in a stream.** Keep the k smallest in a max-heap (push negated values).
- **Values expire** (only the last w scores count). Evicted values may matter again when bigger ones leave, so discarding
  is no longer safe; use lazy deletion or a sorted container.
- **Static array, single query.** Without a stream, quickselect beats O(n log k) on average: the next problem.

## What to carry forward

The k-th largest is the weakest member of the top-k club, so keep the club in a min-heap of size k and let its root guard
the door. The next problem asks the same question once on a fixed array, where partitioning beats the heap.
