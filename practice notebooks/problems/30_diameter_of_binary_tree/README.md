# Diameter of Binary Tree (LeetCode 543)

**Area:** trees · **Difficulty:** Medium · **Key operations:** post-order height, candidate = left + right at every node, nonlocal best

## Problem

The diameter of a binary tree is the number of **edges** on the longest path between any two nodes. The path does not have to pass through the root. Given the root, return the diameter. The tree is given in LeetCode's level-order form, `None` marking a missing child.

## Example

```
[1, 2, 3, 4, 5]        1
                      / \
                     2   3
                    / \
                   4   5
```

The longest path is `4 -> 2 -> 1 -> 3` (or `5 -> 2 -> 1 -> 3`): 3 edges, so the answer is 3.

## Brute force

Every path has a unique highest node where it "bends". The longest path bending at a node is `height(left) + height(right)`, where `height` counts the edges down to the deepest leaf (plus one for the child itself). So: for every node compute both heights from scratch, take the maximum over all nodes.

O(n²) time on a skewed tree, O(h) space. The wasted work: `height(subtree)` is recomputed once for every ancestor of that subtree. A chain of n nodes recomputes the bottom's height n times.

## From brute force to optimal

`height(node)` already visits `node.left` and `node.right` and computes exactly the two numbers the diameter formula needs. Instead of calling `height` again from the outside, update a running `best = max(best, left + right)` *inside* `height`, while the two arm lengths are in hand. Then return `1 + max(left, right)` upward, because a path continuing up through the parent can use only one arm.

Each node's height is computed exactly once, so one post-order pass answers the question. The invariant: when `height(node)` returns, `best` already covers every path whose highest point lies inside `node`'s subtree.

## Intuition

Picture each node as a hinge with two arms hanging down; the arm lengths are the subtree heights. Opening the hinge flat gives a path of length `left + right`. Post-order means we measure both arms before looking at the hinge, so at every hinge we can try "open it flat" as a candidate and remember the widest opening. Going up we hand the parent only the longer arm plus the edge to the parent, because a path through the parent cannot bend twice. The answer may be found deep in the tree and never touch the root; `best` is kept outside the recursion for exactly that reason.

## Walkthrough

`enter v` is the pre-order visit, `node v: ...` the post-order return. Indentation is depth.

```
enter 1
    enter 2
        enter 4
        node 4: arms left=0 right=0 -> bend 0, best 0, return arm 1      4 is a leaf
        enter 5
        node 5: arms left=0 right=0 -> bend 0, best 0, return arm 1
    node 2: arms left=1 right=1 -> bend 2, best 2, return arm 2          4-2-5 is 2 edges
    enter 3
    node 3: arms left=0 right=0 -> bend 0, best 2, return arm 1
node 1: arms left=2 right=1 -> bend 3, best 3, return arm 3              4-2-1-3 is 3 edges
```

```
      1          arms at 1: left 2 (down to 4 or 5), right 1 (down to 3)
     / \         bend at 1 = 2 + 1 = 3  <- the answer
    2   3
   / \           arms at 2: 1 and 1, bend 2
  4   5
```

The value returned upward (`arm 3` for node 1) is the height; it is not the answer. `best` is.

## Steps

1. `best = 0`. Define `height(node)`: return 0 for `None`.
2. Post-order: `left = height(node.left)`, `right = height(node.right)`.
3. `best = max(best, left + right)` (the path that bends at this node, in edges).
4. Return `1 + max(left, right)`: only one arm continues up to the parent.
5. Call `height(root)` for its side effect and return `best`.

## Complexity

O(n) time, one post-order visit per node. O(h) space for the recursion stack, h the tree height (O(n) for a chain).

## Pitfalls

- **Returning `max(left, right)` without the `+ 1`.** Every arm stays 0, every bend is 0, the answer is 0. The edge from the child up to the current node is the `+ 1`.
- **Counting nodes instead of edges.** `left + right + 1` counts the nodes on the path; `[1, 2, 3, 4, 5]` returns 4 and a single node returns 1. The diameter is `left + right`.
- **Returning the root's height instead of `best`.** `return height(root)` returns the longest single arm; `[1, 2]` has height 2 but diameter 1, and the real answer may bend below the root.
- **Returning `left + right` upward.** A path through the parent cannot bend twice; the parent needs only the longer arm.
- **Forgetting `nonlocal best`.** Assigning `best` inside the nested function creates a new local and raises `UnboundLocalError` (or, with a list/attribute workaround, silently keeps 0).
