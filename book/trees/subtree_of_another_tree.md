# Subtree of Another Tree

*LeetCode 572 · Easy · Pattern: Tree serialization + substring search · Reading time ~6 min*

## What the problem is really asking

Given a big tree `root` and a small tree `subRoot`, is there a node in the big tree whose entire subtree is identical to
the small tree? "Entire" is the key word: the match must run all the way to the leaves. You cannot stop early and leave
extra nodes hanging below.

```text
 root:       3          subRoot:   4       True: the subtree
            / \                   / \      at 4 is exactly
           4   5                 1   2     4 / 1, 2
          / \
         1   2

 root:       3          subRoot:   4       False: under the big
            / \                   / \      4, node 2 has a child
           4   5                 1   2     0 that subRoot lacks
          / \
         1   2
            /
           0
```

## Do it by hand first

You would scan the big tree for a node with value 4 (the small root), then overlay the small tree there and check node
by node, exactly as in Same Tree. In the second picture the overlay matches 4, 1, 2 and then finds 0 under 2 where the
small tree has nothing.

```text
candidate start   overlay with subRoot
3                 3 != 4  fail at once
4                 4=4, 1=1, 2=2, 0 vs None  fail
5                 5 != 4  fail at once
1, 2, 0           values != 4  fail at once
```

Your hand kept track of **a candidate start node, then a pair of fingers** for the overlay. That is Same Tree, launched
from every node.

## The first honest attempt

For each node of `root`, call `same(node, subRoot)`. Return True if any call does.

```text
big tree, every node as a start; each overlay re-walks
a region below it:

  start 4:    4 . 1 . 2 . 0       (walks 4 nodes)
  start 2:        2 . 0           (walks 2 again)
  start 0:            0           (walks 0 again)
```

With n nodes in the big tree and m in the small one, that is O(n · m) time and O(h) space. The repeated work: deep
nodes are re-compared once for every candidate ancestor whose overlay reaches them before failing. This is the same
waste as naive substring search, where the pattern is re-aligned at every position and re-reads the same characters.

## The turning point

**Claim: write a tree in pre-order with an explicit marker for every missing child, and every subtree becomes a
contiguous substring of its tree's string. Two subtrees are identical exactly when their strings are equal.**

Why contiguous: pre-order emits a node, then its entire left subtree, then its entire right subtree, and only then
returns to anything outside. So a subtree's tokens come out in one unbroken run.

Why equal strings mean equal trees: with null markers, the string decodes back to exactly one tree. Without them,
`[1,2]` and `[1,null,2]` both write `1,2`. With them they become `1,2,#,#,#` and `1,#,2,#,#`.

One more detail: a delimiter before every token. Without it, the small tree `2` (written `2##`) would be found inside
`12##`. Writing `,2,#,#` and `,12,#,#` makes that impossible, because a match must start at a comma.

So the problem becomes: serialize both trees once, and ask whether the small string occurs in the big string. Python's
`in` on strings runs a linear-time search in practice (KMP gives the same bound with a guarantee), so the whole thing is
O(n + m).

## Watch it work

`root = [3,4,5,1,2]`, `subRoot = [4,1,2]`. Serialization is a post-order assembly: each call returns its own string, and a
parent glues `,val` in front of its children's strings. `*` marks the running call.

```text
Frame 1: ser(1) and ser(2) return as leaves
            3          stack: ser(3), ser(4)
           / \
          4   5        1 -> ",1,#,#"
         / \           2 -> ",2,#,#"
       *1  *2
```

A leaf writes its value and two null markers.

```text
Frame 2: ser(4) glues ",4" + left + right
            3          stack: ser(3)
           / \
         *4   5        4 -> ",4,1,#,#,2,#,#"
         / \
       [.] [.]
```

The run for 4's subtree is contiguous: 4, then all of 1's subtree, then all of 2's.

```text
Frame 3: ser(5), then ser(3) finishes
           *3          5 -> ",5,#,#"
           / \
         [.] [.]       3 -> ",3,4,1,#,#,2,#,#,5,#,#"
```

The whole big tree is now one string.

```text
Frame 4: subRoot serializes the same way
          4            small = ",4,1,#,#,2,#,#"
         / \
        1   2
```

The small tree's string is its pre-order with markers.

```text
Frame 5: search small in big
 big:   ,3,4,1,#,#,2,#,#,5,#,#
          ^^^^^^^^^^^^^^
          match at index 2 -> True
```

Now the second root, with 0 under 2:

```text
Frame 6: big = ",3,4,1,#,#,2,0,#,#,#,5,#,#"
 small:   ,4,1,#,#,2,#,#
 big:   ,3,4,1,#,#,2,0,#,#,#,5,#,#
                     ^ "0" where small has "#"
         no occurrence anywhere -> False
```

Across frames, each call's returned string is exactly its subtree written in pre-order, so a subtree match is a
substring match.

## Why it is correct

Pre-order with null markers is a one-to-one encoding: the string can be decoded into exactly one tree, so equal strings
mean equal trees. Every subtree of `root` appears as a contiguous run in the big string, starting at its own comma. The
delimiters ensure a match of the small string can only start at a token boundary and end at one, so it aligns with
whole tokens; and a run of tokens that decodes as one complete tree, starting at a node, is that node's subtree.
Therefore "small occurs in big" holds iff some subtree equals `subRoot`.

## Cost

Brute force: O(n · m) time, O(h) space. Serialization: O(n + m) to build the strings (if built by appending to a list
and joining once; repeated string concatenation in the recursion can cost more on deep trees) plus a linear search;
O(n + m) space for the strings.

## Variations you will meet

- **Merkle hashing.** Return a hash of (value, left hash, right hash) for each node and compare hashes to the small
  tree's; O(n + m) with a cheap equality check on collision.
- **Find duplicate subtrees (LeetCode 652).** Serialize every subtree, count strings in a dictionary.
- **Guaranteed linear search.** Use KMP or Z-function on the token lists instead of relying on `in`.

## What to carry forward

A tree written in pre-order with null markers is a string that keeps its shape, and subtrees become substrings. The next
problem goes back to returning numbers up: a height, plus a check folded into it.
