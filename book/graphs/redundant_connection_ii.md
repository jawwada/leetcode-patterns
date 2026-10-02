# Redundant Connection II
*LeetCode 685 · Hard · Pattern: Union-Find (disjoint set union) · Reading time ~13 min*

## What the problem is really asking

Start with a **rooted** tree on nodes `1..n`. Every edge points from a parent to a child.
One node, the root, has no parent, and every other node has exactly one. Someone added one
extra directed edge `u -> v`, so there are now `n` edges. Return an edge whose removal turns
the graph back into a rooted tree. If several edges work, return the one that appears last
in the input.

The answer is still one edge, as in Redundant Connection. But direction changes what
"broken" means. A rooted tree has two rules: **every non-root node has exactly one
parent**, and **following parents from anywhere reaches the root without looping**. The
extra edge can break either rule, or both at once. That is the whole difficulty. A plain
"first union that fails" answer can name the wrong edge, because the real fault might be a
node with two parents.

```text
  edges = [[2,1],[3,1],[4,2],[1,4]]       answer [2,1]

      3                 parent_of
      |                 node 1: 2 AND 3   <- two parents
      v                 node 2: 4
      1 <------ 2       node 4: 1
      |         ^       node 3: (none)
      v         |
      4 --------+       cycle: 1 -> 4 -> 2 -> 1
```

Node 1 has two parents, 2 and 3. There is also a loop `1 -> 4 -> 2 -> 1`. Removing `[3,1]`,
the later of the two parent edges, fixes the double parent but leaves the loop. Removing
`[2,1]` fixes both at once, and what remains is the chain `3 -> 1 -> 4 -> 2`.

## Do it by hand first

Before touching any data structure, ask what one extra arrow can do to a rooted tree. The
arrow `u -> v` lands on some node `v`. There are only two possibilities.

```text
  (A) v already had a parent     (B) v is the root
      -> v now has TWO parents       -> nobody has two parents,
                                        but a loop runs through
                                        the root
  A1: no loop          A2: loop too        B: loop only
     1                   3                  1 -> 2
    / \                  |                  ^    |
   v   v                 v                  |    v
   2 -> 3                1 <-- 2            4 <- 3
                         |     ^             (+ 1 -> 5)
                         v     |
                         4 ----+
  [[1,2],[1,3],[2,3]]   [[2,1],[3,1],      [[1,2],[2,3],
                          [4,2],[1,4]]       [3,4],[4,1],[1,5]]
  answer [2,3]          answer [2,1]       answer [4,1]
```

By hand, you do two things. First, look at in-degrees: does any node have two incoming
arrows? If so, one of those two arrows must go, because the fixed tree gives that node one
parent. The edge to remove is one of exactly two candidates. Call the earlier one `cand1`
and the later one `cand2`.

- In A1, either candidate works. The tie-break says take the later one, `cand2 = [2,3]`.
- In A2, deleting `cand2 = [3,1]` leaves the loop `1 -> 4 -> 2 -> 1`. So `cand2` cannot be
  the answer, and it has to be `cand1 = [2,1]`.
- In B, there are no candidates at all. Some edge on the loop must go, and as in Redundant
  Connection, it should be the last loop edge in input order: `[4,1]`.

Your hand kept two things: a **parent-of table**, to spot the double parent, and a
**which-piece table**, to spot the loop. The second is union-find again.

## The first honest attempt

Try every edge, from last to first. Delete it, and check whether the remaining `n - 1`
edges form a rooted tree. That means exactly one node with in-degree 0, every other node
with in-degree 1, and a DFS from that root that reaches all `n` nodes. Return the first
edge that passes.

On our example, scanning from the last edge backwards:

```text
  remove [1,4]  -> node 1 still has 2 parents      fail
  remove [4,2]  -> node 1 still has 2 parents      fail
  remove [3,1]  -> root 3 reaches only {3}         fail
  remove [2,1]  -> root 3 reaches {3,1,4,2}        PASS
  ^ n candidates x O(n) check each = O(n^2)
```

The waste is that the in-degree scan was redone `n` times. One scan already shows that only
the two arrows into node 1 can possibly be the answer. All the other trials were doomed
before they started.

## The turning point

**Claim: one in-degree scan narrows the answer to at most two edges, and one union-find pass
with `cand2` left out decides between them.**

Here is the argument, case by case.

*No node has two parents (case B).* Every node already has in-degree at most 1, and there
are `n` edges on `n` nodes. So every node has in-degree exactly 1, and there is no root
left. Follow parents backward from any node and you must loop. The loop is the only fault,
so removing any loop edge restores a tree. This is now exactly Redundant Connection: the
first union that fails, in input order, is the last edge of the loop.

*Some node `v` has two parents.* The answer is `cand1` or `cand2`. Leave out `cand2` and
union every other edge, ignoring direction.

- If no union fails, the remaining `n - 1` edges are connected and acyclic as an undirected
  graph. Every node now has in-degree at most 1. Along with `n - 1` edges, that forces
  exactly one root, so it is a rooted tree. Removing `cand2` works, and since `cand2` is the
  later candidate, it wins the tie-break.
- If a union fails, the edges without `cand2` still contain an undirected cycle. That cycle
  has `k` edges on `k` nodes, and every node has in-degree at most 1, so each node on it has
  in-degree exactly 1. In other words, the cycle is a **directed** loop. Removing `cand2`
  did not break it, so `cand2` cannot be the answer. The answer must be `cand1`.

Why not just leave out both candidates and see what happens? Then the pass would know
nothing about which of the two was guilty. Leaving out exactly one candidate is the test.

The only state we need beyond the previous problem is `parent_of[v]`. It is filled in one
scan and spots the second parent the moment it arrives. This union-find skips rank. It does
`uf[rv] = ru` directly and keeps path halving. With `n` small and halving on, that is still
fast in practice.

## Watch it work

`edges = [[2,1],[3,1],[4,2],[1,4]]`, `n = 4`. Index 0 is unused.

```text
Frame 1  scan [2,1]: parent_of[1] was 0 -> set to 2
  node:       1 2 3 4
  parent_of:  2 0 0 0       cand1 = none, cand2 = none
```
Node 1 gets its first parent.

```text
Frame 2  scan [3,1]: parent_of[1] is already 2
  node:       1 2 3 4
  parent_of:  2 0 0 0       cand1 = [2,1]   (earlier)
                            cand2 = [3,1]   (later)
```
This is a second arrow into node 1, so the two candidates are recorded. Note that
`parent_of[1]` keeps 2.

```text
Frame 3  scan [4,2] and [1,4]: no more conflicts
  node:       1 2 3 4
  parent_of:  2 4 0 1       candidates unchanged
```
The scan is done. Node 3 is the only node with no parent.

```text
Frame 4  union-find, edge [2,1]: roots 2,1 -> uf[1] = 2
  index:  1 2 3 4         2    3    4
  uf:     2 2 3 4         |
                          1
```
This is the first union. Direction is ignored, and the second endpoint's root goes under the
first.

```text
Frame 5  edge [3,1] == cand2 -> skipped
  index:  1 2 3 4         2    3    4
  uf:     2 2 3 4         |
                          1
```
We provisionally pretend that `cand2` was never there.

```text
Frame 6  edge [4,2]: find(4)=4, find(2)=2 -> uf[2] = 4
  index:  1 2 3 4         4    3
  uf:     2 4 3 4         |
                          2
                          |
                          1
```
The roots differ, so 2's tree goes under 4. Now there is a chain of height 2.

```text
Frame 7  edge [1,4]: find(1) halves uf[1] = uf[2] = 4
  index:  1 2 3 4           4      3
  uf:     4 4 3 4          / \
                          2   1
  find(1)=4 == find(4)=4 -> loop survives without cand2
  -> return cand1 = [2,1]
```
The loop `1 -> 4 -> 2 -> 1` is still there even though `cand2` is gone, so the fault is
`cand1`.

For contrast: on `[[1,2],[1,3],[2,3]]`, the scan sets `cand1 = [1,3]` and `cand2 = [2,3]`.
The pass unions `[1,2]` and `[1,3]`, skips `[2,3]`, and finishes with no collision, so it
returns `cand2`. On `[[1,2],[2,3],[3,4],[4,1],[1,5]]`, there are no candidates. The pass
collides at `[4,1]`, with all of `1..4` already under root 1, and returns it.

What stayed invariant: `parent_of` held the first parent seen for each node. The forest's
trees were the undirected components of the edges processed so far, excluding `cand2`, and
before the collision those edges contained no cycle.

## Why it is correct

The fault analysis is complete, because the extra arrow either lands on a node that has a
parent, which is case A, or on the root, which is case B. In case B, every node has
in-degree exactly 1, and the remaining structure is a tree plus one edge that closes a
loop through the root. Removing any loop edge restores a rooted tree. The union-find pass
reports the first edge whose endpoints are already connected. By the Redundant Connection
argument, that is the last loop edge in input order, which is what the tie-break asks for.

In case A, the answer is one of the two edges into `v`, because the restored tree gives `v`
one parent. With `cand2` excluded, every node has in-degree at most 1. A collision means an
undirected cycle exists, and with in-degree at most 1 that cycle is directed, so the
remaining edges are not a tree, and `cand2` is wrong. The input guarantees an answer, so it
is `cand1`. No collision means `n - 1` acyclic edges on `n` nodes. That is a spanning tree
in which each node has at most one parent, so exactly one root exists. Removing `cand2`
works, and the tie-break prefers it as the later edge. If `cand1` would also work, `cand2`
still wins.

## Cost

- Time `O(n * alpha(n))`, or `O(n log n)` worst case without rank. There is one `O(n)` scan
  and one pass of union-find over at most `n` edges.
- Space `O(n)`, for `parent_of` and `uf`.
- The brute force removes each edge and re-validates: `O(n^2)` time, `O(n)` space.

## Variations you will meet

- **Undirected version.** Redundant Connection has no in-degree story at all. It is just the
  first failed union.
- **Validate a rooted tree (directed).** Exactly one node with in-degree 0, all others with
  in-degree 1, and every node reachable from the root. This is the same in-degree scan,
  used as a checker. Validate Binary Tree Nodes (LeetCode 1361) is this with child arrays.
- **List every removable edge.** In A1 both candidates work. In A2 only `cand1` works. In B
  every loop edge works, and you list them by walking the tree path between the ends of
  the colliding edge.
- **Detecting a directed cycle in general** (more than one extra edge) needs DFS colouring
  or Kahn's algorithm, as in Course Schedule. Union-find ignores direction, and it only
  worked here because in-degrees were at most 1.

## What to carry forward

With direction, first look for a node with two parents. Drop the later parent edge and run
union-find. If a loop survives, blame the earlier one. If there were no candidates, blame
the first failed union. The next problem, Accounts Merge, leaves edge lists behind. The
union-find keys become accounts, and the "edges" come from shared emails that you have to
discover yourself.
