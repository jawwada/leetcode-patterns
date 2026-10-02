# Serialize and Deserialize N-ary Tree

*LeetCode 428 · Hard · Pattern: Preorder with child counts, consumed by a single cursor · Reading time ~9 min*

## What the problem is really asking

Same contract as the binary version: `serialize(root)` produces a string, and `deserialize(s)` rebuilds an identical tree. The difference is that each node now has a list of children of any length, which may be zero, one, or fifty. The empty tree must round-trip too.

The answer is again a pair of inverse functions. What makes it harder than the binary case is that the trick we just learned, a `#` for each of the two child slots, depends on every node having exactly two slots. An N-ary node has no fixed number of slots, so the reader cannot know when a node's children end unless the format tells it.

```text
tree:            1
             /   |   \
            3    2    4
           / \
          5   6

children lists:  1 -> [3, 2, 4]
                 3 -> [5, 6]
                 5, 6, 2, 4 -> []
```

## Do it by hand first

Write the preorder: `1 3 5 6 2 4`. Try to rebuild it. After `1` comes `3`, a child of `1`. Is `5` a child of `3`, or a second child of `1`? You cannot tell. Two different trees can share the same preorder:

```text
   1                  1
  / \                / \
 2   3              2   4         both: preorder 1 2 3 4
     |              |
     4              3
```

When you drew the example by hand, you kept asking one question at each node: how many children does this one have? Once you know `1` has 3 children and `3` has 2, the rest falls out. Read `1`, which promises 3 children. Read `3`, the first of them, which promises 2. Read `5`, which promises 0. Read `6`, which promises 0. That completes `3`'s 2 children, so `3` is done. `2` is `1`'s second child, `4` is its third, and `1` is done.

```text
value:   1  3  5  6  2  4
count:   3  2  0  0  0  0
```

What your hand tracked was a stack of open promises, "node X still owes me k more children". That stack is the recursion, and the count is the one number per node that the format must carry.

## The first honest attempt

The format everyone draws on a whiteboard is nested parentheses. A node is written as its value followed by its children inside brackets. The reference brute force produces this:

```text
"1(3(5(),6()),2(),4())"
```

To deserialize, read the value up to `(`. Then scan the inside of the brackets, tracking bracket depth, and split at every comma that sits at depth 0. Recurse on each piece.

The problem is the scan. On a deep chain, each level rescans the whole remainder to find its depth-0 commas and its matching bracket. Then the child call scans almost all of it again.

```text
"1(2(3(4())))"

level 1 scans:  2(3(4()))      9 chars
level 2 scans:    3(4())       6 chars
level 3 scans:      4()        3 chars
                ~ quadratic in total
```

That is `O(n^2)` time on a chain. The same characters are re-read once per ancestor, only to learn where a subtree ends.

## The turning point

**Claim: if each node is written as its value followed by its number of children, then plain preorder is self-delimiting, and a single forward cursor can rebuild the tree without any lookahead.**

The binary codec told the reader where a branch stops with a `#` per empty slot. The N-ary codec tells the reader in advance how many subtrees follow. The reader works like this:

- `build()`: read the value, then read the count `c`, make the node, then call `build()` exactly `c` times and collect the results as its children.

Each call knows exactly how many subtrees to consume, and each child call consumes exactly its own subtree's tokens, so the cursor lands on the next sibling when a child returns. Nobody ever searches for a matching bracket. Every token is read once. The encoder mirrors it: write value, write `len(children)`, then recurse on each child.

```text
tape:  1 3 | 3 2 | 5 0 | 6 0 | 2 0 | 4 0
       v c   v c   v c   v c   v c   v c
       ^ one cursor, moves right, never back
```

Some details matter in practice. The empty tree serializes to `""`, and the decoder checks for it before reading. Space-separated tokens handle negatives and multi-digit values. A `#`-after-last-child marker is an equivalent alternative: write the children, then `#`, and let `build` loop until it sees `#`. Either fact is enough, but the count is one token per node, while the marker is one token per node plus one per child list. On a 10^4-deep chain the recursion depth matters, so switch to an explicit stack of `(node, remaining_count)` if needed.

## Watch it work

Tape `"1 3 3 2 5 0 6 0 2 0 4 0"`, read as pairs (value, count). The promise stack shows each open node as `value:remaining`, with the bottom first.

Frame 1. Read `(1, 3)`. The root `1` owes 3 children.

```text
tape:  1 3  3 2  5 0  6 0  2 0  4 0
       ^^^                              tree:  1
promises: [1:3]
```

Frame 2. Read `(3, 2)`. That is `1`'s first child, and it owes 2 of its own.

```text
tape:  1 3  3 2  5 0  6 0  2 0  4 0
            ^^^                         tree:  1
promises: [1:2, 3:2]                           |
                                               3
```

Frame 3. Read `(5, 0)`, a leaf, which returns at once. `3` now owes 1.

```text
tape:  1 3  3 2  5 0  6 0  2 0  4 0
                 ^^^                    tree:  1
promises: [1:2, 3:1]                           |
                                               3
                                              /
                                             5
```

Frame 4. Read `(6, 0)`, a leaf. `3` now owes 0, so it returns, and the cursor is already at `1`'s next child.

```text
tape:  1 3  3 2  5 0  6 0  2 0  4 0
                      ^^^               tree:  1
promises: [1:2]                                |
                                               3
                                              / \
                                             5   6
```

Frame 5. Read `(2, 0)`, a leaf, which is `1`'s second child. `1` owes 1.

```text
tape:  1 3  3 2  5 0  6 0  2 0  4 0
                           ^^^          tree:    1
promises: [1:1]                                /  \
                                              3    2
                                             / \
                                            5   6
```

Frame 6. Read `(4, 0)`, a leaf, which is `1`'s third child. `1` owes 0 and returns. The cursor is exactly at the end of the tape.

```text
tape:  1 3  3 2  5 0  6 0  2 0  4 0
                                ^^^     tree:    1
promises: []                                  /  |  \
                                             3   2   4
                                            / \
                                           5   6
```

At every frame the cursor sat at the start of the next subtree that the top promise was waiting for. When a promise reached zero, the cursor was already in place for the node below it. The cursor never moved backwards.

## Why it is correct

The invariant is that `build()`, called with the cursor at the start of some subtree `T`'s encoding, returns a copy of `T` and leaves the cursor just past that encoding.

By induction on the size of `T`: `T`'s encoding is `v c` followed by the encodings of its `c` children, in order. `build()` reads `v` and `c`. The first child call starts at the first child's encoding and, by induction, stops just past it, which is where the second child's encoding begins, and so on. After `c` calls the cursor is just past the last child, which is just past `T`. The children list is in the original order, so the rebuilt node equals `T`. The base case is a leaf, `v 0`, which reads two tokens and makes no calls. The empty tree is handled separately by the empty string.

The encoder produces exactly this shape, because `dfs` writes `v`, then `len(children)`, then recurses into each child in list order. So the decoder's assumption about the tape is always met. The counts remove the ambiguity: the two trees in the hand example encode as `1 2 2 0 3 1 4 0` and `1 2 2 1 3 0 4 0`, which differ.

## Cost

- **Time `O(n)`** each way. Every node writes and reads exactly two tokens.
- **Space `O(n)`** for the string. Recursion depth is the tree height, `O(n)` on a chain.
- The parentheses format with depth-0 splitting is `O(n^2)` on a chain, because each level rescans what its descendants will scan again.

## Variations you will meet

- **Sentinel instead of count.** Write `#` after each node's last child. Decoding is "build children until you see `#`". It is equally correct and slightly longer. This is the direct generalisation of the binary `#` format.
- **Encode N-ary as binary (LeetCode 431).** Use left-child/right-sibling. The first child becomes the left pointer and the next sibling the right pointer. Then the previous problem's binary codec handles any N-ary tree unchanged.
- **Encode and Decode Strings.** The same idea one level down: put each string's length in front of it so the reader never has to search for a delimiter. Length prefixes and child counts are the same trick.
- **Level-order with group separators.** LeetCode's own display writes children groups level by level, separated by `null`. It works, but needs a parent queue, just like the binary BFS brute force.

## What to carry forward

When a node has no fixed number of slots, write how many children follow. Preorder with counts becomes a self-delimiting tape that one cursor reads left to right. The next and final problem leaves sequences behind and returns to the post-order "children report up to the parent" style. This time the report is one of three states, and a greedy rule decides when a parent must act.
