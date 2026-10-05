# Binary Tree Inorder Traversal

*LeetCode 94 · Easy · Pattern: Iterative traversal with an explicit stack · Reading time ~7 min*

## The problem

Return the values of a binary tree in inorder: left subtree, then the node, then the right subtree. The follow-up asks
for an iterative solution.

```text
Example: root = [1,null,2,3] -> [1,3,2].
```

## What the problem is really asking

Return the node values in **inorder**: everything in the left subtree, then the node itself, then everything in the right subtree, applied recursively. The follow-up asks you to do it without recursion.

The recursive version is three lines; the real exercise is the follow-up: make the call stack visible, so you can pause and stop it. The next problems lean on exactly that.

Running example: `[4,2,5,1,3]`.

```text
          4
        /   \
       2     5
      / \
     1   3

 inorder: 1 2 3 4 5
 (project every node straight down onto a line:
  1   2   3   4   5  - the tree read left to right)
```

Keep that projection: inorder reads the tree left to right as if flattened onto the x-axis. In a binary search tree, like this one, that line is sorted.

## Do it by hand first

Ask "what comes first?" The leftmost node: start at 4 and keep going left, 4, 2, 1, until there is no left child. Write 1. Who is next? You have to go *back up* to 2. Write 2. Then 2 has a right subtree, so go there and again find its leftmost node: 3. Write 3. Back up, past 2 (already done), to 4. Write 4. Then 4's right subtree: leftmost is 5. Write 5.

```text
 going down-left you passed:   4, 2, 1
 coming back you needed them in reverse:  1, then 2, then 4
 -> a pile where the last thing put on is the first taken off
```

Your hand kept a list of **ancestors you walked past on the way down-left and still owe a visit**. You returned to them in reverse order. That is a stack.

## The first honest attempt

The textbook recursion: `inorder(left); visit(node); inorder(right)`. It is `O(n)` time and `O(h)` space, and nothing is recomputed. So what is wrong with it?

The stack is hidden inside the interpreter.

```text
 skewed tree, every node a left child:
   n
  /
 n-1          Python call stack: n frames deep
 /            default recursion limit ~1000
...           a 10^4-node chain -> RecursionError
 1
```

And you cannot pause after the third value and resume later, which a BST iterator or "k-th smallest" needs. The waste is not repeated work; it is control you gave away.

## The turning point

**Claim: the recursion's only state is the set of ancestors whose left subtree is in progress, and those are always pushed by sliding left, so an explicit stack of nodes reproduces the recursion exactly.**

A pending frame of `inorder(node)` has called `inorder(node.left)` and waits to visit `node`. Every such frame was created by moving left. Once it visits its node and calls `inorder(node.right)`, it has nothing left to do, so it need not stay on the stack.

That gives a loop with two moves:

- **Slide left.** From the current node, push every node on the way down the left spine until you fall off at `None`.
- **Pop and turn right.** Pop the top. Its left side is finished, so visit it. Then set the current node to its right child and slide left again from there.

```text
 while node or stack:
     while node:
         stack.append(node); node = node.left
     node = stack.pop(); out.append(node.val)
     node = node.right
```

The loop condition matters. After popping the root, the stack can be empty while the root's right subtree is still unexplored. `while stack` alone would stop there; `while node or stack` keeps going.

## Watch it work

Tree `[4,2,5,1,3]`. The stack is drawn bottom to top.

Frame 1. Slide left from the root.

```text
        [4]         stack: 4 2 1   (top = 1)
       /            node:  None    (fell off 1's left)
     [2]            out:   []
     /
   [1]
```

Three pushes; nothing visited yet.

Frame 2. Pop 1, visit it, turn right.

```text
 pop 1 -> out: [1]
 stack: 4 2      node: 1.right = None
```

1 has no right child, so the next slide does nothing.

Frame 3. Pop 2, visit it, turn right.

```text
 pop 2 -> out: [1, 2]
 stack: 4        node: 2.right = 3
```

2's left side is done, and the walk moves into 2's right subtree.

Frame 4. Slide left from 3 (just 3 itself), then pop it.

```text
 slide: stack 4 3
 pop 3 -> out: [1, 2, 3]
 stack: 4        node: None
```

Frame 5. Pop 4, visit it, turn right.

```text
 pop 4 -> out: [1, 2, 3, 4]
 stack: (empty)  node: 4.right = 5   <- stack empty, but
                                        node is not: keep going
```

This is the moment `while stack` would end the loop early.

Frame 6. Slide to 5, pop it; node and stack are both empty, so stop.

```text
 slide: stack 5;  pop 5 -> out: [1, 2, 3, 4, 5]
 stack: (empty)  node: None  -> loop ends
```

Invariant across frames: the stack held exactly the ancestors (and current node) whose left subtree was finished or in progress but who had not been visited yet, bottom to top in root-to-leaf order.

## Why it is correct

A node is pushed only when we slide past it going left, and popped only after everything pushed above it has been popped. Everything pushed above it is in its left subtree, and each of those is popped only after its own left subtree and right subtree have been fully processed. So when a node is popped, its entire left subtree has been output. It is output then, and immediately afterwards its right subtree is processed in full before anything below it in the stack is popped. That is the definition of inorder. Every node is reached either by sliding left or as some popped node's right child, so all nodes appear.

## Cost

- Time `O(n)`: each node is pushed once and popped once.
- Space `O(h)`: the stack holds at most one root-to-leaf spine. (Morris traversal reaches `O(1)` extra space by temporarily threading right pointers back to ancestors.)

## Variations you will meet

- **Preorder iteratively.** Visit when pushing, not when popping. Appending on push is also the bug that turns your inorder into preorder.
- **BST iterator (LeetCode 173).** Split the loop: the constructor slides left from the root; `next()` pops, then slides left from the popped node's right child. Amortised `O(1)` per call, `O(h)` memory.
- **Reverse inorder.** Swap `left` and `right` and you read the BST in descending order.

## What to carry forward

The stack is the list of ancestors still owed a visit: slide left pushing, pop to visit, step right, repeat. The next problem asks what makes a tree a BST at all, and one answer is "its inorder line is strictly increasing".
