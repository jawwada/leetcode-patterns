# Clone Graph (LeetCode 133)

**Area:** graphs · **Difficulty:** Medium · **Key operations:** BFS from the start node, old -> new dict as the visited set, create a clone on first sight, wire clone -> clone edges

## Problem

Given a node of a connected undirected graph (each node has a value and a list of neighbours), return a deep copy of the graph: the same shape built from brand-new nodes, none of them shared with the input. In this script `solve` returns the copy read back as `{value: sorted neighbour values}` so it can be compared, and the tests also check that no node object is shared.

## Example

```
1 -- 2
|    |        {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]}
4 -- 3

-> the same adjacency, from four fresh Node objects
```

## Brute force

Three passes with no map. Pass 1: traverse the graph and collect every original node in a list. Pass 2: make one fresh copy per original, in the same order. Pass 3: for every edge `(u, v)` of the original, scan the list of copies for the one whose value equals `v.val` and append it to `u`'s copy.

O(V · E) time, O(V) space. The scan is the waste: each of the E edge endpoints does a linear search over up to V copies to answer "which copy belongs to this original?".

## From brute force to optimal

"Which copy belongs to this original?" is a pure key → value question, so a dict `clones[original] = copy` answers it in O(1). With the dict in hand the three passes collapse into one traversal: when a neighbour is met for the first time, create its clone and store it; when it is met again through another edge, just look it up. The dict doubles as the visited set, which is also what stops the traversal looping forever on cycles. Each node is cloned once and each edge wired once: O(V + E).

## Intuition

Picture a shadow graph growing beside the original. A BFS frontier sweeps the original; each time the frontier touches a node for the first time it casts a shadow node and remembers the pairing. For every edge the frontier crosses, it draws a parallel shadow edge between the two shadows. When the sweep is done, the shadow is a complete copy that shares nothing with the original. The pairing table is the only state you need.

## Walkthrough

Start at node 1. `clones` is drawn as the set of values that already have a copy; the copy's adjacency is read back after each wire.

```
init          clones {1}          queue [1]
pop 1         neighbours 2, 4
  2 not cloned -> new Node(2), enqueue        clones {1,2}       queue [2]
  wire clone1 -> clone2                        copy {1: [2]}
  4 not cloned -> new Node(4), enqueue        clones {1,2,4}     queue [2,4]
  wire clone1 -> clone4                        copy {1: [2,4]}
pop 2         neighbours 1, 3
  1 already cloned -> look it up
  wire clone2 -> clone1                        copy {1: [2,4], 2: [1]}
  3 not cloned -> new Node(3), enqueue        clones {1,2,3,4}   queue [4,3]
  wire clone2 -> clone3                        copy {1: [2,4], 2: [1,3]}
pop 4         neighbours 1, 3: both cloned
  wire clone4 -> clone1, clone4 -> clone3      copy {1: [2,4], 2: [1,3], 4: [1,3]}
pop 3         neighbours 2, 4: both cloned
  wire clone3 -> clone2, clone3 -> clone4      copy {1: [2,4], 2: [1,3], 3: [2,4], 4: [1,3]}
queue empty -> return clones[1]
```

Four `Node(...)` calls, eight wires (one per directed edge), zero scans.

## Steps

1. If `node` is `None`, return `None`.
2. `clones = {node: Node(node.val)}`, `queue = deque([node])`.
3. Pop `cur`. For each neighbour `nb`: if `nb` is not in `clones`, create `clones[nb] = Node(nb.val)` and enqueue `nb`.
4. Append `clones[nb]` to `clones[cur].neighbors`.
5. When the queue is empty, return `clones[node]`.

## Complexity

O(V + E) time: each node is popped once and each directed edge wired once. O(V) space for the dict and the queue.

## Pitfalls

- **Appending the original neighbour.** `clones[cur].neighbors.append(nb)` makes the adjacency read correctly while the copy points into the original graph; always append `clones[nb]`.
- **Enqueuing the wrong node.** `queue.append(cur)` instead of `nb` means the new neighbour is cloned but never popped, so its own edges are never wired and nodes two steps away are never cloned.
- **Returning the original.** `return node` passes any adjacency comparison and fails the deep-copy requirement; return `clones[node]`.
- **Cloning a node twice.** Creating the clone without checking the dict first gives a node reached via two edges two copies, breaking cycles. Check `nb not in clones` before creating.
- **Forgetting the `None` input.** An empty graph is `None` in, `None` out.
