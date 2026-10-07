## Graphs I: BFS & DFS

> A graph is just *things* (nodes) and *you can get from this one to that one* (edges). BFS spreads from the start like a ripple in a pond, one ring of equal distance at a time; DFS runs down one corridor to its end before backing up. Both visit every node they can reach exactly once, because they mark a node the moment they discover it.

**Reach for it when** the problem talks about cells connected up/down/left/right, islands or regions, something spreading in rounds (rot, fire, a signal), "fewest steps / moves / jumps / transformations" where every move costs the same, "can I reach", copying a structure that has cycles, or a situation that changes one move at a time (a board, a word, a key ring).

**In this repo:** `graphs/` (19 of its 45 problems; Graphs II and III take the rest) · bank: `practice/simple/41_number_of_islands.py`, `practice/simple/42_clone_graph.py`, `practice/simple/44_rotting_oranges.py` · basics: `practice/simple/basics/graphs/01_adjacency_list_bfs_dfs.py`, `practice/simple/basics/searches/03_bfs_grid_shortest_path.py`, `practice/simple/basics/searches/04_dfs_recursive_and_iterative.py`, `practice/simple/basics/searches/05_connected_components.py`, `practice/simple/basics/searches/06_multi_source_bfs_01_matrix.py`

### The picture

Half of every graph problem is one sentence: *what is a node, and what is an edge?* Once you can say it, the code is one of two loops.

| The problem says | A node is | An edge is | It asks | Tool |
|---|---|---|---|---|
| a grid of land and water | a cell `(r, c)` | a step up/down/left/right onto land | how many groups? | flood fill (DFS or BFS) |
| "every minute the rot spreads" | a cell | a neighbour, one minute later | when is the last one reached? | multi-source BFS |
| "change one letter at a time" | a word | two words one letter apart | fewest changes | BFS, neighbours from wildcard buckets |
| "slide a tile into the gap" | a whole board, as a string | one slide | fewest moves | BFS over states |
| "keys open locks" | (cell, keys held) | one step | fewest steps | BFS over augmented states |
| "ride buses" | a bus route | two routes share a stop | fewest buses | BFS over routes |
| "deep-copy this graph" | a node object | its neighbour list | a copy | traversal + old→new map |

Weighted edges are [Graphs III](#s19); "in what order?" and "are these connected?" are [Graphs II](#s18).

```text
A grid is a graph you never build:              BFS from S spreads in rings of equal distance:

              (r-1, c)                          S . . #            0 1 2 #
    (r, c-1)   (r, c)   (r, c+1)                . # . .    -->     1 # 3 4
              (r+1, c)                          . . . #            2 3 4 #

each cell's edges go to the 4 cells             queue over time:  [0] [1 1] [2 2] [3 3] [4 4]
around it that are on the board                 ring k leaves the queue before ring k+1 starts

DFS on the same grid runs down one corridor as far as it can, then backs up to the last fork.
Same cells, same cost, but its order says nothing about distance.
```

**Why it is fast:** every node goes into the container at most once (it is marked the moment it goes in) and every edge is looked at once from each end, so a traversal costs O(V + E); on a grid that is O(rows · cols). The brute force in most of these problems starts a fresh search from every cell and re-walks the same region again and again: O((rows · cols)²). One `seen` set shared by all the searches is the whole speed-up.

### From idea to code

**The idea in one sentence:** *put the start in a container and mark it; then repeatedly take one node out, and put in every neighbour you have never seen, marking it as it goes in.* A queue (oldest first) makes that BFS. A stack (newest first) makes it DFS, which is fine for flooding a region; anything that needs the real DFS tree (cycle colours, topological order, bridges in [Graphs II](#s18)) uses recursion.

| Decision | Fewest steps (BFS) | Count / measure regions (flood) |
|---|---|---|
| **State**: what must I remember? | a `deque` frontier and `dist`, which doubles as `seen` | `seen`, a stack for the current flood, `count` and `best` |
| **Definition**: what exactly does each variable mean? | `dist[v]` = fewest moves from the start to `v`; the queue = discovered cells not expanded yet | `seen` = cells already pushed; `count` = floods started so far |
| **Invariant**: what is true at the end of every step? | the queue holds at most two distances, the `d`s in front of the `d + 1`s; every cell in `dist` is either waiting in the queue or already expanded, and enters the queue exactly once | every cell in `seen` is either waiting in the stack or already expanded, and enters the stack exactly once; when a flood ends, its whole region is in `seen` |
| **Step**: how does one item change the state? | pop a cell; every neighbour that is on the board, passable and new gets `d + 1` and joins the queue | pop a cell; every new land neighbour is marked and pushed |
| **Record**: when is the answer updated? | a distance is written when a cell is *discovered* (it is final already) | `count += 1` when the outer loop finds unseen land; `best = max(best, area)` when a flood ends |
| **Init**: starting values | every source in the queue and in `dist`, at distance 0 | `seen` empty, `count = best = 0` |
| **Return**: what comes back, and for "not found"? | the target's distance when it is *popped*; `-1` if the queue runs dry | `count`, `best` |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "the four cells around me" | `for dr, dc in DIRS: nr, nc = r + dr, c + dc` |
| "still on the board" | `0 <= nr < rows and 0 <= nc < cols` |
| "never discovered" | `(nr, nc) not in seen` (or `not in dist`) |
| "mark it as I discover it" | `seen.add(nxt)` on the line just before `queue.append(nxt)` |
| "the oldest discovery next" (BFS) | `r, c = queue.popleft()` |
| "the newest discovery next" (DFS) | `r, c = stack.pop()` |
| "one ring further out" | `dist[nxt] = dist[cur] + 1` |
| "a whole ring at once" | `for _ in range(len(queue)):` |
| "a new island starts here" | an outer loop over every cell: `if land and not seen: count += 1` |

**Turn the story into a graph before you type.** Six questions decide every line of a BFS:

| # | Ask | Example answers | It becomes |
|---|---|---|---|
| 1 | **Node**: what changes from one move to the next? | a cell `(r, c)` · a word · a board string · `(r, c, keys)` | what goes in `seen` (hashable: a tuple or a string) |
| 2 | **Edge**: what is ONE legal move? | step onto a free cell · change one letter · turn one wheel | `def neighbours(node): yield ...` |
| 3 | **Cost**: does every move cost the same? | yes · only 0 or 1 · any w ≥ 0 | BFS · a deque (0-1 BFS) · a heap ([Graphs III](#s19)) |
| 4 | **Start**: one source, or many at once? | the entrance · every rotten orange · every 0 | all of them in the queue and in `seen`, at distance 0 |
| 5 | **Goal**: what ends the search? | reach a cell · hold every key · run to the end | `if is_goal(node): return d`, checked when the node is *popped* |
| 6 | **Extra**: can two arrivals at the same place have different futures? | more keys · more budget left · a different set of visited nodes | put it in the node; check that places × extras fits (≲ 10⁶) |

Never put the move count itself in the node: the queue order already carries it, and with it inside, `seen` can no longer merge two arrivals at the same place. On an open 6 × 6 grid, a BFS from corner to corner pops 36 states when the node is the cell, and 111 when it is `(r, c, moves)`.

Step zero is listing a node's neighbours. From an edge list you build an adjacency list once; on a grid you compute them on the fly.

```python
def build_graph(n, edges, directed=False):
    graph = [[] for _ in range(n)]               # graph[u] = the nodes one edge away from u
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)                   # undirected: store both directions
    return graph


DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))        # down, up, right, left


def grid_neighbours(grid, r, c):
    """The in-bounds cells next to (r, c). A grid is a graph whose edges you never store."""
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc


print(build_graph(6, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]))   # [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3], []]
print(build_graph(3, [(0, 1), (1, 2)], directed=True))            # [[1], [2], []]
print(list(grid_neighbours(["...", "...", "..."], 0, 0)))         # [(1, 0), (0, 1)]  a corner has 2
print(list(grid_neighbours(["...", "...", "..."], 1, 1)))         # [(2, 1), (0, 1), (1, 2), (1, 0)]
```

**Try it**
- Compare `build_graph(2, [(0, 1)], directed=True)` with `build_graph(2, [(0, 1)])`: `[[1], []]` versus `[[1], [0]]`. In the directed one, node 1 has no way back to 0.
- Delete the `0 <=` part of the row check and print `list(grid_neighbours(["...", "...", "..."], 0, 0))`: `(-1, 0)` shows up. Python reads `grid[-1]` as the *last* row instead of failing, so the top edge would quietly touch the bottom edge.
- Feed 1-indexed edges: `build_graph(3, [(1, 2), (2, 3)])` raises `IndexError` (there is no `graph[3]`). When nodes are numbered from 1, allocate `n + 1` lists.
- An adjacency matrix becomes lists in one line: for `M = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]`, `[[j for j, x in enumerate(row) if x] for row in M]` gives `[[1, 2], [0], [0]]`.

The BFS template. The order inside the loop is a decision: a cell is marked and given its distance when it is *pushed* (that distance is already final, because it was discovered from the closest ring), and compared with the target when it is *popped*.

```python
def shortest_steps(grid, start, target):
    """Fewest moves from start to target over cells that are not '#'; -1 if unreachable."""
    start, target = tuple(start), tuple(target)  # LeetCode passes lists; dict keys must be tuples
    rows, cols = len(grid), len(grid[0])
    if grid[start[0]][start[1]] == "#":
        return -1                                 # RETURN: you cannot start inside a wall
    queue = deque([start])                        # STATE + INIT: the frontier, oldest first
    dist = {start: 0}                             # STATE + INIT: dist[cell] = fewest moves; also "seen"
    while queue:
        r, c = queue.popleft()                    # the closest cell not expanded yet
        if (r, c) == target:
            return dist[(r, c)]                   # RETURN: first time it leaves the queue = shortest
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1     # RECORD on discovery: one ring further out, final already
                queue.append((nr, nc))                # STEP: it joins the frontier
    return -1                                     # RETURN: the queue ran dry, target never reached


maze = ["S..#",
        ".#..",
        "...#"]
print(shortest_steps(maze, (0, 0), (1, 3)))            # 4
print(shortest_steps(maze, (0, 0), (2, 2)))            # 4
print(shortest_steps(["S#.", "##."], (0, 0), (1, 2)))  # -1
```

**Try it**
- Swap `queue.popleft()` for `queue.pop()` (a stack) and run `shortest_steps(["....", "....", "...."], (0, 0), (2, 0))`: it says 8 where BFS says 2. Without the queue's order, "first time out = shortest" stops being true.
- Print `[dist[x] for x in queue]` as the first line inside the loop: the queue never holds more than two distances, `d` and `d + 1`. That is the invariant that makes BFS correct.
- Move the target test to discovery time (return right after the `append` when `(nr, nc) == target`): the same answers, found one ring sooner, except `shortest_steps(["S"], (0, 0), (0, 0))` now returns -1. The start is never "discovered", so it needs its own check.
- Delete the wall-start check: `shortest_steps(["#."], (0, 0), (0, 1))` returns 1, a path that begins inside a wall.

**Three ways for BFS to know a distance.** Pick one per problem; never mix them.

| Style | The lines | Use it when |
|---|---|---|
| a `dist` map | `dist = {start: 0}` … `dist[nxt] = dist[cur] + 1` | you need every node's distance (01 Matrix, Walls and Gates); it doubles as `seen` |
| the distance rides in the queue | `queue.append((nxt, d + 1))` | a state search that only needs the goal's distance (Word Ladder, Open the Lock) |
| whole rings | `for _ in range(len(queue)):` … then `steps += 1` | the answer is a number of rounds (Rotting Oranges), or a ring must finish together (Word Ladder II) |

Here are the six answers for Open the Lock (752): the node is the 4-digit string, an edge turns one wheel one click, every move costs 1, the start is `"0000"`, the goal is the target, and nothing extra matters (dead ends are simply nodes you may not enter). The loop itself never changes, so write it once as `bfs_states` and pass the answers in as arguments:

```python
def bfs_states(starts, neighbours, is_goal, key=lambda s: s):
    """Fewest moves from any start state to a goal state, or -1. key(state) must be hashable."""
    queue = deque((s, 0) for s in starts)         # STATE + INIT: (state, moves): the distance rides along
    seen = {key(s) for s in starts}               # STATE + INIT: every state ever queued
    while queue:
        state, moves = queue.popleft()
        if is_goal(state):
            return moves                          # RETURN: popped first = fewest moves
        for nxt in neighbours(state):
            if key(nxt) not in seen:
                seen.add(key(nxt))                # STEP: mark on push...
                queue.append((nxt, moves + 1))    # ...one move further out
    return -1                                     # RETURN: every reachable state was tried


def open_lock(deadends, target):
    dead = set(deadends)
    if "0000" in dead:
        return -1
    def turns(s):                                 # one wheel, one click up or down
        for i in range(4):
            for step in (1, -1):
                t = s[:i] + str((int(s[i]) + step) % 10) + s[i + 1:]
                if t not in dead:
                    yield t
    return bfs_states(["0000"], turns, lambda s: s == target)


print(open_lock(["0201", "0101", "0102", "1212", "2002"], "0202"))   # 6
print(open_lock(["8888"], "0009"))                                   # 1
print(open_lock(["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "8888"))   # -1
```

**Try it**
- Delete the `if "0000" in dead` check: `open_lock(["0000"], "8888")` answers 8 instead of -1. `turns` only filters the states you move *to*, so the start itself needs its own check.
- Turn the wheels upward only (`for step in (1,)`): `open_lock([], "0009")` takes 9 moves instead of 1. Each edge you leave out is a move the search can never make.
- Predict `open_lock(["0001", "0009", "0010", "0090", "0100", "0900", "1000", "9000"], "0002")` before running it: -1, because every first move is a dead end.

The DFS template: count the islands and measure the biggest. The outer loop is what turns "flood one region" into "count the regions". A cell is marked when it is pushed, so it can never be pushed twice, and counted when it is popped:

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

**Try it**
- Mark at pop time instead: delete `seen.add((nx, ny))` and put `seen.add((x, y))` right after `x, y = stack.pop()`. `islands(["11", "11"])` now says `(1, 5)`: cell (1, 0) is pushed by (0, 0) and again by (1, 1), so it is popped twice.
- Delete `0 <=` from `0 <= nx < rows` and run `islands(["1", "0", "1"])`: `(2, 2)`. The top cell's "up" neighbour is `grid[-1]`, the bottom row, so the first island counts a phantom second cell.
- Run `area_recursive(["1" * 5000], 0, 0, set())`: `RecursionError`. The iterative `islands(["1" * 5000])` answers `(1, 5000)` without trouble.
- Collect every island's `area` in a list instead of keeping the max: `sea` gives `[1, 2, 4]` once sorted.

### Watch it work

Each line is one ring of the BFS; at the end the grid shows every cell's distance from `S`.

```python
def trace_rings(grid, start):
    dist, queue, ring = {start: 0}, deque([start]), 0
    while queue:
        layer = [queue.popleft() for _ in range(len(queue))]   # exactly the cells at distance `ring`
        print(f"ring {ring}: {layer}")
        for r, c in layer:
            for nr, nc in grid_neighbours(grid, r, c):
                if grid[nr][nc] != "#" and (nr, nc) not in dist:
                    dist[(nr, nc)] = ring + 1
                    queue.append((nr, nc))
        ring += 1
    for r, row in enumerate(grid):
        print("   ", " ".join("#" if ch == "#" else str(dist.get((r, c), "?")) for c, ch in enumerate(row)))


trace_rings(maze, (0, 0))
```

**Try it**
- Predict the distances for `trace_rings(maze, (1, 2))`, then run it: the rings spread both ways and the far cell (1, 0) is 4 away.
- Wall in a cell: `trace_rings(["S..#", ".##.", "...#"], (0, 0))`. Cell (1, 3) keeps its `?`: that is the `-1` case of `shortest_steps`.
- Pop one cell per iteration instead of a whole layer, write `dist[(r, c)] + 1` instead of `ring + 1`, and print each popped cell's distance: `0 1 1 2 2 3 3 4 4`, never decreasing.

### Where it goes wrong

1. **Marking `seen` when you pop instead of when you push** (and nothing else). A node gets pushed by several neighbours before its first pop: the queue fills with copies and anything counted per pop is counted twice (a 2×2 block of land has area 5). The other correct form: mark on pop *and skip a node already marked*. Copies still get into the queue, but none is expanded twice; Dijkstra must use this form ([Graphs III](#s19)).
2. **Half a bounds check.** Without `0 <=`, Python reads `grid[-1]` as the last row instead of failing, so the top edge silently touches the bottom edge. Always write `0 <= nr < rows`.
3. **Forgetting to mark the start.** Without `seen.add((r, c))` before the flood, the start is pushed again by its own neighbour: `islands(["11"])` returns `(1, 3)`.
4. **One search on a disconnected graph.** With `build_graph(4, [(0, 1), (2, 3)])`, a search from 0 reaches only {0, 1}. Counting or visiting everything needs the outer loop that tries every node as a start.
5. **DFS for "fewest steps".** DFS finds *a* path, not the shortest: on an open 3×4 grid a stack-based search reports 8 moves from (0, 0) to (2, 0), BFS reports 2.
6. **Counting pops instead of rings.** When the answer is a number of rounds, drop the ring loop (or put `minutes += 1` inside it) and you count pops: the first Rotting Oranges grid answers 6 instead of 4. Finish the whole ring, then add one.
7. **Deep recursion.** A recursive flood of a 300×300 island can need 90,000 nested calls; Python stops at about 1,000. Use an explicit stack (or BFS) on big grids, and say so.
8. **Flood fill with the new colour equal to the old one.** A fill that uses the paint as its "seen" mark never ends on `[[1, 1]]` from (0, 0) with colour 1: painting changes nothing, so the two cells keep pushing each other. Return early when the colours are equal.
9. **An undirected edge stored once.** `build_graph(2, [(0, 1)], directed=True)[1]` is `[]`: from node 1 there is no way back.
10. **Positions given as lists.** LeetCode passes `[0, 0]`: `shortest_steps(maze, [0, 0], (1, 3))` without the conversion raises `TypeError: unhashable type: 'list'`, and a list `target` silently returns -1 because `(1, 3) == [1, 3]` is False. Convert first: `start, target = tuple(start), tuple(target)`.
11. **`1` versus `"1"`.** Number of Islands stores the strings `"1"`/`"0"`; Max Area of Island and Number of Enclaves store the ints. `islands([[1, 1], [0, 1]])` returns `(0, 0)`, because `1 != "1"`.
12. **`seen` keyed on less than the whole state.** In BFS over states, `(cell, keys)` is the node, not `cell`. Keying on the cell blocks the walk from coming back with more keys.

### Edge cases to say out loud

Start equals target · start or target is a wall · target unreachable · no land at all · one big island · diagonal cells (not neighbours unless the problem says 8 directions) · nodes with no edges · nodes numbered from 1 · positions given as lists.

```python
assert shortest_steps(["S"], (0, 0), (0, 0)) == 0            # the start is the target
assert shortest_steps(["#."], (0, 0), (0, 1)) == -1          # you cannot start inside a wall
assert shortest_steps(["S#."], (0, 0), (0, 2)) == -1         # a wall cuts the only way
assert shortest_steps(maze, [0, 0], [1, 3]) == 4             # positions given as lists still work
assert islands(["000"]) == (0, 0)                             # no land: 0 islands, area 0
assert islands(["111", "111"]) == (1, 6)                      # one island covers everything
assert islands(["1", "0", "1"]) == (2, 1)                     # top and bottom rows do not touch
assert islands(["101", "010", "101"]) == (5, 1)               # diagonal cells are not neighbours
assert build_graph(3, []) == [[], [], []]                     # nodes without edges still exist
print("edge cases pass")
```

**Try it**
- Predict, then add: `assert shortest_steps(["S.", ".."], (0, 0), (1, 1)) == 2`.
- What should `islands(["1"])` return? Write the assert before running it (`(1, 1)`).
- Try 8 directions without touching the shared `DIRS`: copy `islands` as `islands8`, define `DIRS8 = DIRS + ((1, 1), (1, -1), (-1, 1), (-1, -1))` and loop over `DIRS8` inside it. `islands8(["101", "010", "101"])` is one island of 5.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Count / measure regions** | outer loop over every cell; count the launches; the flood returns its size | 200, 695, 733 |
| **Multi-source BFS** | push *every* source before the loop; a ring = one minute, or one step from the nearest source | 994, 286, 542 |
| **Return the path** | a `parent` map instead of `dist`; walk it back from the target | any shortest path |
| **8 directions, blocked start** | 8 entries in the direction list; check the start cell before the loop | 1091 |
| **Border-first** | flood from the border instead of asking every cell; what stays unmarked is enclosed | 130, 1020, 417 |
| **Two floods** | flood one island to collect it, then multi-source BFS from all its cells toward the other | 934 |
| **Copy a graph** | an `old -> new` dict is both `seen` and the lookup for neighbours | 133 |
| **Carry a label across edges** | a colour flips (bipartite) or a ratio multiplies (division) along each edge | 785, 886, 399 |
| **BFS over states** | the node is a string or a tuple; neighbours come from a function; `bfs_states` is unchanged | 752, 773, 127 |
| **BFS over augmented states** | node = (cell, extra); `seen` keys on the whole tuple | 864, 1293 |
| **BFS over groups** | expand a whole group (a bus route, all equal values) once, then never again | 815, 1345 |
| **Hard extras** | pruned branching · (node, visited mask) · every parent per layer | 854, 847, 126 |

**Multi-source BFS.** Rotting Oranges is worked line by line in [From Idea to Code](#s01). The same idea with distances instead of minutes is 01 Matrix: every 0 is a source, so all of them go into the queue at distance 0 before the loop starts. The first time the wave reaches a cell, it came from the *nearest* 0. Walls and Gates is the same code with the gates as the zeros.

```python
def update_matrix(mat):
    rows, cols = len(mat), len(mat[0])
    dist = [[-1] * cols for _ in range(rows)]       # STATE: -1 = not reached yet, so dist doubles as seen
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0                      # INIT: every source at distance 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for nr, nc in grid_neighbours(mat, r, c):
            if dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1       # RECORD on discovery: already final
                queue.append((nr, nc))              # STEP
    return dist                                     # RETURN


print(update_matrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]))   # [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
print(update_matrix([[0, 1, 1, 1, 0]]))                   # [[0, 1, 2, 1, 0]]
```

**Try it**
- Seed only the first 0: `update_matrix([[0, 1, 1, 1, 0]])` gives `[[0, 1, 2, 3, 4]]` instead of `[[0, 1, 2, 1, 0]]`. Every source has to start at the same moment.
- Swap `popleft()` for `pop()`: `[[0, 1, 1, 1, 0]]` comes out `[[0, 3, 2, 1, 0]]`. A stack hands out the newest cell, so a first visit is no longer the closest one.
- Count the pushes on a 30 × 30 grid with zeros on the diagonal: 900 with every zero as a source at once, 27,000 if you run one BFS per zero and keep the minimum.
- Picture one invisible super-source joined to every 0 by a free edge: this is a plain one-source BFS from it.

**Return the path.** Interviewers often follow up with "now show me the path". Remember who discovered each cell (`parent`), and walk those links back from the target. The `parent` map also serves as `seen`.

```python
def shortest_path(grid, start, target):
    parent = {start: None}                  # STATE + INIT: parent[cell] = the cell that discovered it; also "seen"
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == target:                   # RECORD: walk the parents back to the start
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]               # RETURN
        for nxt in grid_neighbours(grid, *cur):
            if grid[nxt[0]][nxt[1]] != "#" and nxt not in parent:
                parent[nxt] = cur           # STEP: remember who discovered nxt
                queue.append(nxt)
    return []


print(shortest_path(maze, (0, 0), (1, 3)))             # [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)]
print(shortest_path(["S#.", "##."], (0, 0), (1, 2)))   # []
```

**Try it**
- With `pop()` instead of `popleft()`, the open 3×4 grid `["....", "....", "...."]` from (0, 0) to (2, 0) returns an 8-move snake instead of the 2-move path.
- `len(shortest_path(maze, (0, 0), (1, 3))) - 1` is 4, the same number `shortest_steps` gives: a path of k + 1 cells has k moves.
- `shortest_path(maze, (0, 0), (0, 0))` is `[(0, 0)]`: a path with zero moves.

**Border-first.** "Can this cell reach the border?" asked for every cell repeats the same search. Ask the reverse once: *which cells can the border reach?* One flood from all border cells marks everything that escapes; what is left is enclosed. In Pacific Atlantic, water flows downhill, so from the ocean we walk *uphill*. The helper takes the step rule as a function, because that rule is the only thing that changes.

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

**Try it**
- Change `>=` to `>` in `uphill`: `(1, 4)` disappears from the answer. Its only way to the Pacific crosses `(1, 3)`, which has the same height.
- Print `len(pacific), len(atlantic)` inside `pacific_atlantic`: 16 and 16, with 7 cells in common.
- Number of Enclaves with the same helper: for `g = [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]`, flood from the border land cells with `lambda a, b: g[b[0]][b[1]] == 1`, then subtract the number reached from the total land: 3.
- `capture_surrounded(["XOX", "XOX", "XXX"])` captures nothing: that region touches the top edge.

**Copy a graph.** The copy needs one new node per old node, and every edge must connect *copies*. A dict `old -> new` answers "do I already have a copy of this node?" in O(1), which also makes it the visited set: that is what stops the traversal from going round a cycle forever.

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.neighbors = []


def clone_graph(node):
    if node is None:
        return None
    clones = {node: Node(node.val)}               # old -> new: the visited set AND the lookup table
    queue = deque([node])
    while queue:
        cur = queue.popleft()
        for nb in cur.neighbors:
            if nb not in clones:                  # first sighting: make its copy, expand it later
                clones[nb] = Node(nb.val)
                queue.append(nb)
            clones[cur].neighbors.append(clones[nb])   # wire copy -> copy, never copy -> original
    return clones[node]


a, b, c, d = Node(1), Node(2), Node(3), Node(4)             # the square 1-2-3-4-1
a.neighbors, b.neighbors, c.neighbors, d.neighbors = [b, d], [a, c], [b, d], [a, c]
copy = clone_graph(a)
print(copy.val, [n.val for n in copy.neighbors])           # 1 [2, 4]
print(copy is a, copy.neighbors[0] is b)                   # False False
print(copy.neighbors[0].neighbors[0] is copy)              # True  (the cycle closes on the copy)
```

**Try it**
- In the append line, use `nb` instead of `clones[nb]`: now `copy.neighbors[0] is b` prints True. The copy points back into the original graph.
- Delete `queue.append(nb)`: `copy.neighbors[0].neighbors` comes out empty. The copies get made, but only the start is ever expanded.
- Print `len(clones)` right before the `return`: 4 copies, although every node was reached twice.
- `clone_graph(None)` is `None`, and a lone `Node(7)` copies to a node with no neighbours.

**Carry a label across each edge.** Sometimes a node gets a value from the node that discovered it. In Is Graph Bipartite the label is a colour that *flips* across every edge; an edge whose two ends got the same colour closes an odd cycle. In Evaluate Division the label is a ratio that *multiplies* along the path: `a / b = 2` is an edge a → b worth 2 and an edge b → a worth 1/2.

```python
def is_bipartite(graph):
    color = {}                                # STATE: color[v] = 0 or 1; also "seen"
    for s in range(len(graph)):               # every component needs its own start
        if s in color:
            continue
        color[s] = 0                          # INIT
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in color:
                    color[v] = 1 - color[u]   # STEP: neighbours get the other colour
                    queue.append(v)
                elif color[v] == color[u]:
                    return False              # RECORD: an edge inside one colour = an odd cycle
    return True                               # RETURN


def calc_equation(equations, values, queries):
    graph = defaultdict(list)                 # a / b = k: edge a -> b worth k, edge b -> a worth 1 / k
    for (x, y), k in zip(equations, values):
        graph[x].append((y, k))
        graph[y].append((x, 1 / k))

    def ratio(src, dst):                      # DFS that carries src / node along the path
        if src not in graph or dst not in graph:
            return -1.0
        seen, stack = {src}, [(src, 1.0)]
        while stack:
            node, r = stack.pop()
            if node == dst:
                return r
            for nxt, k in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append((nxt, r * k))    # src / nxt = (src / node) * (node / nxt)
        return -1.0

    return [ratio(x, y) for x, y in queries]


print(is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]), is_bipartite([[1, 2], [0, 2], [0, 1]]))   # True False
print(is_bipartite([[1], [0], [3, 4], [2, 4], [2, 3]]))                                         # False
print(calc_equation([["a", "b"], ["b", "c"]], [2.0, 3.0],
                    [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]))             # [6.0, 0.5, -1.0, 1.0, -1.0]
```

**Try it**
- Start from node 0 only (drop the outer loop): the disconnected example `[[1], [0], [3, 4], [2, 4], [2, 3]]` now says True. The triangle 2-3-4 is never coloured.
- Print `color` at the end for the square `[[1, 3], [0, 2], [1, 3], [0, 2]]`: `{0: 0, 1: 1, 3: 1, 2: 0}`. Opposite corners share a colour.
- Forget the reverse edge (delete the `graph[y].append(...)` line): `b / a` comes back -1.0 instead of 0.5.
- Ask for `["c", "a"]`: 0.16666666666666666, found by walking c → b → a and multiplying 1/3 · 1/2.

**BFS over states.** Open the Lock already showed the recipe. Two more of the same shape: a board becomes a string (hashable, so it fits in `seen`), and a word's neighbours come from buckets like `"h*t"` instead of comparing every pair of words.

```python
TOUCH = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4), 4: (1, 3, 5), 5: (2, 4)}   # 2x3 board, by index


def sliding_puzzle(board):
    def slides(s):                                # swap the blank with each tile touching it
        z = s.index("0")
        for j in TOUCH[z]:
            t = list(s)
            t[z], t[j] = t[j], t[z]
            yield "".join(t)
    start = "".join(str(x) for row in board for x in row)       # a board becomes a hashable string
    return bfs_states([start], slides, lambda s: s == "123450")


def ladder_length(begin, end, words):
    buckets = defaultdict(list)                   # "h*t" -> every word that fits the pattern
    for w in words:
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)

    def one_letter_away(w):
        for i in range(len(w)):
            yield from buckets[w[:i] + "*" + w[i + 1:]]

    moves = bfs_states([begin], one_letter_away, lambda w: w == end)
    return moves + 1 if moves != -1 else 0        # the problem counts words, not moves


print(sliding_puzzle([[1, 2, 3], [4, 0, 5]]), sliding_puzzle([[4, 1, 2], [5, 0, 3]]),
      sliding_puzzle([[1, 2, 3], [5, 4, 0]]))                                        # 1 5 -1
print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))     # 5
```

**Try it**
- Add `print(w, end=" ")` as the first line of `one_letter_away` and rerun the cell: the ladder's line now starts `hit hot dot lot dog log`, the order in which BFS expands the words, ring by ring.
- In `bfs_states` (in the Open the Lock cell), print `len(seen)` just before `return -1` and rerun that cell; then call only `sliding_puzzle([[1, 2, 3], [5, 4, 0]])`: 360. Only half of the 720 boards can be reached from it.
- `ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"])` is 0: `"cog"` is in no bucket, so it is never generated.
- Predict `sliding_puzzle([[3, 2, 4], [1, 5, 0]])` before running it (14).

**BFS over augmented states.** When the same cell can be in different situations, the situation is part of the node (question 6 of the recipe): (cell, keys held) or (cell, eliminations left). Every move still costs one step, so BFS still works; `seen` just has to remember the whole tuple.

```python
def all_keys(grid):
    rows, cols = len(grid), len(grid[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "@")
    full = (1 << sum(ch.islower() for row in grid for ch in row)) - 1   # one bit per key

    def moves(state):
        r, c, keys = state
        for nr, nc in grid_neighbours(grid, r, c):
            ch = grid[nr][nc]
            bit = 1 << (ord(ch.lower()) - ord("a")) if ch.isalpha() else 0   # key a and lock A share a bit
            if ch == "#" or (ch.isupper() and not keys & bit):
                continue                          # a wall, or a lock whose key we do not hold
            yield nr, nc, (keys | bit if ch.islower() else keys)
    return bfs_states([(*start, 0)], moves, lambda s: s[2] == full)


def eliminate_obstacles(grid, k):
    rows, cols = len(grid), len(grid[0])

    def moves(state):
        r, c, left = state
        for nr, nc in grid_neighbours(grid, r, c):
            if left - grid[nr][nc] >= 0:          # stepping onto a 1 spends one elimination
                yield nr, nc, left - grid[nr][nc]
    return bfs_states([(0, 0, k)], moves, lambda s: (s[0], s[1]) == (rows - 1, cols - 1))


print(all_keys(["@.a..", "###.#", "b.A.B"]), all_keys(["@..aA", "..B#.", "....b"]), all_keys(["@Aa"]))   # 8 6 -1
print(eliminate_obstacles([[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]], 1))                 # 6
```

**Try it**
- In `all_keys`, pass `key=lambda s: s[:2]` to `bfs_states`, so `seen` remembers only the cell, and run `all_keys(["a.@A.b"])`: -1 instead of 7. After fetching `a` on the left, the walk must cross cells it has already seen to reach the lock.
- Run `eliminate_obstacles` on the same grid with `k = 0`: 10, the long way round. With `k = 7` the answer is 6, the straight-line distance: once the budget covers every wall on a shortest route, walls stop mattering.
- Count the states before you run: R × C cells and k keys give at most R · C · 2^k. For `["@.a..", "###.#", "b.A.B"]` that is 15 · 4 = 60.

**BFS over groups.** Sometimes one move reaches a whole group at once: every stop of a bus route, every index holding the same value. The group is the expensive part, so expand each group *once*. Bus Routes counts buses, so the nodes are routes, reached through a stop → routes index.

```python
def num_buses(routes, source, target):
    if source == target:
        return 0
    routes_at = defaultdict(list)                 # stop -> every route through it
    for i, route in enumerate(routes):
        for stop in route:
            routes_at[stop].append(i)
    queue = deque((i, 1) for i in routes_at[source])   # boarding any bus at source = 1 bus
    boarded, expanded = set(routes_at[source]), {source}
    while queue:
        i, buses = queue.popleft()
        for stop in routes[i]:
            if stop == target:
                return buses
            if stop in expanded:
                continue
            expanded.add(stop)                    # look at each stop's routes once
            for j in routes_at[stop]:
                if j not in boarded:
                    boarded.add(j)                # board each route once
                    queue.append((j, buses + 1))
    return -1


print(num_buses([[1, 2, 7], [3, 6, 7]], 1, 6))                                 # 2
print(num_buses([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12))    # -1
```

**Try it**
- Delete `if source == target: return 0`: `num_buses([[1, 2, 7], [3, 6, 7]], 1, 1)` returns 1, a bus ride you never needed.
- Print `i, buses` after each `popleft()` for the first example: route 0 with 1 bus, then route 1 with 2 buses. Stops are never counted.
- `num_buses([[1, 2, 3, 4, 5, 6]], 1, 6)` is 1: one ride covers five stops, because an edge is a bus, not a stop.

#### Hard extras (after the core is automatic)

Three hard problems built from the same parts. **K-Similar Strings** is BFS over strings that only branches on swaps that put the right letter into the first wrong slot. That loses nothing: in any best sequence, the swap that finally fills slot i can be moved to the front, because swaps that do not touch slot i commute with it. **Shortest Path Visiting All Nodes** is BFS over (node, visited mask), with every node as a start. **Jump Game IV** deletes a value's bucket of equal indexes the first time it is used, so each bucket is read once.

```python
def k_similar(s1, s2):
    def fix_first_mismatch(s):                    # only swaps that put the right letter at the first bad slot
        i = next(k for k in range(len(s)) if s[k] != s2[k])
        for j in range(i + 1, len(s)):
            if s[j] == s2[i] and s[j] != s2[j]:
                yield s[:i] + s[j] + s[i + 1:j] + s[i] + s[j + 1:]
    return bfs_states([s1], fix_first_mismatch, lambda s: s == s2)


def visit_all_nodes(graph):
    full = (1 << len(graph)) - 1
    starts = [(i, 1 << i) for i in range(len(graph))]     # start anywhere: every node is a source
    walk = lambda s: ((v, s[1] | (1 << v)) for v in graph[s[0]])
    return bfs_states(starts, walk, lambda s: s[1] == full)


def min_jumps(arr):
    same = defaultdict(list)                      # value -> every index holding it
    for i, x in enumerate(arr):
        same[x].append(i)
    dist, queue = {0: 0}, deque([0])
    while queue:
        i = queue.popleft()
        if i == len(arr) - 1:
            return dist[i]
        for j in [i - 1, i + 1] + same.pop(arr[i], []):   # a value's bucket is used once, then gone
            if 0 <= j < len(arr) and j not in dist:
                dist[j] = dist[i] + 1
                queue.append(j)


print(k_similar("abac", "baca"), k_similar("abc", "bca"))                                  # 2 2
print(visit_all_nodes([[1, 2, 3], [0], [0], [0]]))                                         # 4
print(min_jumps([100, -23, -23, 404, 100, 23, 23, 23, 3, 404]), min_jumps([7]), min_jumps([7, 6, 9, 6, 9, 6, 9, 7]))   # 3 0 1
```

**Try it**
- Replace `fix_first_mismatch` with a generator of every swap of two different letters: `k_similar("abcdef", "bcdefa")` still says 5, but BFS now pops 720 strings instead of 6.
- In `visit_all_nodes`, start from node 0 only (`starts = [(0, 1)]`): 5 instead of 4. Starting at a leaf is shorter, which is why every node is a source.
- In `min_jumps`, keep the buckets (`same[arr[i]]` instead of `same.pop(arr[i], [])`) and time both on `[7] * 10_000 + [8]`. Both answer 2, but the kept-bucket version re-reads 10,000 equal indexes on every pop and takes seconds instead of milliseconds.

**Word Ladder II, in words:** run the BFS ring by ring and record, for every word, *all* the words of the previous ring that reach it (a parents map). Remove a ring's words from the dictionary only after the whole ring is done, so that two parents in the same ring can both register. Stop after the ring that contains `endWord`, then walk the parents map backwards from `endWord` to list every path.

### Say it in the interview

Regions:

> "Each land cell is a node joined to its land neighbours, so an island is a connected component. A fresh search from every cell re-walks each island, O((mn)²); with one shared `seen` every cell is pushed once, O(mn). Unseen land launches a new flood: one more island. I flood with an explicit stack so a big island can't hit the recursion limit."

Fewest moves:

> "Every move costs 1, so BFS. A cell at distance k + 1 can only be discovered from a cell at distance k, and ring k leaves the queue before ring k + 1, so the first time the target is popped its distance is minimal. I mark on enqueue, so each cell enters once: O(mn)."

Point at the `seen.add` right before the `append`, the bounds check with both halves, and the line where you record. For a state search, answer the six questions out loud before writing any code. Follow-ups to expect: return the path (a parent map), 8 directions (a longer direction list), "don't modify the input" (a `seen` set instead of sinking cells), recursion depth (an explicit stack), and a Word Ladder that is too slow (bidirectional BFS: always expand the smaller frontier).

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| 01 Matrix | `graphs/zero_one_matrix.py` | multi-source BFS from every 0; a cell's first visit is its distance |
| Bus Routes | `graphs/bus_routes.py` | BFS over routes, not stops: a stop → routes index; board each route once, expand each stop once |
| Clone Graph | `graphs/clone_graph.py` · `practice/simple/42_clone_graph.py` | one traversal; the old → new dict is both the visited set and the neighbour lookup |
| Flood Fill | `graphs/flood_fill.py` | recolouring is the visited mark; return early if the new colour equals the old one |
| Jump Game IV | `graphs/jump_game_iv.py` | BFS on indexes; a value's bucket of equal indexes is used once, then deleted |
| K-Similar Strings | `graphs/k_similar_strings.py` | BFS over strings; branch only on swaps that fix the first mismatched slot |
| Max Area of Island | `graphs/max_area_of_island.py` | flood each island once from its first cell; the flood returns its size |
| Number of Enclaves | `graphs/number_of_enclaves.py` | sink every land cell the border can reach; count the land left |
| Number of Islands | `graphs/number_of_islands.py` · `practice/simple/41_number_of_islands.py` | count how many times the scan has to start a new flood |
| Pacific Atlantic Water Flow | `graphs/pacific_atlantic_water_flow.py` | climb uphill from each ocean's border; answer = cells both floods reach |
| Rotting Oranges | `graphs/rotting_oranges.py` · `practice/simple/44_rotting_oranges.py` | multi-source BFS from all rotten oranges; one ring = one minute; -1 if fresh ones remain |
| Shortest Path in a Grid with Obstacles Elimination | `graphs/shortest_path_in_a_grid_with_obstacles_elimination.py` | state = (row, col, eliminations left); more budget at the same cell is a different state |
| Shortest Path to Get All Keys | `graphs/shortest_path_to_get_all_keys.py` | state = (row, col, key bitmask); the goal is any cell with the full mask |
| Shortest Path Visiting All Nodes | `graphs/shortest_path_visiting_all_nodes.py` | state = (node, visited mask); seed all n starts; the first full mask wins |
| Sliding Puzzle | `graphs/sliding_puzzle.py` | the board as a 6-char string; neighbours = swap the blank with a touching index |
| Surrounded Regions | `graphs/surrounded_regions.py` | mark the O's reachable from the border as safe; flip every other O |
| Walls and Gates | `graphs/walls_and_gates.py` | multi-source BFS from all gates; the first write into a room is final, so INF itself means "unvisited" |
| Word Ladder | `graphs/word_ladder.py` | BFS on words; wildcard buckets ("h*t") list neighbours without comparing all pairs |
| Word Ladder II | `graphs/word_ladder_ii.py` | BFS by rings keeping every parent from the previous ring; backtrack from endWord |

### Self-check

1. Why mark a node as seen when you push it, not when you pop it?
<details><summary>Answer</summary>Between being pushed and being popped, a node can be discovered again by other neighbours. If it is only marked at pop time, every discovery pushes another copy: the queue grows, work repeats, and anything counted per pop (like an area) is counted more than once. Marking on push lets each node into the container exactly once. (Marking on pop also works if you skip nodes that are already marked; that is the form Dijkstra needs.)</details>

2. Why does BFS give the fewest moves while DFS does not?
<details><summary>Answer</summary>The queue only ever holds distances <code>d</code> and <code>d + 1</code>, in that order, so nodes come out in order of distance; when the target first comes out, no shorter path can still be waiting. DFS follows whichever corridor it tried first, so it reaches the target along <em>some</em> path, not necessarily a short one.</details>

3. In Shortest Path to Get All Keys, why can't <code>seen</code> hold just the cell?
<details><summary>Answer</summary>The same cell with more keys is a different situation: locks that were walls are now open. A walk often has to come back over cells it has already crossed, for example to fetch a key behind it. With cell-only <code>seen</code>, <code>["a.@A.b"]</code> answers -1 instead of 7.</details>

4. Why should the move count never be part of the node?
<details><summary>Answer</summary>The queue order already tells you the distance (or the distance rides along beside the state). With the count inside, the same cell reached after 3 moves and after 5 moves are two different nodes, so <code>seen</code> cannot merge them and the search re-explores places it has already been: on an open 6 × 6 grid, 111 pops instead of 36.</details>
