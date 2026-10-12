---
rank: 96
slug: convex_hull
---

Given points in the plane, return the corners of the smallest convex polygon that contains them all, in counter-clockwise order. Picture a rubber band snapped around nails: it bends only at the hull's corners. For the points `(0, 0), (1, 3), (2, 1), (2, 2), (3, 2), (4, 0), (4, 4)` the hull is `(0, 0), (4, 0), (4, 4), (1, 3)`, and the other three lie inside it.

The brute force tests every pair of points as a candidate edge and keeps it when all other points lie on one side, which costs `O(n^3)`. Andrew's monotone chain sorts once and then walks. Sorted by `x`, the points run from the leftmost to the rightmost, and those two extremes split the hull into a lower chain and an upper chain. Walking the lower chain from left to right, a convex boundary turns left at every corner, which is exactly what the cross product of #95 measures. So the chain is a stack: before pushing a new point, pop the top while the two top points and the new point fail to turn left, `cross ≤ 0`. A popped point sits on or above the segment that now skips it, so it cannot be a corner of the lower boundary, and it never comes back.

The upper chain is the same walk from right to left, where a convex top boundary also turns left at every corner, so the same function builds it. The two chains share their endpoints, the leftmost and the rightmost points, so dropping the last point of each before joining them lists every corner exactly once, counter-clockwise from the leftmost point, the lowest one on a tie.

```text
 y                      sorted: (0,0) (1,3) (2,1) (2,2) (3,2) (4,0) (4,4)
 4  .  .  .  .  ●
 3  .  ●  .  .  .       lower   pops (cross ≤ 0)   stack after the push
 2  .  .  ○  ○  .       (0,0)                      (0,0)
 1  .  .  ○  .  .       (1,3)                      (0,0) (1,3)
 0  ●  .  .  .  ●       (2,1)   (1,3)              (0,0) (2,1)
    0  1  2  3  4  x    (2,2)                      (0,0) (2,1) (2,2)
                        (3,2)   (2,2)              (0,0) (2,1) (3,2)
 ● corner of the hull   (4,0)   (3,2) (2,1)        (0,0) (4,0)
 ○ inside the hull      (4,4)                      (0,0) (4,0) (4,4)

upper, right to left: pops (4,0) (3,2) (2,1) (2,2), keeps (4,4) (1,3) (0,0)
hull = lower minus its last + upper minus its last = (0,0) (4,0) (4,4) (1,3)
```

```pseudo
FUNCTION Cross(o, a, b)                 // > 0 when o → a → b turns left
    RETURN (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

FUNCTION HalfHull(pts)
    chain ← empty list                  // used as a stack: chain[-1] is the top
    FOR EACH p IN pts
        WHILE len(chain) ≥ 2 AND Cross(chain[-2], chain[-1], p) ≤ 0
            chain.pop()                 // last turn is not counter-clockwise
        chain.append(p)
    RETURN chain

FUNCTION ConvexHull(points)
    pts ← sorted(set(points))           // by x, then y; duplicates dropped
    IF len(pts) ≤ 2
        RETURN pts
    lower ← HalfHull(pts)
    upper ← HalfHull(reversed(pts))
    RETURN lower[0..len(lower) - 2] + upper[0..len(upper) - 2]
```

Sorting costs `O(n log n)`, and each chain is `O(n)` because every point is pushed once and popped at most once; the stacks take `O(n)` space. Reach for the hull when a problem asks for a fence or an enclosing boundary, for the extreme points of a set, or for the farthest pair, which always sits on the hull. The popping rule decides what happens to collinear points: `cross ≤ 0` drops a point in the middle of an edge, while Erect the Fence wants such points kept, so it pops only when `cross < 0` and then removes duplicates, because when all the points are collinear both chains contain every one of them. The classic mistake is joining the chains without dropping their last points, which lists the leftmost and rightmost corners twice; the second is sorting by `x` alone, which lets points that share an `x` arrive in any order: if the input `(3, 3), (3, 0), (3, 1)` arrives in that order, the chains keep the middle point `(3, 1)` and lose the corner `(3, 0)`.

*Practice:* LC 587 Erect the Fence · LC 1924 Erect the Fence II
