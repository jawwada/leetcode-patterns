# Checking Existence of Edge Length Limited Paths
*LeetCode 1697 · Hard · Pattern: Union-Find (disjoint set union) · Reading time ~10 min*

## What the problem is really asking

You have an undirected graph on `n` nodes. Each edge has a length, and there may be
several edges between the same pair. Then comes a batch of queries `[p, q, limit]`: is
there a path from `p` to `q` that uses **only** edges strictly shorter than `limit`?
Return one boolean per query, in the order the queries were given.

Note what is *not* asked. The path's total length does not matter. A path of a hundred
edges is fine as long as each single edge is short enough. So every query is really a
connectivity question on a filtered graph: delete every edge of length `>= limit`, then
ask whether `p` and `q` are still in the same component.

What makes it hard is that every query filters at a different level, and there can be
`10^5` edges and `10^5` queries.

The example we will trace: a path of five nodes.

```text
         10       5       9       13
   (0) ----- (1) ----- (2) ----- (3) ----- (4)

   queries               filtered graph            answer
   q0 [0, 4, limit 14]   all four edges kept       true
   q1 [1, 4, limit 13]   13 is NOT < 13: 3-4 cut   false
   q2 [1, 3, limit 6]    only the 5-edge kept      false
```

## Do it by hand first

Take query `q1 = [1, 4, 13]`. A person crosses out every edge of length 13 or more, then
looks at what is left:

```text
   limit 13:  keep 10, 5, 9      cut 13

   (0) ----- (1) ----- (2) ----- (3)       (4)
   \_______________________________/       \_/
          one blob                         alone
   1 and 4 in different blobs -> false
```

Now do `q0` with limit 14. You do not start over. You look at your previous drawing, notice
that the only change is that the 13-edge is now allowed, draw it in, and see 1 and 4 join.

That is the observation your hand made without being told: going from a smaller limit to a
larger one only **adds** edges. The blobs from the smaller limit are still valid; they can
only merge. What your hand kept track of was "the blobs so far", and it grew them.

## The first honest attempt

Answer each query independently: build the adjacency list of edges with length `< limit`,
run a BFS or DFS from `p`, and check whether `q` was reached.

Each query costs `O(n + E)`, so all of them cost `O(Q * (n + E))`. With `10^5` of each that
is `10^10`. Hopeless.

Where is the waste? Sort the queries by limit in your head and look at consecutive ones:

```text
   query  limit  edges allowed     what its BFS discovers
   q2       6    {5}               1-2
   q1      13    {5, 9, 10}        1-2 (again), 2-3, 0-1
   q0      14    {5, 9, 10, 13}    1-2, 2-3, 0-1 (again), 3-4
                                   ^^^^^^^^^^^^^^^^^^^^^
   each query rebuilds every merge the previous query made
```

Each query's graph contains the previous query's graph. Yet each BFS pays from scratch for
components that were already known. With many queries at nearly the same limit, almost the
entire cost of each BFS is rediscovering what the previous BFS already found.

## The turning point

**Claim: as the limit grows, the filtered graph only gains edges, so its components only
merge. Answer the queries in increasing order of limit while growing one union-find, and
no work is ever repeated.**

Justification: if `limit1 <= limit2`, every edge with length `< limit1` also has length
`< limit2`. So the edge set at `limit2` contains the edge set at `limit1`, and any two
nodes connected at `limit1` are still connected at `limit2`. Union-find is exactly the
structure that supports "add an edge" and "are these two connected?" cheaply, and the one
thing it cannot do, splitting, is never needed if we only move the limit upward.

But the queries arrive in an arbitrary order. That is where the second idea comes in:
**offline processing**. The problem gives us all queries up front, and the answers do not
depend on each other. So we are free to answer them in whatever order suits us, as long as
we write each answer back into its original slot.

The algorithm, as a sweep along the weight axis:

1. Sort the edges by length.
2. Sort the query **indices** by limit (sorting indices, not the queries themselves, is
   what lets us write `ans[i]` into the right slot).
3. Keep a pointer `j` into the sorted edges, starting at 0, and a fresh union-find.
4. For each query index `i` in limit order: while `edges[j]` has length strictly less than
   this query's limit, union its endpoints and advance `j`. Then
   `ans[i] = find(p) == find(q)`.

```text
   the weight axis
   0    5    6    9   10   13   14
   |----e----|----e----e----e----|
             ^ q2           ^q1  ^ q0
   edges left of a flag are glued in before that flag answers
   (13 sits ON q1's flag: not strictly less, not glued yet)
```

Each edge is unioned exactly once over the whole run, because `j` never moves backward.
Each query does two finds. The only real cost left is the two sorts.

This is the first problem in the chapter where the order of the input is something *you*
choose. The pattern is general: when queries are monotone in some parameter and the
structure supports only one direction of change (union-find adds, never removes), sort the
queries so the parameter moves in that one direction.

## Watch it work

Sorted edges: `1-2 (5)`, `2-3 (9)`, `0-1 (10)`, `3-4 (13)`. Query order by limit:
`q2 (6)`, `q1 (13)`, `q0 (14)`. The solution unions with `parent[find(u)] = find(v)`.

```text
Frame 1   start
   edges  [1-2:5] [2-3:9] [0-1:10] [3-4:13]
           ^ j=0
   node    0  1  2  3  4
   parent  0  1  2  3  4      ans = [?, ?, ?]
```
No edges glued yet; queries will be answered in the order q2, q1, q0.

```text
Frame 2   q2 = [1, 3, limit 6]
   5 < 6  -> union(1, 2), j=1      9 < 6? no, stop
   parent  0  2  2  3  4
   find(1)=2  find(3)=3  -> ans[2] = false
```
Only the 5-edge is below 6; 1 and 3 are in different blobs.

```text
Frame 3   q1 = [1, 4, limit 13]
   9  < 13 -> union(2, 3), j=2
   10 < 13 -> union(0, 1), j=3
   13 < 13? no, stop
   parent  3  3  3  3  4
```
Nodes 0 to 3 are one blob rooted at 3; the 13-edge waits.

```text
Frame 4   answer q1
   find(1)=3   find(4)=4  -> ans[1] = false
   ans = [?, false, false]
```
Strictly less matters: with `<=` this would wrongly say true.

```text
Frame 5   q0 = [0, 4, limit 14]
   13 < 14 -> union(3, 4), j=4 (all edges used)
   parent  4  3  3  4  4      (find(0) halved 0's link)
   find(0)=4  find(4)=4  -> ans[0] = true
   return [true, false, false]
```
The last edge joins everything, and the answers land in original order.

Across the frames the pointer `j` and the union-find only moved forward; nothing was ever
undone or recomputed. Every query saw exactly the edges below its own limit, no more and
no fewer.

## Why it is correct

Invariant: when query `i` with limit `L` is answered, the union-find contains exactly the
edges of length `< L`.

The edges are sorted by length, and the inner loop adds edges while their length is `< L`,
stopping at the first one that is not. So after the loop, all edges before `j` have length
`< L` and all edges from `j` on have length `>= L`. Because queries are processed in
non-decreasing limit, the edges added for earlier queries all have length below an earlier
limit, hence below `L` too, so nothing wrong was glued in earlier. That establishes the
invariant.

Given the invariant, the standard union-find property (same root if and only if connected
by the edges added) says `find(p) == find(q)` exactly when a path of edges shorter than `L`
joins them. Writing into `ans[i]` keeps the original order. Parallel edges are harmless:
the second union of an already-joined pair does nothing.

## Cost

- **Time `O(E log E + Q log Q + (E + Q) * alpha(n))`**: two sorts, then each edge is unioned
  once and each query does two finds.
- **Space `O(n + Q)`**: the parent array, the sorted index list and the answers (plus the
  sorted copy of the edges).
- **Brute force** was `O(Q * (n + E))`; sharing one growing union-find across all queries is
  what removes the factor `Q`.

## Variations you will meet

- **Online queries (LeetCode 1724, the follow-up).** If queries arrive one at a time and
  you may not reorder them, you cannot sweep. Build a minimum spanning forest once; then the
  answer is "is the heaviest edge on the forest path from `p` to `q` below `limit`?", which
  needs a persistent union-find or binary lifting over the forest.
- **Minimum limit that connects `p` and `q`.** Same sweep, but stop at the first edge whose
  union joins them; that edge's weight is the answer. This is the "bottleneck path" and it
  is exactly what Swim in Rising Water asks, later in the chapter.
- **Number of pairs connected below each limit.** Keep component sizes in the union-find;
  each union of sizes `a` and `b` adds `a * b` new connected pairs.
- **Edges with length `<= limit`.** Change one comparison. It is the most common bug here,
  so read the statement twice.

## What to carry forward

When queries are monotone in a threshold and union-find can only grow, answer them offline
in threshold order with one sweep pointer. The next problem keeps the greedy edge sweep but
runs two union-finds side by side, one per player, over edges that one or both may use.
