# Kth Smallest Element in a BST (LeetCode 230)

**Area:** trees · **Difficulty:** Medium · **Key operations:** push the left spine, pop the next smallest, count down k, step to the right child

## Problem

Given the root of a binary search tree and an integer `k`, return the `k`-th smallest value in the tree (1-indexed).

## Example

```
[5, 3, 6, 2, 4, None, None, 1], k = 3

          5
         / \
        3   6
       / \
      2   4
     /
    1

sorted order 1, 2, 3, 4, 5, 6  ->  the 3rd is 3
```

## Brute force

Traverse the whole tree inorder (left, node, right), which for a BST yields the values in sorted order, store them in a list, and return index `k - 1`.

O(n) time and O(n) space. The wasted work: every node is visited and stored even when `k` is 1, and the traversal cannot stop early because the recursion has no way to say "done" without a flag threaded through every call.

## From brute force to optimal

Inorder order is the sorted order, so no sorting is ever needed; the only question is how to stop after `k` values. Make the traversal lazy with an explicit stack. Push the whole left spine from the root (the smallest value ends up on top). Pop: that is the next value in sorted order. Then move to the popped node's right child and push *its* left spine, because everything in that right subtree comes next in order. Count down `k` on each pop and return as soon as it hits zero. The stack holds the ancestors whose values are still pending, smallest on top.

## Intuition

Draw the tree with every node placed at the x-coordinate of its value. Inorder traversal is a sweep from left to right. The stack is the chain of nodes above and to the right of the sweep line that are still waiting to be reported. Each pop moves the sweep line one node to the right; stepping into the right child and diving left finds the very next node on the line. Because you can pause after any pop, you stop exactly at the `k`-th one.

## Walkthrough

The stack is drawn top first.

```
          5
         / \
        3   6
       / \
      2   4
     /
    1

push 5, go left          stack [5]
push 3, go left          stack [3, 5]
push 2, go left          stack [2, 3, 5]
push 1, go left          stack [1, 2, 3, 5]      left of 1 is None: dive ends
pop 1    k 3 -> 2        stack [2, 3, 5]         right of 1 is None
pop 2    k 2 -> 1        stack [3, 5]            right of 2 is None
pop 3    k 1 -> 0        stack [5]               k == 0: return 3
```

Node 4 and node 6 were never touched. Had `k` been 4, the walk would continue: step right from 3 to 4, push 4, pop 4 with `k` reaching 0.

## Steps

1. `stack = []`, `node = root`.
2. Loop: while `node` exists, push it and go left.
3. Pop the top; decrement `k`; if `k` is now 0, return the popped value.
4. `node = popped.right`; back to step 2.

## Complexity

O(h + k) time: the first dive pushes at most `h` nodes, and each of the `k` pops does amortised O(1) work. O(h) space for the stack.

## Pitfalls

- **Returning when `k == 1`.** `k` is 1-indexed and was just decremented, so the `k`-th pop is when it reaches 0. Checking for 1 returns one pop early (2 instead of 3 in the example), and `k = 1` never triggers, so the stack is popped empty.
- **Diving right instead of left.** Pushing the right spine emits the larger values first; the example returns 6 for `k = 3`.
- **Going left again after a pop.** The left subtree of a popped node was already emitted; stepping left re-pushes it and values repeat. `[3, 1, 4, None, 2]` with `k = 2` returns 3 instead of 2. After a pop, continue with the right child.
- **Visiting the node before its left subtree.** That is preorder, not sorted order. The dive must finish before the first pop.
- **Recursive inorder without an early exit.** It works but visits the whole tree; the explicit stack is what makes stopping at `k` natural.
