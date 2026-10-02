# Recover Binary Search Tree

*LeetCode 99 · Hard · Pattern: Inorder traversal with previous-node pointer · Reading time ~11 min*

## What the problem is really asking

Someone took a valid binary search tree and swapped the values of exactly two nodes. The shape is untouched, and only two labels changed places. Find those two nodes and swap their values back, in place.

The answer is not a returned value. It is a repaired tree, and the repair is always a single value swap. The difficulty is locating the two culprits. Looking at nodes one at a time does not help much, because a misplaced value can look perfectly fine relative to its parent and children and still break the BST rule against some distant ancestor. Validate Binary Search Tree taught that the BST rule is global. Here we need more than a yes/no answer about it: we need to point at exactly the two nodes that broke it.

```text
broken tree:          4
                    /   \
                   6     2       6 and 2 were swapped
                  / \   / \
                 1   3 5   7

repaired tree:        4
                    /   \
                   2     6
                  / \   / \
                 1   3 5   7
```

Here both culprits happen to break a parent-child rule, but that is luck. Take `[3,1,4,null,null,2]`, where `2` and `3` were swapped. The root `3` is bigger than its left child `1` and smaller than its right child `4`. The node `2` is a perfectly good left child of `4`. Every parent-child pair looks fine, yet `2` sits in the right subtree of `3`. The bug shows only against the whole order.

## Do it by hand first

Flatten the tree. Kth Smallest and Validate BST both rested on one fact: the inorder walk of a BST reads its values in increasing order. So read the broken tree inorder and look at the line.

```text
inorder of broken tree:

   1   6   3   4   5   2   7
       ^                   ^
    too high            too low

as a staircase (height = value):
                                #
       #                        #
       #              #         #
       #         #    #         #
       #    #    #    #         #
       #    #    #    #    #    #
  #    #    #    #    #    #    #
  1    6    3    4    5    2    7
       ^bump                ^pit
```

A correct BST would be a rising staircase: 1 2 3 4 5 6 7. Here the staircase has a bump (`6` far too early) and a pit (`2` far too late). Walk along it and mark every place where the next step goes down:

- `6 -> 3` goes down. That is the first dip.
- `5 -> 2` goes down. That is the second dip.

The culprits are the high side of the first dip (`6`) and the low side of the second dip (`2`). Swap them and the staircase rises cleanly.

What did your hand keep track of? Only the previous step's height. You never needed to see the whole line at once, just "is this step lower than the last one?" That one remembered value is the seed of the algorithm: an inorder walk carrying a `prev` pointer.

## The first honest attempt

Do the inorder walk into a list of nodes. Sort a copy of their values. Walk the list and the sorted copy together and write the sorted values back into the nodes. Only the two swapped positions actually change.

```text
inorder nodes:  1  6  3  4  5  2  7
sorted values:  1  2  3  4  5  6  7
                   ^           ^
                   only these two differ
```

That is `O(n log n)` time and `O(n)` extra space. The waste is clear from the picture. The sequence is almost sorted. It differs from sorted in exactly two positions. A full sort spends `n log n` rebuilding an order we already have, just to find two misplaced items. And storing every node is unnecessary when the defect shows up as a local comparison between neighbours in the walk.

## The turning point

**Claim: swapping two values in an increasing sequence creates either one dip or two dips, and in both cases the culprits are the larger value of the first dip and the smaller value of the last dip.**

Here a "dip" means an adjacent pair `prev > cur` in the inorder sequence.

Why one or two? Suppose positions `i < j` hold swapped values `big` (now at `i`) and `small` (now at `j`).

- **Far apart (`j > i + 1`).** At position `i` the value `big` is larger than its right neighbour, which was supposed to be bigger than the old value at `i` but smaller than `big`. That is dip one, and its left side is `big`. At position `j` the value `small` is smaller than its left neighbour. That is dip two, and its right side is `small`. Every other adjacent pair is untouched, so there are exactly two dips.
- **Adjacent (`j = i + 1`).** The two values sit next to each other and form a single dip `big > small`. The left side of this one dip is `big`, and the right side is `small`.

```text
far apart:   1  [6] 3  4  5  [2] 7      dips: 6>3, 5>2
                 ^ first.prev    ^ last.cur

adjacent:    1  [3][2] 4               dip:  3>2
                 ^  ^  same dip gives both
```

One rule covers both cases. On every dip, if `first` is not set yet, set `first = prev`. Then always set `second = cur`. In the far-apart case, `second` gets overwritten by the second dip, which is what we want. In the adjacent case there is no second dip, so `second` stays as the right side of the only dip. That is also correct.

Which structure turns this into an algorithm? An inorder traversal that remembers one node behind it. The iterative version from Binary Tree Inorder Traversal is a natural fit: a stack for the left spine, `prev` for the last visited node, and the dip test at each pop. No list of values is ever built. At the end, swap `first.val` and `second.val`. We swap values, not nodes, because the problem forbids changing the structure.

```text
inorder walk state:
  stack : the left spine still to visit
  prev  : last node visited (one step behind)
  first : set once, at the first dip (prev side)
  second: overwritten at every dip (cur side)
```

## Watch it work

Broken tree `[4,6,2,1,3,5,7]`, inorder `1 6 3 4 5 2 7`. The stack is written bottom to top.

Frame 1. Push the left spine `4, 6, 1`, then pop and visit `1`. There is no `prev`, so there is nothing to compare.

```text
line:   [1]  6   3   4   5   2   7
stack:  [4, 6]
prev: -    first: -    second: -
```

Frame 2. Pop and visit `6`. Since `prev = 1` is less than 6, the line is rising.

```text
line:    1  [6]  3   4   5   2   7
stack:  [4]       (then 6.right = 3 is pushed)
prev: 1    first: -    second: -
```

Frame 3. Pop and visit `3`. Since `prev = 6` is greater than 3, this is the first dip. `first` is unset, so `first = 6`, and `second = 3`.

```text
line:    1   6 \ [3]  4   5   2   7
              dip
stack:  [4]
prev: 6    first: 6    second: 3
```

If the tree had only this dip (the adjacent case), we would already have the answer.

Frame 4. Pop and visit `4`, the root. `3 < 4` is fine. Then go right to `2` and push its left spine `2, 5`.

```text
line:    1   6   3  [4]  5   2   7
stack:  [2, 5]
prev: 3    first: 6    second: 3
```

Frame 5. Pop and visit `5`. `4 < 5` is fine.

```text
line:    1   6   3   4  [5]  2   7
stack:  [2]
prev: 4    first: 6    second: 3
```

Frame 6. Pop and visit `2`. Since `prev = 5` is greater than 2, this is the second dip. `first` is already set and stays `6`. `second` is overwritten to `2`.

```text
line:    1   6   3   4   5 \ [2]  7
                          dip
stack:  []
prev: 5    first: 6    second: 2
```

Frame 7. Visit `7`. `2 < 7` is fine, and the walk ends. Swap the values of `first` and `second`.

```text
first (was 6) <- 2      second (was 2) <- 6

          4                 line: 1 2 3 4 5 6 7
        /   \                      rising: OK
       2     6
      / \   / \
     1   3 5   7
```

Across frames, `prev` was always the node visited just before the current one, and the stack never held more than one root-to-leaf path. `first` was written once and never changed. `second` tracked the right side of the most recent dip.

## Why it is correct

Inorder visits nodes in the order of their positions in the sorted sequence. So the pairs `(prev, cur)` the walk compares are exactly the adjacent pairs of that sequence, each compared once. A valid BST produces no dips. The case analysis in the turning point shows that one swap produces exactly one dip (adjacent swap) or exactly two dips (otherwise), with `big` on the left of the first and `small` on the right of the last. The update rule records `prev` of the first dip and `cur` of the last dip. So when the walk ends, `first` is the node holding `big` and `second` is the node holding `small`. Swapping their values restores every position to its sorted value. Since inorder positions are fixed by the shape, which never changed, the result is the original valid BST.

The rule cannot be fooled into picking a wrong node. Values are distinct, and there is exactly one swap, so no third dip can exist to mislead it.

## Cost

- **Time `O(n)`.** One inorder pass, with a constant-time dip test per node.
- **Space `O(h)`.** That is the explicit stack, at most one root-to-leaf path. There is no list of values.
- The brute force (list, sort, write back) is `O(n log n)` time and `O(n)` space.
- **`O(1)` space** is possible with Morris traversal. It temporarily threads each node's inorder predecessor's empty right pointer back to the node, walks without a stack, and removes the threads as it goes. It runs the same dip logic. Mention it as the follow-up, and only write it if asked.

## Variations you will meet

- **Validate Binary Search Tree.** This is the same walk with the same `prev` pointer, but it stops at the first dip and returns false. Recover is Validate that keeps going and remembers where it failed.
- **Find the two swapped elements in an array.** With no tree at all, it is the identical dip rule in one linear scan. The tree only changes how you produce the sequence.
- **More than two values out of place.** The two-dip structure is gone. Collect the inorder values and sort them (the brute force) or compute the minimum swaps via cycle decomposition. Know that the elegant rule depends on "exactly one swap".
- **Minimum Absolute Difference in BST (LeetCode 530).** The same inorder-with-`prev` walk, but at every step you record `cur - prev` instead of testing for a dip.

## What to carry forward

A BST is a sorted line in disguise. Walk it inorder with one node of memory and the defect shows up as a dip: take the high side of the first dip and the low side of the last. The next problem reverses the direction of travel. Instead of reading a sequence off a tree, we are handed two sequences, preorder and inorder, and must grow the tree back from them.
