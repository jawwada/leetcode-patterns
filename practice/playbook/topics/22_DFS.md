## Depth-First Search (DFS)

DFS explores one branch before returning to the previous choice. Use a recursive call or an explicit stack. A visited set prevents repeated work in cycles; an outer loop starts a new search for each disconnected component. These examples count islands and flood regions.

<!-- cell -->

```python
def build_graph(n, edges, directed=False):
    graph = [[] for _ in range(n)]               # graph[u] = the nodes one edge away from u
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)                   # undirected: store both directions
    return graph

def grid_neighbours(grid, r, c):
    """The in-bounds cells next to (r, c). A grid is a graph whose edges you never store."""
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc
```

<!-- cell -->

```python
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
```

<!-- cell -->

The DFS template answers the other big question, how many regions there are and how big. Number of Islands counts the groups of `"1"` cells joined up, down, left or right; the sea below has 3 islands. Max Area of Island asks for the biggest one, 4 cells here.

The outer loop is what turns "flood one region" into "count the regions": every cell gets a chance to start a flood, and only unseen land does. A cell is marked when it is pushed, so it can never be pushed twice, and it is counted when it is popped. The recursive version does the same job on the call stack: it checks a cell when it arrives there, then visits the four neighbours.

<!-- cell -->

```python
def islands(grid):
    """(number of islands, largest island area) for a grid of '1' land and '0' water."""
    rows, cols = len(grid), len(grid[0])
    seen = set()                                  # STATE + INIT: cells already pushed (never push twice)
    count = best = 0                              # STATE + INIT: islands so far, largest area so far
    for r in range(rows):
        for c in range(cols):                     # every cell gets a chance to start a flood
            if grid[r][c] != "1" or (r, c) in seen:
                continue
            count += 1                            # RECORD: unseen land = a brand-new island
            seen.add((r, c))
            stack, area = [(r, c)], 0
            while stack:                          # flood the island with an explicit stack
                x, y = stack.pop()
                area += 1                         # every cell is popped exactly once
                for dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1" and (nx, ny) not in seen:
                        seen.add((nx, ny))        # STEP: mark on push...
                        stack.append((nx, ny))    # ...so no cell is pushed twice
            best = max(best, area)                # RECORD: the island is complete
    return count, best                            # RETURN


def area_recursive(grid, r, c, seen):
    """The same flood, recursive: check when you ARRIVE, then visit the 4 neighbours."""
    if not (0 <= r < len(grid) and 0 <= c < len(grid[0])) or grid[r][c] != "1" or (r, c) in seen:
        return 0                                  # off the board, water, or counted already
    seen.add((r, c))
    return 1 + sum(area_recursive(grid, r + dr, c + dc, seen) for dr, dc in DIRS)


sea = ["11000",
       "11000",
       "00100",
       "00011"]
print(islands(sea))                       # (3, 4)
print(area_recursive(sea, 0, 0, set()))   # 4
```

<!-- cell -->

**Try it**
- Mark at pop time instead: delete `seen.add((nx, ny))` and put `seen.add((x, y))` right after `x, y = stack.pop()`. `islands(["11", "11"])` now says `(1, 5)`: cell (1, 0) is pushed by (0, 0) and again by (1, 1), so it is popped twice.
- Delete `0 <=` from `0 <= nx < rows` and run `islands(["1", "0", "1"])`: `(2, 2)`. The top cell's "up" neighbour is `grid[-1]`, the bottom row, so the first island counts a phantom second cell.
- Run `area_recursive(["1" * 5000], 0, 0, set())`: `RecursionError`. The iterative `islands(["1" * 5000])` answers `(1, 5000)` without trouble.
- Collect every island's `area` in a list instead of keeping the max: `sea` gives `[1, 2, 4]` once sorted.

<!-- cell -->

```python
assert islands(["000"]) == (0, 0)                             # no land: 0 islands, area 0

assert islands(["111", "111"]) == (1, 6)                      # one island covers everything

assert islands(["1", "0", "1"]) == (2, 1)                     # top and bottom rows do not touch

assert islands(["101", "010", "101"]) == (5, 1)               # diagonal cells are not neighbours
```

<!-- cell -->

The next two variations change where the flood starts. Surrounded Regions asks you to flip every region of `O`s that does not touch the border, so the board `["XXXX", "XOOX", "XXOX", "XOXX"]` keeps only its bottom `O`.

"Can this `O` reach the border?" asked for every cell repeats the same search. Asked the other way round, *which cells can the border reach?*, it is one flood from all border cells, and whatever stays unmarked is enclosed. Number of Enclaves asks the same question for land cells, counting the ones that cannot walk off the grid.

Pacific Atlantic Water Flow asks which cells can send water to both oceans, with the Pacific along the top and left edges and the Atlantic along the bottom and right, when water only flows to a neighbour that is equally high or lower. On `[[1, 2], [4, 3]]` three cells manage it: (0, 1), (1, 0) and (1, 1).

From each ocean we walk *uphill*, and the cells both floods reach are the answer. The helper takes the step rule as a function, because that rule is the only thing that changes between the two problems.

<!-- cell -->

```python
def flood(grid, starts, can_step):
    """Every cell reachable from any start, stepping from a to b only when can_step(a, b)."""
    seen, stack = set(starts), list(starts)
    while stack:
        r, c = stack.pop()
        for nr, nc in grid_neighbours(grid, r, c):
            if (nr, nc) not in seen and can_step((r, c), (nr, nc)):
                seen.add((nr, nc))
                stack.append((nr, nc))
    return seen


def capture_surrounded(board):
    rows, cols = len(board), len(board[0])
    edge_o = [(r, c) for r in range(rows) for c in range(cols)
              if board[r][c] == "O" and (r in (0, rows - 1) or c in (0, cols - 1))]
    safe = flood(board, edge_o, lambda a, b: board[b[0]][b[1]] == "O")   # O's that touch the border
    return ["".join("O" if (r, c) in safe else "X" for c in range(cols)) for r in range(rows)]


def pacific_atlantic(h):
    rows, cols = len(h), len(h[0])
    uphill = lambda a, b: h[b[0]][b[1]] >= h[a[0]][a[1]]                # water flows down, so we walk up
    pacific = flood(h, [(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)], uphill)
    atlantic = flood(h, [(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows)], uphill)
    return sorted(pacific & atlantic)


print(capture_surrounded(["XXXX", "XOOX", "XXOX", "XOXX"]))   # ['XXXX', 'XXXX', 'XXXX', 'XOXX']
heights = [[1, 2, 2, 3, 5],
           [3, 2, 3, 4, 4],
           [2, 4, 5, 3, 1],
           [6, 7, 1, 4, 5],
           [5, 1, 1, 2, 4]]
print(pacific_atlantic(heights))   # [(0, 4), (1, 3), (1, 4), (2, 2), (3, 0), (3, 1), (4, 0)]
```

<!-- cell -->

**Try it**
- Change `>=` to `>` in `uphill`: `(1, 4)` disappears from the answer. Its only way to the Pacific crosses `(1, 3)`, which has the same height.
- Print `len(pacific), len(atlantic)` inside `pacific_atlantic`: 16 and 16, with 7 cells in common.
- Number of Enclaves with the same helper: for `g = [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]`, flood from the border land cells with `lambda a, b: g[b[0]][b[1]] == 1`, then subtract the number reached from the total land: 3.
- `capture_surrounded(["XOX", "XOX", "XXX"])` captures nothing: that region touches the top edge.
