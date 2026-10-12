# Recover a Tree From Preorder Traversal

*LeetCode 1028 · Hard · Pattern: Stack of ancestors indexed by depth · Reading time ~10 min*

## The problem

A tree was serialised by preorder DFS: each node is written as D dashes followed by its value, where D is its depth
(the root has none). A node with a single child always has it on the left. Rebuild the tree.

```text
Example: "1-2--3--4-5--6--7" gives [1,2,5,3,4,6,7].
```

## What the problem is really asking

A binary tree was written out by a preorder walk. Each node appears as some dashes followed by its value, and the number of dashes is the node's depth (the root has none). If a node has only one child, that child is always the left one. You get the string and must rebuild the tree.

The answer is a tree. The input is a single flat stream, and the only structural hint per node is one number, its depth. The challenge is turning "depth 2, value 4" into "right child of node 2" without scanning backwards or forwards over the string again and again. Values can have several digits, which makes the parsing a little fiddly.

```text
"1-2--3--4-5--6--7"

token:  1   -2   --3  --4   -5   --6  --7
depth:  0    1    2    2    1     2    2

tree:          1            depth 0
             /   \
            2     5         depth 1
           / \   / \
          3   4 6   7       depth 2
```

## Do it by hand first

Read left to right and draw as you go. `1` at depth 0 is the root. `2` at depth 1 must hang under the root, and it goes left because the left slot is free. `3` at depth 2 hangs under the most recent depth-1 node, `2`, on the left. Now `4` at depth 2. Its parent is at depth 1, and the most recent depth-1 node is still `2`, whose left slot is taken, so `4` goes right. Then `5` at depth 1. Its parent is at depth 0, the root, and the root's left is taken, so `5` goes right.

```text
when "-5" arrives (depth 1):
   path you were on:  1 -> 2 -> 4      (depths 0,1,2)
   cut it back to depth 0:  1
   hang 5 under 1 (right, since left is taken)
   new path:          1 -> 5
```

What your hand tracked was the current path from the root down to the last node you drew, one node per depth. A new token at depth `d` means "cut the path back to length `d`, then hang me under the last node on it". That path is a stack, and the dash count tells you how tall to leave it.

## The first honest attempt

Tokenise the string into `(depth, value)` pairs. Recursively: the first token is the root, at depth `d`. Scan forward for the second token at depth `d + 1`. That token starts the right subtree, and everything between it and the root is the left subtree. Recurse on the two slices.

```text
left chain "10-20--30---40----50":

build(10): scan 20,30,40,50 for a 2nd depth-1 token  (4 reads)
build(20): scan 30,40,50   for a 2nd depth-2 token   (3 reads)
build(30): scan 40,50                                (2 reads)
build(40): scan 50                                   (1 read)
           ----------------------------------------
           every level re-reads the tokens below it
           total ~ n^2 / 2
```

On a lopsided tree each call rescans almost everything after it, re-reading depths that were already parsed, only to find where a subtree ends. That is `O(n^2)` time, plus the cost of copying slices. The repeated work is "find the end of this subtree", answered from scratch at every level.

## The turning point

**Claim: when a token at depth `d` arrives, its parent is the most recent node seen at depth `d - 1`, and every node deeper than `d - 1` on the current path is finished for good.**

Why? Preorder writes a node, then all of its left subtree, then all of its right subtree. So when a node at depth `d` appears, it is a child of the last node at depth `d - 1` that was written. Any node in between would have to be at depth `>= d`, which is inside that parent's earlier subtree. And once we return to depth `d`, everything we saw at depths `>= d` belongs to subtrees that preorder has closed. Preorder never comes back into a closed subtree.

This gives a stack whose index is depth. `stack[i]` is the current ancestor at depth `i`, so `len(stack)` is the depth just below the last node. On each token:

1. Count dashes to get `d`, then read all the digits to get the value.
2. Pop until `len(stack) == d`. The popped nodes are finished.
3. The top is the parent. Attach to its left if the left is empty, otherwise to its right. The "a single child is always left" rule makes this choice unambiguous. Preorder lists a left subtree before the right, so the first child to arrive is the left one.
4. Push the new node.

At the end, `stack[0]` is the root.

```text
depth:    0     1     2
stack:  [ 1 ,  2 ,  4 ]      len 3 = depth of next child
                       \
new token at d=1:  pop until len == 1  -> [ 1 ]
                   parent = top = 1
```

The scan-ahead disappears. A subtree's end is not found by searching. It is discovered when a shallower token arrives and pops it.

## Watch it work

Input `"1-2--3--4-5--6--7"`. The caret marks the token just read. The stack is written bottom (root) to top, and its index is depth.

Frame 1. `1` at depth 0. There is nothing to pop and no parent. Push.

```text
1-2--3--4-5--6--7          tree:  1
^
stack (by depth): [1]
```

Frame 2. `-2` at depth 1. `len(stack) = 1` is already `d`, so nothing is popped. The parent is `1`, whose left is free.

```text
1-2--3--4-5--6--7          tree:  1
 ^^                              /
stack: [1, 2]                   2
```

Frame 3. `--3` at depth 2. The parent is `2`, whose left is free.

```text
1-2--3--4-5--6--7          tree:  1
   ^^^                           /
stack: [1, 2, 3]                2
                               /
                              3
```

Frame 4. `--4` at depth 2. `len = 3 > 2`, so pop `3`, which is finished. The parent is `2`, whose left is taken, so `4` goes right.

```text
1-2--3--4-5--6--7          tree:  1
      ^^^                        /
popped: 3                       2
stack: [1, 2, 4]               / \
                              3   4
```

Frame 5. `-5` at depth 1. Pop `4` and `2`, closing the whole left subtree. The parent is `1`, whose left is taken, so `5` goes right.

```text
1-2--3--4-5--6--7          tree:   1
         ^^                       / \
popped: 4, 2                     2   5
stack: [1, 5]                   / \
                               3   4
```

Frame 6. `--6` at depth 2. Nothing is popped. The parent is `5`, so `6` goes left.

```text
1-2--3--4-5--6--7          tree:   1
           ^^^                    / \
stack: [1, 5, 6]                 2   5
                                / \  /
                               3  4 6
```

Frame 7. `--7` at depth 2. Pop `6`. The parent is `5`, whose left is taken, so `7` goes right. The string ends, and we return `stack[0] = 1`.

```text
1-2--3--4-5--6--7          tree:   1
              ^^^                 / \
popped: 6                        2   5
stack: [1, 5, 7]                / \ / \
                               3  4 6  7
```

Throughout, the stack was exactly the root-to-current-node path, with `stack[i]` at depth `i`. Each node was pushed once and popped at most once. The cursor in the string only moved right.

## Why it is correct

The invariant is that after processing each token, the stack holds the path from the root to the most recently read node, with `stack[i]` the ancestor at depth `i`.

It holds after the first token, because the root alone is pushed. Suppose it holds and a node `x` at depth `d` arrives. In preorder, `x`'s parent `p` is at depth `d - 1` and was written before `x`. Every token written after `p` and before `x` is in the subtree of a child of `p`, at depth `>= d`. So `p` is still on the path at index `d - 1`, and the stack entries at indices `>= d` are exactly those finished descendants. Popping down to length `d` exposes `p`. Pushing `x` makes the stack the path to `x`, so the invariant is preserved.

Left versus right: `p` gets its children in preorder order, and its left subtree is written before its right. So the first child of `p` to appear is the left child, unless `p` has only a right child. The problem rules that out by saying a lone child is always left. So "left if free, else right" places every node correctly.

## Cost

- **Time `O(L)`**, where `L` is the string length (`O(n)` in nodes). Every character is read once while counting dashes or reading digits. Every node is pushed once and popped at most once.
- **Space `O(h)`** for the stack, which is one root-to-node path, plus the `n` output nodes.
- The recursive scan-ahead version is `O(n^2)` time on skewed trees.

## Variations you will meet

- **Construct from preorder + inorder (the previous problem).** There, the second list told you subtree sizes. Here, depth plays that role. Both avoid rescans by consuming preorder with one forward cursor.
- **Parse an indented outline or a directory listing** (`tree` output, YAML-like nesting, Python indentation). This is identical: indentation is depth, and a stack of open parents cut back to the current depth gives each line its parent. Python's tokenizer does this with INDENT/DEDENT.
- **Lone child may be right.** The string becomes ambiguous (`"1-2"` could be either side). You would need an extra marker in the format, which is exactly what the null sentinels in the next problem provide.
- **N-ary version.** Drop the left/right choice and append to `parent.children`. The stack logic is unchanged.

## What to carry forward

Depth tells you how many ancestors a node has, so keep the ancestors on a stack and cut it back to the depth before hanging the new node. The stack is the path, and a shallower token closes subtrees for free. The next problem lets you design the format yourself: write preorder with a marker for every empty child, and the reader needs no stack and no depths, just recursion and a cursor.
