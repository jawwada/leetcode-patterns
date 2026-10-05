# Shortest Path Visiting All Nodes
*LeetCode 847 · Hard · Pattern: BFS over augmented states (position + bitmask/budget) · Reading time ~9 min*

## The problem

An undirected connected graph with n <= 12 nodes is given as adjacency lists. Return the length of the shortest walk
that visits every node at least once; you may start anywhere and revisit nodes and edges.

```text
Example: [[1,2,3],[0],[0],[0]] -> 4 via 1-0-2-0-3.
```

## What the problem is really asking

You get an undirected, connected graph with n nodes (n <= 12) as adjacency lists. Find
the length of the shortest walk that visits every node at least once. You may start at any
node, stop at any node, and reuse nodes and edges as often as you like. Every edge has
length 1.

The answer is a number of edges walked. Because revisits are allowed, this is not a
Hamiltonian path question (which would forbid revisits). It is a small Travelling Salesman
problem on an unweighted graph: the answer is a shortest walk, but "shortest" is measured
over a goal that depends on everything you have done so far.

```text
  the graph (a star)           how it is stored

          1                    graph = [[1, 2, 3],   node 0
          |                             [0],         node 1
      2 - 0 - 3                         [0],         node 2
                                        [0]]         node 3

  best walk: 1 - 0 - 2 - 0 - 3     4 edges
  node 0 is passed through twice; that is allowed
```

What makes it hard: the natural BFS on nodes is useless, because the target is not a node
but a condition ("every node seen"), and reaching node 0 a second time is not wasteful,
it is required.

## Do it by hand first

You would start at a leaf, because starting at the centre wastes a return trip. Start at 1.
Walk to 0. Now 2 and 3 are left; go to 2, come back to 0, go to 3. Four edges. Could three
work? Three edges touch at most four node-visits, and each leaf can only be reached through
0, so visiting three leaves needs 0 between every pair of them: leaf 0 leaf 0 leaf. That is
five node-visits, four edges.

```text
  step   at   visited so far
  ----   --   --------------
   0     1    {1}
   1     0    {0, 1}
   2     2    {0, 1, 2}
   3     0    {0, 1, 2}        same node as step 1,
   4     3    {0, 1, 2, 3}     different "visited so far"
```

Look at steps 1 and 3. Both stand on node 0. They are different situations, because at
step 3 the set of visited nodes is bigger. Your hand was tracking **the current node and
the set visited so far**. That pair is the seed of the solution.

## The first honest attempt

"A walk visits the nodes in some order of first appearance. Between two consecutive new
nodes, it should take a shortest path. So compute all-pairs distances with one BFS per
node, then try every order of the n nodes, summing distances between consecutive ones."

```text
  dist (star):        orders tried: n! = 24

       0  1  2  3     1,0,2,3 -> 1 + 1 + 2 = 4
    0  0  1  1  1     1,0,3,2 -> 1 + 1 + 2 = 4
    1  1  0  2  2     1,2,0,3 -> 2 + 1 + 1 = 4
    2  1  2  0  2     1,2,3,0 -> 2 + 2 + 1 = 5
    3  1  2  2  0     ...

  prefixes 1,2,0 and 2,1,0 both stand on node 0 having
  seen {0,1,2}: identical futures, extended separately
```

It is correct and costs O(n! x n). For n = 12 that is 479 million orders. The repeated
work: two partial orders that have visited the same *set* and stand on the same node have
exactly the same best continuation, yet every permutation of the prefix is extended on its
own. With k nodes in the prefix, there are up to (k-1)! copies of the same situation.

## The turning point

**Claim: the future of a partial walk depends only on (current node, set of visited
nodes). With n <= 12 the set is a 12-bit mask, so there are at most n x 2^n = 49,152
states, and one BFS over them finds the shortest walk.**

The order in which the visited nodes were first reached is irrelevant to what remains to
be done. What is left to do is "visit the nodes not in the mask, starting from here", and
that depends on the node and the mask alone.

So build the state graph. A state is `(u, mask)`. For every graph edge u - v there is a
state edge

```text
  (u, mask)  ->  (v, mask | 1 << v)       length 1
```

Moving to v adds v to the set (if it was already there, the mask does not change). All
edges have length 1, so BFS gives shortest distances in this state graph.

Three details make it work.

- **Start anywhere = multi-source BFS.** Seed the queue with all n states `(i, 1 << i)` at
  distance 0. That is one BFS instead of n separate ones, exactly like seeding every
  rotten orange at minute 0.
- **Goal = any state whose mask is full.** `full = (1 << n) - 1`. The code checks when a
  state is generated, returning `d + 1` the moment a neighbour completes the mask.
- **Visited is on the pair, not the node.** Node 0 with mask `0011` and node 0 with mask
  `0111` are different nodes of the state graph; both must be allowed. Only re-entering
  the *same* pair is cut.

Draw the state graph as the chapter keeps asking. It is layered by how many bits are set,
and BFS climbs toward the top layer:

```text
  the state space, grouped by mask (bit i = node i seen)

  top     1111  <- goal: any node here
           ^
  3 bits  0111 1011 1101          (u, mask) for u in mask
           ^
  2 bits  0011 0101 1001           masks with two or more
           ^                       leaves but no 0 (0110,
  1 bit   0001 0010 0100 1000      1110, ...) are unreachable
          start: all four, d = 0

  edges either stay in a mask (re-walking a seen node)
  or climb one level (seeing a new node)
```

The chapter's refrain again: the graph is not the star, it is the state. The star has 4
nodes; the state graph we search has up to 4 x 16 = 64.

## Watch it work

Masks are written as 4-bit strings, node 3 on the left, node 0 on the right: `0101`
means nodes 0 and 2 are visited.

```text
Frame 1  seed, d = 0
  queue: (0,0001) (1,0010) (2,0100) (3,1000)
  seen : 4 states
```

Every node is a starting point, each with only itself visited.

```text
Frame 2  expand d = 0 -> d = 1
  (0,0001) -> (1,0011) (2,0101) (3,1001)
  (1,0010) -> (0,0011)
  (2,0100) -> (0,0101)
  (3,1000) -> (0,1001)
  seen : 10 states
```

From the centre you reach each leaf; from each leaf you reach the centre. Node 0 now
appears in three different states.

```text
Frame 3  expand d = 1 -> d = 2
  (1,0011) -> (0,0011)  already seen
  (0,0011) -> (2,0111) (3,1011)
  (0,0101) -> (1,0111) (3,1101)
  (0,1001) -> (1,1011) (2,1101)
  seen : 16 states
```

Leaves can only go back to 0 with the same mask (already seen), so new states come from
the centre states, each adding a second leaf.

```text
Frame 4  expand d = 2 -> d = 3
  (2,0111) -> (0,0111)
  (3,1011) -> (0,1011)
  (3,1101) -> (0,1101)
  the other three d=2 states give the same three
  seen : 19 states
```

Every three-node state at a leaf must return to the centre, without changing its mask.

```text
Frame 5  expand d = 3
  pop (0,0111): neighbour 3 -> mask 1111 == full
  return d + 1 = 4
```

The first state that completes the mask is generated from depth 3, so the answer is 4.

Throughout, every state in the queue had depth equal to the number of edges walked, the
queue held at most two depths at once, and node 0 appeared in seven different states,
which is exactly the revisiting a node-only visited set would have forbidden.

## Why it is correct

Every walk in the original graph that starts at node s corresponds to a path in the state
graph starting at `(s, 1 << s)`, with the same number of edges: the mask at each step is
just the set of nodes the walk has touched so far, which is determined by the walk. The
walk visits every node exactly when its path ends at a state with a full mask.

So the answer is the distance from the set of start states to the nearest full-mask state.
Multi-source BFS computes distances from a set of sources: treat it as one virtual source
joined to every start by a zero-length edge. Because all real edges have length 1, the
depth at which a state is first discovered is its distance (layer property). States are
expanded in non-decreasing depth, so the first time any neighbour completes the mask, its
depth `d + 1` is minimal: any shorter completion would have come from a state of smaller
depth, which was expanded earlier. The graph is connected, so a full mask is always
reachable; the trailing `return -1` never runs. The single-node graph is handled first
(answer 0).

## Cost

- **Time O(n^2 x 2^n)**: n x 2^n states, each scanning up to n neighbours. For n = 12 that
  is at most about 600,000 neighbour checks.
- **Space O(n x 2^n)** for the visited set and the queue.
- The permutation brute force is O(n! x n), plus O(n x (n + E)) for all-pairs BFS.

## Variations you will meet

- **Weighted edges.** BFS no longer works on the state graph; use Dijkstra over the same
  `(node, mask)` states, or precompute all-pairs shortest distances and run the classic
  Held-Karp DP: `dp[mask][u] = min(dp[mask without u][v] + dist[v][u])`.
- **Must return to the start (a tour).** Fix the start node and add the distance back to it
  at the end. This is TSP proper; the same DP applies.
- **Visit every cell exactly once (Unique Paths III).** Revisits are forbidden, which
  breaks the "only the set matters" argument for counting distinct paths, and backtracking
  with a visited set is the standard tool.
- **Visit only a required subset.** Put only the required nodes in the mask and keep the
  rest as free nodes: the mask shrinks to 2^r while the node part stays n.

## What to carry forward

When the goal is "touch everything" on a small graph, the state is (where I am, what I have
touched), the mask makes the goal a single comparison, and multi-source seeding handles
"start anywhere". The next problem, the box-pushing puzzle, keeps the augmented state
(box position plus player position) but changes the edge weights: player walking is free
and only pushes cost, so BFS becomes 0-1 BFS with a deque.
