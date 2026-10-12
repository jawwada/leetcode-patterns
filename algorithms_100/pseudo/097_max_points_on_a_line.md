---
rank: 97
slug: max_points_on_a_line
---

Given distinct points with integer coordinates, return the largest number of them that lie on one straight line. For `(1, 1), (3, 2), (5, 3), (4, 1), (2, 3), (1, 4)` the answer is `4`, because `(1, 4), (2, 3), (3, 2), (4, 1)` all lie on the line `x + y = 5`.

The brute force takes every pair of points as a line and counts the points on it with the cross product of #95, which costs `O(n^3)`. The faster view fixes one anchor point at a time. Every line through the anchor is pinned down by its direction alone, so the other points fall into groups by their slope from the anchor, and the biggest group plus the anchor itself is the best line through that anchor. A hash map from slope to count does the grouping in one pass, and the best over all anchors is the answer. Pairing each anchor only with the points after it is enough, because every line is counted in full from its first point.

Everything rests on the slope key being exact. A floating slope `dy / dx` fails twice: vertical lines divide by zero, and distinct slopes can round to the same double, as `94911150 / 94911151` and `94911151 / 94911152` do. A reduced fraction is exact and canonical. Dividing `dy` and `dx` by their gcd (#91) turns `2/4` and `1/2` into the same key `(1, 2)`. Flipping both signs when `dx < 0` makes the two directions along a line agree, so points on either side of the anchor share a key. Every vertical pair gets the single key `(1, 0)`, and horizontal pairs come out as `(0, 1)` with no special case, because `gcd(0, dx) = dx`.

```text
 y                       ● on the line x + y = 5    ○ elsewhere
 4  ●  .  .  .  .
 3  .  ●  .  .  ○
 2  .  .  ●  .  .
 1  ○  .  .  ●  .
    1  2  3  4  5  x

anchor (1,1)  to (3,2)  dy,dx =  1, 2                   key (1, 2)
              to (5,3)  dy,dx =  2, 4   / gcd 2         key (1, 2)
              to (4,1)  dy,dx =  0, 3   / gcd 3         key (0, 1)
              to (2,3)  dy,dx =  2, 1                   key (2, 1)
              to (1,4)  dx = 0, vertical                key (1, 0)
              biggest group: (1, 2) with 2 points → a line of 3
anchor (3,2)  to (5,3)  dy,dx =  1, 2                   key (1, 2)
              to (4,1)  dy,dx = -1, 1                   key (-1, 1)
              to (2,3)  dy,dx =  1,-1   flip            key (-1, 1)
              to (1,4)  dy,dx =  2,-2   flip, / gcd 2   key (-1, 1)
              biggest group: (-1, 1) with 3 points → a line of 4
later anchors find at most a line of 3, so the answer is 4
```

```pseudo
FUNCTION SlopeKey(p, q)
    dx ← q.x - p.x
    dy ← q.y - p.y
    IF dx = 0
        RETURN (1, 0)                   // vertical line
    IF dx < 0
        dx ← -dx                        // p → q and q → p: the same line
        dy ← -dy
    g ← Gcd(dy, dx)                     // Euclid (#91), positive since dx > 0
    RETURN (dy / g, dx / g)             // exact divisions

FUNCTION MaxPoints(points)
    n ← len(points)
    IF n ≤ 2
        RETURN n
    best ← 0
    FOR i FROM 0 TO n - 1
        counts ← empty map              // slope key → points on that line
        FOR j FROM i + 1 TO n - 1
            key ← SlopeKey(points[i], points[j])
            counts[key] ← counts.get(key, 0) + 1
            IF counts[key] + 1 > best
                best ← counts[key] + 1  // + 1 for the anchor itself
    RETURN best
```

The two loops visit `n(n - 1) / 2` pairs, each with a gcd that costs `O(log C)` for coordinates up to `C`, so the time is `O(n^2 log C)`, and one anchor's map holds fewer than `n` keys, so the space is `O(n)`. Reach for slope keys whenever points, segments or vectors must be grouped by direction: deciding whether points are collinear, merging the pieces of a line chart that share a slope, or counting the lines through a point. The classic mistake, besides the floating key, is skipping the sign normalization, which files `(1, -1)` and `(-1, 1)` under different keys although they are the same slope. Max Points on a Line promises distinct points; with duplicates, a copy of the anchor lies on every line through it and needs its own counter, added to the biggest group.

*Practice:* LC 149 Max Points on a Line · LC 1232 Check If It Is a Straight Line · LC 2280 Minimum Lines to Represent a Line Chart
