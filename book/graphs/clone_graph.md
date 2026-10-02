# Clone Graph
*LeetCode 133 · Medium · Pattern: Graph traversal with old->new node map · Reading time ~8 min*

## What the problem is really asking

You are handed a pointer to one node of a connected, undirected graph. Each node has a value
(`1..n`, unique) and a list of neighbour pointers. Return a pointer to the matching node of a
**deep copy**: a second graph built entirely from new node objects, with the same values and
the same edges, sharing no object with the original.

The answer is a graph, not a number. What makes it more than a loop is that the graph has
cycles and shared neighbours, so the same original node is reached along many edges, and it
must still map to **one** copy.

```text
  the graph (a 4-cycle)          how it is stored
                                 node 1: neighbors [2, 4]
      1 ----- 2                  node 2: neighbors [1, 3]
      |       |                  node 3: neighbors [2, 4]
      |       |                  node 4: neighbors [1, 3]
      4 ----- 3
                                 every edge appears twice:
  you get: a pointer to node 1   once in each endpoint's list
```

The copy must look identical, edge for edge, but if you compare any copied node with any
original using `is`, the answer must be `False`.

## Do it by hand first

Copy the square on paper. Start at node 1: draw a new circle `1'`. Node 1 points to 2 and 4,
so draw `2'` and `4'` and connect `1'` to both. Move on to 2: it points to 1 and 3. Is there
already a `1'`? Yes, you drew it. Do not draw another one; connect `2'` to the existing
`1'`. There is no `3'` yet, so draw it and connect. Move to 4: it points to 1 and 3, and both
copies exist already, so just connect. Finally 3: both its neighbours have copies, connect.

```text
  original              copy, with the "already drawn?" lookups
  1 --- 2               1'--- 2'      2 -> 1 : 1' exists, reuse
  |     |               |     |       4 -> 1 : 1' exists, reuse
  4 --- 3               4'--- 3'      4 -> 3 : 3' exists, reuse
```

The question you kept asking was "**have I already drawn the copy of this node, and where is
it?**". Your eye answered it by looking at the page. In code that question is a dictionary
from original node to copy. It is the seed of the whole solution.

## The first honest attempt

Do it in passes. Pass 1: walk the graph and collect every original node in a list. Pass 2:
create one new node per original, same value, in a parallel list. Pass 3: for every original
edge `u -> v`, find the copy of `v` by scanning the list of copies for a node with value
`v.val`, and append it to the copy of `u`.

```text
  copies = [ 1'  4'  3'  2' ]   (DFS discovery order)

  wiring 2' -> 3 : scan 1' no, 4' no, 3' yes   3 steps
  wiring 3' -> 2 : scan 1' no, 4' no, 3' no,
                   2' yes                       4 steps
  every one of the 2E edge ends repeats a scan
  of up to V nodes
```

Correct, but `O(V*E)`. The repeated work is the scan: the same question, "which copy belongs
to this original?", is answered by linear search over and over, for the same nodes, once per
edge end that touches them.

## The turning point

**Claim: one hash map from original node to its copy answers "which copy?" in `O(1)`, and the
same map is the visited set that keeps the traversal from looping on cycles.**

The first half is plain: "original -> copy" is a key-value lookup, so use a dictionary keyed
by the node object itself (objects hash by identity in Python, so values need not even be
unique).

The second half is the real insight. A graph traversal needs a visited set, or the cycle
1-2-3-4-1 sends it round forever. Our map already contains exactly the nodes we have met.
"Has `v` been seen?" is `v in clones`. One structure does both jobs, so cloning and wiring
can happen in **one** traversal instead of three passes.

Here is the rule for each original node `u` we pop, and each neighbour `v` of `u`:

1. If `v` has no copy yet, create `clones[v]` and enqueue `v` (we still have to wire `v`'s
   own neighbour list later).
2. Append `clones[v]`, the copy, never `v`, to `clones[u].neighbors`.

Step 2 runs for **every** edge end, new or seen; step 1 only on first sight. Because each
node is popped once and wires its whole neighbour list once, every original adjacency list is
copied exactly once, in the same order.

BFS or DFS? Either works; the map is what matters. The solution uses a BFS queue, so below
the queue and the layer are drawn, but nothing here depends on distance.

## Watch it work

The square, starting from node 1. `map` lists the originals that have a copy. Copies are
primed: `1'` is the copy of `1`.

```text
Frame 1   setup, layer 0
  map  = { 1:1' }
  q    = [ 1 ]
  1'.n = [ ]
```
The entry node gets its copy before the loop, so the map already marks it as seen.

```text
Frame 2   pop 1 (layer 0)
  v=2: new -> create 2', enqueue
  v=4: new -> create 4', enqueue
  map  = { 1:1', 2:2', 4:4' }
  q    = [ 2 4 ]          <- layer 1
  1'.n = [ 2' 4' ]
```
Both neighbours are first sightings, so both get copies and join the queue.

```text
Frame 3   pop 2 (layer 1)
  v=1: in map -> reuse 1'
  v=3: new -> create 3', enqueue
  map  = { 1, 2, 4, 3 }   (all copied)
  q    = [ 4 3 ]          <- 3 is layer 2
  2'.n = [ 1' 3' ]
```
The edge back to 1 does not create a second `1'`; it reuses the one in the map.

```text
Frame 4   pop 4 (layer 1)
  v=1: in map -> reuse 1'
  v=3: in map -> reuse 3'
  q    = [ 3 ]
  4'.n = [ 1' 3' ]
```
Node 3 was discovered by 2 a moment ago, so 4 only wires to it; it is not enqueued twice.

```text
Frame 5   pop 3 (layer 2) -> done
  v=2: reuse 2'    v=4: reuse 4'
  q    = [ ]
  3'.n = [ 2' 4' ]

  copy:  1'--- 2'       return clones[1] = 1'
         |     |
         4'--- 3'
```
The queue is empty; every copied list matches its original, and we return the copy of the
entry node.

Invariant across the frames: every original node in the queue or already popped has exactly
one copy in the map, and every popped node's copy has its full neighbour list.

## Why it is correct

Three facts.

**One copy per original.** A copy is created only inside `if v not in clones`, and the
entry node's copy is created before the loop. So each original is copied at most once; since
the graph is connected and BFS reaches every node, exactly once.

**Every edge copied, in place.** Each original node is enqueued exactly once (at the moment
its copy is created) and therefore popped exactly once. When it is popped, the loop walks its
whole neighbour list and appends the copy of each neighbour. So `clones[u].neighbors` ends up
as the image of `u.neighbors` under the map: same length, same order.

**No sharing.** Only copies are ever appended to copies' lists; originals never appear in
the new graph.

Together: the map is a bijection between old and new nodes that preserves every edge, which
is the definition of an identical but separate graph.

## Cost

- **Time `O(V + E)`**: each node is created and popped once; each of the `2E` list entries
  is handled once with an `O(1)` map lookup.
- **Space `O(V)`**: the map holds `V` entries and the queue at most `V` nodes (not counting
  the copy itself, which is the output).

## Variations you will meet

- **Copy List with Random Pointer (LeetCode 138).** A linked list whose nodes also have a
  `random` pointer is a graph with out-degree two. Same map, same rule. A famous `O(1)`-space
  trick interleaves copies into the list instead of using a map.
- **Clone a binary tree with random pointers, or an N-ary tree.** Same map; with a pure
  tree you could skip it, because every node is reached once.
- **Recursive DFS version.** `clone(u)`: if `u` in map return it; else create, store **before**
  recursing (or a cycle recurses forever), then fill neighbours with `clone(v)`.
- **Graph is not connected.** You would need a list of all nodes and an outer loop over them,
  the same shape as Number of Connected Components later in the chapter.

## What to carry forward

When nodes can be reached by many paths, keep a map from original to "my result for it"; the
map is both the memo and the visited set. The next problem, Word Ladder, goes further: the
graph is not handed to you at all, and you must generate each word's neighbours on the fly.
