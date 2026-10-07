## Graphs II: Ordering & Connectivity

> Two questions about how nodes relate. **Order**: *what can I do first?* Keep taking a node that nothing is waiting on (topological sort). **Connectivity**: *are these two in the same group?* Every group has a boss; merging two groups means pointing one boss at the other (union-find).

**Reach for it when** the problem says:
- **Order:** prerequisites, dependencies, "must come before", build order, an alphabet hidden in sorted words, "minimum time when tasks run in parallel".
- **Connectivity:** merge, same group, connected, "edges arrive one at a time", "the extra edge that makes a cycle", "after each operation, how many groups?", "queries with a weight limit".

"Which cable, if cut, disconnects the network?" is bridges and "use every ticket exactly once" is an Eulerian path; both are in the hard extras at the end of Variations.

**In this repo:** `graphs/` (19 of its 45 problems) · bank: `practice/simple/43_course_schedule.py`, `practice/simple/47_redundant_connection.py` · basics: `practice/simple/basics/graphs/02_topological_sort_kahn_and_dfs.py`, `practice/simple/basics/graphs/03_union_find.py`

### The picture

```text
TOPOLOGICAL SORT (Kahn): keep taking whatever nothing is waiting on

      0 -----> 1            indegree = how many arrows point INTO a node
      |        |
      v        v            start      indegree  0:0  1:1  2:1  3:2    ready [0]
      2 -----> 3            take 0  ->           1:0  2:0  3:2         ready [1, 2]
                            take 1  ->                     3:1         ready [2]
                            take 2  ->                     3:0         ready [3]
                            take 3  ->  order 0 1 2 3

A cycle 1 -> 2 -> 3 -> 1: each waits on another, none ever reaches 0, and "ready" runs dry early.
```

```text
UNION-FIND: every group is a tree, and its root is the group's name

  union(0, 1)   union(2, 3)          union(1, 3): find(1) = 0, find(3) = 2,
                                     so hang root 2 under root 0
     0     2                              0
     |     |                             / \
     1     3                            1   2
                                            |
                                            3      find(3) walks 3 -> 2 -> 0; path halving then
                                                   points 3 at its grandparent, the root
  union(0, 2) now: find(0) == find(2) == 0, so it returns False: they were already connected.
```

**Which tool?**
- *An order, with a cycle check* → Kahn: iterative, no recursion limit, and a cycle shows up as `len(order) < n`. Use DFS colours when you are already inside a DFS, or need "the nodes that can reach a cycle" (802).
- *Connectivity on a graph given once* → one BFS or DFS ([Graphs I](#s17)).
- *Edges arriving over time, many queries, or "the edge that closes a cycle"* → union-find.

**Why it is fast:** the brute-force ordering rescans every edge each round to find a node that is ready: O(V · (V + E)). Kahn keeps one counter per node, and taking a node only changes the counters of *its* successors, so each edge is touched once: O(V + E). For connectivity, re-running a BFS for every "connected?" question costs O(V + E) each time. Groups only ever merge, so a forest of parent pointers answers in nearly O(1), as long as the trees stay flat. Union by size keeps them flat: a node goes one level deeper only when its group is hung under a group at least as big, so its group at least doubles each time, and depth ≤ log₂ n. Path halving flattens the rest. Together they cost amortised α(n) per operation (the inverse Ackermann function), effectively a constant.

### From idea to code

**The idea in two sentences:** *Order: count each node's unfinished predecessors, take any node whose count is 0, and taking it lowers its successors' counts.* *Connectivity: `find` walks up to the root that names a group, `union` points one root at the other, and a `union` whose two roots are already equal has just found an edge that closes a cycle.*

| Decision | Topological sort (Kahn) | Union-find |
|---|---|---|
| **State**: what must I remember? | `graph[u]` (u before v), `indegree[v]`, and a queue of ready nodes | `parent[x]`, `size[root]`, and the number of groups if asked |
| **Definition**: what exactly does each variable mean? | `indegree[v]` = predecessors of `v` not taken yet | `find(x)` = the root of x's tree; same root means same group |
| **Invariant**: what is true at the end of every step? | every node in the queue has all its predecessors already in `order` | every group is one tree; `r` is a root exactly when `parent[r] == r` |
| **Step**: how does one item change the state? | pop `u`, append it; for each successor `v`: `indegree[v] -= 1`, push `v` when it reaches 0 | `union(a, b)`: find both roots; if they differ, hang the smaller tree under the bigger |
| **Record**: when is the answer updated? | the pop order is the topological order | `union` returns `False`: already connected (cycle edge); `True`: one group fewer |
| **Init**: starting values | the queue holds *every* node with indegree 0, isolated nodes too | `parent = list(range(n))`, `size = [1] * n`, `count = n` |
| **Return**: what comes back, and for "not found"? | `order` if `len(order) == n`; otherwise a cycle: `[]`, `False` or `""` | the count, the redundant edge, or groups bucketed by `find` |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "b must come before a" (pair `[a, b]`) | convert once: the edge `(b, a)`, then think u → v everywhere |
| "everything I can do right now" | `deque(v for v in range(n) if indegree[v] == 0)` |
| "u is done, so v waits on one fewer" | `indegree[v] -= 1` |
| "v is free now" | `if indegree[v] == 0: queue.append(v)` |
| "some nodes never got free" | `len(order) < n`: there is a cycle |
| "on the path I am walking right now" (DFS) | `color[v] == GRAY` |
| "who is the boss of x's group?" | `find(x)` |
| "merge the two groups" | `parent[find(b)] = find(a)`: roots, never the nodes themselves |
| "they were already together" | `find(a) == find(b)`, so `union` returns `False` |

Kahn's algorithm with one edge convention, u → v ("u before v"). LeetCode's Course Schedule writes `[a, b]` for "b before a", so its wrapper converts once and never thinks about it again:

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

**Try it**
- Convert the wrong way in `find_order` (`(a, b)` instead of `(b, a)`): the first example gives `[3, 1, 2, 0]`, the order backwards. The second still gives `[]`, because reversing every edge keeps every cycle. That is how this bug survives Course Schedule I and only shows up in II.
- The smallest order: replace the deque with a heap (`heapq.heapify`, `heappop`, `heappush`) and run `topo_kahn(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)])`: `[4, 5, 0, 2, 3, 1]` instead of the deque's `[4, 5, 2, 0, 3, 1]`.
- Replace `popleft()` with `pop()` (a stack): the first example gives `[0, 2, 1, 3]`, a different order that is just as valid. Kahn does not care which ready node goes first.
- Predict `find_order(4, [[1, 0], [2, 1], [3, 2], [1, 3]])` before running it: `[]`. Course 0 is taken, but 1, 2 and 3 wait on each other in a circle.

The DFS version needs three colours, not two. A node reached again can be *finished* (it was reached earlier by another path, which is fine) or *on the current path* (a cycle). A node finishes after everything it leads to, so the reversed finishing order is a topological order:

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

**Try it**
- Use two colours only: change `if color[v] == GRAY` to `if color[v] != WHITE`. The diamond `[(0, 1), (0, 2), (2, 1)]` now comes back `[]`: node 1 was finished, not on the path, but the two look the same.
- Print `finished` before reversing: `[0, 1, 3, 2, 4, 5]` for the first example. The deepest nodes finish first.
- Return `finished` without reversing: every edge now points backwards. It is a valid order for the graph with all arrows flipped.
- Run a 10,000-node chain, `topo_dfs(10_000, [(i, i + 1) for i in range(9_999)])`: `RecursionError`. Kahn has no recursion, which is worth saying in an interview.

Union-find. Path halving makes each node on the way up point at its grandparent; union by size hangs the smaller tree below the bigger one:

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))              # STATE + INIT: everyone starts as their own root
        self.size = [1] * n                       # STATE + INIT: size[root] = members of that group
        self.count = n                            # STATE + INIT: number of groups

    def find(self, x):                            # the root that names x's group
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving: skip to the grandparent
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                          # RECORD: already connected (this edge closes a cycle)
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra                       # union by size: the smaller tree hangs below
        self.parent[rb] = ra                      # STEP: two groups become one
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True


dsu = DSU(6)
print([dsu.union(a, b) for a, b in [(0, 1), (2, 3), (1, 3), (0, 2)]])   # [True, True, True, False]
print(dsu.count, dsu.find(3) == dsu.find(0), dsu.size[dsu.find(0)])      # 3 True 4
```

**Try it**
- On a fresh `DSU(6)` do the unions `(0, 1)`, `(2, 3)`, `(1, 3)`, print `parent`, call `find(3)`, and print again: `[0, 0, 0, 2, 4, 5]` becomes `[0, 0, 0, 0, 4, 5]`. Node 3 now points at its old grandparent, the root.
- Link nodes instead of roots: change `self.parent[rb] = ra` to `self.parent[b] = a`. Then `d = DSU(3); d.union(0, 1); d.union(2, 1); print(d.find(0) == d.find(1))` prints False: node 1 was pulled out from under 0.
- Print `dsu.size`: `[4, 1, 2, 1, 1, 1]`. Only a root's entry means something; `size[2] = 2` is left over from when 2 was a root.
- Delete the two `if ra == rb` lines and rerun the cell: the last union returns True and `count` drops to 2, although the groups are still `{0, 1, 2, 3}`, `{4}` and `{5}`.

In an interview, two functions are enough. Halving alone keeps `find` fast in practice; add union by size if you are asked for the guarantee:

```py
parent = list(range(n))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]      # halving: skip to the grandparent
        x = parent[x]
    return x

def union(a, b):                           # False: a and b were already connected
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    parent[ra] = rb
    return True
```

### Watch it work

Kahn on the picture's graph, then union-find hunting for the extra edge in Redundant Connection:

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


def trace_redundant(edges):                       # nodes are 1..n
    dsu = DSU(len(edges) + 1)
    for u, v in edges:
        merged = dsu.union(u, v)
        print(f"edge {u}-{v}: {'merge' if merged else 'already connected -> redundant'}  parent[1:]={dsu.parent[1:]}")
        if not merged:
            return [u, v]


trace_kahn(4, [(0, 1), (0, 2), (1, 3), (2, 3)])
print(trace_redundant([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))   # [1, 4]
```

**Try it**
- `trace_kahn(3, [(0, 1), (1, 2), (2, 1)])`: after taking 0 the queue is empty while 1 and 2 still wait on each other. That is what a cycle looks like from inside Kahn's algorithm.
- `trace_redundant([[1, 2], [1, 3], [2, 3]])` returns `[2, 3]`: the triangle closes on its last edge.
- Shuffle the input: `trace_redundant([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]])` returns `[1, 3]`. The answer is whichever edge of the cycle comes last.

### Where it goes wrong

1. **Edge direction.** `[a, b]` means "b before a", so the edge is `b -> a`. Reversed edges give the order backwards (`[3, 1, 2, 0]` above), and Course Schedule I still passes because reversing edges keeps cycles, so the bug hides until part II. Convert once, at the top.
2. **Forgotten nodes.** Seed the queue with *every* node of indegree 0, including nodes with no edges at all. In Alien Dictionary every letter is a node, even one that appears in no rule (`["ab", "adc"]` must output `c` too).
3. **Duplicate edges with a set adjacency.** If `graph[x]` is a set, add to `indegree[y]` only when `y` was really new. Without that guard, `alien_order(["ab", "ac", "bb", "bc"])` returns `""` instead of `"abc"`: the fact "b before c" was counted twice but can only be freed once. With list adjacency duplicates are harmless: counted twice, freed twice.
4. **Two colours in DFS.** "Visited" is not "on my path": with two colours, the diamond `0->1, 0->2, 2->1` looks like a cycle.
5. **Linking nodes instead of roots.** `parent[b] = a` can pull `b` out of its old group (`union(0, 1)`, then `union(2, 1)` leaves 0 and 1 apart). Always link `find(b)` under `find(a)`.
6. **No halving, no union by size.** With a plain `parent[find(a)] = find(b)`, the unions `union(0, k)` for k = 1 … 999 build one long chain, and `find(0)` then walks 999 links.
7. **Counting every union.** Lower the group count only when the roots differed; a repeated edge must not change it.
8. **1-indexed nodes.** Courses, people and tree nodes are often numbered `1..n`: `DSU(3).union(1, 3)` raises `IndexError`. Allocate `n + 1`.
9. **Comparing parents instead of roots.** After `union(0, 1)`, `union(2, 3)`, `union(0, 2)` the parents are `[0, 0, 0, 2]`: `parent[3] == parent[1]` is False although `find(3) == find(1)`. Only roots name groups.

### Edge cases to say out loud

One node · no edges (any order is valid, every node is its own group) · a self-loop (a cycle of length 1; `union(x, x)` is False) · duplicate edges · several separate chains · a word that comes before its own prefix (Alien Dictionary) · one node and no edges is a valid tree.

```python
def respects(order, edges):                       # does every edge (u, v) have u earlier than v?
    pos = {x: i for i, x in enumerate(order)}
    return all(pos[u] < pos[v] for u, v in edges)


assert find_order(1, []) == [0]                                     # one course, nothing to wait for
assert find_order(2, [[1, 1]]) == []                                # a self-loop is a cycle of length 1
assert find_order(3, [[1, 0], [1, 0]]) == [0, 2, 1]                 # a duplicate edge is counted AND freed twice
assert respects(topo_dfs(4, [(0, 1), (2, 3)]), [(0, 1), (2, 3)])    # two separate chains
assert respects(topo_dfs(5, []), [])                                # no edges: any order is valid
d = DSU(3)
assert d.union(0, 0) is False and d.count == 3                      # a node is already with itself
assert d.union(0, 1) and d.union(1, 2) and d.count == 1
print("edge cases pass")
```

**Try it**
- Predict `find_order(2, [[0, 1], [1, 0]])` before running it (`[]`: two courses waiting on each other).
- `respects([0, 1, 2], [(2, 0)])` is False. Test any order you produce with `respects` instead of comparing it with one "expected" order: many orders are correct.
- `topo_dfs(1, [(0, 0)])` returns `[]`: node 0 is still GRAY when it looks at itself.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Is any order possible?** | count the pops; possible iff all n come out | 207 |
| **Return an order** | keep the pop order | 210 |
| **Smallest or unique order** | a heap instead of the deque; the order is unique iff the queue never holds two nodes | 444 |
| **Derive the edges first** | compare neighbouring words; their first different letter is one edge; prefix check | 269 |
| **Longest path in a DAG** | in topological order, push `finish[v] = max(finish[v], finish[u] + time[v])` | 2050 |
| **Peel leaves** | Kahn on an undirected tree: remove degree-1 leaves ring by ring; the last 1–2 nodes are the centre | 310 |
| **Tree check / component count / judge** | n − 1 edges and no failed union; `dsu.count`; in-degree minus out-degree | 261, 323, 997 |
| **The cycle edge, undirected** | the first union that returns False | 684 |
| **Group by a shared key** | each key (an email) remembers its first owner; union with it | 721 |
| **Union, then act per component** | sort letters inside each component; stones − groups | 1202, 947 |
| **Equations as unions** | union every `a == b`, then check that no `a != b` falls inside one group | 990 |
| **Two-colouring with a DSU** | every neighbour of u joins one group, and that group must not contain u | 785 |
| **Online counting** | a new node adds 1; each successful union subtracts 1 | 305 |
| **Hard extras** | see the end of this section | 685, 1203, 952, 924, 2092, 1579, 1697, 1192, 332 |

**One call away from the template.** A tree on n nodes is "just enough" edges: exactly n − 1, and none of them wasted on a loop. A component count starts at n and every real merge removes one. The Town Judge needs no graph at all, only degrees.

```python
def valid_tree(n, edges):                         # exactly n - 1 edges, and none of them closes a cycle
    dsu = DSU(n)
    return len(edges) == n - 1 and all(dsu.union(u, v) for u, v in edges)


def count_components(n, edges):                   # start with n groups; every real merge removes one
    dsu = DSU(n)
    for u, v in edges:
        dsu.union(u, v)
    return dsu.count


def find_judge(n, trust):                         # degrees only: trusted by n - 1 people, trusts nobody
    score = [0] * (n + 1)
    for a, b in trust:
        score[a] -= 1                             # trusting anyone disqualifies a
        score[b] += 1
    return next((i for i in range(1, n + 1) if score[i] == n - 1), -1)


print(valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]), valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]))   # True False
print(count_components(5, [[0, 1], [1, 2], [3, 4]]))                                                           # 2
print(find_judge(3, [[1, 3], [2, 3]]), find_judge(3, [[1, 3], [2, 3], [3, 1]]), find_judge(1, []))               # 3 -1 1
```

**Try it**
- Drop the `len(edges) == n - 1` check: `valid_tree(4, [[0, 1], [2, 3]])` becomes True. No cycle, but two pieces; the edge count is what rules that out.
- Delete `score[a] -= 1` in `find_judge`: `find_judge(3, [[1, 3], [2, 3], [3, 1]])` returns 3, a "judge" who trusts somebody.
- `count_components(4, [[0, 1], [1, 0], [2, 3]])` is 2: the repeated edge's union returns False, so the count does not drop.
- `valid_tree(1, [])` is True: a single node with no edges is a tree.

**Derive the edges first (Alien Dictionary).** The sorted word list hides the alphabet. Two *neighbouring* words give at most one fact: at their first different letter, the earlier word's letter comes first. Letters after that difference say nothing. And if a word comes before its own prefix (`"abc"` before `"ab"`), no alphabet can do that.

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

**Try it**
- Delete the `else:` branch (the prefix check): `alien_order(["abc", "ab"])` returns `"abc"` instead of `""`.
- Delete the `break`: `alien_order(["ab", "ba"])` returns `""` instead of `"ab"`, because the letters after the first difference produced the false fact "b before a".
- `alien_order(["ab", "adc"])` is `"abcd"`: `c` appears in no rule but still belongs to the alphabet.
- `alien_order(["z", "z"])` is `"z"`: equal words give no rule and no contradiction.

**Longest path in a DAG (Parallel Courses III).** A course can start only when its *slowest* prerequisite has finished, so `finish[v] = time[v] + max(finish of its prerequisites)`. In Kahn's order every prerequisite has already reported when `v` is popped, so each edge pushes its value forward exactly once.

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

**Try it**
- Add `time[u - 1]` again (`finish[u] + time[u - 1] + time[v - 1]`): the first example says 11. `finish[u]` already includes u's own time.
- Print `finish` at the end: `[0, 3, 2, 8]`. Course 3 starts at month 3, when its slower prerequisite ends.
- With no relations, `minimum_time(3, [], [3, 2, 5])` is 5: everything runs in parallel.
- Chain them: `minimum_time(3, [[1, 2], [2, 3]], [3, 2, 5])` is 10.

**Peel leaves (Minimum Height Trees).** The best root of a tree is its centre, and the centre is what is left after peeling the tree like an onion: remove every leaf (degree 1) at once, then the new leaves, until at most two nodes remain. It is Kahn's algorithm on an undirected tree, with "degree 1" in place of "indegree 0".

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

**Try it**
- Peel one leaf at a time (drop the `for _ in range(len(leaves))` line and keep its body): the star in the first example answers `[1, 3]` instead of `[1]`. A ring of leaves must go together.
- Change `while remaining > 2` to `> 1`: the second example answers `[]` instead of `[3, 4]`. A tree can have two centres.
- Predict the centre of the path 0-1-2-3-4, then check: `find_min_height_trees(5, [[0, 1], [1, 2], [2, 3], [3, 4]])` is `[2]`; with only four nodes in a line it is `[1, 2]`.

**Group by a shared key (Accounts Merge).** Comparing every pair of accounts to see whether they share an email is O(n²). Turn it around: each email remembers the *first* account it saw, and every later account with the same email is unioned with that first one. Then bucket the emails by their group's root.

```python
def accounts_merge(accounts):
    dsu = DSU(len(accounts))
    owner = {}                                    # email -> the first account that listed it
    for i, (_, *emails) in enumerate(accounts):
        for e in emails:
            if e in owner:
                dsu.union(i, owner[e])            # a shared email: same person
            else:
                owner[e] = i
    groups = defaultdict(list)
    for e, i in owner.items():
        groups[dsu.find(i)].append(e)             # bucket every email under its group's root
    return sorted([accounts[root][0]] + sorted(es) for root, es in groups.items())


print(accounts_merge([["John", "a@m", "b@m"], ["John", "b@m", "c@m"], ["Mary", "d@m"], ["John", "x@m"]]))
# [['John', 'a@m', 'b@m', 'c@m'], ['John', 'x@m'], ['Mary', 'd@m']]
```

**Try it**
- Print `owner` and `dsu.parent` after the first loop: `b@m` belongs to account 0, and account 0 now hangs under account 1. The two Johns who share nothing stay apart, although they have the same name.
- Delete the `else:` branch (never record an owner): the result is `[]`. `owner` is both the shared-email detector and the list of emails to print.

**Union, then act per component.** Some problems only need the groups: union everything first, then do one thing per component. In Smallest String With Swaps, swaps chain together, so the letters inside a component can be put in *any* order: sort them. In Most Stones Removed, a stone glues its row to its column, and every group of stones can be cleared down to one stone.

```python
def smallest_string_with_swaps(s, pairs):
    dsu = DSU(len(s))
    for a, b in pairs:
        dsu.union(a, b)                     # swaps chain: any order inside a component is reachable
    groups = defaultdict(list)
    for i in range(len(s)):
        groups[dsu.find(i)].append(i)       # one component's indexes, increasing
    out = list(s)
    for idx in groups.values():
        for i, ch in zip(idx, sorted(s[i] for i in idx)):
            out[i] = ch                     # smallest letters to the smallest indexes
    return "".join(out)


def remove_stones(stones):
    dsu = DSU(20002)                        # rows 0..10000 and columns 10001..20001 share one DSU
    for r, c in stones:
        dsu.union(r, 10001 + c)             # a stone glues its row to its column
    groups = {dsu.find(r) for r, _ in stones}
    return len(stones) - len(groups)        # each group can be cleared down to one stone


print(smallest_string_with_swaps("dcab", [[0, 3], [1, 2]]), smallest_string_with_swaps("dcab", [[0, 3], [1, 2], [0, 2]]),
      smallest_string_with_swaps("cba", [[0, 1], [1, 2]]))                                     # bacd abcd abc
print(remove_stones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]), remove_stones([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]),
      remove_stones([[0, 0]]))                                                                # 5 3 0
```

**Try it**
- Print `groups` for `"dcab", [[0, 3], [1, 2]]`: `{0: [0, 3], 1: [1, 2]}`. Index 0 can only trade with index 3, so sorting the whole string (`"abcd"`) would be wrong; the answer is `"bacd"`.
- Forget the column offset (`dsu.union(r, c)`): `remove_stones([[0, 1], [1, 2]])` answers 1 instead of 0, because column 1 got glued to row 1.
- `remove_stones([[0, 0], [5, 5]])` is 0: two stones that share neither a row nor a column.

**Online counting (Number of Islands II).** Land appears one cell at a time and the island count is needed after every step. Recounting the grid each time repeats almost all of the work. Instead: a new cell is a new island (+1), and it swallows each *different* neighbouring island (−1 per successful union).

```python
def num_islands_2(m, n, positions):
    parent, count, out = {}, 0, []                # only land cells live in the union-find

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for r, c in positions:
        if (r, c) not in parent:                  # adding the same cell twice changes nothing
            parent[(r, c)] = (r, c)
            count += 1                            # a new island of one cell...
            for nb in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if nb in parent:                  # (only land cells are keys, so no bounds check)
                    ra, rb = find((r, c)), find(nb)
                    if ra != rb:
                        parent[ra] = rb
                        count -= 1                # ...that swallows each DIFFERENT neighbouring island
        out.append(count)
    return out


print(num_islands_2(3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]]))           # [1, 1, 2, 3]
print(num_islands_2(3, 3, [[0, 0], [0, 2], [1, 1], [0, 1], [0, 1]]))   # [1, 2, 3, 1, 1]
```

**Try it**
- Remove the duplicate guard (make the `if` always true): `num_islands_2(3, 3, [[0, 0], [0, 0]])` reports `[1, 2]`, a second island that does not exist.
- Decrement for every land neighbour (drop the `if ra != rb`): `num_islands_2(2, 2, [[0, 0], [0, 1], [1, 0], [1, 1]])` gives `[1, 1, 1, 0]`. The last cell's two neighbours were already one island.
- Print `{cell: find(cell) for cell in parent}` at the end of the second example: all four cells report the same root.

#### Hard extras (skim)

The same two tools, each with one more twist. Skim them once the core above is automatic.

| Variation | What changes | Problems |
|---|---|---|
| **The cycle edge, directed** | a node with two parents first: try dropping the later edge, else the earlier one | 685 |
| **An order inside an order** | topo-sort the items and the groups separately; output groups in order, items inside | 1203 |
| **Prime hubs** | each prime factor remembers its first owner; union with it | 952 |
| **Facts per component** | per root: its size and how many infected nodes it holds | 924 |
| **Unions over time** | one timestamp at a time; reset everyone not connected to person 0 | 2092 |
| **Two players** | two DSUs; shared edges first, then each player's own | 1579 |
| **Offline thresholds** | sort queries by limit, let edges in by weight, answer into the original slots | 1697 |
| **Bridges** | DFS low-link: tree edge (u, v) is a bridge iff `low[v] > disc[u]` | 1192 |
| **Use every edge once** | Hierholzer: write a node down when it is stuck, reverse at the end | 332 |

**Prime hubs (Largest Component by Common Factor).** The Accounts Merge trick with primes as the keys: two numbers are connected if they share a prime, so every number is unioned with the first owner of each of its prime factors.

```python
def largest_component(nums):
    dsu = DSU(len(nums))
    owner = {}                                    # prime -> the first index divisible by it
    for i, x in enumerate(nums):
        p = 2
        while p * p <= x:
            if x % p == 0:
                dsu.union(i, owner.setdefault(p, i))
                while x % p == 0:
                    x //= p
            p += 1
        if x > 1:                                 # a prime factor bigger than sqrt is left over
            dsu.union(i, owner.setdefault(x, i))
    return max(dsu.size[dsu.find(i)] for i in range(len(nums)))


print(largest_component([4, 6, 15, 35]), largest_component([20, 50, 9, 63]))   # 4 2
```

**Try it**
- `largest_component([2, 3, 6])` is 3: 2 and 3 share nothing, but 6 glues them through the primes 2 and 3.
- Delete the leftover-prime lines (`if x > 1: ...`): `[4, 6, 15, 35]` now answers 2. The 3 in 6 and the 5 in 15 are only found after the loop, so those links never happen.

**Unions over time, and offline thresholds.** Union-find can only merge, never split, so feed it events in the right order. In Find All People With Secret, a timestamp's meetings are unioned together, and afterwards everybody who did *not* end up connected to person 0 is reset to a group of one: their links knew no secret and must not carry one later. In Edge Length Limited Paths, sort the queries by limit and let edges in by weight; each query is then one `find` comparison, written back into its original slot.

```python
def find_all_people(n, meetings, first):
    dsu = DSU(n)
    dsu.union(0, first)
    meetings = sorted(meetings, key=lambda m: m[2])
    i = 0
    while i < len(meetings):
        j, met = i, set()
        while j < len(meetings) and meetings[j][2] == meetings[i][2]:   # every meeting at this moment
            x, y, _ = meetings[j]
            dsu.union(x, y)
            met.update((x, y))
            j += 1
        for p in met:                             # links that never touched person 0 are forgotten
            if dsu.find(p) != dsu.find(0):
                dsu.parent[p], dsu.size[p] = p, 1
        i = j
    return [p for p in range(n) if dsu.find(p) == dsu.find(0)]


def limited_paths(n, edges, queries):
    dsu = DSU(n)
    edges = sorted(edges, key=lambda e: e[2])
    answer, j = [False] * len(queries), 0
    for qi in sorted(range(len(queries)), key=lambda i: queries[i][2]):   # smallest limit first
        p, q, limit = queries[qi]
        while j < len(edges) and edges[j][2] < limit:   # let in every edge lighter than the limit
            dsu.union(edges[j][0], edges[j][1])
            j += 1
        answer[qi] = dsu.find(p) == dsu.find(q)   # write into the query's ORIGINAL slot
    return answer


print(find_all_people(6, [[1, 2, 5], [2, 3, 8], [1, 5, 10]], 1))   # [0, 1, 2, 3, 5]
print(find_all_people(4, [[2, 3, 1], [1, 2, 2]], 1))               # [0, 1, 2]  (3 met 2 BEFORE 2 knew)
print(limited_paths(3, [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]], [[0, 1, 2], [0, 2, 5]]))   # [False, True]
```

**Try it**
- Replace the reset line with `pass`: `find_all_people(4, [[2, 3, 1], [1, 2, 2]], 1)` returns `[0, 1, 2, 3]`. Person 3 "learns" the secret through a meeting that happened before 2 knew it.
- Change `<` to `<=` in `limited_paths`: the first query becomes True, although its only edge weighs 2 and the limit is 2 (the problem says strictly less).
- Ask the queries in the other order, `[[0, 2, 5], [0, 1, 2]]`: `[True, False]`. The answers land in their original slots.

**Bridges (Critical Connections).** Removing each edge and re-running a BFS costs O(E · (V + E)). One DFS can do it. Picture the DFS tree with every non-tree edge as a *rope* from a deep node up to an ancestor. Cut the tree edge above v: v's subtree stays attached exactly when some rope from inside it reaches above the cut.

```text
        0 <------+      tree edges go down; the non-tree edge 2-0 is a rope from 2 up to 0
        |        |
        1        |      cut 0-1 or 1-2: the rope from 2 still holds that piece, so neither is a bridge
       / \       |
      2   3      |      cut 1-3: nothing below 3 climbs above 1, so 3 falls off: a bridge
      |          |
      +----------+      disc = visiting order; low[v] = the smallest disc a rope from v's subtree reaches
```

```python
def critical_connections(n, connections):
    graph = [[] for _ in range(n)]
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)
    disc = [-1] * n                               # discovery time; -1 = not visited yet
    low = [0] * n                                 # smallest disc reachable from u's subtree with one back edge
    bridges, timer = [], 0

    def dfs(u, parent):
        nonlocal timer
        disc[u] = low[u] = timer
        timer += 1
        for v in graph[u]:
            if v == parent:
                continue                          # do not count the edge we came in on
            if disc[v] == -1:                     # tree edge: explore the child first
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:              # v's subtree cannot get back to u or above it
                    bridges.append([u, v])
            else:                                 # visited: an ancestor (back edge) or a finished descendant (larger disc: harmless)
                low[u] = min(low[u], disc[v])

    dfs(0, -1)
    return bridges


print(critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))           # [[1, 3]]
print(critical_connections(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]))   # [[3, 4], [1, 3]]
```

**Try it**
- Delete the `if v == parent: continue` lines: the first example returns `[]`. The edge back to the parent looks like a rope, so every subtree seems to have a way around.
- Change `low[v] > disc[u]` to `>=`: `[0, 1]` is reported too, although it sits on the triangle. `>=` belongs to the test for an articulation *node* (one whose removal disconnects; the root has its own rule), not to the bridge test.
- Print `disc` and `low` after `dfs(0, -1)`: `[0, 1, 2, 3]` and `[0, 0, 0, 3]`. Node 3's low (3) is bigger than node 1's disc (1): nothing below 3 reaches back, so 1-3 is a bridge.
- `critical_connections(5000, [[i, i + 1] for i in range(4999)])` raises `RecursionError`. Run `import sys; sys.setrecursionlimit(20_000)` first and it returns all 4999 edges. LeetCode allows n = 10⁵: raise the limit or make the DFS iterative.

Two more limits of this version. Parallel edges: `critical_connections(2, [[0, 1], [0, 1]])` gives `[[0, 1]]`, but removing one copy disconnects nothing; skip the parent *edge id*, not the parent node. A disconnected graph: `critical_connections(4, [[0, 1], [2, 3]])` misses the bridge 2-3, because the DFS has to be started from every unvisited node.

**Use every edge once (Reconstruct Itinerary).** Backtracking over ticket orders can dead-end deep down and undo a lot. Hierholzer's trick: always fly the smallest unused ticket; when you are stuck at an airport, it must be the *end* of what is left, so write it down and back up one step. Airports are written in reverse, so reverse at the end.

```python
def find_itinerary(tickets):
    graph = defaultdict(list)
    for a, b in sorted(tickets, reverse=True):
        graph[a].append(b)                        # reverse-sorted, so pop() hands out the smallest
    route, stack = [], ["JFK"]
    while stack:
        while graph[stack[-1]]:                   # keep flying while this airport has unused tickets
            stack.append(graph[stack[-1]].pop())
        route.append(stack.pop())                 # stuck here: this airport is finished, write it down
    return route[::-1]                            # airports were written in reverse finishing order


print(find_itinerary([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]))   # ['JFK', 'MUC', 'LHR', 'SFO', 'SJC']
print(find_itinerary([["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]))                  # ['JFK', 'NRT', 'JFK', 'KUL']
```

**Try it**
- Write each airport down on the way *in* instead (append it when you fly to it, no reverse): the second example becomes `['JFK', 'KUL', 'NRT', 'JFK']`, which needs a KUL → NRT ticket that does not exist.
- Sort ascending instead: `pop()` now hands out the *largest* destination. For `[["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]` you get `['JFK', 'SFO', 'ATL', 'JFK', 'ATL', 'SFO']`: it uses every ticket, but it is not the smallest route.
- Print `route[-1], stack` each time an airport is written: KUL goes first, while the stack still holds the trip so far.

**Four more, in words.**
- *Sort Items by Groups (1203):* give every ungrouped item its own new group. Build the item graph and a group graph (`group[u] -> group[v]` when the groups differ), topo-sort both, then output the groups in group order with each group's items in item order. Either sort failing means `[]`.
- *Redundant Connection II (685):* directed, one parent per node. If some node has two parents, the answer is one of those two edges: skip the later one and union the rest; if a cycle still appears, the earlier edge was the culprit. If no node has two parents, return the first edge that closes a cycle.
- *Remove Max Edges to Keep Graph Fully Traversable (1579):* two DSUs, one per player. Shared (type 3) edges go first, kept once if they merge anything; then type 1 for Alice and type 2 for Bob. Answer = edges − kept, or −1 if either player's DSU still has more than one group.
- *Minimize Malware Spread (924):* union the adjacency matrix, count the infected nodes per root, and remove the infected node whose component has exactly one infected node and the largest size (ties: the smallest index; none: `min(initial)`).

### Say it in the interview

> "Prerequisites form a directed graph, and I need an order that respects every edge: a topological sort. The brute force rescans all edges for a course with nothing pending, O(V · (V + E)). I'll keep an indegree counter per course and a queue of courses at zero; taking a course only decrements its successors, so every edge is touched once, O(V + E). If fewer than n courses come out, the rest are stuck on a cycle."

> "Groups only ever merge, so I'll use union-find with path halving and union by size: amortised α(n) per operation, effectively constant. A union that finds both ends already under the same root is exactly the edge that closes a cycle."

Point at the `indegree[v] == 0` line, the `len(order) == n` check, and the `if ra == rb: return False` line: those three lines are the whole idea. Follow-ups to expect: *the smallest order?* (a heap instead of the deque), *is the order unique?* (no, if the queue ever holds two nodes at once), *show me the cycle* (DFS colours: when you meet a GRAY node, the GRAY path from it to the current node is the cycle), and *how fast is union-find?* (α(n) amortised, as above).

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Accounts Merge | `graphs/accounts_merge.py` | email → first account index; union on every repeat; bucket emails by root |
| Alien Dictionary | `graphs/alien_dictionary.py` | neighbouring words give one edge at their first difference; a word before its prefix → ""; Kahn |
| Checking Existence of Edge Length Limited Paths | `graphs/checking_existence_of_edge_length_limited_paths.py` | offline: sort queries by limit, union the edges lighter than it, answer in the original order |
| Course Schedule | `graphs/course_schedule.py` · `practice/simple/43_course_schedule.py` | Kahn: possible iff all n courses get popped |
| Course Schedule II | `graphs/course_schedule_ii.py` | Kahn's pop order is the answer; shorter than n means a cycle → [] |
| Critical Connections in a Network | `graphs/critical_connections_in_a_network.py` | Tarjan: tree edge (u, v) is a bridge iff low[v] > disc[u] |
| Find All People With Secret | `graphs/find_all_people_with_secret.py` | union one timestamp at a time; reset everyone not connected to person 0 |
| Find the Town Judge | `graphs/find_the_town_judge.py` | score = in-degree − out-degree; only the judge reaches n − 1 |
| Graph Valid Tree | `graphs/graph_valid_tree.py` | exactly n − 1 edges and no union fails |
| Largest Component Size by Common Factor | `graphs/largest_component_size_by_common_factor.py` | union each number with the first owner of each prime factor; count numbers per root |
| Minimize Malware Spread | `graphs/minimize_malware_spread.py` | removing a node saves its component only if it is the only infected one; pick the biggest (ties: smallest index; none: min(initial)) |
| Number of Connected Components in an Undirected Graph | `graphs/number_of_connected_components.py` | start at n; every successful union subtracts one |
| Number of Islands II | `graphs/number_of_islands_ii.py` | new land: +1, then −1 for each distinct neighbouring root it merges |
| Parallel Courses III | `graphs/parallel_courses_iii.py` | longest path in a DAG: push finish times forward in Kahn order |
| Reconstruct Itinerary | `graphs/reconstruct_itinerary.py` | Hierholzer: fly the smallest ticket, write an airport when stuck, reverse |
| Redundant Connection | `graphs/redundant_connection.py` · `practice/simple/47_redundant_connection.py` | the first union whose two ends already share a root |
| Redundant Connection II | `graphs/redundant_connection_ii.py` | a two-parent node? try dropping the later edge, else the earlier; otherwise the cycle edge |
| Remove Max Number of Edges to Keep Graph Fully Traversable | `graphs/remove_max_number_of_edges_to_keep_graph_fully_traversable.py` | two DSUs; shared edges first; removable = edges − kept |
| Sort Items by Groups Respecting Dependencies | `graphs/sort_items_by_groups_respecting_dependencies.py` | topo-sort items and groups separately; loners get their own group |

### Self-check

1. You reversed every edge in Course Schedule by mistake. Why does part I still pass while part II fails?
<details><summary>Answer</summary>Reversing every edge turns each cycle into a cycle and each acyclic graph into an acyclic graph, so "is there an order?" has the same answer. But the order you return is valid for the <em>reversed</em> graph: every course now comes out before its own prerequisites, so part II's answer is wrong.</details>

2. Kahn's algorithm stopped with `len(order) < n`. What can you say about the nodes left over?
<details><summary>Answer</summary>Each of them still has indegree at least 1, and every unfinished predecessor of a leftover node is itself a leftover. Walking backwards along those edges never has to stop, so in a finite graph it must repeat a node: there is a cycle among the leftovers. (Some leftovers may only sit downstream of the cycle.)</details>

3. What does `union(a, b)` returning False tell you, and which problems use exactly that?
<details><summary>Answer</summary>a and b were already connected before this edge, so the edge closes a cycle. Redundant Connection returns that edge, Graph Valid Tree fails on it, a component count ignores it, and Kruskal's MST (<a href="#s19">Graphs III</a>) skips it.</details>

4. When does union-find beat a BFS for "are a and b connected?"
<details><summary>Answer</summary>For a fixed graph and a single question, one BFS or DFS is simplest and just as fast. When edges arrive over time, when there are many questions between the arrivals, or when you need "the edge that closes a cycle", union-find wins: each operation is nearly O(1) and nothing is recomputed.</details>
