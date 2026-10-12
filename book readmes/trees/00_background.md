# Trees

*28 problems · Reading time ~32 min*

## The chapter

A tree is a node with children, and the moment a node has two, loops give way to recursion. This chapter teaches how
to write a function for a node by trusting it on the children: returning one value up, carrying state down, walking
two trees in lockstep, sweeping by level with a queue, and exploiting the sorted order of a binary search tree.

Problems, in reading order:

1. [Maximum Depth of Binary Tree](maximum_depth_of_binary_tree.md) · Easy
2. [Invert Binary Tree](invert_binary_tree.md) · Easy
3. [Same Tree](same_tree.md) · Easy
4. [Symmetric Tree](symmetric_tree.md) · Easy
5. [Subtree of Another Tree](subtree_of_another_tree.md) · Easy
6. [Balanced Binary Tree](balanced_binary_tree.md) · Easy
7. [Diameter of Binary Tree](diameter_of_binary_tree.md) · Easy
8. [Sum of Left Leaves](sum_of_left_leaves.md) · Easy
9. [Path Sum](path_sum.md) · Easy
10. [Path Sum II](path_sum_ii.md) · Medium
11. [Count Good Nodes in Binary Tree](count_good_nodes_in_binary_tree.md) · Medium
12. [Binary Tree Maximum Path Sum](binary_tree_maximum_path_sum.md) · Hard
13. [Binary Tree Level Order Traversal](binary_tree_level_order_traversal.md) · Medium
14. [Binary Tree Right Side View](binary_tree_right_side_view.md) · Medium
15. [Cousins in Binary Tree](cousins_in_binary_tree.md) · Easy
16. [Vertical Order Traversal of a Binary Tree](vertical_order_traversal_of_a_binary_tree.md) · Hard
17. [Binary Tree Inorder Traversal](binary_tree_inorder_traversal.md) · Easy
18. [Validate Binary Search Tree](validate_binary_search_tree.md) · Medium
19. [Kth Smallest Element in a BST](kth_smallest_element_in_a_bst.md) · Medium
20. [Lowest Common Ancestor of a BST](lowest_common_ancestor_of_a_bst.md) · Medium
21. [Lowest Common Ancestor of a Binary Tree](lowest_common_ancestor_of_a_binary_tree.md) · Medium
22. [Closest Binary Search Tree Value II](closest_binary_search_tree_value_ii.md) · Hard
23. [Recover Binary Search Tree](recover_binary_search_tree.md) · Hard
24. [Construct Binary Tree from Preorder and Inorder Traversal](construct_binary_tree_from_preorder_and_inorder_traversal.md) · Medium
25. [Recover a Tree From Preorder Traversal](recover_a_tree_from_preorder_traversal.md) · Hard
26. [Serialize and Deserialize Binary Tree](serialize_and_deserialize_binary_tree.md) · Hard
27. [Serialize and Deserialize N-ary Tree](serialize_and_deserialize_n_ary_tree.md) · Hard
28. [Binary Tree Cameras](binary_tree_cameras.md) · Hard

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

## Advanced patterns

The basic moves (return a value up, carry a value down, sweep by rows, use the BST order) solve the Easy and Medium
problems on their own. The Hard problems in this chapter combine them in specific ways. Each pattern below is one of
those combinations. If you can name the pattern while reading a problem, you are most of the way to the solution.

### 1. Return one arm, record both arms

**When it shows up.** The answer is a path that may bend at any node: longest path, heaviest path, any "between two
nodes" quantity. Often the values can be negative.

**The intuition.** A path through the tree has exactly one highest node, where it bends. Below that node it goes down
at most two arms, one left and one right. So "best path overall" is "best over all nodes X of the best path that bends
at X". In post-order, when X holds both children's answers, it can score its own bending path right away. What it
hands its parent is something different: a path that goes down from X along one arm only, because the parent can attach
just one arm per side. Negative values add one rule. An arm that sums below zero is worse than no arm, so the parent
clips it to 0 before using it. The node's own value is never clipped, because a path must contain at least one node.

```text
 tree:      -10          post-order, arms clipped at 0
            /  \
           9    20       node  L   R   record      return
               /  \       9    0   0     9           9
              15   -7    15    0   0    15          15
                         -7    0   0    -7          -7
                         20   15   0    35  <- best 35
                        -10    9  35    34          25

 at 20: arm -7 clipped to 0, bend = 20+15+0 = 35
        return 20+15 = 35 (one arm only) to -10
```

The best path is 15 -> 20 with sum 35. Passing through -10 to reach 9 costs more than it gains: 34 < 35.

**Where you'll use it.** Diameter of Binary Tree (heights, no negatives) and Binary Tree Maximum Path Sum (weights,
clipping). Beyond the chapter: Longest Univalue Path (LeetCode 687), where an arm only counts if its value matches.

### 2. Post-order states and a greedy choice from the leaves

**When it shows up.** "Place the minimum number of X so that every node is covered / watched / monitored." Each node's
fate depends on its neighbours, both above and below.

**The intuition.** A number is not enough to describe a subtree here. What the parent needs to know is a small fact:
does this child need help, is it fine, or does it offer help upward? That gives three states: NEEDS, COVERED,
HAS_CAMERA. Decide from the leaves upward, and be lazy: a node puts a camera on itself only when a child NEEDS one,
because only then is the decision forced. A leaf never takes one: its parent can watch it, and from that higher spot
the parent also watches its own parent and the leaf's sibling. An empty child reports COVERED, since it needs nothing and
offers nothing. That one choice is what makes leaves report NEEDS. The root has no parent to defer to, so if it ends up
NEEDS, it pays for one more camera.

```text
 chain 1-2-3-4-5, states computed bottom-up:

   1  CAM      child 2 NEEDS  -> camera here     cameras
   |                                              = 2
   2  NEEDS    child 3 only COVERED, nobody sees me
   |
   3  COVERED  child 4 has a camera
   |
   4  CAM      child 5 NEEDS  -> camera here
   |
   5  NEEDS    leaf: both empty children COVERED
```

**Where you'll use it.** Binary Tree Cameras. The same "return a small state, act only when forced" idea solves House
Robber III (LeetCode 337), where each node returns the pair (best if robbed, best if not).

### 3. In-order as a sorted stream, read one step behind

**When it shows up.** A BST question that is really a question about its sorted sequence: k-th smallest, the minimum
gap between values, two values that were swapped, checking validity.

**The intuition.** In-order of a BST prints the values in increasing order. So any "look at neighbours in sorted
order" question becomes a question about adjacent pairs in that stream. You don't need the stream as a list. Keep one
pointer, `prev`, to the node visited just before the current one, and compare at each visit. For two swapped values,
a swap leaves one or two "dips" where `prev > cur`. The culprits are the left side of the first dip and the right side
of the last dip. The iterative walk with a stack is the natural host: each pop is the next value in sorted order.

```text
 BST 1..5 with 2 and 5 swapped:     in-order stream:

          3                         1   5   3   4   2
         / \                            \_/     \_/
        5   4                           dip     dip
       /     \                        5 > 3   4 > 2
      1       2
                      first  = prev of first dip = 5
                      second = cur of last dip   = 2
                      swap their values back
```

**Where you'll use it.** Binary Tree Inorder Traversal (the machine itself), Kth Smallest Element in a BST (stop after
k pops), Recover Binary Search Tree (dips). Beyond: Minimum Absolute Difference in BST (LeetCode 530).

### 4. Paused in-order iterators, started in the middle

**When it shows up.** You need the values of a BST in sorted order, but starting near some target and walking outward,
or you need two sorted streams merged without listing everything.

**The intuition.** The stack of the iterative in-order walk is a paused traversal. It holds exactly the ancestors whose
values are still to come, and its top is the next value. Instead of starting the walk at the minimum, you can start
it anywhere with one BST search. Going down toward the target, every node with value <= target goes on a predecessor
stack (then turn right), and every larger node goes on a successor stack (then turn left). When the search falls off,
the two tops are the closest values on each side. Advancing a successor stack pops the top, then pushes its right child
and that child's left chain. Predecessors mirror it. Each stream gets farther from the target as it advances, so the
k closest values come from merging the two heads, like the merge step of merge sort.

```text
 BST:      4          target 3.7, k = 2
          / \
         2   5        search: 4 > t  succ=[4], go left
        / \                   2 <= t pred=[2], go right
       1   3                  3 <= t pred=[2,3], go right
                                     -> None, stop

 heads: pred 3 (dist 0.7)   succ 4 (dist 0.3)
 take 4; succ pops 4, pushes 5        succ=[5]
 heads: pred 3 (dist 0.7)   succ 5 (dist 1.3)
 take 3                               answer [4, 3]
```

**Where you'll use it.** Closest Binary Search Tree Value II. Beyond: Binary Search Tree Iterator (LeetCode 173) and
Two Sum IV on a BST (LeetCode 653), which runs a forward and a backward iterator toward each other.

### 5. Self-delimiting pre-order: sentinels or counts, one cursor

**When it shows up.** "Serialize", "encode", "compare subtrees as strings", or any format where a tree must be
written as a flat sequence and read back without ambiguity.

**The intuition.** A plain pre-order list does not identify a tree: `1 2 3` could be a chain or a root with two
children. Write a sentinel `#` for every empty child and the ambiguity disappears, because every branch now says where
it ends. A tree of n nodes has n + 1 empty slots, so the tape is 2n + 1 tokens. The decoder is the encoder run in
reverse: read a token; if `#`, return None; else make a node, read its left subtree, then its right. One cursor moves
forward and never goes back. The pending recursive calls remember which slots are still open, so there is no index
arithmetic. When nodes have any number of children, write the child count after each value instead of sentinels, and
the decoder calls itself exactly that many times.

```text
 tree:     1
          / \       tape:  1 2 # # 3 4 # # 5 # #
         2   3      index: 0 1 2 3 4 5 6 7 8 9 10
            / \                     ^
           4   5                   cursor at index 4

 after 4 tokens: read(2) is done (both # consumed);
 read(1) has its left child and now calls read() for
 its right, which will consume tokens 4..10
 n = 5 nodes, 6 sentinels, 11 tokens = 2n + 1
```

**Where you'll use it.** Subtree of Another Tree (serialize both, then substring search), Serialize and Deserialize
Binary Tree, Serialize and Deserialize N-ary Tree. Beyond: Find Duplicate Subtrees (LeetCode 652), which uses each
subtree's serialization as a hash key.

### 6. Rebuilding from a traversal: the root comes first, the boundary is found, not scanned

**When it shows up.** "Construct the tree from these traversals", or a string that describes a tree by depth.

**The intuition.** Pre-order always writes a root before its subtrees, so it tells you who the root is. It does not
tell you where the left subtree ends. Something else must answer that. With an in-order list, the root's position
splits it into left and right parts. A dict from value to in-order index makes that lookup O(1), so the whole build is
O(n) instead of O(n^2). With depth markers (dashes), the answer is a stack whose length is the current depth: a node at
depth d pops the stack down to length d, and the top is its parent. Everything popped belonged to subtrees that pre-order
has finished and will never revisit. In both cases you never search ahead for where a subtree stops; the structure of
the input tells you when you get there.

```text
 pre  = [3, 9, 20, 15, 7]   in = [9, 3, 15, 20, 7]
                                   0  1   2   3  4
 root 3 -> in-index 1 -> left = in[0..0], right = in[2..4]
 root 9 -> in-index 0 -> a leaf
 root 20 -> in-index 3 -> left = in[2..2], right = in[4..4]

 "1-2--3--4-5--6--7", depth stack by token:
   token 4, d=2: pop to len 2 -> [1, 2], parent 2, push 4
   token 5, d=1: pop to len 1 -> [1],    parent 1, push 5
                 stack now [1, 5]; subtree of 2 is closed
```

**Where you'll use it.** Construct Binary Tree from Preorder and Inorder Traversal (index map), Recover a Tree From
Preorder Traversal (depth stack). Beyond: Construct Binary Search Tree from Preorder Traversal (LeetCode 1008), where
(low, high) bounds replace the in-order list.

### 7. Coordinates first, then sort

**When it shows up.** The output order is geometric (columns, diagonals, a picture of the tree on a grid) and
does not follow any traversal order.

**The intuition.** No single walk visits nodes in "column, then row, then value" order. So stop trying to make one
do it. Give every node coordinates during any walk: the root is (row 0, col 0), a left child is (row + 1, col - 1),
a right child is (row + 1, col + 1). Each coordinate comes from the parent in O(1), carried down like depth. Once every
node is a record, the tree's shape no longer matters. Sort by a tuple key in priority order, and group. Python compares
tuples element by element, so `(row, val)` sorted inside each column bucket applies both tie rules at once.

```text
 tree:        1           (row, col) per node:
            /   \         1 (0, 0)
           2     3        2 (1,-1)   3 (1, 1)
          / \   / \       4 (2,-2)   6 (2, 0)
         4   6 5   7      5 (2, 0)   7 (2, 2)

 column 0 bucket: (0,1) (2,6) (2,5) -> sorted -> [1, 5, 6]
 6 and 5 share a cell, so the smaller value goes first
 answer: [[4], [2], [1, 5, 6], [3], [7]]
```

**Where you'll use it.** Vertical Order Traversal of a Binary Tree. The "carry a coordinate down" half also appears in
Cousins in Binary Tree (depth and parent). Beyond: Maximum Width of Binary Tree (LeetCode 662), where the coordinate is
a heap-style position index.

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

The order is built so that each problem reuses the previous one's machinery and adds one new piece. The early problems
are short on purpose: their job is to make "trust the child" feel automatic before the Hard problems lean on it.

### Warm-up: one function, one value up

**Maximum Depth of Binary Tree.** It sounds like you must explore every root-to-leaf path and keep the longest. You
don't: the depth of a node is one more than the deeper child's depth, and that single sentence is the whole solution.
This is where you learn to write the function for one node and trust the calls on its children.

**Invert Binary Tree.** Same one-visit-per-node walk, but now the work is changing the tree instead of computing a number.
The trap is losing a child while swapping. The new idea is that recursion can rebuild a structure, not just measure it.

**Same Tree.** Now there are two trees, walked in lockstep with two fingers. The interesting part is the base cases:
both empty, one empty, values differ. Get those three right and the recursion writes itself.

**Symmetric Tree.** Lockstep again, but within one tree and in mirror image: the left's left pairs with the right's
right. The question to ask is "what are the two things I am comparing?" The answer is two subtrees, not one node,
and that is the step up from Same Tree.

**Subtree of Another Tree.** The obvious answer runs Same Tree from every node, which is O(n * m). The curious question
is whether a tree can be turned into a string so that "subtree" becomes "substring". It can, if empty children are
written down as markers. This is your first look at serialization.

### Returning more than an answer

**Balanced Binary Tree.** Checking balance at every node and recomputing heights each time costs O(n^2) on a stick. The
fix is to return the height and fold the check into it, with -1 as a "already failed below" signal that stops the work
early. One return value now carries two meanings.

**Diameter of Binary Tree.** The longest path may not touch the root at all, which breaks the naive "height of left plus
height of right at the root" answer. The function returns a height, but at every node it records left + right on the
side. This is the "return one arm, record both" template in its cleanest form.

### Carrying state down

**Sum of Left Leaves.** A node cannot tell on its own whether it is a left child; only its parent knows. So the parent
passes that fact down as an argument. This is the first time information flows down instead of up.

**Path Sum.** Carry a running total down and test it at the leaves. The trap is testing at a node with one child,
which is not a leaf. The idea is that the argument you pass down is the state of the path so far.

**Path Sum II.** Now you need every matching path, not just yes or no. Copying the path at each step is wasteful; the
better move is one shared list, append on the way down, pop on the way up. That append-recurse-pop rhythm is
backtracking, and it is also where the "forgot to copy the path" bug lives.

**Count Good Nodes in Binary Tree.** A node is good if nothing above it is bigger. You don't need the whole path, only
its maximum. The lesson is to carry the smallest summary of the path that answers the question.

**Binary Tree Maximum Path Sum.** Diameter's template, but with values that can be negative. Now an arm can hurt, so it
is clipped at zero, and the answer must start at negative infinity because a path needs at least one node. It is Hard
because three small details (clip, no clip on the node itself, initial value) must all be right at once.

### Thinking in rows

**Binary Tree Level Order Traversal.** Switch from depth to breadth. A queue holds the next nodes, and taking a snapshot
of its length tells you where one row ends. The question it answers is "how do I know a level is over?"

**Binary Tree Right Side View.** One node per row: the last one popped in each level. The DFS alternative is just as
instructive: visit right before left and keep the first node seen at each new depth.

**Cousins in Binary Tree.** Two nodes are cousins if they share a depth but not a parent. Carry both facts down, then
compare two pairs. It is short, but it trains you to carry a tuple of facts rather than one.

**Vertical Order Traversal of a Binary Tree.** No traversal visits nodes column by column with the right tie rule. The
way out is to stop fighting the shape: give every node coordinates, then sort records. It is the chapter's first lesson
that a tree problem can turn into a sorting problem.

### The BST order

**Binary Tree Inorder Traversal.** The recursive version is three lines. The real content is the iterative one: a
stack that holds the left spine still to visit. Every later BST problem that needs to stop early, pause, or run two
walks at once is built on this machine.

**Validate Binary Search Tree.** Checking each node against its parent passes on trees that are wrong. The BST rule is
global, so each node must sit inside a (low, high) window inherited from all its ancestors. Bounds carried down are
the new idea.

**Kth Smallest Element in a BST.** In-order is sorted, so the k-th pop is the answer. The interesting part is stopping:
the iterative walk lets you quit after k pops instead of building the whole list.

**Lowest Common Ancestor of a Binary Search Tree.** With order, you never need to search both sides. Walk down from the
root; while both targets are on the same side, go that way. The first node where they split is the answer.

**Lowest Common Ancestor of a Binary Tree.** Without order, you can't tell which side a node is on without looking. So
each call reports "I found something below me", and the first node that hears yes from both sides (or is a target
itself with a yes below) is the answer. It turns the BST descent into a post-order signal.

**Closest Binary Search Tree Value II.** Listing everything and sorting by distance ignores the BST. The better question
is: can an in-order walk start at the target and go both ways? Two paused iterators, seeded by one search, merge outward.
It builds directly on the iterative in-order stack.

**Recover Binary Search Tree.** Two values were swapped; find them without a list. The in-order stream now has one or
two dips, and one pointer to the previous node is enough to spot them. It reuses the same walk, now watching neighbours.

### Building and flattening

**Construct Binary Tree from Preorder and Inorder Traversal.** Pre-order tells you the root; in-order tells you how
many nodes go left. Scanning for the root each time costs O(n^2); an index map makes it O(n). This is the first time
you reverse a traversal.

**Recover a Tree From Preorder Traversal.** Now the input is one string with dashes for depth. There is no in-order to
split on, so the question is how to know where a subtree ends. A stack indexed by depth answers it: a shallower token
pops the finished nodes.

**Serialize and Deserialize Binary Tree.** Now you design the format yourself. Pre-order with a `#` for every empty
child is complete, and the reader is the writer's recursion run backwards with one cursor. It ties back to the string
trick from Subtree of Another Tree.

**Serialize and Deserialize N-ary Tree.** Any number of children breaks the "two `#` per leaf" rule. Writing a child
count after each value restores self-delimiting order. The idea generalises: the format must tell the reader how much
to read next.

### The finale

**Binary Tree Cameras.** The minimum number of cameras to watch every node. It looks like it needs search over
placements, but a post-order that returns one of three states, with a lazy rule (only take a camera when a child needs
one), is provably optimal. It combines the post-order template from Diameter with a greedy argument, and it is the best
test of whether "decide what goes up" has become second nature.
