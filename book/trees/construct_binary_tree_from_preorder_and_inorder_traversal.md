# Construct Binary Tree from Preorder and Inorder Traversal

*LeetCode 105 · Medium · Pattern: Recursive tree construction with index map · Reading time ~8 min*

## What the problem is really asking

You are given two lists describing the same binary tree. One is its preorder walk (node, then left subtree, then right subtree). The other is its inorder walk (left subtree, then node, then right subtree). All values are distinct. Rebuild the tree.

The answer is a whole tree, a structure with shape, not a number. Each list alone is ambiguous: many different trees share the same preorder. The puzzle is how the two lists together pin down exactly one shape, and how to read that shape off without repeatedly searching through them.

```text
preorder: 3  9  20 15 7
inorder : 9  3  15 20 7

tree:        3
            / \
           9   20
              /  \
             15   7
```

## Do it by hand first

The first preorder value is always the root, because preorder writes a node before anything under it. So the root is `3`. Find `3` in inorder. Everything left of it in inorder belongs to the left subtree, and everything right of it belongs to the right subtree, because inorder writes the whole left subtree, then the node, then the whole right subtree.

```text
preorder: [3] 9  20 15 7       root = 3
inorder :  9 [3] 15 20 7
           ^      ^^^^^^^
          left     right
         (1 node) (3 nodes)
```

So the left subtree has 1 node and the right has 3. In preorder, after the root comes the entire left subtree (1 value: `9`), then the entire right subtree (`20 15 7`). Repeat on each part. In `20 15 7`, `20` is the root. In its inorder piece `15 20 7`, `15` is left and `7` is right.

Your hand did two lookups per node: "who is next in preorder?" (that is the root) and "where is that value in inorder?" (that tells the sizes). Notice that the preorder side was always just the next unread value. You never jumped around in preorder. That is the seed of the efficient version: a cursor moving through preorder, and a fast way to answer "where is `v` in inorder?".

## The first honest attempt

Turn the hand method into recursion on slices. Take `preorder[0]` as the root. Find its index `mid` in inorder with a linear search. Recurse on `preorder[1:mid+1]` with `inorder[:mid]` for the left subtree, and on `preorder[mid+1:]` with `inorder[mid+1:]` for the right.

```text
call for root 3: scan inorder for 3      -> 2 reads
                 copy 4 + 4 list cells
call for root 20: scan "15 20 7" for 20   -> 2 reads
                 copy 2 + 2 cells
...
skewed tree (a chain): scans of n, n-1, n-2, ... -> O(n^2)
```

There are two costs that repeat. The linear search re-reads inorder values to find each root, and on a chain it re-reads almost the whole list at every level. The slicing copies sub-lists that are only ever read. Both are `O(n)` per call, so the whole thing is `O(n^2)` in the worst case.

## The turning point

**Claim: preorder tells you who the root is, inorder tells you how big the left subtree is, and with a value-to-index map plus a single preorder cursor, every node costs `O(1)`.**

Fix each cost separately.

- **The search.** "Where is `v` in inorder?" is a question with a fixed answer for each `v`. Build `index = {value: position}` once, in `O(n)`, and every later lookup is `O(1)`. This needs distinct values, which the problem guarantees.
- **The slices.** A subtree's inorder part is always a contiguous range. Pass two indices `(lo, hi)` instead of a copy.
- **The preorder side.** Here is the elegant part. If we always build the left subtree completely before starting the right, nodes are created in exactly preorder order. So one shared cursor `pre`, advanced by one each time a node is made, always points at the correct next root. No bounds are needed on the preorder side at all.

The function becomes: `make(lo, hi)` builds the subtree whose inorder values are `inorder[lo:hi]`. If the range is empty, return nothing. Otherwise take `preorder[pre]` as the root, advance `pre`, look up `mid`, and build `make(lo, mid)` then `make(mid + 1, hi)`. The order matters: left first, or the cursor hands the right subtree's root to the left call.

```text
preorder:  3  9  20 15 7       one cursor, moves right only
           ^pre
inorder :  9  3  15 20 7       window [lo, hi) shrinks
          [lo          hi)     around each subtree
```

## Watch it work

`preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`, `index = {9:0, 3:1, 15:2, 20:3, 7:4}`.

Frame 1. `make(0,5)`: the cursor reads `3`, `mid = 1`. The left window is `[0,1)` and the right is `[2,5)`.

```text
pre : [3] 9  20 15 7    pre 0->1       tree:   3
ino :  9 [3] 15 20 7
      L      R  R  R
```

Frame 2. `make(0,1)`: the cursor reads `9`, `mid = 0`. Both child windows `[0,0)` and `[1,1)` are empty, so `9` is a leaf.

```text
pre :  3 [9] 20 15 7    pre 1->2       tree:   3
ino : [9] 3  15 20 7                          /
                                             9
```

Frame 3. Back in the root, `make(2,5)`: the cursor reads `20`, `mid = 3`. The left window is `[2,3)` and the right is `[4,5)`.

```text
pre :  3  9 [20] 15 7   pre 2->3       tree:   3
ino :  9  3  15 [20] 7                        / \
             L       R                       9   20
```

Frame 4. `make(2,3)`: the cursor reads `15`. Its windows are empty, so it is a leaf hung left of `20`.

```text
pre :  3  9  20 [15] 7  pre 3->4       tree:   3
ino :  9  3 [15] 20  7                        / \
                                             9   20
                                                /
                                              15
```

Frame 5. `make(4,5)`: the cursor reads `7`, a leaf hung right of `20`. `pre = 5` equals `n`, and every call returns.

```text
pre :  3  9  20 15 [7]  pre 4->5       tree:   3
ino :  9  3  15 20 [7]                        / \
                                             9   20
                                                /  \
                                              15    7
```

At every frame the cursor pointed at the first preorder value of the window being built. Each call consumed exactly `hi - lo` preorder entries, one per node in its window. That is why the right subtree always found its root under the cursor.

## Why it is correct

The invariant is that `make(lo, hi)` is called with the cursor at the first preorder entry of the subtree whose inorder is `inorder[lo:hi]`, and it returns that subtree with the cursor moved exactly `hi - lo` places.

Use induction on the window size. An empty window consumes nothing and returns nothing, which is correct. For a non-empty window, the subtree's preorder starts with its root, so `preorder[pre]` is the root. Its inorder position `mid` splits the window into the left subtree's range `[lo, mid)` and the right subtree's range `[mid+1, hi)`. In preorder, the root is followed by all of the left subtree, then all of the right subtree. By induction, `make(lo, mid)` consumes exactly the left subtree's `mid - lo` entries, leaving the cursor at the right subtree's first entry, which is just what `make(mid+1, hi)` needs. The total consumed is `1 + (mid - lo) + (hi - mid - 1) = hi - lo`.

## Cost

- **Time `O(n)`.** Each node is created once, with one `O(1)` map lookup. Empty calls are at most `n + 1`.
- **Space `O(n)`.** The map holds `n` entries, plus `O(h)` recursion depth.
- The slicing brute force is `O(n^2)` time and `O(n^2)` space in the worst case.

## Variations you will meet

- **Inorder + postorder (LeetCode 106).** Postorder ends with the root, so run the cursor from the right end, moving left, and build the right subtree before the left.
- **Preorder + postorder (LeetCode 889).** Without inorder the split is ambiguous when a node has one child. The next preorder value is the left child's root. Its position in postorder tells you the left subtree's size. Any valid tree is accepted.
- **BST from preorder alone (LeetCode 1008).** Inorder of a BST is just the sorted values, so you need no second list. Even better, pass a value bound `(low, high)` and consume preorder while values fit. That is `O(n)` with no map.
- **Duplicate values.** The map breaks, because `index[v]` is ambiguous. Two traversals no longer determine the tree. This is why Serialize and Deserialize does not use this method.

## What to carry forward

Preorder says who the root is, inorder says how big the left side is. One cursor through preorder plus a map into inorder rebuilds the tree in a single pass. The next problem again rebuilds from a preorder stream with a single cursor, but instead of a second list it gets each node's depth written as dashes, and a stack of ancestors replaces the inorder window.
