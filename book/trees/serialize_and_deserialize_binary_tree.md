# Serialize and Deserialize Binary Tree

*LeetCode 297 · Hard · Pattern: Preorder with null sentinels · Reading time ~10 min*

## The problem

Design a Codec with serialize(root) -> str and deserialize(str) -> root such that deserialize(serialize(t)) reproduces
t exactly; any format is allowed.

```text
Example: [1,2,3,null,null,4,5] -> "1,2,#,#,3,4,#,#,5,#,#" and
  back.
```

## What the problem is really asking

Design two functions. `serialize(root)` turns a binary tree into a string, and `deserialize(s)` turns that string back into a tree identical to the original, with the same shape and the same values in the same places. You choose the format.

The answer is a pair of inverse functions. The freedom is the hard part. You must pick a format that captures the shape, not just the values, and that can be read back without guesswork. Values may repeat and may be negative. That rules out tricks that identify nodes by value, such as the preorder-plus-inorder method from two problems ago.

```text
tree:         1
             / \
            2   3
               / \
              4   5

one valid encoding:  "1,2,#,#,3,4,#,#,5,#,#"
deserialize(that) -> the same tree
```

## Do it by hand first

Try writing just the preorder: `1 2 3 4 5`. Now try to draw the tree back from that. You cannot. `2` could be the left child of `1`, or the right child, with `3` below it. Even two nodes are ambiguous:

```text
  1          1
 /            \          both have preorder "1 2"
2              2
```

What was missing is where the branches stop. So when you write the preorder, also write a mark every time you reach an empty child slot. Walking the example by hand: write `1`, go left, write `2`. `2` has no left child, so write `#`. It has no right child, so write `#`. Back at `1`, go right, write `3`, go left, write `4`, then `#`, `#`. Go right from `3`, write `5`, then `#`, `#`.

```text
walk:   1 -> 2 -> (empty) (empty) -> 3 -> 4 -> (empty) (empty)
        -> 5 -> (empty) (empty)
tape:   1  2  #  #  3  4  #  #  5  #  #
```

Now read the tape back by hand. `1` is a node, so the next thing is its left subtree. `2` is a node, so the next thing is its left subtree. `#` means empty. The next thing is `2`'s right subtree: `#`, empty. `2` is done, so the next thing is `1`'s right subtree, `3`, and so on. Your hand kept track of which slot you were filling, and that was always "the next unfilled slot in preorder order". Recursion keeps that bookkeeping for you.

## The first honest attempt

The format most people reach for first is the one LeetCode itself prints: level order, with `null` for every missing child.

```text
serialize (BFS):  1,2,3,null,null,4,5,null,null,null,null

deserialize needs:
  tokens: 1  2  3  n  n  4  5  n  n  n  n
          ^  i -> pairs of tokens per parent
  queue of parents waiting for children:
     [1] -> 1 takes (2,3)        queue [2,3]
     [2,3] -> 2 takes (n,n)      queue [3]
     [3]   -> 3 takes (4,5)      queue [4,5]
     [4,5] -> 4 takes (n,n), 5 takes (n,n)
```

It works and it is `O(n)`. The cost is not asymptotic. It is bookkeeping. The decoder must keep a queue of parents still waiting for children, a running token index, and a left/right toggle. The structure is rebuilt by remembering who is waiting, rather than being implied by the order of the tokens. Every bug in hand-written versions lives in that bookkeeping: off-by-one indexes, forgetting to enqueue, handling trailing nulls. We want a format where the decoder is as simple as the encoder.

## The turning point

**Claim: preorder with a sentinel for every empty child is a complete, self-delimiting description of the tree, and the decoder is the same recursion as the encoder, run in reverse.**

Why it is complete: every node writes its value, then its full left subtree, then its full right subtree. Every empty slot writes `#`. So the tape is a direct transcript of the recursive walk. Reading it with the same recursion reproduces the same calls in the same order:

- `read()`: take the next token. If it is `#`, return empty. Otherwise make a node, set its left to `read()`, then its right to `read()`.

Why it is self-delimiting: a subtree's tokens end exactly when its recursion returns, and nothing else is needed to know where. The sentinels stop each branch. There are no sizes, no depths, no index arithmetic, and no queue. A tree of `n` nodes has exactly `n + 1` empty slots, so the tape is `2n + 1` tokens.

```text
encode:  walk(node): None -> "#"
                     else -> val, walk(left), walk(right)

decode:  read():     "#"  -> None
                     else -> node(val), read(), read()
                     ^ mirror image, line for line
```

The one piece of shared state is a cursor (an iterator over the tokens) that only moves forward. The previous problem used a stack because the format told us depths. Here the call stack plays that role automatically, since each pending `read()` call is a slot waiting to be filled.

Some details matter in practice. Use a real delimiter such as `,`, because values can be negative and `-` already appears in them. Do not use preorder + inorder, because duplicate values break the value-to-index map. On a skewed tree of 10^4 nodes the recursion is 10^4 deep, so raise Python's recursion limit or switch to an explicit stack.

## Watch it work

The example tree, with `n = 5` nodes and `2n + 1 = 11` tokens.

Frame 1. Serialize: the preorder walk emits a value per node and `#` per empty slot.

```text
idx:   0  1  2  3  4  5  6  7  8  9  10
tape:  1  2  #  #  3  4  #  #  5  #  #
```

Frame 2. Deserialize starts. `read()` takes `tok[0] = 1` and makes the root. Its left slot calls `read()`.

```text
tape:  1  2  #  #  3  4  #  #  5  #  #
       ^                                   tree:  1
pending slots (call stack): 1.left                ?
```

Frame 3. `tok[1] = 2` becomes `1.left`. Then `tok[2] = #` fills `2.left` and `tok[3] = #` fills `2.right`. `2` is complete, so its call returns. Now `1.right` is pending.

```text
tape:  1  2  #  #  3  4  #  #  5  #  #
          ^  ^  ^                          tree:  1
pending: 1.right                                 / \
                                                2   ?
```

Frame 4. `tok[4] = 3` becomes `1.right`. Its left slot reads `tok[5] = 4`, and then `tok[6], tok[7] = #, #` close `4`.

```text
tape:  1  2  #  #  3  4  #  #  5  #  #
                   ^  ^  ^  ^              tree:  1
pending: 3.right                                 / \
                                                2   3
                                                   /
                                                  4
```

Frame 5. `tok[8] = 5` becomes `3.right`, and `tok[9], tok[10] = #, #` close it. Every pending slot is filled, and the cursor is exactly at the end.

```text
tape:  1  2  #  #  3  4  #  #  5  #  #
                               ^  ^  ^     tree:  1
pending: (none)                                  / \
                                                2   3
                                                   / \
                                                  4   5
```

At every frame, the cursor sat on the first token of the subtree belonging to the deepest pending slot. Each `read()` call consumed exactly its own subtree's tokens. The cursor never moved backwards, and no token was read twice.

## Why it is correct

The invariant is that `read()`, called with the cursor at the start of the encoding of some subtree `T`, returns a copy of `T` and leaves the cursor just past `T`'s encoding.

Prove it by induction on the size of `T`. If `T` is empty, its encoding is the single token `#`. `read()` consumes it and returns empty, so the claim holds. If `T` has root value `v` and subtrees `A` and `B`, its encoding is `v` followed by the encoding of `A` followed by the encoding of `B`. That is exactly what `walk` produces. `read()` consumes `v`, then calls `read()` with the cursor at the start of `A`'s encoding. By induction this returns `A` and stops just past it, which is the start of `B`. The second call returns `B` and stops just past it. The node assembled is `T`, and the cursor is just past `T`.

Applying this to the whole tape gives `deserialize(serialize(t)) == t`. Nothing in the argument compares values, so duplicates and negatives are harmless.

## Cost

- **Time `O(n)`** each way. One token is produced and consumed per node and per empty slot, and there are `2n + 1` tokens in total.
- **Space `O(n)`** for the string. Recursion depth is `O(h)`, which is `O(n)` on a chain.
- The level-order format is also `O(n)` time and space, so the gain is in simplicity and robustness, not asymptotics.

## Variations you will meet

- **Serialize and Deserialize BST (LeetCode 449).** No sentinels are needed. Write plain preorder. On decode, consume values while they fit the `(low, high)` bound inherited from the ancestors. The BST order replaces the `#` markers, making the string more compact.
- **Find Duplicate Subtrees (LeetCode 652).** Serialize every subtree with this same format and count identical strings in a hash map. This links back to Subtree of Another Tree: a canonical string turns "same shape and values" into string equality.
- **Iterative decoder.** Keep an explicit stack of nodes whose right slot is still open. This is needed when the tree is too deep for recursion.
- **N-ary trees (the next problem).** There are no fixed two slots, so a `#` per slot no longer works directly. You need to say how many children follow.

## What to carry forward

Preorder plus a sentinel for every empty slot makes the stream self-delimiting, and the decoder is the encoder read backwards, sharing only a forward cursor. The next problem asks for the same round trip on N-ary trees, where a node has no fixed number of slots. The fix is to write each node's child count next to its value.
