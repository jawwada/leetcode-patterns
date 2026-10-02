# Path Sum II

*LeetCode 113 · Medium · Pattern: DFS backtracking with a shared path list · Reading time ~8 min*

## What the problem is really asking

Same rules as Path Sum: a path starts at the root, ends at a leaf, and its values must add up to `targetSum`. The difference is the answer. Instead of a yes or no, return every matching path, each written as the list of values from root to leaf. The answer is a list of lists, and it can be empty.

```text
 root = [1,2,3,3,1,null,2]     targetSum = 6

            1
          /   \
         2     3
        / \     \
       3   1     2

 paths:  1-2-3 = 6  keep      1-2-1 = 4  drop
         1-3-2 = 6  keep
 answer: [[1,2,3], [1,3,2]]
```

What is new and slightly hard is that the yes or no version could throw the path away and remember only a number. Now the path *is* the output, so you must hold it somewhere while you walk, and you must not pay to rebuild it at every node.

## Do it by hand first

On paper you would trace with your finger and keep a written list of the nodes under your finger, adding a value each time you step down and crossing off the last one each time you step back up:

```text
 step          written list     still needed
 down to 1     1                5
 down to 2     1 2              3
 down to 3     1 2 3            0   leaf: copy "1 2 3" out
 back up       1 2
 down to 1     1 2 1            2   leaf: no
 back up       1 2
 back up       1
 down to 3     1 3              2
 down to 2     1 3 2            0   leaf: copy "1 3 2" out
```

You kept two things: the number still needed, as in Path Sum, and one written list that grew and shrank like a stack. You never wrote a second list for the right branch; you erased back to the shared prefix `1` and kept writing. The only time you wrote a fresh list was when you copied a winner into the answer.

## The first honest attempt

The direct recursion gives each call its own list: the child receives `path + [node.val]`, a brand new list. At each leaf the list is stored; at the end, every stored list is summed and the matches kept.

```text
 call at node    list it allocates
 1               [1]
 2               [1,2]          <- copies [1]
 3               [1,2,3]        <- copies [1,2]
 1 (right of 2)  [1,2,1]        <- copies [1,2] again
 3               [1,3]          <- copies [1] again
 2               [1,3,2]        <- copies [1,3]
                 \___ shared prefixes copied over and over ___/
```

Every node copies the whole prefix above it, O(h) each, so O(n·h) work and memory even when nothing matches. Then every leaf re-sums a prefix its ancestors already added up. Two kinds of waste: re-summing and re-copying.

## The turning point

**Claim: at every moment of a depth-first walk, the root-to-current-node path is exactly the recursion stack, so one list that is pushed on entry and popped on exit is always the correct path, and only matches ever need a copy.**

Take the two wastes one at a time.

*Re-summing* is solved by the previous problem: carry `remaining` down, subtract the node's value on entry, and a leaf only checks `remaining == 0`.

*Re-copying* is solved by noticing that all paths share prefixes, and the depth-first order visits them in exactly the order a stack supports. When you leave node 2's subtree for good, everything below 2 is finished; the next path to be built starts with `[1]`, which is what remains after popping 2. So keep one list:

```text
 enter node:  path.append(node.val)
 leaf match:  ans.append(path[:])     # snapshot, not the list
 leave node:  path.pop()
```

The pop is the "undo" that makes this backtracking: before a call returns, it restores `path` to exactly what it was when the call began. Siblings then see their parent's prefix, untouched.

The copy `path[:]` is essential and is the most common bug. If you store `path` itself, every entry in `ans` is the same list object; it keeps changing as the walk continues and ends up empty after the final pop.

```text
 ans.append(path)    ans -> [ L, L ]  both point at one list L
                     after the walk L == []  ->  [[], []]
 ans.append(path[:]) ans -> [ [1,2,3], [1,3,2] ]  frozen copies
```

Copies now happen only at matching leaves, and each match has to appear in the output anyway, so the copying is paid for by the output, not by the search.

This is the same choose, explore, un-choose skeleton you meet in backtracking problems like Subsets. Here the tree's own edges are the choices, so there is no loop over candidates; the two recursive calls are the loop.

## Watch it work

Tree `[1,2,3,3,1,null,2]`, target 6. Each frame shows the current node `*`, the shared `path`, `remaining` after subtracting, and `ans`.

**Frame 1.** Enter 1, then 2.

```text
          *1                path = [1, 2]
          /                 rem  = 6-1-2 = 3
        *2*                 ans  = []
        / \
       3   1
```

Two appends, two subtractions.

**Frame 2.** Enter leaf 3: match.

```text
          *1                path = [1, 2, 3]
          /                 rem  = 0, leaf
         *2                 ans  = [[1,2,3]]
         /
       *3*
```

A copy of `path` goes into `ans`; then 3 is popped.

**Frame 3.** Path back to `[1,2]`, enter leaf 1: no match.

```text
          *1                path = [1, 2, 1]
          /                 rem  = 2, leaf
         *2                 ans  = [[1,2,3]]
           \
           *1*
```

Remainder 2 is not 0. Pop 1, then node 2 is done and pops 2.

**Frame 4.** Path back to `[1]`, enter 3 on the right.

```text
          *1                path = [1, 3]
            \               rem  = 6-1-3 = 2
            *3*             ans  = [[1,2,3]]
              \
               2
```

The prefix `[1]` was reused, not rebuilt.

**Frame 5.** Enter leaf 2: match.

```text
          *1                path = [1, 3, 2]
            \               rem  = 0, leaf
            *3              ans  = [[1,2,3],
              \                     [1,3,2]]
              *2*
```

Second snapshot stored.

**Frame 6.** Pops unwind: 2, 3, 1.

```text
           1                path = []
          / \               ans  = [[1,2,3],
         2   3                      [1,3,2]]
```

`path` is empty again, exactly as it started; the snapshots in `ans` are untouched.

Invariant across the frames: `path` always held the values from the root to the current node, in order, and `rem` was the target minus their sum.

## Why it is correct

Claim: when the call for `node` begins, `path` holds the root-to-parent values; while it runs, after the append, `path` holds root-to-`node`; when it returns, `path` is back to root-to-parent. Proof by induction on subtree size. A call appends one value, each child call leaves `path` unchanged on return (inductive hypothesis), and the final pop removes the one value it added. So at any leaf, `path` is precisely that leaf's root-to-leaf path and `remaining` is the target minus its sum. Each leaf is reached exactly once, so each matching path is recorded exactly once, and because it is recorded as a copy, later mutations cannot alter it.

## Cost

- Time O(n·h) in the worst case: n visits with O(1) work each, plus copying up to O(n) matching paths of length up to h. With few matches, it is O(n).
- Space O(h) beyond the output: one shared path and a recursion stack of depth h. The brute force needed O(n·h) even when nothing matched.

## Variations you will meet

- **Binary Tree Paths** (LeetCode 257). Return all root-to-leaf paths as strings. Same shared path, no target; snapshot every leaf.
- **Path Sum III** (LeetCode 437). Paths may start anywhere downward. Count, do not list; carry a map of prefix sums along the path and backtrack it the same way you pop `path`.
- **Immutable path alternative.** Passing `path + [val]` to children is simpler and needs no pop, at O(h) per node. Fine for interviews if you name the cost; the shared list is the version that scales.
- **Iterative version.** Use an explicit stack of `(node, remaining, path_length)` and truncate the shared list to `path_length` when you pop a node, which is the same undo written by hand.

## What to carry forward

One shared list, append on entry, pop on exit, copy only what you keep. Count Good Nodes next carries a different kind of state down: not a sum or a path but a running maximum, and it never needs undoing because each child gets its own copy of one integer.
