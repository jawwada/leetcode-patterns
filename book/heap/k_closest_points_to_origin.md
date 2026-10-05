# K Closest Points to Origin

*LeetCode 973 · Medium · Pattern: Size-k heap (keep the k best) · Reading time ~7 min*

## The problem

Given points [[x, y], ...] on a plane and an integer k, return the k points closest to the origin by Euclidean
distance, in any order.

```text
Example: points=[[1,3],[-2,2]], k=1 -> [[-2,2]] because 8 < 10.
  Example: [[3,3],[5,-1],[-2,4]], k=2 -> [[3,3],[-2,4]].
```

## What the problem is really asking

You get n points on a plane and a number k. Return the k points nearest to (0, 0), in any order. Nearness is ordinary
straight-line distance, `sqrt(x^2 + y^2)`.

The answer is a set of k points, not a single number and not a sorted list. "Any order" is a gift: you only have to split
the points into "in" and "out", never rank the winners among themselves.

```text
points [3,3] [5,-1] [-2,4] [1,-1]     k = 2

 y  B=(-2,4) A=(3,3) D=(1,-1) C=(5,-1)
 4  B       |
 3          |           A
 2          |
 1          |
 0  --------o---------------------
-1          |   D               C
   -2  -1   0   1   2   3   4   5  x

 d = x^2+y^2:  A 18   C 26   B 20   D 2
 two closest: D (2) and A (18)
```

## Do it by hand first

Go through the points one at a time with k = 2 empty seats.

- A (18): a seat is free. Seat it.
- C (26): a seat is free. Seat it.
- B (20): no seat. Who is the worst seated point? C at 26. B is closer, so C leaves and B sits.
- D (2): no seat. The worst seated point is now B at 20. D is closer, so B leaves.

Seated at the end: A and D.

What did your eyes do at each full-house step? They looked for the **farthest** seated point and compared the newcomer
only with it. You never compared D with A. So the thing to keep track of is a club of k points that can always name its
farthest member. That is the same "keep the k best" club as Kth Largest in a Stream, with the definition of "worst"
turned around.

## The first honest attempt

Compute every point's squared distance, sort all n points by it, and return the first k. O(n log n) time, O(n) space.

The waste is ordering the losers, and ordering the winners among themselves:

```text
sorted by d:  D 2 | A 18 || B 20 | C 26
              ^^^^^^^^^^    ^^^^^^^^^^^
              winners:      losers: their relative
              order unused  order computed for nothing
```

When n is a million and k is 10, almost all of the sort's effort goes into arranging points that will be thrown away.

## The turning point

**Claim: a point farther than the current k-th closest point can never be in the answer, so each new point only has to
beat the farthest member of the club.**

If k seated points are all closer than a newcomer P, then P has at least k points ahead of it now, and future points can
only add more ahead of it. P is out forever. Conversely, if P is closer than the farthest seated point F, then F now has k
points closer than it (the other k-1 members plus P), so F is out forever. The farthest member is the only one that ever
needs to be compared.

So we need a container of k points with the **largest** distance on top: a max-heap of size k. Here the chapter's main
Python quirk shows up. `heapq` only builds min-heaps. To make the largest distance come out first, store its negation:
the most negative key is the smallest key, and the most negative key belongs to the largest distance.

```text
distance d:    2    18    20    26
key -d:       -2   -18   -20   -26
min-heap root:                  ^ -26 is smallest -> farthest
```

Two details keep the code clean:

- **No square roots.** `sqrt` is increasing, so comparing `x^2 + y^2` gives the same order as comparing true distances.
  Squared distances stay integers, so there is no floating point at all.
- **Tuples as heap items.** Push `(-d, x, y)`. The heap compares the first field, and on equal distance it compares x and
  then y. Those are integers, so ties never crash; which tied point wins does not matter because any valid answer is
  accepted.

The loop is the stream loop from two problems ago: push, and if the size is k+1, pop the root. The heap's contents at the
end are the answer. Picture the club as a disc around the origin whose radius is the farthest member's distance. A point
outside the disc bounces off; a point inside gets in and the disc shrinks to fit the new farthest member. The radius
never grows.

## Watch it work

Points in the order A(3,3), C(5,-1), B(-2,4), D(1,-1), k = 2. Heap entries are `(-d, x, y)`; shown here as `-d:point`.

```text
Frame 1: push A, d=18
     -18:A           array [(-18,3,3)]
                     size 1 <= 2, keep
disc radius: 18
```

One seat is filled; the disc is defined by A alone.

```text
Frame 2: push C, d=26
     -26:C           array [(-26,5,-1), (-18,3,3)]
      /              size 2 <= 2, keep
   -18:A
disc radius: 26 (C is farthest)
```

C sifted up to the root because -26 < -18. The root is the farthest seated point.

```text
Frame 3: push B, d=20 -> size 3, pop root C
   before pop:        after pop:
     -26:C              -20:B
     /    \             /
  -18:A  -20:B       -18:A
array [(-20,-2,4), (-18,3,3)]    disc radius: 26 -> 20
```

B was inside the disc of radius 26, so the farthest member C was evicted and the disc shrank to B's distance.

```text
Frame 4: push D, d=2 -> size 3, pop root B
   before pop:        after pop:
     -20:B              -18:A
     /    \             /
  -18:A   -2:D        -2:D
array [(-18,3,3), (-2,1,-1)]     disc radius: 20 -> 18
```

D was far inside the disc; B left; A is now the farthest member and guards the door.

```text
Frame 5: done. return the points in the heap
     [[3,3], [1,-1]]   (any order is accepted)
```

The heap was never larger than k+1 = 3. Its root was always the farthest member, and the disc radius went 18, 26, 20,
18: it only grew while seats were still empty, and only shrank once the club was full.

## Why it is correct

Invariant: **after processing the first i points, the heap holds the min(i, k) closest among them.**

Base case: zero points, empty heap. Step: if the heap had fewer than k items, the new point is pushed and kept; the
invariant holds because all points so far are kept. If the heap had k items, the new point P is pushed and the farthest
of the k+1 items is popped. The k remaining are the k closest of the k+1, and every point discarded earlier was farther
than at least k points that are still at least as close as those kept, so no discarded point beats a kept one. After
all n points the heap holds the k closest overall.

Ties: if several points share the k-th distance, any of them may be kept, which the problem allows.

## Cost

- **Size-k max-heap:** O(n log k) time, since each point costs one push and at most one pop on a heap of at most k+1
  items. O(k) extra space. Works on a stream of points.
- **Quickselect on distance:** O(n) expected time, O(1) extra if you may reorder the input. Partition on squared distance
  around index k; everything before index k is the answer. This is the previous problem's tool applied to a key.
- **Sort:** O(n log n) time, O(n) space for keys.

## Variations you will meet

- **k farthest points.** Now the bouncer is the closest member, so a plain min-heap on d works with no negation.
- **Closest to an arbitrary point (a, b).** Use `(x-a)^2 + (y-b)^2`. Nothing else changes.
- **Return the k closest in sorted order.** Drain the heap: it pops farthest first, so reverse at the end, or sort the k
  survivors (O(k log k)).
- **Find K Closest Elements (sorted 1D array, LeetCode 658).** The input is sorted, so the answer is a contiguous window
  and binary search on the window's left edge beats any heap.

## What to carry forward

"Keep the k smallest" means the bouncer is the largest, so negate keys to get a max-heap out of `heapq`. The next
problem keeps the same size-k club, but "worst" depends on two keys and one of them is a string, which you cannot negate.
