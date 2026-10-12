## Geometry with Exact Arithmetic

Normalize integer directions to compare slopes without floating-point rounding. The example groups points on the same line and treats duplicate points separately.

<!-- cell -->

The last recipe is geometry without floats. Max Points on a Line asks for the largest number of the given points that lie on one straight line: `[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]` gives 4. All points on one line through an anchor share a direction `(dx, dy)`. Floats cannot be trusted as keys, but the direction reduced by the gcd, with a fixed sign, is exact and hashable: `(2, 6)` and `(-1, -3)` both become `(1, 3)`, and vertical lines are `(0, 1)` with no division at all.

A copy of the anchor has no direction, since `gcd(0, 0)` is 0, but it lies on every line through the anchor, so the code counts copies separately and adds them to the best line. Each point anchors only the points after it, because a line through an earlier point was already counted from there. Two copies of `[1, 1]` and the point `[2, 2]` make one line of 3.

<!-- cell -->

```python
def slope_key(dx, dy):                         # one exact key per line direction
    g = math.gcd(dx, dy)                       # > 0 for two distinct points
    dx, dy = dx // g, dy // g
    if dx < 0 or (dx == 0 and dy < 0):         # (1, 2) and (-1, -2) are the same line
        dx, dy = -dx, -dy
    return dx, dy


def max_points(points):
    best = 0
    for i, (x1, y1) in enumerate(points):      # anchor every line at its first point
        same, dirs = 1, Counter()              # the anchor and its copies; directions to the rest
        for x2, y2 in points[i + 1:]:
            if (x1, y1) == (x2, y2):
                same += 1                      # a copy lies on every line through the anchor
            else:
                dirs[slope_key(x2 - x1, y2 - y1)] += 1
        best = max(best, same + max(dirs.values(), default=0))
    return best


print(slope_key(2, 6), slope_key(-1, -3), slope_key(0, -5))           # (1, 3) (1, 3) (0, 1)
print(max_points([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]))     # 4
print(max_points([[1, 1], [1, 1], [2, 2]]))                             # 3
```

<!-- cell -->

**Try it**
- Use a float key instead, `(y2 - y1) / (x2 - x1) if x2 != x1 else math.inf`, and run `max_points([[0, 0], [94911151, 94911150], [94911152, 94911151]])`: 3. The answer is 2: the two slopes differ, but they round to the same float.
- Delete the sign rule and run `max_points([[0, 0], [1, 1], [-1, -1]])`: 2 instead of 3, because `(1, 1)` and `(-1, -1)` became different keys.
- Call `slope_key(0, 0)`: `ZeroDivisionError`. That is why copies of the anchor never reach it.

<!-- cell -->

```python
assert max_points([]) == 0 and max_points([[0, 0]]) == 1 and max_points([[0, 0], [0, 0]]) == 2

assert max_points([[1, 0], [1, 5], [1, -3], [2, 2]]) == 3  # a vertical line
```
