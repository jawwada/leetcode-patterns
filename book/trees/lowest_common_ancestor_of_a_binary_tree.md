# Lowest Common Ancestor of a Binary Tree

*LeetCode 236 · Medium · Pattern: Post-order "found below me" recursion · Reading time ~9 min*

## What the problem is really asking

Same question as the previous problem, with the ordering taken away. You get an ordinary binary tree and two nodes `p` and `q` that are both in it. Return the deepest node that has both in its subtree; a node counts as being in its own subtree.

The answer is still the place where the root-to-`p` and root-to-`q` paths split. What changed is that a node's value no longer tells you which side a target is on. Standing at the root, you have no idea whether `p` is left or right.

Running example: `root = [3,5,1,6,2,0,8,null,null,7,4]`, `p = 6`, `q = 4`.

```text
                3
             /     \
            5       1
           / \     / \
          6   2   0   8
          p  / \
            7   4
                q
 path to 6:  3 -> 5 -> 6
 path to 4:  3 -> 5 -> 2 -> 4
                   ^ split here -> LCA = 5
```

## Do it by hand first

With the picture you just look, but imagine you can only see one node at a time. Then the natural way is to ask each subtree a question and wait for its answer: "is `p` or `q` down there?"

```text
 ask 5's left subtree   (6):        "I contain p"
 ask 5's right subtree  (2,7,4):    "I contain q"
 -> 5 has one target on each side: 5 is the split point
 ask 3's left subtree   (5,...):    "I contain both"
 ask 3's right subtree  (1,0,8):    "nothing here"
 -> 3 is a common ancestor, but not the lowest
```

Your hand kept, for each subtree, a tiny **report**: nothing, "found p", "found q", or "found the answer already". A parent decides by combining the two reports from its children. Reports flow *up* the tree, so this is a post-order recursion: children first, then the parent.

## The first honest attempt

Do what we did in the BST version, but with searching: one DFS that records the path from the root to `p` as a list of nodes, a second DFS for the path to `q`, then walk both lists in parallel and return the last node they share.

```text
 DFS for p visits: 3 5 6                 path [3,5,6]
 DFS for q visits: 3 5 6 2 7 4           path [3,5,2,4]
                   ^^^^^ walked again
 compare:  3=3  5=5  6!=2  -> LCA 5
```

It is `O(n)` time and `O(n)` space. The waste: the tree is searched twice, the shared prefix `3, 5` is stored twice, and both paths are built only to find where they diverge. One pass should be able to find both targets *and* notice the split as it happens.

## The turning point

**Claim: let each call return one node or `None`, meaning "the most useful thing I found in my subtree". Then the LCA is the first node, bottom-up, that receives a non-`None` report from both children, or that is itself a target.**

Define `f(root)`:

- If `root` is `None`, return `None`: nothing here.
- If `root` is `p` or `root` is `q`, return `root` immediately.
- Otherwise ask both children: `left = f(root.left)`, `right = f(root.right)`.
- If both are non-`None`, the targets are on different sides of `root`. Return `root`: it is the split point.
- Otherwise return whichever is non-`None` (or `None`), passing the report up unchanged.

The subtle step is the early return at `p` or `q`. Why can we stop at `p` without looking for `q` underneath it? Because both targets are guaranteed to exist. If `q` is *not* in `p`'s subtree, then `q` is somewhere else, and some ancestor will get `p` from one side and `q` from the other. If `q` *is* under `p`, then `p` is the LCA, and nobody above will ever see a second report, so `p` will be passed all the way up as the answer. Either way, returning `p` at once gives the right result, and we never need to know which case we are in.

So a report means "this subtree contains `p`", "contains `q`", or "contains the LCA". A parent never needs to tell these apart: it only checks whether one or both sides spoke.

Compare targets by identity (`root is p`), not by value. Values in this problem are unique, but the habit protects you in the variants where they are not.

## Watch it work

Tree as drawn, `p = 6`, `q = 4`. Post-order: each frame shows the reports arriving at a node.

Frame 1. The left-most call reaches 6, which is `p`.

```text
 f(3) -> f(5) -> f(6)
 6 is p -> return 6 immediately
 report at 5's left:  6
```

Frame 2. 5's right subtree: 7 finds nothing, 4 is `q`.

```text
 f(2) -> f(7): left None, right None -> None
 f(2) -> f(4): 4 is q -> return 4
```

Frame 3. Node 2 combines its reports.

```text
          2            left = None, right = 4
         / \           one side spoke -> pass it up
       None  4         f(2) returns 4
```

Frame 4. Node 5 combines.

```text
          5            left = 6, right = 4
         / \           BOTH sides spoke -> split here
        6   4          f(5) returns 5   (the LCA)
```

Frame 5. The right subtree of the root finds nothing.

```text
 f(1): f(0) -> None, f(8) -> None
 f(1) returns None
```

Frame 6. The root combines.

```text
          3            left = 5, right = None
         / \           one side spoke -> pass it up
        5  None        f(3) returns 5  -> answer 5
```

Across frames, every return value was either `None`, a target found in that subtree, or the LCA once it had been formed, and the LCA, once formed, was passed up unchanged because the other side of each ancestor was empty.

## Why it is correct

Claim, for any subtree `T` rooted at `r`:

- if `T` contains neither target, `f(r)` returns `None`;
- if `T` contains exactly one target, `f(r)` returns that target;
- if `T` contains both, `f(r)` returns their LCA.

Induction from the leaves up. `None` returns `None`. If `r` is a target, `f(r)` returns `r`: correct for the one-target case, and correct for the both-targets case because a target with the other target beneath it is the LCA. Otherwise `r` is not a target, and by induction each child reports correctly. If both children return non-`None`, one target is on each side, so the paths split at `r` and `r` is the LCA. If only one child returns non-`None`, everything `T` contains is in that child's subtree, so its report (target or LCA) is also the right report for `T`. If neither does, `T` contains nothing.

Apply it to the whole tree, which contains both targets: `f(root)` is the LCA.

## Cost

- Time `O(n)`: each node is visited at most once (the early return can skip a subtree below a target, which only helps).
- Space `O(h)`: the recursion stack. A skewed tree gives `O(n)`; an iterative version with a parent map trades the recursion for an `O(n)` dictionary.

## Variations you will meet

- **Targets may be missing (LeetCode 1644).** The early return is no longer safe: `p` alone would be reported as the LCA. Recurse fully, count how many targets were actually seen, and accept the answer only if the count is 2.
- **Nodes have parent pointers (LeetCode 1650).** Walk up from `p` and `q`; it becomes "intersection of two linked lists". Use two pointers that switch to the other start when they reach the top, and they meet at the LCA.
- **LCA of many nodes (LeetCode 1676).** Put the targets in a set and test `root in targets`; the same "one side or both sides spoke" rule works unchanged.
- **Back in a BST.** Use the previous problem's value-steered descent instead: `O(h)` time and `O(1)` space.

## What to carry forward

Collapse each subtree into a single report and let the parent combine two reports: the LCA is the first node where both sides speak. The next problem returns to the BST and its sorted inorder line, running two iterators outward from a target to collect the `k` closest values.
