## Topological Sort

A topological order places every prerequisite before what depends on it. Kahn's algorithm repeatedly removes a node with indegree zero; DFS records finishing order and reverses it. A directed cycle makes a complete order impossible. For Course Schedule, [a, b] means the edge b → a.

<!-- cell -->

```python
def topo_kahn(n, edges):
    """Edges (u, v) mean "u before v". Returns an order of 0..n-1, or [] if there is a cycle."""
    graph = [[] for _ in range(n)]
    indegree = [0] * n                            # STATE: indegree[v] = predecessors of v not taken yet
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    queue = deque(v for v in range(n) if indegree[v] == 0)   # STATE + INIT: everything ready right now
    order = []
    while queue:
        u = queue.popleft()                       # any ready node will do
        order.append(u)                           # RECORD: the pop order is a valid order
        for v in graph[u]:
            indegree[v] -= 1                      # STEP: u is done, so v waits on one fewer
            if indegree[v] == 0:                  # u was v's last missing predecessor
                queue.append(v)
    return order if len(order) == n else []       # RETURN: anyone never freed sits on or behind a cycle


def find_order(n, prerequisites):                 # Course Schedule II: [a, b] means "take b before a"
    return topo_kahn(n, [(b, a) for a, b in prerequisites])   # convert once, then think u -> v


print(find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))   # [0, 1, 2, 3]
print(find_order(3, [[0, 1], [1, 2], [2, 0]]))           # []  (0 needs 1, 1 needs 2, 2 needs 0)
print(find_order(3, []))                                 # [0, 1, 2]  (no rules: any order)
```

<!-- cell -->

**Try it**
- Convert the wrong way in `find_order` (`(a, b)` instead of `(b, a)`): the first example gives `[3, 1, 2, 0]`, the order backwards. The second still gives `[]`, because reversing every edge keeps every cycle. That is how this bug survives Course Schedule I and only shows up in II.
- The smallest order: replace the deque with a heap (`heapq.heapify`, `heappop`, `heappush`) and run `topo_kahn(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)])`: `[4, 5, 0, 2, 3, 1]` instead of the deque's `[4, 5, 2, 0, 3, 1]`.
- Replace `popleft()` with `pop()` (a stack): the first example gives `[0, 2, 1, 3]`, a different order that is just as valid. Kahn does not care which ready node goes first.
- Predict `find_order(4, [[1, 0], [2, 1], [3, 2], [1, 3]])` before running it: `[]`. Course 0 is taken, but 1, 2 and 3 wait on each other in a circle.

<!-- cell -->

The DFS version returns the same thing, an order or `[]`, and it needs three colours, not two. A node reached again can be *finished*, reached earlier along another path, which is harmless, or still *on the current path*, which means a cycle; "on the path I am walking right now" is `color[v] == GRAY`. A node finishes after everything it leads to, so the reversed finishing order is a topological order: the six-node graph below gives `[5, 4, 2, 3, 1, 0]`.

<!-- cell -->

```python
WHITE, GRAY, BLACK = 0, 1, 2                      # not visited, on the current path, finished


def topo_dfs(n, edges):
    """Edges (u, v) mean u before v. Returns reversed DFS finishing order, or [] on a cycle."""
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    color, finished = [WHITE] * n, []             # STATE + INIT: colours; nodes in the order they finish

    def visit(u):                                 # False means "found a cycle"
        color[u] = GRAY                           # u is on the path we are walking right now
        for v in graph[u]:
            if color[v] == GRAY:                  # stepped back onto our own path: a cycle
                return False
            if color[v] == WHITE and not visit(v):
                return False
        color[u] = BLACK                          # everything reachable from u is finished
        finished.append(u)                        # STEP: so u finishes after all of its successors
        return True

    for u in range(n):
        if color[u] == WHITE and not visit(u):
            return []
    return finished[::-1]                         # RETURN: reversed finishing order


print(topo_dfs(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]))   # [5, 4, 2, 3, 1, 0]
print(topo_dfs(3, [(0, 1), (0, 2), (2, 1)]))                           # [0, 2, 1]  (1 is reached twice: no cycle)
print(topo_dfs(3, [(0, 1), (1, 2), (2, 0)]))                           # []
```

<!-- cell -->

**Try it**
- Use two colours only: change `if color[v] == GRAY` to `if color[v] != WHITE`. The diamond `[(0, 1), (0, 2), (2, 1)]` now comes back `[]`: node 1 was finished, not on the path, but the two look the same.
- Print `finished` before reversing: `[0, 1, 3, 2, 4, 5]` for the first example. The deepest nodes finish first.
- Return `finished` without reversing: every edge now points backwards. It is a valid order for the graph with all arrows flipped.

<!-- cell -->

### Trace the ready queue

<!-- cell -->

```python
def trace_kahn(n, edges):                         # edges (u, v): u before v
    graph, indegree = [[] for _ in range(n)], [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    queue = deque(v for v in range(n) if indegree[v] == 0)
    print(f"start:  indegree={indegree}  queue={list(queue)}")
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
        print(f"take {u}: indegree={indegree}  queue={list(queue)}")
```

<!-- cell -->

```python
trace_kahn(4, [(0, 1), (0, 2), (1, 3), (2, 3)])
```

<!-- cell -->

```python
def respects(order, edges):                       # does every edge (u, v) have u earlier than v?
    pos = {x: i for i, x in enumerate(order)}
    return all(pos[u] < pos[v] for u, v in edges)

assert find_order(1, []) == [0]                                     # one course, nothing to wait for

assert find_order(2, [[1, 1]]) == []                                # a self-loop is a cycle of length 1

assert find_order(3, [[1, 0], [1, 0]]) == [0, 2, 1]                 # a duplicate edge is counted AND freed twice

assert respects(topo_dfs(4, [(0, 1), (2, 3)]), [(0, 1), (2, 3)])    # two separate chains

assert respects(topo_dfs(5, []), [])                                # no edges: any order is valid

print("edge cases pass")
```

<!-- cell -->

Sometimes the edges are hidden, and the first job is to find them. Alien Dictionary gives words sorted in an unknown alphabet and asks for that alphabet, or `""` when no alphabet fits: `["wrt", "wrf", "er", "ett", "rftt"]` gives `"wertf"`. Two *neighbouring* words give at most one fact, at their first different letter, where the earlier word's letter comes first; the letters after that difference say nothing. And a word placed before its own prefix, `"abc"` before `"ab"`, is impossible in any alphabet.

<!-- cell -->

```python
def alien_order(words):
    graph = {c: set() for w in words for c in w}  # every letter is a node, even one with no rules
    indegree = {c: 0 for c in graph}
    for w1, w2 in zip(words, words[1:]):          # only NEIGHBOURING words are compared
        for x, y in zip(w1, w2):
            if x != y:                            # the first difference is the only fact: x before y
                if y not in graph[x]:             # a set, so each edge is counted once
                    graph[x].add(y)
                    indegree[y] += 1
                break
        else:                                     # no difference in the common part...
            if len(w1) > len(w2):                 # ...and "abc" sits before "ab": impossible
                return ""
    queue = deque(c for c in graph if indegree[c] == 0)
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for nxt in graph[c]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return "".join(order) if len(order) == len(graph) else ""


print([alien_order(ws) for ws in (["wrt", "wrf", "er", "ett", "rftt"], ["z", "x", "z"], ["abc", "ab"])])   # ['wertf', '', '']
```

<!-- cell -->

**Try it**
- Delete the `else:` branch (the prefix check): `alien_order(["abc", "ab"])` returns `"abc"` instead of `""`.
- Delete the `break`: `alien_order(["ab", "ba"])` returns `""` instead of `"ab"`, because the letters after the first difference produced the false fact "b before a".
- `alien_order(["ab", "adc"])` is `"abcd"`: `c` appears in no rule but still belongs to the alphabet.
- `alien_order(["z", "z"])` is `"z"`: equal words give no rule and no contradiction.

<!-- cell -->

A topological order can also carry values forward, which turns Kahn's algorithm into a longest-path algorithm. Parallel Courses III gives each course a duration, lets any number of courses run at once, and asks for the fewest months to finish them all: with `time = [3, 2, 5]` and course 3 waiting for courses 1 and 2, the answer is 8. A course starts when its *slowest* prerequisite ends, so `finish[v] = time[v] + max(finish of its prerequisites)`, and in Kahn's order every prerequisite has reported before v is popped.

<!-- cell -->

```python
def minimum_time(n, relations, time):
    graph, indegree = [[] for _ in range(n + 1)], [0] * (n + 1)
    for a, b in relations:                        # courses are 1..n; a must finish before b starts
        graph[a].append(b)
        indegree[b] += 1
    finish = [0] + time                           # finish[c] = earliest month c can end (so far)
    queue = deque(c for c in range(1, n + 1) if indegree[c] == 0)
    while queue:
        u = queue.popleft()                       # every prerequisite of u has reported: finish[u] is final
        for v in graph[u]:
            finish[v] = max(finish[v], finish[u] + time[v - 1])   # v cannot end before u ends + v's own time
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return max(finish)


print(minimum_time(3, [[1, 3], [2, 3]], [3, 2, 5]))                                 # 8
print(minimum_time(5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5]))   # 12
```

<!-- cell -->

**Try it**
- Add `time[u - 1]` again (`finish[u] + time[u - 1] + time[v - 1]`): the first example says 11. `finish[u]` already includes u's own time.
- Print `finish` at the end: `[0, 3, 2, 8]`. Course 3 starts at month 3, when its slower prerequisite ends.
- With no relations, `minimum_time(3, [], [3, 2, 5])` is 5: everything runs in parallel.
- Chain them: `minimum_time(3, [[1, 2], [2, 3]], [3, 2, 5])` is 10.

<!-- cell -->

Kahn's idea also works on an undirected tree, with "degree 1" in place of "indegree 0". Minimum Height Trees asks for every root that gives a tree its smallest height: the star with centre 1 has the single answer `[1]`. The best root is the centre, and the centre is what is left after peeling the tree like an onion: remove every leaf at once, then the new leaves, until at most two nodes remain.

<!-- cell -->

```python
def find_min_height_trees(n, edges):
    if n <= 2:
        return list(range(n))
    graph, degree = [[] for _ in range(n)], [0] * n
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        degree[u] += 1
        degree[v] += 1
    leaves = deque(v for v in range(n) if degree[v] == 1)   # like Kahn's indegree-0 queue
    remaining = n
    while remaining > 2:
        for _ in range(len(leaves)):              # peel one whole ring of leaves at once
            leaf = leaves.popleft()
            remaining -= 1
            for nb in graph[leaf]:
                degree[nb] -= 1
                if degree[nb] == 1:               # nb just became a leaf of what is left
                    leaves.append(nb)
    return sorted(leaves)


print(find_min_height_trees(4, [[1, 0], [1, 2], [1, 3]]))                   # [1]
print(find_min_height_trees(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]))   # [3, 4]
print(find_min_height_trees(1, []))                                         # [0]
```

<!-- cell -->

**Try it**
- Peel one leaf at a time (drop the `for _ in range(len(leaves))` line and keep its body): the star in the first example answers `[1, 3]` instead of `[1]`. A ring of leaves must go together.
- Change `while remaining > 2` to `> 1`: the second example answers `[]` instead of `[3, 4]`. A tree can have two centres.
- Predict the centre of the path 0-1-2-3-4, then check: `find_min_height_trees(5, [[0, 1], [1, 2], [2, 3], [3, 4]])` is `[2]`; with only four nodes in a line it is `[1, 2]`.
