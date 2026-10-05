# Redundant Connection (LeetCode 684)

**Area:** graphs / union find · **Difficulty:** Medium · **Key operations:** find the root of each endpoint, compare roots, union by attaching one root under the other

## Problem

A tree with `n` nodes labelled `1..n` had one extra edge added, so you are given `n` undirected edges. Return the edge that can be removed so the graph becomes a tree again. If several edges would work, return the one that appears last in the input.

## Example

```
edges = [[1,2],[2,3],[3,4],[1,4],[1,5]] -> [1,4]

   1 --- 2
   |     |      5 hangs off 1
   4 --- 3

The cycle is 1-2-3-4-1. Of its four edges, [1,4] appears last in the input.
```

## Brute force

Process the edges in order. Before adding edge `(u, v)`, run a BFS over the edges added so far to test whether `v` is already reachable from `u`. The first edge whose endpoints are already connected closes the cycle and is the answer.

O(n²) time (`n` checks, each walking up to `n` nodes), O(n) space. The wasted work: every check re-walks the same growing component from scratch instead of remembering which nodes were already joined.

## From brute force to optimal

The only question ever asked is "are `u` and `v` already in the same component?", and components only ever *merge*, never split. A disjoint-set union answers that in near-constant time: `find(x)` returns the representative (root) of `x`'s component, `union` attaches one root under the other. Each edge then costs two finds and at most one union, and the first edge whose endpoints share a root is the one that closes the cycle. Because exactly one extra edge was added, that edge is also the last cycle edge in input order, which is what the problem asks for.

## Intuition

Picture each node as an island flying a flag, where the flag is the root of its group. A new edge between islands flying different flags is a bridge joining two groups: lower one flag by pointing that root at the other. A new edge between islands already flying the same flag would be a second route between them, so it closes a loop and is the redundant one. `find` follows parent pointers up to the flag; path compression re-points nodes closer to the root as it climbs, so later lookups are shorter.

## Walkthrough

`parent[1..5]` after each step; a node whose parent is itself is a root.

```
start                                        parent [1, 2, 3, 4, 5]
edge (1,2): find(1)=1  find(2)=2  differ -> parent[2]=1   parent [1, 1, 3, 4, 5]
            1          roots: 1 3 4 5
            |
            2
edge (2,3): find(2)=1  find(3)=3  differ -> parent[3]=1   parent [1, 1, 1, 4, 5]
            1
           / \
          2   3
edge (3,4): find(3)=1  find(4)=4  differ -> parent[4]=1   parent [1, 1, 1, 1, 5]
            1
          / | \
         2  3  4
edge (1,4): find(1)=1  find(4)=1  SAME ROOT -> (1,4) closes a cycle, return [1,4]
```

Edge `(1,5)` is never examined.

## Steps

1. `parent = list(range(n + 1))`, nodes are `1..n` so index 0 is unused.
2. `find(x)`: while `parent[x] != x`, set `parent[x] = parent[parent[x]]` (compression) and move `x` up; return `x`.
3. For each edge `(u, v)` in input order: `ru, rv = find(u), find(v)`.
4. If `ru == rv`, return `[u, v]` in its input orientation.
5. Otherwise `parent[rv] = ru`.

## Complexity

O(n α(n)) time, effectively linear: path compression makes each `find` amortised near-constant. O(n) space for the parent array.

## Pitfalls

- **Comparing parents instead of roots (`parent[u] == parent[v]`).** Two nodes of one component can have different parents (`3 -> 2 -> 1` and `1`), so the cycle edge is missed and a root gets re-parented.
- **Attaching the node instead of its root (`parent[v] = ru`).** That cuts `v` off from its old component and forgets earlier connections; `[[1,2],[3,2],[1,3]]` then finds no cycle at all.
- **Array of size `n`.** Nodes are labelled `1..n`, so `find(n)` raises `IndexError`; allocate `n + 1`.
- **Returning `[ru, rv]`.** The answer must be the edge as given, `[u, v]`.
- **Relying on "last in input" for a general graph.** Taking the first cycle-closing edge is correct only because exactly one extra edge was added.
