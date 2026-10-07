## 0–1 BFS

If every edge costs 0 or 1, a deque keeps the distance frontier ordered: a zero-cost move joins the front, and a cost-one move joins the back.

<!-- cell -->

Two weight patterns come first, and the simpler one lets a deque replace the heap. When every weight is 0 or 1, the heap only ever holds two distances, `d` and `d + 1`, and a deque keeps that order for free: a free move joins the *front* of the line with `dq.appendleft(...)`, a paid move the back with `dq.append(...)`.

Minimum Cost to Make at Least One Valid Path in a Grid puts an arrow in every cell: right, left, down or up. Following a cell's arrow is free, turning it to point elsewhere costs 1, and the problem asks for the cheapest way to make a path from the top-left to the bottom-right corner: 3 for the first grid below.

<!-- cell -->

```python
ARROWS = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}   # sign in the cell -> direction it points


def min_cost_valid_path(grid):
    rows, cols = len(grid), len(grid[0])
    dist = {(0, 0): 0}
    dq = deque([(0, 0, 0)])                         # (cost, r, c): only two cost values live in here, d and d + 1
    while dq:
        d, r, c = dq.popleft()
        if d > dist[(r, c)]:
            continue                                # stale, exactly like Dijkstra
        if (r, c) == (rows - 1, cols - 1):
            return d
        for sign, (dr, dc) in ARROWS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                w = 0 if grid[r][c] == sign else 1  # follow the arrow for free, turn it for 1
                if d + w < dist.get((nr, nc), math.inf):
                    dist[(nr, nc)] = d + w
                    if w == 0:
                        dq.appendleft((d, nr, nc))  # same cost: jump the line
                    else:
                        dq.append((d + 1, nr, nc))  # one more: back of the line


print(min_cost_valid_path([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]]))   # 3
print(min_cost_valid_path([[1, 1, 3], [3, 2, 2], [1, 1, 4]]))                           # 0
print(min_cost_valid_path([[1, 2], [4, 3]]))                                            # 1
```

<!-- cell -->

**Try it**
- Change `dq.appendleft(...)` to `dq.append(...)`, a plain FIFO: `[[1, 1, 3], [3, 2, 2], [1, 1, 4]]` now answers 1 instead of 0. A cost-1 entry got out before the free path arrived.
- Print `[x[0] for x in dq]` just before each `popleft()` on the first grid: only two values ever, `d` and `d + 1`, in order. That is why a deque can replace the heap.
- Swap the deque for `heapq` (push `(d + w, nr, nc)`, pop the smallest): plain Dijkstra, the same three answers, with an extra log factor.

<!-- cell -->

The same deque works on states. Minimum Moves to Move a Box to Their Target Location asks for the fewest pushes that bring a box onto its target, while the player walks for free. A node is `(box, player)`: a player step that does not touch the box costs 0, and walking into the box pushes it one cell for a cost of 1, if the cell beyond is free. The answer is the cost of the first popped state whose box sits on the target.
