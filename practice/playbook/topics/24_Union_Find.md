## Union-Find (Disjoint Set Union)

Each connected component has a representative root. `find(x)` returns that root. `union(a, b)` merges two different roots; it returns False if the roots already match. Link roots, and use union by size plus path compression to keep paths short.

<!-- cell -->

Union-find answers "are a and b in the same group?" while groups keep merging. After `union(0, 1)`, `union(2, 3)` and `union(1, 3)`, nodes 0 and 3 share a root, so `union(0, 2)` returns False: they were already together. "Merge the two groups" is `parent[find(b)] = find(a)`, which links roots and never the nodes themselves. Path halving makes each node on the way up point at its grandparent, and union by size hangs the smaller tree below the bigger one.

<!-- cell -->

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

<!-- cell -->

**Try it**
- On a fresh `DSU(6)` do the unions `(0, 1)`, `(2, 3)`, `(1, 3)`, print `parent`, call `find(3)`, and print again: `[0, 0, 0, 2, 4, 5]` becomes `[0, 0, 0, 0, 4, 5]`. Node 3 now points at its old grandparent, the root.
- Link nodes instead of roots: change `self.parent[rb] = ra` to `self.parent[b] = a`. Then `d = DSU(3); d.union(0, 1); d.union(2, 1); print(d.find(0) == d.find(1))` prints False: node 1 was pulled out from under 0.
- Print `dsu.size`: `[4, 1, 2, 1, 1, 1]`. Only a root's entry means something; `size[2] = 2` is left over from when 2 was a root.
- Delete the two `if ra == rb` lines and rerun the cell: the last union returns True and `count` drops to 2, although the groups are still `{0, 1, 2, 3}`, `{4}` and `{5}`.

<!-- cell -->

In an interview, two functions are enough. Path halving alone keeps `find` fast in practice; add union by size if you are asked for the guarantee:

```py
parent = list(range(n))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]      # path halving: skip to the grandparent
        x = parent[x]
    return x

def union(a, b):                           # False: a and b were already connected
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    parent[ra] = rb
    return True
```

<!-- cell -->

### Trace merging roots

<!-- cell -->

```python
def trace_redundant(edges):                       # nodes are 1..n
    dsu = DSU(len(edges) + 1)
    for u, v in edges:
        merged = dsu.union(u, v)
        print(f"edge {u}-{v}: {'merge' if merged else 'already connected -> redundant'}  parent[1:]={dsu.parent[1:]}")
        if not merged:
            return [u, v]
```

<!-- cell -->

```python
print(trace_redundant([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))
```

<!-- cell -->

```python
d = DSU(3)

assert d.union(0, 0) is False and d.count == 3                      # a node is already with itself

assert d.union(0, 1) and d.union(1, 2) and d.count == 1
```

<!-- cell -->

### Count components and recognize a tree

<!-- cell -->

```python
def valid_tree(n, edges):                         # exactly n - 1 edges, and none of them closes a cycle
    dsu = DSU(n)
    return len(edges) == n - 1 and all(dsu.union(u, v) for u, v in edges)

def count_components(n, edges):                   # start with n groups; every real merge removes one
    dsu = DSU(n)
    for u, v in edges:
        dsu.union(u, v)
    return dsu.count

print(valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]), valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]))   # True False

print(count_components(5, [[0, 1], [1, 2], [3, 4]]))                                                           # 2
```

<!-- cell -->

Union-find takes over when groups come from shared keys. Accounts Merge gives accounts as a name followed by emails and merges any two that share an email, since one person owns both; a shared name proves nothing. Below, the two Johns who share `b@m` merge, and the John with only `x@m` stays apart. Instead of comparing every pair of accounts, O(n²), each email remembers the *first* account that listed it, every later account with that email is unioned with it, and the emails are finally bucketed by their group's root.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Print `owner` and `dsu.parent` after the first loop: `b@m` belongs to account 0, and account 0 now hangs under account 1. The two Johns who share nothing stay apart, although they have the same name.
- Delete the `else:` branch (never record an owner): the result is `[]`. `owner` is both the shared-email detector and the list of emails to print.
- Run `accounts_merge([["A", "x"], ["A", "y"], ["A", "x", "y"]])`: `[['A', 'x', 'y']]`. The third account bridges two that share nothing.

<!-- cell -->

Some problems only need the groups: union everything first, then do one thing per component. Smallest String With Swaps lets you swap the letters at any listed pair of indexes, as often as you like, and asks for the smallest string you can reach: `"dcab"` with the pairs `[0, 3]` and `[1, 2]` becomes `"bacd"`. Swaps chain, so the letters inside a component can be put in *any* order, and the answer sorts them.

Most Stones Removed lets you remove a stone that shares a row or a column with another stone still on the board, and asks for the most stones you can remove: 5 of the 6 stones below. A stone glues its row to its column, and every group of stones can be cleared down to one stone, so the answer is the number of stones minus the number of groups.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Print `dict(groups)` for `"dcab", [[0, 3], [1, 2]]`: `{0: [0, 3], 1: [1, 2]}`. Index 0 can only trade with index 3, so sorting the whole string (`"abcd"`) would be wrong; the answer is `"bacd"`.
- Forget the column offset (`dsu.union(r, c)`): `remove_stones([[0, 1], [1, 2]])` answers 1 instead of 0, because column 1 got glued to row 1.
- `remove_stones([[0, 0], [5, 5]])` is 0: two stones that share neither a row nor a column.

<!-- cell -->

The last union-find variation counts groups while they form. Number of Islands II turns water into land one cell at a time and asks for the island count after every step: on a 3 × 3 grid, adding (0, 0), (0, 1), (1, 2) and (2, 1) gives `[1, 1, 2, 3]`. Recounting the grid each time repeats almost all the work. Instead, a new cell is a new island, +1, and it swallows each *different* neighbouring island, −1 per successful union.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Remove the duplicate guard (make the `if` always true): `num_islands_2(3, 3, [[0, 0], [0, 0]])` reports `[1, 2]`, a second island that does not exist.
- Decrement for every land neighbour (drop the `if ra != rb`): `num_islands_2(2, 2, [[0, 0], [0, 1], [1, 0], [1, 1]])` gives `[1, 1, 1, 0]`. The last cell's two neighbours were already one island.
- Print `{cell: find(cell) for cell in parent}` at the end of the second example: all four cells report the same root.
