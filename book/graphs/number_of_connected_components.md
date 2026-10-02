# Number of Connected Components in an Undirected Graph
*LeetCode 323 · Medium · Pattern: Union-Find (disjoint set union) · Reading time ~11 min*

## What the problem is really asking

You get `n` nodes named `0..n-1` and a list of undirected edges. Count the groups: two nodes
are in the same group if you can walk from one to the other along edges. A node with no
edges at all is a group of one.

The answer is a single integer. You already know how to count islands with a flood fill,
and this is the same question on a graph. The new part is the tool. This problem introduces a data structure that the
next six problems all build on: **union-find**, also called a disjoint set union. It
answers one question, "are these two things already in the same group?", in close to
constant time. It also supports exactly one change: "glue these two groups together."

Our running example is `n = 6`, `edges = [[0,1],[2,3],[1,3],[4,5],[3,0]]`.

```text
  the graph                    adjacency lists
                               0: 1 3
    0 ---- 1                   1: 0 3
    |      |                   2: 3
    |      |                   3: 2 1 0
    3 ---- 2      4 ---- 5     4: 5
    (3-0 closes a loop)        5: 4

  groups: {0,1,2,3}  {4,5}     answer = 2
```

## Do it by hand first

Read the edges one at a time, with six coins on the table, one per node. Each coin starts
alone in its own pile. For each edge, push the two piles together, unless the two coins are
already in the same pile.

```text
  start      [0] [1] [2] [3] [4] [5]        6 piles
  0-1        [0 1] [2] [3] [4] [5]          5 piles
  2-3        [0 1] [2 3] [4] [5]            4 piles
  1-3        [0 1 2 3] [4] [5]              3 piles
  4-5        [0 1 2 3] [4 5]                2 piles
  3-0        same pile already, no change   2 piles
```

Your hand kept track of two things. First, **which pile each coin is in**. Second, **how
many piles there are**. A pile count starts at `n` and only goes down. It drops by exactly
one each time an edge joins two *different* piles. An edge inside one pile changes nothing.
That is the whole algorithm. All that is left is a way to answer "which pile is this coin
in?" quickly on a computer.

## The first honest attempt

Build adjacency lists. For every node, run a DFS with a fresh visited set, collect what it
reaches, and count the node only if it is the smallest id in what it reached. That way each
group is counted once.

```text
  DFS from 0 visits {0,1,2,3}   count it (0 is smallest)
  DFS from 1 visits {0,1,2,3}   skip       <- same walk
  DFS from 2 visits {0,1,2,3}   skip       <- same walk
  DFS from 3 visits {0,1,2,3}   skip       <- same walk
  DFS from 4 visits {4,5}       count it
  DFS from 5 visits {4,5}       skip       <- same walk
```

Each DFS costs `O(V + E)` and there are `V` of them, so the total is `O(V * (V + E))`. The
waste: a group of size `k` gets walked `k` times. One shared visited set fixes that
(`O(V + E)`, the flood-fill count you know), but it needs the whole graph up front. We take
another route, because the next problems feed edges one at a time and ask about
connectivity *while* they arrive.

## The turning point

**Claim: to count groups we never need paths. We only need, for each node, a name for its
group, and a way to merge two names.**

Here is how we store a group name cheaply. Every group elects one member as its
**root**. Every node keeps one number, `parent[x]`. A root points to itself. Every other
node points to some other member of its group, and following the pointers always ends at
the root. The groups are trees of arrows, and the whole structure is a **forest**. It
lives in one plain array.

```text
  parent array (index = node, value = who it points to)
  index:   0  1  2  3  4  5
  parent: [0, 0, 0, 2, 4, 4]

  the same thing drawn as a forest (arrows go up)
       0           4
      / \          |
     1   2         5
         |
         3
  roots are nodes with parent[x] == x: 0 and 4 -> 2 groups
```

Two operations run on it.

**find(x)** follows `parent` pointers until it reaches a node that points to itself, and
returns that root. Two nodes are in the same group exactly when `find` gives the same root
for both.

**union(a, b)** computes `ra = find(a)` and `rb = find(b)`. If they are equal, nothing
happens, because the nodes are already in one group. Otherwise it makes one root point at
the other: `parent[rb] = ra`. The second tree is now hanging under the first root. One
group has disappeared, so `count -= 1`.

Left alone, this can degrade. Union `0-1`, then `1-2`, then `2-3`, and each time hang the
old root under the new node, and you build a chain. Then `find` on the bottom node walks
the whole chain, which is `O(n)`. Two small rules fix it.

**Union by size (or rank).** When you merge two trees, hang the *smaller* tree under the
*larger* root. A node only gets deeper when its tree is the smaller side of a merge. Each
time that happens, the tree it lives in at least doubles in size. A tree can only double
`log n` times, so no node is ever deeper than `log n`. The solution file stores **rank**
instead of size. Rank is an upper bound on a tree's height. A tie bumps the winner's rank
by one, and otherwise the lower rank goes under. The guarantee is the same `log n`. In
every merge in our example, size and rank make the same choice. When there is a tie, the
code keeps the first endpoint's root on top.

**Path compression.** While `find` walks up, it re-points nodes closer to the root, so the
next walk is shorter. The code uses the compact form called *path halving*. It sets each
visited node's parent to its grandparent, then jumps there.

```text
  find(3) before          path halving step         after
       0                  parent[3] = parent[2]          0
       |                          = 0                  / | \
       2                  x = 0, a root: stop         1  2  3
       |
       3
```

With both rules together, a sequence of `m` operations costs `O(m * alpha(n))`. Here
`alpha` is the inverse Ackermann function, which is at most 4 for any `n` that fits in the
universe. In practice, constant.

## Watch it work

`n = 6`, `edges = [[0,1],[2,3],[1,3],[4,5],[3,0]]`, `count` starts at 6.

```text
Frame 1  edge 0-1: find(0)=0, find(1)=1, tie -> 1 under 0
  index:  0 1 2 3 4 5        0    2  3  4  5
  parent: 0 0 2 3 4 5        |
  rank:   1 0 0 0 0 0        1               count = 5
```
Two separate roots, so a real merge. Node 0 wins the tie and its rank grows to 1.

```text
Frame 2  edge 2-3: find(2)=2, find(3)=3, tie -> 3 under 2
  index:  0 1 2 3 4 5        0    2    4  5
  parent: 0 0 2 2 4 5        |    |
  rank:   1 0 1 0 0 0        1    3          count = 4
```
Same shape on the other pair. Now there are two trees of height 1.

```text
Frame 3  edge 1-3: find(1)=0, find(3)=2, ranks 1=1 -> 2 under 0
  index:  0 1 2 3 4 5          0       4  5
  parent: 0 0 0 2 4 5         / \
  rank:   2 0 1 0 0 0        1   2
                                 |
                                 3           count = 3
```
The edge touches non-roots, so we union their *roots*, not the nodes themselves. The tie
on rank makes root 0's rank 2.

```text
Frame 4  edge 4-5: find(4)=4, find(5)=5 -> 5 under 4
  index:  0 1 2 3 4 5          0        4
  parent: 0 0 0 2 4 4         / \       |
  rank:   2 0 1 0 1 0        1   2      5
                                 |
                                 3           count = 2
```
A third tree forms. It is separate from the first one.

```text
Frame 5  edge 3-0: find(3) walks 3->2->0, halving on the way
  index:  0 1 2 3 4 5          0        4
  parent: 0 0 0 0 4 4        / | \      |
  rank:   2 0 1 0 1 0       1  2  3     5
  find(0)=0 == find(3)=0 -> same group, skip    count = 2
```
The edge is inside one group, so the count stays. Notice that `find(3)` also flattened the
tree as a side effect: `parent[3]` went from 2 to 0.

What stayed true in every frame: the number of self-pointing roots equals `count`, and two
nodes are in the same group exactly when they share a root. Compression only re-pointed
nodes to another member of the same tree, so no group ever changed because of it.

## Why it is correct

Before any edge is read, there are `n` singleton groups and `count = n`. That is right for a
graph with no edges. Suppose the forest's groups are exactly the components of the edges
read so far, and we read edge `u-v`. If `find(u) == find(v)`, then `u` and `v` were already
connected, so the components do not change and we leave everything alone. If the roots
differ, then the edge joins two components that were separate. The new graph has exactly
those two merged, and nothing else changes. Pointing one root at the other does precisely
that, and `count` drops by one. Path compression never moves a node out of its tree. It
only points the node at an ancestor. So the invariant "trees = components, count = number
of trees" survives every step. After the last edge, `count` is the answer.

## Cost

- Time `O(n + E * alpha(n))`. We need `O(n)` to build the array, plus one pair of finds and
  at most one link per edge, and each is near-constant with rank plus compression.
- Space `O(n)`. That is the `parent` and `rank` arrays. No adjacency list is ever built.
- For comparison, a DFS with a shared visited set is `O(n + E)` time and `O(n + E)` space.
  It is just as fast, but it needs the whole graph stored first.

## Variations you will meet

- **Shared-visited DFS/BFS.** Build adjacency lists and count how many times you launch a
  traversal from an unvisited node. Use this when the graph is given in full and you also
  need paths or orders.
- **Edges arrive as a stream.** "Report the component count after each edge" is where
  union-find wins outright, because a DFS would have to restart each time. Number of
  Islands II, later in this chapter, is exactly this on a grid.
- **Component sizes.** Keep `size[root]` and add the two sizes on every union. Then "how big
  is my group?" is one `find` away. This shows up in Minimize Malware Spread.

## What to carry forward

Union-find is a parent-pointer forest. `find` names your group, and `union` glues two groups
and lowers the count by one, but only when the roots differ. The next problem, Graph Valid
Tree, asks what it means when a union does *not* happen: that failed union is a cycle.
