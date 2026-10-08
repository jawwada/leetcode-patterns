## Graphs I: BFS & DFS

> A graph is just *things* (nodes) and *you can get from this one to that one* (edges). BFS spreads from the start like a ripple in a pond, one ring of equal distance at a time; DFS runs down one corridor to its end before backing up. Both visit every node they can reach exactly once, because they mark a node the moment they discover it.

**Reach for it when** the problem talks about cells connected up, down, left and right, islands or regions, or something spreading in rounds: rot, fire, a signal. Reach for it too when it asks for the fewest steps, moves, jumps or transformations and every move costs the same, when it asks "can I reach", when a structure with cycles must be copied, or when a situation changes one move at a time: a board, a word, a lock.

### The picture

Half of every graph problem is one sentence: *what is a node, and what is an edge?* Once you can say it, the code is one of two loops.

In a grid of land and water, a node is a cell `(r, c)` and an edge is a step up, down, left or right onto land, so "how many groups?" is a flood fill, by DFS or by BFS. When rot spreads every minute, an edge is one minute of spreading, and "when is the last cell reached?" is a BFS from every rotten cell at once.

The node is whatever changes from one move to the next. When a word changes one letter at a time, the node is a word, joined to every word one letter away. When tiles slide into a gap, it is the whole board as a string; when keys open locks, a cell with the keys in hand; when the question counts buses, a bus route, joined to every route that shares a stop. All of them ask for the fewest moves, so all of them are BFS.

A graph you must deep-copy is walked once, with a map from every old node to its copy. Weighted edges are [Graphs III](#s19); "in what order?" and "are these connected?" are [Graphs II](#s18).

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

**Why it is fast.** The brute force in most of these problems starts a fresh search from every cell. On a grid of one big island, every search re-walks the whole island, so the work is O((rows · cols)²). One `seen` set shared by all the searches is the whole speed-up.

With a shared `seen`, every node goes into the container at most once, because it is marked the moment it goes in, and every edge is looked at once from each end. A traversal therefore costs O(V + E), which on a grid is O(rows · cols): each cell is pushed once and looks at its four neighbours once.

### From idea to code

**The idea in one sentence:** *put the start in a container and mark it; then repeatedly take one node out, and put in every neighbour you have never seen, marking it as it goes in.*

A queue, oldest out first, makes that BFS. A stack, newest out first, makes it DFS, and that is all a flood fill needs. Only a few jobs need the real DFS tree, with its "on the current path" information: cycle colours, topological order and bridges, all in [Graphs II](#s18). Those use recursion.

The seven decisions for the fewest-steps BFS read as one story. The **state** is a `deque` frontier and a `dist` map, and `dist` doubles as `seen`. By **definition**, `dist[v]` is the fewest moves from the start to `v`, and the queue holds the discovered cells not expanded yet. The **invariant**, true at the end of every step, is that the queue holds at most two distances, the `d`s in front of the `d + 1`s, and that every cell in `dist` is waiting in the queue or already expanded, so it entered exactly once.

A **step** pops a cell and gives every neighbour that is on the board, passable and new the distance `d + 1` as it joins the queue. That is the **record** too: the distance is written at discovery, and it is already final. **Init** puts every source in the queue and in `dist` at distance 0, and the **return** is the target's distance when it is *popped*, or -1 if the queue runs dry.

For counting and measuring regions the story changes little. The state is a `seen` set of the cells already pushed, a stack for the current flood, and two counters: `count`, the floods started so far, and `best`, the largest area. The invariant is that every cell in `seen` is waiting in the stack or already expanded, so it enters the stack exactly once, and that a finished flood has put its whole region into `seen`.

A step pops a cell, then marks and pushes every new land neighbour. The outer loop records `count += 1` when it finds unseen land, and the flood records `best = max(best, area)` when it ends. Everything starts empty with `count = best = 0`, and the return is `count` and `best`.

The sentences you say map onto the lines you type. "The four cells around me" is `for dr, dc in DIRS: nr, nc = r + dr, c + dc`, and "still on the board" is `0 <= nr < rows and 0 <= nc < cols`. "Never discovered" is `(nr, nc) not in seen`, or `not in dist`.

"Mark it as I discover it" is `seen.add(nxt)` on the line just before `queue.append(nxt)`. "The oldest discovery next" is `queue.popleft()`, which makes it BFS; "the newest discovery next" is `stack.pop()`, which makes it DFS. "One ring further out" is `dist[nxt] = dist[cur] + 1`, and "a whole ring at once" is `for _ in range(len(queue)):`. "A new island starts here" is an outer loop over every cell with `if land and not seen: count += 1`.

Turn the story into a graph before you type. Six questions decide every line of a BFS:

1. **Node**: what changes from one move to the next? A cell `(r, c)`, a word, a board string or `(r, c, keys)`; whatever it is goes into `seen`, so it must be hashable, a tuple or a string.
2. **Edge**: what is one legal move? Step onto a free cell, change one letter, turn one wheel; it becomes `def neighbours(node): yield ...`.
3. **Cost**: does every move cost the same? Yes means BFS; only 0 or 1 means a deque, the 0-1 BFS; any w ≥ 0 means a heap, in [Graphs III](#s19).
4. **Start**: one source, or many at once? The entrance, or every rotten orange, or every 0; all of them go into the queue and into `seen` at distance 0.
5. **Goal**: what ends the search? Reaching a cell, holding every key, or running to the end; `if is_goal(node): return d`, checked when the node is *popped*.
6. **Extra**: can two arrivals at the same place have different futures? More keys, more budget left, a different set of visited nodes; then the extra goes into the node, and places × extras must fit in memory, up to about 10⁶ states.

Never put the move count itself in the node: the queue order already carries it, and with it inside, `seen` can no longer merge two arrivals at the same place. On an open 6 × 6 grid, a BFS from corner to corner pops 36 states when the node is the cell, and 111 when it is `(r, c, moves)`.

Step zero is listing a node's neighbours. From an edge list you build an adjacency list once: `graph[u]` holds every node one edge away from `u`, and an undirected edge is written into both lists. For the six nodes and five edges below, node 3 ends up next to 1, 2 and 4.

On a grid you store no edges at all. The neighbours of `(r, c)` are the four cells around it that are still on the board, computed on the fly, and the corner (0, 0) of a 3 × 3 grid has only two of them.

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
- Feed 1-indexed edges: `build_graph(3, [(1, 2), (2, 3)])` raises `IndexError` (there is no `graph[3]`). When nodes are numbered from 1, allocate `n + 1` lists.
- An adjacency matrix becomes lists in one line: for `M = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]`, `[[j for j, x in enumerate(row) if x] for row in M]` gives `[[1, 2], [0], [0]]`.

The plain shortest-path question comes first, because every other BFS is this loop with a different node. A maze holds walls `#`, and you want the fewest moves from `start` to `target`, or -1 when no route exists; in the maze below, the corner `S` reaches (1, 3) in 4 moves.

Two moments inside the loop are different on purpose. A cell is marked and given its distance when it is *pushed*, because it was discovered from the closest ring, so that distance is already final. It is compared with the target when it is *popped*, because popping is when it is the closest cell not expanded yet.

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

BFS can know a distance in three ways; pick one per problem and never mix them. A `dist` map, `dist = {start: 0}` and then `dist[nxt] = dist[cur] + 1`, gives every node its distance and doubles as `seen`. 01 Matrix, which asks every cell for its distance to the nearest 0, wants exactly that.

The distance can instead ride in the queue, `queue.append((nxt, d + 1))`, which suits a state search that only needs the goal's distance, like the lock below. Or you process whole rings, `for _ in range(len(queue)):` and then `steps += 1`, when the answer is a number of rounds: Rotting Oranges asks how many minutes pass until no fresh orange is left, and one ring is one minute.

A state search is the same loop with a richer node, and Open the Lock shows it in its purest form. A lock has four wheels showing `"0000"`; one move turns one wheel one click up or down; some combinations are dead ends you must never land on; and you want the fewest moves to the target. With the dead ends below, `"0202"` takes 6 moves.

The six answers: the node is the 4-digit string, an edge turns one wheel one click, every move costs 1, the start is `"0000"`, the goal is the target, and nothing extra matters, because a dead end is simply a node you never enter. The loop itself never changes, so it is written once as `bfs_states`, and the six answers go in as arguments.

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

The DFS template answers the other big question, how many regions there are and how big. Number of Islands counts the groups of `"1"` cells joined up, down, left or right; the sea below has 3 islands. Max Area of Island asks for the biggest one, 4 cells here.

The outer loop is what turns "flood one region" into "count the regions": every cell gets a chance to start a flood, and only unseen land does. A cell is marked when it is pushed, so it can never be pushed twice, and it is counted when it is popped. The recursive version does the same job on the call stack: it checks a cell when it arrives there, then visits the four neighbours.

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

The rings are the whole argument for BFS, so watch them form. Each printed line is one ring of the search through the maze above, and at the end the grid shows every cell's distance from `S`, with `?` for a cell the wave never reached.

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

1. **Marking `seen` when you pop instead of when you push.** Between its first push and its pop, a node is pushed again by every other neighbour that reaches it, so the queue fills with copies, and anything counted per pop is counted more than once: a 2×2 block of land gets area 5. The other correct form is to mark on pop *and skip a node that is already marked*: copies still enter the queue, but none is expanded twice. Dijkstra must use that form ([Graphs III](#s19)).
2. **Half a bounds check.** Without `0 <=`, Python reads `grid[-1]` as the last row instead of failing, so the top edge silently touches the bottom edge: `islands(["1", "0", "1"])` reports `(2, 2)` instead of `(2, 1)`. Always write `0 <= nr < rows`.
3. **Forgetting to mark the start.** Without `seen.add((r, c))` before the flood, the start is pushed again by its own neighbour: `islands(["11"])` returns `(1, 3)`.
4. **One search on a disconnected graph.** With `build_graph(4, [(0, 1), (2, 3)])`, a search from 0 reaches only {0, 1}. Counting or visiting everything needs the outer loop that tries every node as a start.
5. **DFS for "fewest steps".** DFS finds *a* path, not the shortest: on an open 3×4 grid a stack-based search reports 8 moves from (0, 0) to (2, 0), BFS reports 2.
6. **Counting pops instead of rings.** When the answer is a number of rounds, drop the ring loop (or put `minutes += 1` inside it) and you count pops: the first Rotting Oranges grid answers 6 instead of 4. Finish the whole ring, then add one.
7. **Deep recursion.** A recursive flood of a 300×300 island can need 90,000 nested calls; Python stops at about 1,000. Use an explicit stack (or BFS) on big grids, and say so.
8. **Flood fill with the new colour equal to the old one.** A fill that uses the paint as its "seen" mark never ends on `[[1, 1]]` from (0, 0) with colour 1: painting changes nothing, so the two cells keep pushing each other. Return early when the colours are equal.
9. **An undirected edge stored once.** `build_graph(2, [(0, 1)], directed=True)[1]` is `[]`: from node 1 there is no way back.
10. **Positions given as lists.** LeetCode passes `[0, 0]`: `shortest_steps(maze, [0, 0], (1, 3))` without the conversion raises `TypeError: unhashable type: 'list'`, and a list `target` silently returns -1 because `(1, 3) == [1, 3]` is False. Convert first: `start, target = tuple(start), tuple(target)`.
11. **`1` versus `"1"`.** Number of Islands stores the strings `"1"`/`"0"`; Max Area of Island and Number of Enclaves, which counts the land cells that cannot walk off the grid, store the ints. `islands([[1, 1], [0, 1]])` returns `(0, 0)`, because `1 != "1"`.
12. **`seen` keyed on less than the whole state.** In BFS over states, `(cell, keys)` is the node, not `cell`. Shortest Path to Get All Keys asks for the fewest moves to collect every key when each lock needs its key; with `seen` keyed on the cell, `["a.@A.b"]` answers -1 instead of 7, because the walk must come back over cells it has already crossed.

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

Every variation below keeps the loop and changes one thing: where the search starts, what a node is, or what rides along with it. The table is the overview; each variation then gets its own paragraph and, for the important ones, its code.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Count / measure regions** | outer loop over every cell; count the launches; the flood returns its size | Number of Islands (200), Max Area of Island (695), Flood Fill (733) |
| **Multi-source BFS** | push *every* source before the loop; a ring = one minute, or one step from the nearest source | Rotting Oranges (994), Walls and Gates (286), 01 Matrix (542) |
| **Return the path** | a `parent` map instead of `dist`; walk it back from the target | any shortest path |
| **8 directions, blocked start** | 8 entries in the direction list; check the start cell before the loop | Shortest Path in Binary Matrix (1091) |
| **Border-first** | flood from the border instead of asking every cell; what stays unmarked is enclosed | Surrounded Regions (130), Number of Enclaves (1020), Pacific Atlantic Water Flow (417) |
| **Two floods** | flood one island to collect it, then multi-source BFS from all its cells toward the other | Shortest Bridge (934) |
| **Copy a graph** | an `old -> new` dict is both `seen` and the lookup for neighbours | Clone Graph (133) |
| **Carry a label across edges** | a colour flips (bipartite) or a ratio multiplies (division) along each edge | Is Graph Bipartite (785), Possible Bipartition (886), Evaluate Division (399) |
| **BFS over states** | the node is a string or a tuple; neighbours come from a function; `bfs_states` is unchanged | Open the Lock (752), Word Ladder (127) |
| **BFS over augmented states** | node = (cell, extra); `seen` keys on the whole tuple | Shortest Path in a Grid with Obstacles Elimination (1293) |
| *Second pass:* **richer nodes** | the node is a whole board, (cell, keys held) or (node, visited mask) | Sliding Puzzle (773), Shortest Path to Get All Keys (864), Shortest Path Visiting All Nodes (847) |
| *Second pass:* **BFS over groups** | expand a whole group (a bus route, all equal values) once, then never again | Bus Routes (815), Jump Game IV (1345) |
| *Second pass:* **pruned branching** | branch only on moves that fix the first mismatch | K-Similar Strings (854) |
| *Second pass:* **every shortest path** | keep every parent from the previous ring; walk back from the end | Word Ladder II (126) |

Flood Fill is the smallest member of the first row: recolour the start pixel and every pixel of the same colour connected to it, so `[[1, 1, 1], [1, 1, 0], [1, 0, 1]]` painted with 2 from the middle becomes `[[2, 2, 2], [2, 2, 0], [2, 0, 1]]`. The paint itself serves as the visited mark, which is why trap 8 exists.

Shortest Path in Binary Matrix is the template with 8 directions and a start cell that may itself be blocked: the fewest cells on a path of 0s from the top-left to the bottom-right corner, moving in any of 8 directions, or -1.

The multi-source variation comes first because it changes only the first line of the template. Rotting Oranges is worked line by line in [From Idea to Code](#s01). The same idea with distances instead of minutes is 01 Matrix: for every cell, how far is the nearest 0, so `[[0, 1, 1, 1, 0]]` becomes `[[0, 1, 2, 1, 0]]`.

Every 0 is a source, so all of them go into the queue at distance 0 before the loop starts, and the first time the wave reaches a cell it came from the *nearest* 0. Walls and Gates asks for the distance from every empty room to its nearest gate, with walls in the way; it is the same code with the gates as the zeros, and a room the wave never reaches keeps its starting value.

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
- Print `list(queue)` right after the seeding loops for the first matrix: all five zeros wait at distance 0, as if one invisible super-source, joined to every 0 by a free edge, had just been expanded. Multi-source BFS is a plain BFS from that super-source.

Interviewers often follow the distance with "now show me the path", so the parent map comes next. Remember who discovered each cell in `parent`, and walk those links back from the target; in the maze the route from `S` to (1, 3) runs along the top row, then down and one step right, five cells in all. The `parent` map also serves as `seen`, because a cell has a parent exactly when it has been discovered.

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

The next two variations change where the flood starts. Surrounded Regions asks you to flip every region of `O`s that does not touch the border, so the board `["XXXX", "XOOX", "XXOX", "XOXX"]` keeps only its bottom `O`.

"Can this `O` reach the border?" asked for every cell repeats the same search. Asked the other way round, *which cells can the border reach?*, it is one flood from all border cells, and whatever stays unmarked is enclosed. Number of Enclaves asks the same question for land cells, counting the ones that cannot walk off the grid.

Pacific Atlantic Water Flow asks which cells can send water to both oceans, with the Pacific along the top and left edges and the Atlantic along the bottom and right, when water only flows to a neighbour that is equally high or lower. On `[[1, 2], [4, 3]]` three cells manage it: (0, 1), (1, 0) and (1, 1).

From each ocean we walk *uphill*, and the cells both floods reach are the answer. The helper takes the step rule as a function, because that rule is the only thing that changes between the two problems.

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

Shortest Bridge joins the two ideas above. A grid holds exactly two islands, and you want the fewest water cells to flip so that they touch. Flood one island with the DFS template to collect its cells, then run a multi-source BFS from all of them at once; the number of water rings the wave crosses before it first touches the other island is the answer.

Copying a graph is a traversal too, and the only new question is what `seen` should be. Clone Graph hands you one node of an undirected graph, each node holding a value and a neighbour list, and asks for a deep copy: the square 1-2-3-4-1 below must come back as four fresh nodes wired into the same square.

The copy needs one new node per old node, and every edge must connect *copies*. A dict `old -> new` answers "do I already have a copy of this node?" in O(1), which also makes it the visited set, and that is what stops the traversal from going round the cycle forever.

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.neighbors = []                       # LeetCode's attribute name, American spelling


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
clone = clone_graph(a)
print(clone.val, [n.val for n in clone.neighbors])         # 1 [2, 4]
print(clone is a, clone.neighbors[0] is b)                 # False False
print(clone.neighbors[0].neighbors[0] is clone)            # True  (the cycle closes on the copy)
```

**Try it**
- In the append line, use `nb` instead of `clones[nb]`: now `clone.neighbors[0] is b` prints True. The copy points back into the original graph.
- Delete `queue.append(nb)`: the last line now raises `IndexError`, because `clone.neighbors[0].neighbors` is empty. The copies get made, but only the start is ever expanded.
- Print `len(clones)` right before the `return`: 4 copies, although every node was reached twice.
- `clone_graph(None)` is `None`, and a lone `Node(7)` copies to a node with no neighbours.

Sometimes a node receives a value from the node that discovered it, and the traversal carries that label along every edge. Is Graph Bipartite asks whether the nodes can be split into two camps so that every edge joins the camps; Possible Bipartition is the same question with "dislikes" as the edges.

Here the label is a colour that *flips* across every edge. An edge whose two ends got the same colour closes an odd cycle, so the answer is False.

Evaluate Division gives facts like `a / b = 2.0` and `b / c = 3.0` and asks for ratios like `a / c`, which is 6.0. The label is a ratio that *multiplies* along the path: `a / b = 2` is an edge a → b worth 2 and an edge b → a worth 1/2.

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

Open the Lock already showed BFS over states, and Word Ladder has exactly its shape. It changes one letter at a time through a word list and asks how many words the shortest chain from `"hit"` to `"cog"` has: 5, along hit, hot, dot, dog, cog. A word's neighbours come from buckets like `"h*t"`, one per word and blanked position, instead of comparing every pair of words, and `bfs_states` does the rest. Without `"cog"` in the list no ladder exists, and the answer is 0.

```python
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


print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))     # 5
print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]))            # 0
```

**Try it**
- Add `print(w, end=" ")` as the first line of `one_letter_away` and rerun the cell: the first line now starts `hit hot dot lot dog log`, the order in which BFS expands the words, ring by ring.
- Return `moves` instead of `moves + 1`: the first ladder says 4. A chain of 5 words has 4 moves, and the problem counts words.
- Print `buckets["*ot"]` inside `ladder_length`: `['hot', 'dot', 'lot']`. Every pair in one bucket is one letter apart, so the bucket lists those neighbours without comparing a single pair of words.
- Put `"hit"` itself into the first word list and rerun: still 5. The start's own buckets now hand `"hit"` back, and `seen` already holds it, so nothing changes.

When the same cell can be in different situations, the situation becomes part of the node: question 6 of the recipe. Shortest Path in a Grid with Obstacles Elimination lets you break at most k walls between the top-left and bottom-right corners and asks for the fewest steps: the 5 × 3 grid below takes 6 with k = 1, and -1 comes back when k is too small. The node is (cell, eliminations left), and since every move still costs one step, `bfs_states` works unchanged, with `seen` keyed on the whole tuple.

```python
def eliminate_obstacles(grid, k):
    rows, cols = len(grid), len(grid[0])

    def moves(state):
        r, c, left = state
        for nr, nc in grid_neighbours(grid, r, c):
            if left - grid[nr][nc] >= 0:          # stepping onto a 1 spends one elimination
                yield nr, nc, left - grid[nr][nc]
    return bfs_states([(0, 0, k)], moves, lambda s: (s[0], s[1]) == (rows - 1, cols - 1))


print(eliminate_obstacles([[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]], 1))   # 6
print(eliminate_obstacles([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 1))                        # -1
```

**Try it**
- Run the first grid with `k = 0`: 10, the long way round. One elimination already buys the straight route, so any k ≥ 1 gives 6.
- Pass `key=lambda s: s[:2]` to `bfs_states`, so `seen` remembers only the cell, and run `eliminate_obstacles([[0, 0, 1, 1], [1, 0, 1, 0]], 1)`: -1 instead of 4. Cell (1, 1) is first reached through the wall at (1, 0), with the budget spent, and that arrival blocks the one through (0, 1) that still has it.
- Before running, bound the work: R · C cells times k + 1 budgets, 5 · 3 · 2 = 30 states for the first grid. Then print `len(seen)` in `bfs_states` just before `return moves` and rerun both cells: the first grid queued 22 states.

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Three of them only need a richer node for `bfs_states`. Sliding Puzzle holds the tiles 1 to 5 and one blank on a 2 × 3 board; one move slides a tile into the blank, and it asks for the fewest moves to reach `123` over `450`, or -1 when the board can never get there: `[[1, 2, 3], [4, 0, 5]]` needs 1 move. The node is the whole board written as a string, which is hashable, so it fits in `seen`.

Shortest Path to Get All Keys has a start `@`, walls `#`, keys as lowercase letters and locks as the matching uppercase letters, and asks for the fewest moves to collect every key: `["@.a..", "###.#", "b.A.B"]` takes 8. A lock can only be crossed with its key in hand, so the node is (cell, keys held), with the keys as a bitmask.

Shortest Path Visiting All Nodes asks for the shortest walk that visits every node of a small graph, starting anywhere and revisiting freely: the star `[[1, 2, 3], [0], [0], [0]]` takes 4 steps. The node is (node, visited mask), and every node is a start, so all of them enter the queue at distance 0.

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


def visit_all_nodes(graph):
    full = (1 << len(graph)) - 1
    starts = [(i, 1 << i) for i in range(len(graph))]     # start anywhere: every node is a source
    walk = lambda s: ((v, s[1] | (1 << v)) for v in graph[s[0]])
    return bfs_states(starts, walk, lambda s: s[1] == full)


print(sliding_puzzle([[1, 2, 3], [4, 0, 5]]), sliding_puzzle([[4, 1, 2], [5, 0, 3]]),
      sliding_puzzle([[1, 2, 3], [5, 4, 0]]))                                        # 1 5 -1
print(all_keys(["@.a..", "###.#", "b.A.B"]), all_keys(["@..aA", "..B#.", "....b"]), all_keys(["@Aa"]))   # 8 6 -1
print(visit_all_nodes([[1, 2, 3], [0], [0], [0]]))                                 # 4
```

**Try it**
- In `bfs_states` (in the Open the Lock cell), print `len(seen)` just before `return -1` and rerun that cell; then call only `sliding_puzzle([[1, 2, 3], [5, 4, 0]])`: 360. Only half of the 720 boards can be reached from it.
- Predict `sliding_puzzle([[3, 2, 4], [1, 5, 0]])` before running it (14).
- In `all_keys`, pass `key=lambda s: s[:2]` to `bfs_states`, so `seen` remembers only the cell, and run `all_keys(["a.@A.b"])`: -1 instead of 7. After fetching `a` on the left, the walk must cross cells it has already seen to reach the lock.
- In `visit_all_nodes`, start from node 0 only (`starts = [(0, 1)]`): 5 instead of 4. Starting at a leaf is shorter, which is why every node is a source.

Sometimes one move reaches a whole group at once, every stop of a bus route or every index holding the same value. The group is the expensive part, so each group is expanded *once*.

Bus Routes gives each bus as the loop of stops it drives, and asks for the fewest buses from a source stop to a target stop; with routes `[1, 2, 7]` and `[3, 6, 7]`, stop 1 reaches stop 6 on 2 buses. The problem counts buses, so the nodes are routes, reached through a stop → routes index.

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

Jump Game IV is the same idea on an array. From index i you may jump to i − 1, i + 1 or any index holding the same value, and it asks for the fewest jumps from the first index to the last: 3 for `[100, -23, -23, 404, 100, 23, 23, 23, 3, 404]`. Run BFS over indexes and delete a value's bucket of equal indexes the first time it is used, so a long run of equal values is read once instead of on every pop.

K-Similar Strings asks for the fewest swaps of two letters that turn one anagram into another: `"abac"` becomes `"baca"` in 2. It is BFS over strings that branches only on swaps putting the right letter into the first wrong slot, and some shortest sequence always begins with such a swap, so the pruning loses nothing.

Word Ladder II asks for *every* shortest ladder, not just its length, so the ring structure has to be kept. Run the BFS ring by ring and record, for every word, *all* the words of the previous ring that reach it, a parents map.

Remove a ring's words from the dictionary only after the whole ring is done, so that two parents in the same ring can both register. Stop after the ring that contains `endWord`, then walk the parents map backwards from `endWord` to list every path.

### Say it in the interview

Regions:

> "Each land cell is a node joined to its land neighbours, so an island is a connected component. A fresh search from every cell re-walks each island, O((mn)²); with one shared `seen` every cell is pushed once, O(mn). Unseen land launches a new flood: one more island. I flood with an explicit stack so a big island can't hit the recursion limit."

Fewest moves:

> "Every move costs 1, so BFS. A cell at distance k + 1 can only be discovered from a cell at distance k, and ring k leaves the queue before ring k + 1, so the first time the target is popped its distance is minimal. I mark on enqueue, so each cell enters once: O(mn)."

Point at the `seen.add` right before the `append`, the bounds check with both halves, and the line where you record. For a state search, answer the six questions out loud before writing any code.

Expect follow-ups, and have the one-line answer ready. The path itself is a parent map. Eight directions is a longer direction list. "Don't modify the input" is a `seen` set instead of sinking cells. Recursion depth is an explicit stack. A Word Ladder that is too slow is bidirectional BFS: search from both ends and always expand the smaller frontier.

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
| Number of Enclaves | `graphs/number_of_enclaves.py` | flood the land the border can reach; the land left over is enclosed |
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
