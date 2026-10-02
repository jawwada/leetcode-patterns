# Jump Game IV
*LeetCode 1345 · Hard · Pattern: BFS on implicit graph with value buckets consumed once · Reading time ~9 min*

## What the problem is really asking

You stand on index 0 of an integer array `arr`. In one jump you may move to `i - 1`, to
`i + 1` (staying in bounds), or to **any** index `j` with `arr[j] == arr[i]`, however far
away. Return the fewest jumps to reach the last index.

The answer is a shortest-path length in an unweighted graph whose nodes are indices. Two
kinds of edges exist: short hops along the line, and "teleporters" joining every pair of
indices that hold the same value. Nobody hands you that graph, and you must not build it
naively: if all n values are equal, the teleporter edges alone number n(n-1)/2, which is
5 x 10^9 for n = 5 x 10^4.

```text
  arr = [100, -23, -23, 404, 100, 23, 23, 23, 3, 404]
  idx     0    1    2    3    4   5   6   7  8    9

  index      : 0 1 2 3 4 5 6 7 8 9    line edges i-1, i+1
  value 100  : *-------*              teleporters join all
  value -23  :   *-*                  indices of one value
  value 404  :       *-----------*
  value  23  :           *-*-*
  value   3  :                 *

  best: 0 -(100)-> 4 -(-1)-> 3 -(404)-> 9      3 jumps
```

What makes it hard is purely efficiency. The BFS is textbook; the trap is that the
same-value groups are cliques, and expanding a clique edge by edge is quadratic.

## Do it by hand first

Start at 0. In one jump you can reach 1 (step right) and 4 (the other 100). Those are
layer 1. From 4 you can step to 3 or 5. From 1 you can step to 2, or teleport to 2 (the
other -23). Layer 2 is {2, 3, 5}. From 3 you can teleport to 9 (the other 404), which is
the end. Three jumps.

```text
  layer 0 : {0}
  layer 1 : {1, 4}         0 steps right; 0 teleports via 100
  layer 2 : {2, 3, 5}      4 steps to 3, 5; 1 reaches 2
  layer 3 : {6, 7, 9}      3 teleports via 404 -> 9 = last index
```

Notice what you did at layer 2 when you reached index 2. You did not look for "other
-23s", because when you stood on index 1 you already used the -23 teleporter and both -23
indices were already marked. Your hand kept two things: the **set of visited indices**, and
a sense of **which teleporters had already been used up**. The second one is the whole
problem.

## The first honest attempt

Plain BFS from index 0. For a popped index i, its neighbours are i - 1, i + 1, and every j
with `arr[j] == arr[i]`, found by scanning the whole array. Mark neighbours visited when
pushing, stop when the last index is popped.

That is correct and costs O(n) per pop, O(n^2) total. The obvious improvement is to
pre-bucket indices by value (`where[v]` = list of indices holding v), so the same-value
neighbours become a dictionary lookup. That feels like it should fix everything. It does
not. Take a run of equal values:

```text
  arr = [1, 7, 7, 7, 7, 7, 2]     where[7] = [1,2,3,4,5]
  idx    0  1  2  3  4  5  6

  pop 1 : iterate where[7] -> push 2,3,4,5   (5 reads, useful)
  pop 2 : iterate where[7] -> all seen       (5 reads, wasted)
  pop 3 : iterate where[7] -> all seen       (5 reads, wasted)
  pop 4 : iterate where[7] -> all seen       (5 reads, wasted)
  pop 5 : iterate where[7] -> all seen       (5 reads, wasted)
```

Every index in the bucket iterates the whole bucket, so a bucket of size m costs m^2 reads.
On `[5] * 50000` that is 2.5 x 10^9 reads and a time-out. The visited check stops anything
from being pushed twice, but it does not stop the reading. Reading an edge whose far end
is already visited is the repeated work.

## The turning point

**Claim: a same-value bucket only ever needs to be expanded once. The first index of value
v to be popped pushes every other index of value v, so after that the bucket can only
produce "already seen" answers. Delete it.**

Why is that true? A bucket is a clique: every member is adjacent to every other member.
When BFS pops the first member, it walks the whole bucket and marks every unvisited member,
pushing each with depth d + 1. When a later member is popped, every member of the bucket
is already marked. So iterating the bucket again can never change any distance. That is
the general rule for cliques in BFS: **a clique is consumed by its first visit**.

Turning the claim into code is one change. Instead of reading `where[arr[i]]`, *remove* it:

```python
nbrs = where.pop(arr[i], [])  # first visitor takes bucket
nbrs.extend((i - 1, i + 1))   # the two line neighbours
```

The second visitor to value v finds no bucket and gets an empty list, so it only looks at
its two line neighbours. The invariant: **each bucket is iterated at most once over the
whole run.** Since the buckets partition the indices, their total size is n, so all
teleport work together costs O(n). The line edges add at most 2 per index. The whole BFS is
linear.

Draw it as the chapter keeps asking: the graph is not the array, it is indices plus a
switch on each teleporter.

```text
  state the algorithm keeps

  indices : 0 1 2 3 4 5 6 7 8 9      seen[] marks pushed indices
  buckets : 100:[0,4]  -23:[1,2]     where{} holds the
            404:[3,9]  23:[5,6,7]    teleporters still ON
            3:[8]

  using a teleporter = pop it from where{} (switch it OFF)
```

There is a neat way to see this as the same idea as Bus Routes. There, each route was a
group, and we marked the route as seen so its stop list was scanned once. Here, each value
is a group, and deleting the bucket is the same "group already expanded" mark. The value
is a bus; its indices are its stops.

One more detail: BFS by layers. The code processes the queue one layer at a time (loop
`len(queue)` times, then `jumps += 1`) so it knows the depth without storing it per node.
The target check happens when an index is popped. Popping and pushing checks both work, as
long as you are consistent.

## Watch it work

`seen` lists marked indices; `where` lists the buckets still switched on.

```text
Frame 1  layer 0
  queue : [0]                     seen : {0}
  where : 100:[0,4] -23:[1,2] 404:[3,9] 23:[5,6,7] 3:[8]
```

Only the start is in the queue; every teleporter is still on.

```text
Frame 2  pop 0 (jumps = 0)
  take where[100] = [0,4]  + line nbrs -1, 1
  push 4 (teleport), push 1 (step)
  queue : [4, 1]                  seen : {0,1,4}
  where : -23:[1,2] 404:[3,9] 23:[5,6,7] 3:[8]
```

Index 0 switches off the 100 teleporter and reaches 4 and 1; layer 1 is {4, 1}.

```text
Frame 3  layer 1 (jumps = 1)
  pop 4 : where[100] gone -> []   line: push 3, push 5
  pop 1 : take where[-23]=[1,2]   push 2;  0 and 2 seen
  queue : [3, 5, 2]               seen : {0..5}
  where : 404:[3,9] 23:[5,6,7] 3:[8]
```

Index 4 finds its teleporter already off and only steps; index 1 consumes the -23 bucket.

```text
Frame 4  layer 2 (jumps = 2)
  pop 3 : take where[404]=[3,9]   push 9
  pop 5 : take where[23]=[5,6,7]  push 6, push 7
  pop 2 : where[-23] gone -> []   1 and 3 seen
  queue : [9, 6, 7]               seen : {0..7, 9}
  where : 3:[8]
```

Two teleporters fire in this layer; index 2 finds its bucket already consumed and adds
nothing.

```text
Frame 5  layer 3 (jumps = 3)
  pop 9 : 9 == n-1  -> return 3
```

The last index is popped in layer 3, so the answer is 3.

Throughout the frames, each index entered `seen` exactly once and at its true layer, and
`where` only ever shrank. Each value was read in full exactly once, by whichever of its
indices was popped first. The bucket for 3 was never touched because the search ended
first.

## Why it is correct

Two facts are needed: BFS gives shortest paths in an unweighted graph, and removing buckets
does not remove any edge that could matter.

The layer property: when index j is first pushed while processing layer d, j's distance
from 0 is d + 1. Every index of layer d was reached in d jumps, so j is reachable in d + 1.
It cannot be reachable in fewer, or it would be adjacent to some index in an earlier layer
and would have been pushed while that layer was processed.

Bucket removal is safe. Suppose index i with value v is popped, and v's bucket was already
removed by an earlier pop of index i' with the same value. When i' was popped, every
member of the bucket that was not yet seen got pushed and marked. So at the time i is
popped, every same-value neighbour of i is already marked, and the teleport edges from i
would push nothing. Skipping them changes no distance. The line edges i - 1 and i + 1 are
still checked for every index, so nothing else is lost.

The answer always exists: the `+1` edges alone walk from 0 to n - 1, so the final `return
-1` is unreachable. The case n = 1 returns 0 before the search.

## Cost

- **Time O(n).** Building `where` is one pass. Each index is pushed and popped at most
  once. Each bucket is iterated at most once and the buckets have total size n. Each pop
  adds two line neighbours. Without removal, an array of equal values costs O(n^2).
- **Space O(n)** for `where`, `seen` and the queue.

The array scan brute force is O(n^2) time on every input, not just the bad ones.

## Variations you will meet

- **Jump Game II (only forward jumps of up to `nums[i]`).** Edges go to an interval, not a
  value class. The same "consume once" idea becomes a greedy over the farthest reach:
  each layer is a contiguous interval, and you never rescan an index of an earlier layer.
- **Teleports with a cost.** If a same-value jump cost more than a step, edge weights
  differ, and you need Dijkstra or 0-1 BFS (when the weights are 0 and 1). Bucket removal is
  then unsafe in general: the first visitor to a bucket is no longer guaranteed to have the
  smallest distance for every member.
- **Jump Game III / VII.** Reachability rather than distance, with jump lengths given by
  values or a window. BFS or a sliding prefix count; the shared lesson is never to
  re-expand a range or group that has already been expanded.
- **Word Ladder with pattern buckets.** If you bucket words by wildcard pattern, you can
  delete a pattern bucket after its first use for exactly the same reason.

## What to carry forward

A group whose members are all adjacent to each other is spent the moment BFS first touches
it, so delete it on first use. That is the line that turns O(n^2) into O(n). The next
problem, K-Similar Strings, moves from pruning *edges* to pruning *branches*: the states
are whole strings, and the trick is to allow only the swaps that could start an optimal
answer.
