# Min Cost to Connect All Points (LeetCode 1584)

**Area:** graphs · **Difficulty:** Medium · **Key operations:** heap pop the cheapest outside point, skip stale entries, add it to the tree, push its distances to every outside point

## Problem

You are given `n` points on a plane. The cost of connecting two points is their Manhattan distance `|x1 - x2| + |y1 - y2|`. Return the minimum total cost to make all points connected: the weight of a minimum spanning tree of the complete graph on the points.

## Example

```
points = [[0,0],[2,2],[3,10],[5,2],[7,0]] -> 20

          2 (3,10)
          .
          .
   1 (2,2)   3 (5,2)
0 (0,0)         4 (7,0)

edges used: 0-1 (4), 1-3 (3), 3-4 (4), 1-2 (9)    total 20
```

## Brute force

Kruskal: list all `n(n-1)/2` edges with their Manhattan weights, sort them, and walk them cheapest first, accepting an edge whenever its endpoints are in different components (a union-find answers that). The accepted edges form the minimum spanning tree.

O(n² log n) time and O(n²) space, dominated by building and sorting the full edge list. The wasted work: every edge is materialised and sorted although at any moment only the cheapest edge *leaving the current tree* can be the next one chosen.

## From brute force to optimal

Grow one tree from an arbitrary start. The cut property says the cheapest edge from the tree to any outside point is always safe to add. So all we need is "the cheapest known edge from the tree to each outside point", kept in a min-heap of `(cost, point)`. When a point joins the tree it pushes its distance to every point still outside; the heap top is then the next point to add. Entries for points that joined via a cheaper edge in the meantime are stale and are skipped when popped. This is Prim's algorithm; it never sorts the whole edge list.

## Intuition

Picture the points on graph paper and the tree as a growing blob. At each step draw the shortest possible line from the blob to a point outside it and absorb that point. The heap is the sorted pile of candidate lines from the blob's current members to the outside; the shortest valid one is always on top. A stale entry is a line to a point that was already absorbed by an even shorter line, so it is simply discarded. Note what the key is: the length of *one* edge, not a path length from the start. Prim is not Dijkstra.

## Walkthrough

Heap shown as its array (smallest at index 0). Point 0 joins for free.

```
pop (0,0)    add 0 (0,0) cost 0   total 0    tree {0}
             push 0->1 4, 0->2 13, 0->3 7, 0->4 7        heap [(4,1),(7,4),(7,3),(13,2)]
pop (4,1)    add 1 (2,2) cost 4   total 4    tree {0,1}
             push 1->2 9, 1->3 3, 1->4 7                 heap [(3,3),(7,3),(7,4),(9,2),(7,4),(13,2)]
pop (3,3)    add 3 (5,2) cost 3   total 7    tree {0,1,3}
             push 3->2 10, 3->4 4                        heap [(4,4),(7,4),(7,3),(9,2),(13,2),(10,2),(7,4)]
pop (4,4)    add 4 (7,0) cost 4   total 11   tree {0,1,3,4}
             push 4->2 14                                heap [(7,3),(7,4),(7,4),(9,2),(13,2),(10,2),(14,2)]
pop (7,3)    STALE, 3 already in tree, skip
pop (7,4)    STALE, skip
pop (7,4)    STALE, skip
pop (9,2)    add 2 (3,10) cost 9  total 20   tree {0,1,2,3,4}   joined == n -> return 20
```

## Steps

1. `in_tree = [False] * n`, `heap = [(0, 0)]`, `total = joined = 0`.
2. While `joined < n`: pop `(cost, i)`.
3. If `in_tree[i]`, the entry is stale: skip it.
4. Mark `i` in the tree, `total += cost`, `joined += 1`.
5. For every point `j` not in the tree, push `(manhattan(i, j), j)`.
6. Return `total`.

## Complexity

O(n² log n) time: each of the `n` joins pushes up to `n` entries and every push and pop costs log of the heap size. O(n²) space for the heap in the worst case. (An array-based Prim that scans for the minimum is O(n²) time and O(n) space, which is optimal on this dense graph; the heap version is what interviews usually expect.)

## Pitfalls

- **Adding `cost` to the pushed key (Dijkstra confusion).** The key must be the single edge's length. Accumulating the cost the current point paid orders candidates by path length from the start and picks the wrong edges: `[[0,0],[10,0],[1,1],[11,1]]` gives 24 instead of 14.
- **`while joined < n - 1`.** A tree has `n - 1` edges but `n` points must join (the start joins for free). Stopping early leaves the last point out.
- **Dropping an `abs`.** `abs(dx) + dy` can be negative; the tree then takes bogus cheap edges.
- **Not skipping stale entries.** Popping a point that is already in the tree and adding its cost again overcounts; the `in_tree` check must come before `total += cost`.
- **Euclidean instead of Manhattan.** The problem defines cost as `|dx| + |dy|`.
