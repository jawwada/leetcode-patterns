# Diameter of Binary Tree

*LeetCode 543 · Easy · Pattern: Post-order height with side-channel answer · Reading time ~6 min*

## What the problem is really asking

The diameter is the number of **edges** on the longest path between any two nodes. A path goes up from one node to some
highest point and back down to another node; it never visits a node twice. It does not need to pass through the root.
The answer is one integer.

```text
          1
         /            longest path: 6-5-3-2-4
        2             edges: 6-5, 5-3, 3-2, 2-4  = 4
       / \
      3   4           it bends at 2 and never
     /                touches the root 1
    5
   /
  6
```

That last point is what makes it harder than depth: the best path can bend anywhere.

## Do it by hand first

Every path has exactly one highest node, where it bends. At that node, the path is "go down the left side as far as you
can, plus go down the right side as far as you can". So at each node, write two arm lengths: the height of the left
subtree and the height of the right subtree. The path bending there has `left + right` edges.

```text
node   left arm   right arm   path bending here
6      0          0           0
5      1          0           1
3      2          0           2
4      0          0           0
2      3          1           4   <- best
1      4          0           4
```

You kept track of **one height per node (to hand upward), and one best-so-far number (on the side)**. That is the
post-order template from the background, in full.

## The first honest attempt

For each node, compute `height(left) + height(right)` with a standalone `height()` function, and take the maximum over
all nodes.

```text
height() calls made from each node of the chain 2-3-5-6:

  at 2:  height(3) walks 3 5 6
  at 3:  height(5) walks   5 6     again
  at 5:  height(6) walks     6     again
```

Each subtree's height is recomputed for every ancestor, so a skewed tree costs O(n²). The heights we need at a node are
exactly the values the recursion computed for its children a moment ago.

## The turning point

**Claim: `height(node)` already holds `height(left)` and `height(right)` in hand at the moment it combines them, so the
diameter candidate `left + right` can be recorded right there, in the same single pass.**

The subtle part is that there are two different quantities at each node, and they must not be mixed up:

```text
             parent
               ^
               |  RETURN: 1 + max(left, right)
               |  (an arm the parent can extend;
               |   only ONE side can continue up)
            [ node ]
            /      \
       left arm   right arm
               |
               v
      RECORD: best = max(best, left + right)
      (a path that bends here; the parent
       cannot extend it, it uses both arms)
```

A path that bends at this node uses both arms, so it cannot continue upward; it is a finished candidate and goes into
`best`. A path that continues to the parent can use only one arm, the longer one, plus the edge to the parent: that is
the returned height.

Units: with `None` returning 0 and a leaf 1, the height counts nodes on the longest downward path, which equals the
number of edges from the parent down. So `left + right` is already in edges. Writing the unit beside each line saves you
from the off-by-one.

## Watch it work

Tree `[1,2,null,3,4,5,null,null,null,6]` from the picture. `ret` is the returned height; `best` is the side variable.
`*` marks the running call.

```text
Frame 1: h(6): L 0, R 0 -> best max(0, 0) = 0, ret 1
       1               stack: h(1) h(2) h(3) h(5)
      /
     2
    / \
   3   4
  /
 5
/
*6 ret 1                best = 0
```

The deepest leaf answers first.

```text
Frame 2: h(5): L 1, R 0 -> best 1, ret 2
       1               stack: h(1) h(2) h(3)
      /
     2
    / \
   3   4
  /
*5 ret 2               best = 1
```

The path 6-5 bends at 5 with one edge.

```text
Frame 3: h(3): L 2, R 0 -> best 2, ret 3
       1               stack: h(1) h(2)
      /
     2
    / \
 *3    4               best = 2
 ret 3
```

The left arm under 2 is now known to be 3 long.

```text
Frame 4: h(4): leaf, L 0, R 0 -> best stays 2, ret 1
       1               stack: h(1) h(2)
      /
     2
    / \
[3]3  *4 ret 1         best = 2
```

The right arm under 2 is 1 long.

```text
Frame 5: h(2): L 3, R 1 -> best max(2, 4) = 4, ret 4
       1               stack: h(1)
      /
    *2 ret 4           best = 4   (path 6-5-3-2-4)
    / \
 [3]   [1]
```

The best path is recorded at its bend. What goes up is only the longer arm plus one.

```text
Frame 6: h(1): L 4, R 0 -> best max(4, 4) = 4, ret 5
    *1 ret 5           answer = best = 4
    /                  (ret 5 is the height, not the
 [4]                    answer; it is discarded)
```

Across frames: the returned value is always the true height of that subtree, and `best` always equals the longest path
bending at any node already finished.

## Why it is correct

Every path has a unique highest node. The longest path whose highest node is v has `height(v.left) + height(v.right)`
edges, since each side independently goes as deep as possible. When `h(v)` runs, both heights are exact (induction, as in
Maximum Depth), so the candidate is recorded correctly. Every node is visited, so `best` ends as the maximum over all
bend points, which is the diameter.

## Cost

Time O(n): one post-order visit per node. Space O(h) for the stack. The brute force is O(n²) on a skewed tree.

## Variations you will meet

- **Binary tree maximum path sum.** Same shape, but values are weights and can be negative, so an arm with negative sum is
  replaced by 0. It appears later in this chapter.
- **Longest univalue path (LeetCode 687).** An arm counts only if the child has the same value as the node.
- **Diameter of an N-ary tree (LeetCode 1522).** Keep the two largest child heights.
- **Diameter of a general tree given as edges.** BFS from any node to the farthest node, then BFS again from there.

## What to carry forward

Return what the parent can extend; record what bends here. Two quantities per node, one goes up, one goes on the side.
The next problem passes information the other way: from the parent down to its children.
