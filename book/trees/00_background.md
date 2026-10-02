# Trees

*28 problems · Reading time ~20 min*

## Why this chapter exists

A tree is the first data structure most people meet that is not a line. Arrays and linked lists have a "next"; a tree has
"children", and the moment there are two of them, the loops you know stop working. What replaces the loop is recursion,
and the whole chapter is really about one skill: writing a function for a node by assuming it already works for the
node's children.

The twenty-eight problems fall into families:

- **Return one number up.** Depth, inversion, balance, diameter: a post-order function that hands its parent a single
  value (maximum depth, invert, balanced, diameter, maximum path sum).
- **Walk two trees at once.** Compare positions in lockstep (same tree, symmetric tree, subtree of another tree).
- **Carry something down.** The parent hands each child a running sum, a running maximum, or a path (sum of left leaves,
  path sum, path sum II, count good nodes, cousins).
- **Process by level.** A queue sweeps the tree one row at a time (level order, right side view, vertical order).
- **Use the BST order.** Left is smaller, right is larger, so in-order is sorted and descents can skip half the tree
  (in-order traversal, validate BST, k-th smallest, LCA of a BST, closest values II, recover BST).
- **Find where two nodes meet.** A post-order "did you find it below you?" signal (LCA of a binary tree).
- **Build and flatten.** Turn a tree into a string or traversal and back again (construct from preorder and inorder,
  recover from preorder string, serialize binary and n-ary trees).
- **Decide with states.** A post-order function that returns one of several states instead of a number (binary tree
  cameras).

## What it is

A binary tree is either **empty**, or a **node** holding a value and two binary trees, called left and right. Read that
definition twice: it mentions itself. A tree is a node plus two smaller trees. Everything in this chapter is that sentence
turned into code.

```text
        3            the shape:  node 3, plus
       / \           left tree  = {9}
      9   20         right tree = {20, 15, 7}
         /  \        and 20 is itself a node plus
        15   7       two smaller trees {15} and {7}
```

In memory there is no "tree" object. There are node objects, each holding a value and two pointers. A missing child is
`None`. The tree is whatever you can reach from the root pointer.

```text
 root
  |
  v
 +-----+------+-------+
 | 3   | left | right |
 +-----+--|---+---|---+
          |       +---------------+
          v                       v
 +-----+------+-------+   +------+------+-------+
 | 9   | None | None  |   | 20   | left | right |
 +-----+------+-------+   +------+--|---+---|---+
                                    v       v
                                 [15 . .] [7 . .]
```

LeetCode writes trees as a level-order list with `null` for missing children: `[3,9,20,null,null,15,7]`. Read it row by
row: 3; then its children 9, 20; then 9's children null, null; then 20's children 15, 7. Trailing nulls are dropped.

```text
index:  0  1  2   3     4     5   6
list:  [3, 9, 20, null, null, 15, 7]
        |  \__/   \_________/ \___/
       root kids  kids of 9   kids of 20
                  (both gone)
```

**Trust the call on the child.** To compute something for a node, pretend the function already returns the right
answer for the left tree and for the right tree. Your only job is to combine those two answers with the node itself,
and to handle the empty tree. You never trace the whole recursion in your head. The recursion mirrors the shape: one
call per node, the call tree of the program is the tree itself.

```text
   f(3) = combine(3, f(left), f(right))
           |          |          |
           |       trust it   trust it
           +-- your only job: this line, plus f(None)
```

**Three orders of visiting.** A recursive walk reaches each node three times: before its left subtree, between the two
subtrees, and after both. Doing your work at one of those moments gives pre-order, in-order or post-order.

```text
          1          pre-order  (node, L, R):  1 2 4 5 3
         / \         in-order   (L, node, R):  4 2 5 1 3
        2   3        post-order (L, R, node):  4 5 2 3 1
       / \
      4   5          level order (by rows):    1 | 2 3 | 4 5

   the walk touches node 2 three times:
     pre  : arrive at 2 from 1, going down
     in   : come back up from 4, about to go to 5
     post : come back up from 5, about to leave for 1
```

Pre-order is for passing information **down** (a running sum, the path so far). Post-order is for passing information
**up** (heights, counts, "found it"). In-order matters for binary search trees, where it visits values in sorted order.

**The post-order template.** Most problems in the first half of this chapter have the same skeleton: a helper returns a
value to the parent, and while it holds both children's values it records a candidate answer in a variable outside the
recursion.

```text
            parent  <-- receives ONE value (e.g. height)
              ^
              | return up: what the parent can extend
           [ node ]
           /      \
        L-value  R-value
              |
              v
       record on the side: best = max(best, L + R)
       (answer that BENDS here; parent cannot extend it)
```

What goes up and what gets recorded are usually different things, and confusing them is the classic bug. Diameter and
maximum path sum are the cleanest examples.

**Breadth-first by level.** Some questions are about rows: "the rightmost node of each level", "the average of each
level". A queue processes the tree row by row. Snapshot the queue's length at the start of a row; pop exactly that many,
pushing their children to the back.

```text
tree:   1         queue before row     row popped    pushed
       / \        [1]                  1             2 3
      2   3       [2, 3]               2 3           4 5
     / \          [4, 5]               4 5           -
    4   5         []                   done
```

**Binary search trees.** A BST adds one ordering rule: every value in the left subtree is smaller than the node, every
value in the right subtree is larger. That makes in-order traversal emit sorted values, and lets a search discard half
the tree at every step.

```text
        8           in-order: 1 3 6 8 10 14  (sorted)
       / \
      3   10        search 6: 6<8 go left, 6>3 go right, found
     / \    \
    1   6    14
```

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| Visit every node (any order) | O(n) | each node is entered once |
| Recursion stack of a DFS | O(h) | one frame per level on the current path |
| BFS queue | O(w) | at most one full level, width w |
| Height of a tree | O(n) | post-order, one visit per node |
| Search / insert in a BST | O(h) | one comparison per level, then go one way |
| In-order of a BST | O(n) | sorted output with no sort |
| Build from level-order list | O(n) | queue hands out child slots in order |
| Compare two trees | O(min(n, m)) | stops at the first mismatch |

**Height versus size.** n is the number of nodes, h the number of levels. The same n can give very different h.

```text
 balanced, n = 7, h = 3        skewed, n = 4, h = 4
         4                     1
       /   \                    \
      2     6                    2
     / \   / \                    \
    1   3 5   7                    3
                                    \
  h ~ log2(n + 1)                    4      h = n
```

Every "O(h)" in this chapter means O(log n) on a balanced tree and O(n) on a stick. Interviewers ask about the stick.

**Recursion depth is the call stack.** When the recursion is at a node, every ancestor of that node has a paused frame
waiting for it. The stack is the path from the root to where you are.

```text
 tree           while visiting 15, the stack is:
    3            +----------------------+
   / \           | f(15)   <- running   |
  9   20         | f(20)   waiting on R |
     /  \        | f(3)    waiting on R |
    15   7       +----------------------+
                 depth 3 = path 3 -> 20 -> 15
```

Python allows about 1000 frames by default. A skewed tree of 10^4 nodes crashes a naive recursion; either raise the limit
or rewrite with an explicit stack that holds exactly these frames.

## The invariant

**Every recursive call returns the correct answer for the subtree rooted at its node, and uses nothing but that subtree
plus whatever was handed down from the parent.** If that holds for the two children, combining correctly makes it hold
for the node; the empty tree is the base. That is induction on the shape, and it is how you prove every solution here.

```text
 legal: f uses only its subtree       illegal: f peeks sideways
                                         or relies on a global
     [ f(node) ]                         that a cousin changed
      /       \
  f(L) ok    f(R) ok                    [ f(2) ] ----> reads 7?
                                         /   \
  combine(node, f(L), f(R))             4     5        7 is not
                                                       below 2
```

For BSTs the invariant is the ordering, and it is **global**, not parent-to-child:

```text
 legal BST             illegal: every parent-child pair looks
                       fine, but 9 sits in 8's LEFT subtree
     8                        8
    / \                      / \
   3   10                   3   10
  / \                      / \
 1   6                    1   9   <- 9 > 3 ok locally,
                                     9 > 8 breaks the rule
```

## How to picture it

Picture the tree drawn on a whiteboard with values **flowing**. Pre-order work is water poured in at the root, running
down each branch and carrying something with it (a sum, a bound, a path). Post-order work is bubbles rising from the
leaves: each node collects two bubbles from below, merges them into one, and sends it up, while sometimes jotting a
record on the side. BFS is a horizontal line sweeping down the drawing one row at a time.

```text
   down (pre-order)        up (post-order)       across (BFS)
        |                       ^                ---- row 0 ----
        v                       |                ---- row 1 ----
       [n]                     [n]               ---- row 2 ----
      /   \                   ^   ^
     v     v                  |   |
```

For a BST, picture the values projected onto a number line: the tree is a recipe for binary search over that line.

## Signals in a problem statement

- "binary tree", "root", "subtree", "leaf": recursive DFS on the shape, base case on `None`.
- "depth", "height", "longest path", "diameter", "balanced": post-order returning a height.
- "path from root to leaf", "sum along the path", "good node (no larger ancestor)": carry state down in pre-order.
- "each level", "row", "right side", "zigzag", "minimum depth by edges": BFS with a queue, level snapshot.
- "BST", "k-th smallest", "valid", "closest value", "sorted order": in-order traversal or ordered descent with bounds.
- "two nodes", "common ancestor": post-order "found below me" signal.
- "serialize", "encode", "construct from traversals": pre-order with null markers, or a recursive build with index ranges.
- "minimum number of cameras / guards to cover": post-order greedy with states.
- Counter-signal: "graph" with cycles or multiple parents means a visited set; this is the graph chapter, not this one.
- Counter-signal: a tree given as edges `[[u, v], ...]` with no root is a graph problem; build adjacency first.
- Counter-signal: "prefix" over strings points to tries.

## Python toolbox

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

from collections import deque
q = deque([root])                    # BFS; popleft() is O(1)
for _ in range(len(q)): node = q.popleft()   # one level

import sys; sys.setrecursionlimit(10**5)     # deep skewed trees

stack, node = [], root               # iterative in-order
while stack or node:
    while node: stack.append(node); node = node.left
    node = stack.pop(); visit(node); node = node.right

best = float('-inf')                 # side-channel answer
def go(n):                            # inside a method use
    nonlocal best                     # nonlocal or self.best
```

`list.pop(0)` is O(n), never use it as a queue. Default arguments like `path=[]` are shared across calls; pass the list
explicitly. `a is b` on two possibly-`None` nodes is the cleanest "both empty" test.

## Mistakes people make

- Returning 1 for an empty tree in a height function. Fix: `None` is height 0, a leaf is 1.
- Counting nodes when the question counts edges (diameter). Fix: write the unit next to the return statement.
- Returning the recorded answer upward instead of the extendable value. Fix: return `1 + max(L, R)`, record `L + R`.
- Swapping children with two plain assignments, losing one. Fix: tuple-assign both at once.
- Checking BST validity only against the parent. Fix: pass down (low, high) bounds.
- Treating "leaf" as "has no left child". Fix: a leaf has neither child.
- Comparing node values before checking for `None`. Fix: handle `None` first.
- Using `list.pop(0)` for BFS. Fix: `collections.deque.popleft()`.
- Mutating a shared path list and appending it to results without copying. Fix: append `path[:]`, pop after recursing.
- Recursing 10^4 deep in Python. Fix: raise the recursion limit or use an explicit stack.

## The journey ahead

1. **Maximum depth**: the first "trust the child" function; return one number up.
2. **Invert**: the same walk, but the work is a change to the tree, not a value.
3. **Same tree**: recursion over two trees in lockstep.
4. **Symmetric tree**: lockstep again, but crossing over (outer with outer, inner with inner).
5. **Subtree of another tree**: lockstep from every node, then a pre-order string that makes it linear.
6. **Balanced**: return a height up, and a sentinel when a check fails below.
7. **Diameter**: return a height up, record an answer on the side; the template in full.
8. **Sum of left leaves**: the parent hands a fact down (am I a left child?).
9. **Path sum**: carry a running total down to the leaves.
10. **Path sum II**: carry the whole path down and backtrack it.
11. **Count good nodes**: carry the running maximum down.
12. **Maximum path sum**: the diameter template with negative values, so arms can be dropped.
13. **Level order**: the BFS queue with a level snapshot.
14. **Right side view**: the last node of each level, or first-visit per depth in DFS.
15. **Cousins**: same depth, different parent; carry both down.
16. **Vertical order**: give every node coordinates, then sort.
17. **In-order traversal**: the iterative stack version of the walk.
18. **Validate BST**: (low, high) bounds carried down.
19. **K-th smallest in a BST**: in-order with early stop.
20. **LCA of a BST**: one ordered descent; the split point is the answer.
21. **LCA of a binary tree**: no order, so post-order "found below me".
22. **Closest BST values II**: two in-order iterators walking outward.
23. **Recover BST**: in-order with a previous pointer to spot two swapped values.
24. **Construct from preorder and inorder**: build a tree from index ranges.
25. **Recover from preorder string**: build with a stack of ancestors by depth.
26. **Serialize binary tree**: pre-order with null markers, read back by a cursor.
27. **Serialize n-ary tree**: child counts replace null markers.
28. **Binary tree cameras**: post-order returning one of three states, greedy from the leaves.
