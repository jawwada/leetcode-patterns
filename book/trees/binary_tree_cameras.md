# Binary Tree Cameras

*LeetCode 968 · Hard · Pattern: Greedy post-order with 3-state return · Reading time ~11 min*

## What the problem is really asking

You may install cameras on nodes of a binary tree. A camera watches its own node, its parent, and its children, so it covers distance one in every direction. Find the minimum number of cameras so that every node is watched.

The answer is one number. This is a covering problem, the kind that is NP-hard on general graphs. What makes it solvable here is the tree shape, and what makes it hard is that a node's fate depends on both directions. A node can be covered by a camera below it (a child), at it, or above it (its parent). A plain post-order return value like "height" or "best path" has no way to say "I am fine, but only if my parent helps".

```text
example: 7 nodes, answer 3

             A
           /   \
          B     E
         /       \
        C         F
       /           \
      D             G

cameras on C, F, A  ->  every node watched
```

## Do it by hand first

Start where the choices are most obvious: the leaves. Leaf `D` must be watched by a camera on `D` or on `C`. Which is better? A camera on `D` watches `D` and `C`. A camera on `C` watches `D`, `C`, and `B`. The camera on `C` covers everything the leaf camera would, and more, so never put a camera on a leaf. The same goes for `G`, where you put the camera on `F`.

```text
camera on D covers {D, C}
camera on C covers {D, C, B}   <- strictly more
```

Now look upward. `C` has a camera, so `B` is watched from below and needs nothing more. `F` has a camera, so `E` is watched. What about `A`? Its children `B` and `E` are watched, but neither has a camera, so nothing watches `A`. Normally we would ask `A`'s parent to take a camera, which would be the lazy choice. But `A` is the root and has no parent, so `A` gets a camera itself. That makes 3.

What did your hand track at each node? Not just "covered or not". You needed three answers: "I am not watched yet, so my parent must take a camera" (`D`, `G`, `A`); "I am watched but have no camera, so I do nothing for my parent" (`B`, `E`); and "I have a camera, so my parent is watched for free" (`C`, `F`). Those three states are the whole algorithm.

## The first honest attempt

Try every subset of nodes as camera positions, smallest subsets first, and stop at the first one that watches everything. Checking a subset costs `O(n)`, and there are `2^n` subsets, so the cost is `O(2^n · n)`. With 7 nodes that is 128 subsets. With 1000 nodes it is impossible.

```text
subsets that put a camera on D or G (a leaf):
  {D, ...}  {G, ...}  {D, G, ...}  ...
  every one of them is dominated by moving the camera
  one level up, yet the brute force checks them all

and the question "is C's subtree OK, and does C need
its parent?" is re-answered for every subset that
agrees on C's subtree but differs elsewhere
```

The waste has two layers. Most subsets are obviously bad, since they waste cameras on leaves. And the status of a subtree depends only on the cameras inside it plus one bit of help from above, yet each global subset re-derives it from scratch.

## The turning point

**Claim: summarise every subtree by one of three states, and decide greedily bottom-up: a node takes a camera only when a child is unwatched, and never otherwise.**

The three states a node reports to its parent:

```text
NEEDS     : I am not watched. Parent, you must take a camera.
COVERED   : I am watched, no camera here. Do nothing for me.
HAS_CAMERA: I have a camera. You (my parent) are watched.
```

The rules, applied in post-order once both children have reported:

1. If either child reports **NEEDS**, take a camera: `cameras += 1`, report **HAS_CAMERA**. This is forced, because an unwatched child can now only be saved by itself, its own children (already decided), or us. Of those, we cover the most.
2. Else, if either child reports **HAS_CAMERA**, report **COVERED**. We are watched from below for free.
3. Else (both children COVERED), report **NEEDS**. Nobody watches us, and we defer to our parent, which is the lazy choice.

Two edge details carry most of the bugs:

- **An empty child reports COVERED.** It needs nothing and offers nothing. With that choice, a leaf sees two COVERED children and reports NEEDS, so its parent takes the camera. That is the "never a camera on a leaf" rule, falling out automatically. If null reported NEEDS, every leaf would take a camera. If null reported HAS_CAMERA, leaves would think they are watched.
- **The root has no parent to defer to.** If the root reports NEEDS, add one camera at the end.

Why is laziness right? A node that is NEEDS can be covered by its parent, by itself, or by a child. Its children already chose not to have cameras (otherwise it would be COVERED). Between itself and its parent, a camera at the parent watches the node, the parent, the grandparent, and the sibling. A camera at the node watches only the node, its children (already fine) and the same parent. So the higher position is never worse. Deferring keeps every option open, and acting when forced picks the highest spot that still saves the child.

Compare this with the earlier post-order problems. Diameter and Maximum Path Sum also return one thing upward while updating a global answer. Here the returned thing is a small state machine instead of a number, and the global answer is a camera counter.

## Watch it work

The tree from the top, with post-order visits `D C B G F E A`. A null child reports COVERED, written `cov`.

Frame 1. `D` is a leaf, and both children report `cov`. Rule 3 applies: `D` reports NEEDS.

```text
             A                    D: (cov, cov) -> NEEDS
           /   \                  cameras = 0
          B     E
         /       \
        C         F
       /           \
     [D]=NEEDS      G
```

Frame 2. `C` has left = NEEDS, so rule 1 applies: `C` takes a camera and reports HAS_CAMERA.

```text
             A                    C: (NEEDS, cov) -> CAM
           /   \                  cameras = 1
          B     E
         /       \
       [C]=CAM    F
       /           \
      D             G
```

Frame 3. `B` has left = HAS_CAMERA and right = null (`cov`). Rule 2 applies: `B` reports COVERED with no camera.

```text
             A                    B: (CAM, cov) -> COVERED
           /   \                  cameras = 1
       [B]=cov  E
         /       \
        C*        F               * = camera
       /           \
      D             G
```

Frame 4. Now the right side. `G` is a leaf and reports NEEDS. `F` sees right = NEEDS and takes a camera.

```text
             A                    G: (cov, cov) -> NEEDS
           /   \                  F: (cov, NEEDS) -> CAM
          B     E                 cameras = 2
         /       \
        C*      [F]=CAM
       /           \
      D            [G]=NEEDS
```

Frame 5. `E` has right = HAS_CAMERA, so it reports COVERED.

```text
             A                    E: (cov, CAM) -> COVERED
           /   \                  cameras = 2
          B   [E]=cov
         /       \
        C*        F*
       /           \
      D             G
```

Frame 6. `A` sees `B` = COVERED and `E` = COVERED. Rule 3 applies: `A` reports NEEDS. It is the root and has no parent, so the final check adds a camera.

```text
           [A]=NEEDS -> +1        A: (cov, cov) -> NEEDS
           /   \                  root check: cameras = 3
          B     E
         /       \                cameras: C, F, A
        C*        F*
       /           \
      D             G
```

The answer is 3. The brute force confirms that no 2-camera placement exists. Across frames, every node in a finished subtree was watched except possibly the subtree's root, and the root's report said exactly which of the three situations it was in. A camera appeared only in a frame where a child said NEEDS, plus once at the root.

## Why it is correct

There are two parts: what the states mean, and why the count is minimal.

**The states are honest.** By induction in post-order: after `dfs(x)` returns, every node strictly below `x` is watched, and the return value correctly describes `x`. Below `x`, a child that reported NEEDS was the only possibly-unwatched node in its subtree, and rule 1 puts a camera on `x`, which watches it. If no child reported NEEDS, both child subtrees are fully watched. Then `x` is watched exactly when a child has a camera (rule 2) or it gets one (rule 1). Otherwise it truthfully reports NEEDS. The root check fixes the last possible gap, so the final placement watches every node.

**The count is minimal (exchange argument).** Use induction over post-order. The hypothesis is that some optimal placement `S` agrees with greedy on every node processed so far. Now process node `p`.

- *Greedy puts a camera on `p` because child `c` reported NEEDS.* In greedy, and therefore in `S`, `c` and `c`'s children have no camera, and everything below `c` is watched by deeper cameras. `S` must still watch `c`, and the only spot left is `p`. So `S` already agrees.
- *Greedy leaves `p` empty, but `S` has a camera there.* No child of `p` is NEEDS, so everything below `p` is watched without that camera. Its only remaining jobs are watching `p` and `p`'s parent. Move it to `p`'s parent, which watches both and more. The new placement is still valid, no larger, and agrees with greedy at `p`. At the root this case cannot arise, because the root check puts a camera there exactly when one is needed.

At the end, greedy's placement equals an optimal one.

On the example you can also see it directly. `D` needs a camera in `{C, D}`, `G` needs one in `{F, G}`, and `A` needs one in `{A, B, E}`. These three sets are disjoint, so at least 3 cameras are required.

## Cost

- **Time `O(n)`.** Each node is visited once in post-order, with constant work.
- **Space `O(h)`** for the recursion stack. The state is one small integer per frame.
- The brute force is `O(2^n · n)`. A full tree DP with three values per node (min cameras if this node has a camera, if it is covered without one, if it is not yet covered) is also `O(n)`. It is the safe fallback when you do not trust the greedy, and it generalises to weighted versions where greedy fails.

## Variations you will meet

- **Weighted cameras (cost per node).** The "move it up" exchange breaks, since a higher camera might cost more. Use the three-value DP per node and take minima. This is minimum-weight dominating set on a tree.
- **Distance-`k` coverage.** States become "distance to nearest camera below" and "distance to deepest unwatched node below". The greedy still places a camera only when an unwatched node is exactly `k` below, at the highest spot that still reaches it.
- **Vertex cover on a tree (cover every edge, not every node).** The same lazy greedy works with two states: a leaf's edge is covered by putting the vertex at the parent.
- **Return the placement, not the count.** Record the node in rule 1 and at the root check. The states do not change.

## What to carry forward

Post-order lets every subtree hand its parent a summary. When "covered" is not enough, make the summary a small set of states (needs help, fine, helping you) and be lazy: place a camera only when a child forces you, and only as high as possible. This closes the Trees chapter. You started by returning a height from each child, and you end by returning a three-state verdict that a greedy rule acts on, the same bottom-up instinct at full strength.
