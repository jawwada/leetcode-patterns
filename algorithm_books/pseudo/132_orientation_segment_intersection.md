---
rank: 132
slug: orientation_segment_intersection
---

Given three points, decide whether the path `o → a → b` turns left, turns right or runs straight; given two segments, decide whether they share a point. Coordinates are integers. The path `(0, 0) → (4, 0) → (2, 3)` turns left, the segments `(0, 0)-(4, 4)` and `(0, 4)-(4, 0)` cross at `(2, 2)`, while `(0, 0)-(2, 2)` and `(3, 3)-(5, 5)` lie on one line without touching.

Slopes bring division, a special case for vertical lines and rounding error; the cross product needs none of them. For the vectors `o → a` and `o → b`, `cross(o, a, b) = (a.x - o.x)(b.y - o.y) - (a.y - o.y)(b.x - o.x)` is the signed area of the parallelogram they span. It is positive when `b` lies to the left of the ray from `o` through `a`, a counter-clockwise turn; negative when `b` lies to the right, a clockwise turn; and zero when the three points are collinear. On integers it is exact.

Two segments cross cleanly when each straddles the other's line: `p1` and `p2` lie on opposite sides of the line `q1 q2`, and `q1` and `q2` on opposite sides of the line `p1 p2`. Opposite sides means opposite signs, so the test is `d1 · d2 < 0` and `d3 · d4 < 0`. One straddle is not enough: `(5, -1)-(5, 1)` straddles the line `y = 0` yet misses `(0, 0)-(2, 0)`. The sign test misses the touching cases, where an endpoint sits exactly on the other segment: its cross product is `0`, and it lies on the segment rather than on the line beyond it exactly when it falls inside the box spanned by the segment's ends. One such check per endpoint covers T-junctions, shared endpoints and collinear overlaps.

```text
 y                                p1 = (0,0)   p2 = (4,4)
 4  q1 .  .  .  p2                q1 = (0,4)   q2 = (4,0)
 3  .  \  .  /  .
 2  .  .  X  .  .                 d1 = cross(q1, q2, p1) = -16   right
 1  .  /  .  \  .                 d2 = cross(q1, q2, p2) =  16   left
 0  p1 .  .  .  q2                d3 = cross(p1, p2, q1) =  16   left
    0  1  2  3  4  x              d4 = cross(p1, p2, q2) = -16   right
                                  d1 · d2 < 0 and d3 · d4 < 0 → true

(0,0)-(2,2) and (3,3)-(5,5): d1 = d2 = d3 = d4 = 0, no straddle, and no
endpoint lies inside the other segment's box → false
from o = (0,0) toward a = (4,0): b = (2,3) gives 12 (left turn),
b = (2,-3) gives -12 (right turn), b = (6,0) gives 0 (straight)
```

```pseudo
FUNCTION Cross(o, a, b)                 // > 0 left turn, < 0 right, 0 straight
    RETURN (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

FUNCTION OnSegment(p, q, r)             // r is on the line pq: inside the box?
    inside_x ← min(p.x, q.x) ≤ r.x ≤ max(p.x, q.x)
    inside_y ← min(p.y, q.y) ≤ r.y ≤ max(p.y, q.y)
    RETURN inside_x AND inside_y

FUNCTION SegmentsIntersect(p1, p2, q1, q2)
    d1 ← Cross(q1, q2, p1)              // side of p1 seen from q1 → q2
    d2 ← Cross(q1, q2, p2)
    d3 ← Cross(p1, p2, q1)              // side of q1 seen from p1 → p2
    d4 ← Cross(p1, p2, q2)
    IF d1 * d2 < 0 AND d3 * d4 < 0
        RETURN true                     // both pairs straddle: a clean crossing
    IF d1 = 0 AND OnSegment(q1, q2, p1)
        RETURN true                     // p1 lies on segment q1 q2
    IF d2 = 0 AND OnSegment(q1, q2, p2)
        RETURN true
    IF d3 = 0 AND OnSegment(p1, p2, q1)
        RETURN true
    IF d4 = 0 AND OnSegment(p1, p2, q2)
        RETURN true
    RETURN false
```

Each test is a handful of multiplications, so both questions cost `O(1)`. With coordinates between `-10^9` and `10^9` the cross product can reach `4 · 10^18`, which fits a signed 64-bit integer but overflows 32 bits; the product `d1 · d2` overflows even 64 bits, so outside Python compare the signs instead of multiplying. Reach for the cross product whenever a problem asks about turns, sides, collinearity or convexity: three points are collinear exactly when it is `0`, which decides Check If It Is a Straight Line and Valid Boomerang, and the convex hull (#133) is built by popping every point that does not turn left. The classic mistake is comparing slopes as floating-point numbers, which divides by zero on vertical lines and rounds the distinct slopes `10^9 / (10^9 - 1)` and `(10^9 + 1) / 10^9` to the same double; Minimum Lines to Represent a Line Chart is known for inputs that break exactly that. The second is skipping the touching checks, which calls segments that share only an endpoint disjoint.

*Practice:* LC 1232 Check If It Is a Straight Line · LC 1037 Valid Boomerang · LC 2280 Minimum Lines to Represent a Line Chart · LC 587 Erect the Fence
