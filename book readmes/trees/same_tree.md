# Same Tree

*LeetCode 100 · Easy · Pattern: Simultaneous tree recursion · Reading time ~5 min*

## The problem

Given two binary trees p and q, return True if they are structurally identical and every corresponding node has the
same value.

```text
Example: p=[1,2,3], q=[1,2,3] -> True; p=[1,2], q=[1,null,2] ->
  False.
```

## What the problem is really asking

Given two trees p and q, say whether they are the same tree: the same shape, and the same value at every position. The
answer is a yes or no. The subtle part is "same shape": two trees with the same values in the same visiting order can
still be different trees.

```text
   p = [1,2]        q = [1,null,2]
       1                1
      /                  \
     2                    2
   2 is a LEFT child    2 is a RIGHT child  -> not the same
```

Both have the values 1 and 2, both produce `2 1` or `1 2` in some traversal, yet the answer is False. Shape is part of
the identity.

## Do it by hand first

Lay one tree over the other. Put one finger on p's root and one on q's root. Compare the values. Then move both fingers
left together and compare; come back and move both right together and compare. The moment one finger lands on a node and
the other on empty space, or the values differ, stop.

```text
p:    1         q:    1        fingers at (1,1)   equal
     / \             / \       fingers at (2,2)   equal
    2   3           2   4      fingers at (3,4)   3 != 4  stop
                                answer: False
```

Your hands kept track of **a pair of positions**, one in each tree, always pointing at the same place. That pair is the
argument of the recursive function.

## The first honest attempt

Serialize both trees completely, writing a marker for every missing child so shape is kept, then compare the two lists.

```text
p -> [1, 2, #, #, 3, #, #]
q -> [1, 2, #, #, 4, #, #]
      ^ ^ ^  ^  ^
      the comparison only needed to reach here,
      but both lists were fully built first
```

That is O(n + m) time and O(n + m) extra memory. The waste: if the roots differ, both whole trees are still flattened
before anything is compared, and two full copies sit in memory just to be read once, in order, side by side.

## The turning point

**Claim: two trees are the same exactly when their roots match, their left subtrees are the same, and their right
subtrees are the same.**

That is not an observation so much as a definition, and the definition is the algorithm. Position i in the two
serializations always refers to the same place in both trees, so instead of flattening and then comparing, compare the
two nodes at the same place as soon as you reach them.

The function now takes **two** nodes. Its base cases are about emptiness:

- both `None`: the same (two empty trees match);
- exactly one `None`: different (one has a node where the other has nothing);
- both real: compare values, then trust the call on the two left children and on the two right children.

A neat way to state the first two in one line: when either node is `None`, the answer is `p is q`. Two `None`s are the
same object; a node is never `None`.

The `and` chain short-circuits: values are checked first, then the left pair, and the right pair is only examined if
everything before it matched.

## Watch it work

p = `[1,2,3]`, q = `[1,2,4]`. Each frame draws the two trees side by side; `*` marks the pair being compared, brackets
show returned results.

```text
Frame 1: same(1, 1): values equal, go to the left pair
   p:  *1        q:  *1        stack: same(1,1)
       / \           / \
      2   3         2   4
```

Values match, so the left pair is the next thing the `and` evaluates.

```text
Frame 2: same(2, 2): values equal, both children None
   p:   1        q:   1        stack: same(1,1), same(2,2)
       / \           / \
     *2   3        *2   4      same(None,None) = True, twice
```

2's left and right pairs are both (None, None), which match.

```text
Frame 3: same(2, 2) returns True
   p:   1        q:   1        stack: same(1,1)
       / \           / \
   [T]2   3     [T]2   4
```

The left half of the root's `and` is satisfied; the right pair is next.

```text
Frame 4: same(3, 4): 3 != 4, return False at once
   p:   1        q:   1        stack: same(1,1)
       / \           / \
   [T]2  *3     [T]2  *4       children of 3 and 4 never visited
```

The value test fails, so no deeper call is made.

```text
Frame 5: same(1, 1) = True and True and False = False
   p: [F]1       q: [F]1       answer False
```

At every frame the two fingers sit on the same position in both trees, and the stack is the shared path from the roots
to that position.

## Why it is correct

Induction on the pair of trees. Two empty trees are the same; an empty and a non-empty tree are not. For two nodes,
assume the child calls answer correctly for their pairs of subtrees. The trees are the same if and only if the root
values agree and both pairs of subtrees are the same, which is exactly the returned expression. Short-circuiting only
skips work after the answer is already known to be False.

## Cost

Time O(min(n, m)): the walk never goes past the smaller tree, and stops at the first mismatch. Space O(h) for the stack,
where h is the height of the shallower shared part.

## Variations you will meet

- **Symmetric tree.** One tree compared with itself, but the two fingers move in mirror image. That is the next problem.
- **Subtree of another tree.** Run this comparison starting from every node of a big tree.
- **Flip equivalent trees (LeetCode 951).** At each pair, allow either the straight match (left-left, right-right) or the
  crossed match (left-right, right-left).
- **Iterative.** A stack or queue of node pairs; push `(p.left, q.left)` and `(p.right, q.right)`.

## What to carry forward

Two trees, two fingers, one recursion: the function's argument is a pair of positions, and the `None` cases decide
shape. The next problem keeps the two fingers but makes them move in opposite directions inside the same tree.
