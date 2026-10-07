## Breadth-First Search (BFS)

BFS explores all states at distance d before states at distance d + 1. When every move costs one, the first discovery gives the shortest distance. Mark a state when it joins the queue. The grid directions and helpers below belong to this notebook.

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

The plain shortest-path question comes first, because every other BFS is this loop with a different node. A maze holds walls `#`, and you want the fewest moves from `start` to `target`, or -1 when no route exists; in the maze below, the corner `S` reaches (1, 3) in 4 moves.

Two moments inside the loop are different on purpose. A cell is marked and given its distance when it is *pushed*, because it was discovered from the closest ring, so that distance is already final. It is compared with the target when it is *popped*, because popping is when it is the closest cell not expanded yet.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Swap `queue.popleft()` for `queue.pop()` (a stack) and run `shortest_steps(["....", "....", "...."], (0, 0), (2, 0))`: it says 8 where BFS says 2. Without the queue's order, "first time out = shortest" stops being true.
- Print `[dist[x] for x in queue]` as the first line inside the loop: the queue never holds more than two distances, `d` and `d + 1`. That is the invariant that makes BFS correct.
- Move the target test to discovery time (return right after the `append` when `(nr, nc) == target`): the same answers, found one ring sooner, except `shortest_steps(["S"], (0, 0), (0, 0))` now returns -1. The start is never "discovered", so it needs its own check.
- Delete the wall-start check: `shortest_steps(["#."], (0, 0), (0, 1))` returns 1, a path that begins inside a wall.

<!-- cell -->

BFS can know a distance in three ways; pick one per problem and never mix them. A `dist` map, `dist = {start: 0}` and then `dist[nxt] = dist[cur] + 1`, gives every node its distance and doubles as `seen`. 01 Matrix, which asks every cell for its distance to the nearest 0, wants exactly that.

The distance can instead ride in the queue, `queue.append((nxt, d + 1))`, which suits a state search that only needs the goal's distance, like the lock below. Or you process whole rings, `for _ in range(len(queue)):` and then `steps += 1`, when the answer is a number of rounds: Rotting Oranges asks how many minutes pass until no fresh orange is left, and one ring is one minute.

A state search is the same loop with a richer node, and Open the Lock shows it in its purest form. A lock has four wheels showing `"0000"`; one move turns one wheel one click up or down; some combinations are dead ends you must never land on; and you want the fewest moves to the target. With the dead ends below, `"0202"` takes 6 moves.

The six answers: the node is the 4-digit string, an edge turns one wheel one click, every move costs 1, the start is `"0000"`, the goal is the target, and nothing extra matters, because a dead end is simply a node you never enter. The loop itself never changes, so it is written once as `bfs_states`, and the six answers go in as arguments.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Delete the `if "0000" in dead` check: `open_lock(["0000"], "8888")` answers 8 instead of -1. `turns` only filters the states you move *to*, so the start itself needs its own check.
- Turn the wheels upward only (`for step in (1,)`): `open_lock([], "0009")` takes 9 moves instead of 1. Each edge you leave out is a move the search can never make.
- Predict `open_lock(["0001", "0009", "0010", "0090", "0100", "0900", "1000", "9000"], "0002")` before running it: -1, because every first move is a dead end.

<!-- cell -->

### Watch it work

The rings are the whole argument for BFS, so watch them form. Each printed line is one ring of the search through the maze above, and at the end the grid shows every cell's distance from `S`, with `?` for a cell the wave never reached.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Predict the distances for `trace_rings(maze, (1, 2))`, then run it: the rings spread both ways and the far cell (1, 0) is 4 away.
- Wall in a cell: `trace_rings(["S..#", ".##.", "...#"], (0, 0))`. Cell (1, 3) keeps its `?`: that is the `-1` case of `shortest_steps`.
- Pop one cell per iteration instead of a whole layer, write `dist[(r, c)] + 1` instead of `ring + 1`, and print each popped cell's distance: `0 1 1 2 2 3 3 4 4`, never decreasing.

<!-- cell -->

```python
assert shortest_steps(["S"], (0, 0), (0, 0)) == 0            # the start is the target

assert shortest_steps(["#."], (0, 0), (0, 1)) == -1          # you cannot start inside a wall

assert shortest_steps(["S#."], (0, 0), (0, 2)) == -1         # a wall cuts the only way

assert shortest_steps(maze, [0, 0], [1, 3]) == 4             # positions given as lists still work

assert build_graph(3, []) == [[], [], []]                     # nodes without edges still exist

print("edge cases pass")
```

<!-- cell -->

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

<!-- cell -->

**Try it**
- Seed only the first 0: `update_matrix([[0, 1, 1, 1, 0]])` gives `[[0, 1, 2, 3, 4]]` instead of `[[0, 1, 2, 1, 0]]`. Every source has to start at the same moment.
- Swap `popleft()` for `pop()`: `[[0, 1, 1, 1, 0]]` comes out `[[0, 3, 2, 1, 0]]`. A stack hands out the newest cell, so a first visit is no longer the closest one.
- Count the pushes on a 30 × 30 grid with zeros on the diagonal: 900 with every zero as a source at once, 27,000 if you run one BFS per zero and keep the minimum.
- Print `list(queue)` right after the seeding loops for the first matrix: all five zeros wait at distance 0, as if one invisible super-source, joined to every 0 by a free edge, had just been expanded. Multi-source BFS is a plain BFS from that super-source.

<!-- cell -->

Interviewers often follow the distance with "now show me the path", so the parent map comes next. Remember who discovered each cell in `parent`, and walk those links back from the target; in the maze the route from `S` to (1, 3) runs along the top row, then down and one step right, five cells in all. The `parent` map also serves as `seen`, because a cell has a parent exactly when it has been discovered.

<!-- cell -->

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

<!-- cell -->

**Try it**
- With `pop()` instead of `popleft()`, the open 3×4 grid `["....", "....", "...."]` from (0, 0) to (2, 0) returns an 8-move snake instead of the 2-move path.
- `len(shortest_path(maze, (0, 0), (1, 3))) - 1` is 4, the same number `shortest_steps` gives: a path of k + 1 cells has k moves.
- `shortest_path(maze, (0, 0), (0, 0))` is `[(0, 0)]`: a path with zero moves.

<!-- cell -->

Shortest Bridge joins the two ideas above. A grid holds exactly two islands, and you want the fewest water cells to flip so that they touch. Flood one island with the DFS template to collect its cells, then run a multi-source BFS from all of them at once; the number of water rings the wave crosses before it first touches the other island is the answer.

Copying a graph is a traversal too, and the only new question is what `seen` should be. Clone Graph hands you one node of an undirected graph, each node holding a value and a neighbour list, and asks for a deep copy: the square 1-2-3-4-1 below must come back as four fresh nodes wired into the same square.

The copy needs one new node per old node, and every edge must connect *copies*. A dict `old -> new` answers "do I already have a copy of this node?" in O(1), which also makes it the visited set, and that is what stops the traversal from going round the cycle forever.

<!-- cell -->

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

<!-- cell -->

**Try it**
- In the append line, use `nb` instead of `clones[nb]`: now `clone.neighbors[0] is b` prints True. The copy points back into the original graph.
- Delete `queue.append(nb)`: the last line now raises `IndexError`, because `clone.neighbors[0].neighbors` is empty. The copies get made, but only the start is ever expanded.
- Print `len(clones)` right before the `return`: 4 copies, although every node was reached twice.
- `clone_graph(None)` is `None`, and a lone `Node(7)` copies to a node with no neighbours.

<!-- cell -->

Sometimes a node receives a value from the node that discovered it, and the traversal carries that label along every edge. Is Graph Bipartite asks whether the nodes can be split into two camps so that every edge joins the camps; Possible Bipartition is the same question with "dislikes" as the edges.

Here the label is a colour that *flips* across every edge. An edge whose two ends got the same colour closes an odd cycle, so the answer is False.

Evaluate Division gives facts like `a / b = 2.0` and `b / c = 3.0` and asks for ratios like `a / c`, which is 6.0. The label is a ratio that *multiplies* along the path: `a / b = 2` is an edge a → b worth 2 and an edge b → a worth 1/2.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Start from node 0 only (drop the outer loop): the disconnected example `[[1], [0], [3, 4], [2, 4], [2, 3]]` now says True. The triangle 2-3-4 is never coloured.
- Print `color` at the end for the square `[[1, 3], [0, 2], [1, 3], [0, 2]]`: `{0: 0, 1: 1, 3: 1, 2: 0}`. Opposite corners share a colour.
- Forget the reverse edge (delete the `graph[y].append(...)` line): `b / a` comes back -1.0 instead of 0.5.
- Ask for `["c", "a"]`: 0.16666666666666666, found by walking c → b → a and multiplying 1/3 · 1/2.

<!-- cell -->

Open the Lock already showed BFS over states, and Word Ladder has exactly its shape. It changes one letter at a time through a word list and asks how many words the shortest chain from `"hit"` to `"cog"` has: 5, along hit, hot, dot, dog, cog. A word's neighbours come from buckets like `"h*t"`, one per word and blanked position, instead of comparing every pair of words, and `bfs_states` does the rest. Without `"cog"` in the list no ladder exists, and the answer is 0.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Add `print(w, end=" ")` as the first line of `one_letter_away` and rerun the cell: the first line now starts `hit hot dot lot dog log`, the order in which BFS expands the words, ring by ring.
- Return `moves` instead of `moves + 1`: the first ladder says 4. A chain of 5 words has 4 moves, and the problem counts words.
- Print `buckets["*ot"]` inside `ladder_length`: `['hot', 'dot', 'lot']`. Every pair in one bucket is one letter apart, so the bucket lists those neighbours without comparing a single pair of words.
- Put `"hit"` itself into the first word list and rerun: still 5. The start's own buckets now hand `"hit"` back, and `seen` already holds it, so nothing changes.

<!-- cell -->

When the same cell can be in different situations, the situation becomes part of the node: question 6 of the recipe. Shortest Path in a Grid with Obstacles Elimination lets you break at most k walls between the top-left and bottom-right corners and asks for the fewest steps: the 5 × 3 grid below takes 6 with k = 1, and -1 comes back when k is too small. The node is (cell, eliminations left), and since every move still costs one step, `bfs_states` works unchanged, with `seen` keyed on the whole tuple.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Run the first grid with `k = 0`: 10, the long way round. One elimination already buys the straight route, so any k ≥ 1 gives 6.
- Pass `key=lambda s: s[:2]` to `bfs_states`, so `seen` remembers only the cell, and run `eliminate_obstacles([[0, 0, 1, 1], [1, 0, 1, 0]], 1)`: -1 instead of 4. Cell (1, 1) is first reached through the wall at (1, 0), with the budget spent, and that arrival blocks the one through (0, 1) that still has it.
- Before running, bound the work: R · C cells times k + 1 budgets, 5 · 3 · 2 = 30 states for the first grid. Then print `len(seen)` in `bfs_states` just before `return moves` and rerun both cells: the first grid queued 22 states.

<!-- cell -->

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Three of them only need a richer node for `bfs_states`. Sliding Puzzle holds the tiles 1 to 5 and one blank on a 2 × 3 board; one move slides a tile into the blank, and it asks for the fewest moves to reach `123` over `450`, or -1 when the board can never get there: `[[1, 2, 3], [4, 0, 5]]` needs 1 move. The node is the whole board written as a string, which is hashable, so it fits in `seen`.

Shortest Path to Get All Keys has a start `@`, walls `#`, keys as lowercase letters and locks as the matching uppercase letters, and asks for the fewest moves to collect every key: `["@.a..", "###.#", "b.A.B"]` takes 8. A lock can only be crossed with its key in hand, so the node is (cell, keys held), with the keys as a bitmask.

Shortest Path Visiting All Nodes asks for the shortest walk that visits every node of a small graph, starting anywhere and revisiting freely: the star `[[1, 2, 3], [0], [0], [0]]` takes 4 steps. The node is (node, visited mask), and every node is a start, so all of them enter the queue at distance 0.

<!-- cell -->

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

<!-- cell -->

**Try it**
- In `bfs_states` (in the Open the Lock cell), print `len(seen)` just before `return -1` and rerun that cell; then call only `sliding_puzzle([[1, 2, 3], [5, 4, 0]])`: 360. Only half of the 720 boards can be reached from it.
- Predict `sliding_puzzle([[3, 2, 4], [1, 5, 0]])` before running it (14).
- In `all_keys`, pass `key=lambda s: s[:2]` to `bfs_states`, so `seen` remembers only the cell, and run `all_keys(["a.@A.b"])`: -1 instead of 7. After fetching `a` on the left, the walk must cross cells it has already seen to reach the lock.
- In `visit_all_nodes`, start from node 0 only (`starts = [(0, 1)]`): 5 instead of 4. Starting at a leaf is shorter, which is why every node is a source.

<!-- cell -->

Sometimes one move reaches a whole group at once, every stop of a bus route or every index holding the same value. The group is the expensive part, so each group is expanded *once*.

Bus Routes gives each bus as the loop of stops it drives, and asks for the fewest buses from a source stop to a target stop; with routes `[1, 2, 7]` and `[3, 6, 7]`, stop 1 reaches stop 6 on 2 buses. The problem counts buses, so the nodes are routes, reached through a stop → routes index.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Delete `if source == target: return 0`: `num_buses([[1, 2, 7], [3, 6, 7]], 1, 1)` returns 1, a bus ride you never needed.
- Print `i, buses` after each `popleft()` for the first example: route 0 with 1 bus, then route 1 with 2 buses. Stops are never counted.
- `num_buses([[1, 2, 3, 4, 5, 6]], 1, 6)` is 1: one ride covers five stops, because an edge is a bus, not a stop.
