# Backtracking

*15 problems · Reading time ~24 min*

## Why this chapter exists

Some questions do not ask for a number. They ask for every configuration that satisfies a rule ("list all subsets", "print every valid board"), or for one configuration that satisfies a tangle of rules ("fill this sudoku"). There is no formula for those answers. You have to build candidates one decision at a time and throw away a partial candidate the moment it cannot work. That is backtracking: a depth-first walk over a tree of decisions, with a pencil you can erase.

The fifteen problems in this chapter fall into a handful of families:

- **Choose a subset** (Subsets, Subsets II, Combination Sum, Combination Sum II): each element is in or out, or you pick the next element from an index onward.
- **Choose an order** (Permutations): every slot picks any element not used yet.
- **Choose one option per position** (Letter Combinations): a fixed-depth product of small alphabets.
- **Build a string under a running constraint** (Generate Parentheses, Remove Invalid Parentheses, Expression Add Operators): a counter or a running value decides which characters may come next.
- **Walk a grid without revisiting** (Word Search, Unique Paths III): the path is a trail of cells, and "un-choose" means un-marking a cell.
- **Place pieces under conflicts** (N-Queens, Sudoku Solver): each placement removes options from the rest of the board.
- **Shrink a multiset** (24 Game): combine two numbers into one, recurse on the smaller collection.
- **Explore a room you cannot see** (Robot Room Cleaner): the "un-choose" is a physical move back.

All of them share one skeleton. Learn the skeleton well and the problems become a matter of naming the choice, the constraint, and the undo.

## What it is

Start with the smallest real question: list every subset of `[1, 2, 3]`.

A human does this by making three decisions in order. Is 1 in? Is 2 in? Is 3 in? Each decision splits the world in two. Draw every sequence of decisions and you get a tree:

```text
depth 0                    []
                   take 1 /    \ skip 1
depth 1                [1]        []
              take 2 /  \       /   \ skip 2
depth 2          [1,2]   [1]  [2]    []
                 /  \    / \   / \   / \
depth 3     [1,2,3][1,2][1,3][1][2,3][2][3][]
                          (8 leaves = 8 subsets)
```

That picture is the whole technique. A **node** is a partial answer. An **edge** is one decision. A **leaf** (or, in some templates, any node) is a complete answer. Backtracking is a depth-first walk of this tree that never builds the tree in memory. It keeps only the root-to-current-node path.

The state the walk maintains is small:

```text
 shared memory (one copy, mutated in place)
 +---------------------------------------------+
 | path   = [1, 2]      labels on the edges     |
 |                      from root to here       |
 | extra  = used flags / counts / remaining /   |
 |          marked cells / board               |
 | result = [[], [1], [1,2]]  copies of answers |
 +---------------------------------------------+

 call stack (one frame per tree level)
 +-------------------------+
 | dfs(start=0)  loop i=0  |  depth 0: chose 1
 +-------------------------+
 | dfs(start=1)  loop i=1  |  depth 1: chose 2
 +-------------------------+
 | dfs(start=2)  <- top    |  depth 2: at node [1,2]
 +-------------------------+
```

Each stack frame remembers one thing: which child of its node it is currently trying (the loop variable). The `path` list is the concatenation of those choices. The depth of the stack equals the length of the path, which equals the depth of the current node in the tree.

### Choose, explore, un-choose

Every backtracking function does the same three moves per child:

```text
   at node N, for each allowed choice c:
     1. choose      path.append(c)    mark c used
     2. explore     dfs(child)        go one level down
     3. un-choose   path.pop()        unmark c
```

Step 3 is the "back" in backtracking. After exploring the child's whole subtree, the shared state must look exactly as it did before step 1, so that the next sibling starts from a clean node. Draw it as a pencil line: choose extends the line by one segment, un-choose erases that segment.

```text
 choose 2        explore          un-choose 2     choose 3
 [] - 1 - 2      [] - 1 - 2 - ..  [] - 1          [] - 1 - 3
 path=[1,2]      (subtree of 2)   path=[1]        path=[1,3]
```

### The three templates

Almost every problem in this chapter is one of three shapes of tree. Knowing which one you are in tells you the loop.

**Template A: include/exclude.** One level per element; two children per node (take it, skip it). Answers are the leaves at depth n. Good when the decision is genuinely binary per item.

```text
 dfs(i):  if i == n: record; return
          take nums[i]  -> dfs(i+1) -> untake
          skip nums[i]  -> dfs(i+1)
```

**Template B: pick-from-index.** A node says "the next element I add has index at least `start`". Its children are `start, start+1, ..., n-1`. Indices only increase down any path, so each combination is generated in exactly one order. Every node is an answer (subsets) or only the nodes meeting a target are (combination sums).

```text
 pick-from-index on [1,2,3]: 8 nodes, every node a subset
                    []
           /         |        \
         [1]        [2]       [3]
        /   \        |
    [1,2]  [1,3]   [2,3]
      |
  [1,2,3]
```

Template B is Template A with the "skip" chains collapsed: "skip 1, skip 2, take 3" becomes a single edge from `[]` to `[3]`. Same answers, fewer nodes.

**Template C: pick-from-set.** A node's children are every element not used yet, in any order. Depth n, branching n, n-1, ..., 1. Leaves are orderings. It needs a `used` flag per element because indices no longer increase.

```text
 pick-from-set on [1,2,3]: 6 leaves = 6 permutations
                      []
          /           |           \
        [1]          [2]          [3]
       /   \        /   \        /   \
   [1,2] [1,3]  [2,1] [2,3]  [3,1] [3,2]
     |     |      |     |      |     |
  [123] [132]  [213] [231]  [312] [321]
```

Grid walks (Word Search), board placements (N-Queens), and multiset shrinking (24 Game) are Template C with a different idea of "element" and "used": a cell and a visited mark, a column and an attacked set, a pair of numbers and their removal from the list.

## Operations and what they cost

| Operation | Cost | Why |
|---|---|---|
| choose: `path.append(x)` | O(1) amortised | end of a dynamic array |
| un-choose: `path.pop()` | O(1) | removes the last slot only |
| mark / unmark a used flag | O(1) | one array write |
| test "is x in path" by scanning | O(n) | linear search; use a flag instead |
| record an answer: `path[:]` | O(n) | must copy, the list keeps changing |
| join a string answer | O(n) | builds a new string |
| prune test at a node | O(1) usually | compare a counter or a bound |
| sort once for dedupe/pruning | O(n log n) | paid once, before the walk |
| recursive call | O(1) + one frame | stack depth = tree depth |
| whole walk | nodes x work per node | every visited node pays once |

### Recording an answer: copy, never alias

```text
 WRONG: result.append(path)

 result ---> [ * , * , * ]          path ---> [ ]
               \   |   /                       ^
                `--+--'---------- all point ---'
 after the walk path is [], so every answer prints as []

 RIGHT: result.append(path[:])

 result ---> [ *  ,  *  ,  * ]
               |     |     |
              [ ]   [1]  [1,2]      separate lists, frozen
```

### Pruning: cutting a subtree

A **prune** is a test made before descending into a child. If the test proves no answer lives below, you skip the child and everything under it. The saving is the entire subtree, not one node.

```text
 Combination Sum, candidates [2,3,6,7], target 7
 node = remaining budget; edge label = candidate taken

 7
 +-2-> 5
 |     +-2-> 3
 |     |     +-2-> 1
 |     |     |     +-2 x  (2 > 1)
 |     |     +-3-> 0      answer [2,2,3]
 |     |     +-6 x  (6 > 3)
 |     +-3-> 2
 |     |     +-3 x  (3 > 2)
 |     +-6 x  (6 > 5)
 +-3-> 4
 |     +-3-> 1
 |     |     +-3 x  (3 > 1)
 |     +-6 x  (6 > 4)
 +-6-> 1
 |     +-6 x  (6 > 1)
 +-7-> 0      answer [7]

 x = child bigger than the budget: cut before entering,
     and (sorted) every sibling to its right goes too
```

Because the candidates are sorted, once one child is too big every child to its right is too big as well, so the loop can `break` instead of `continue`. One comparison removes a whole fan of subtrees.

### Dedupe by sort + skip

When the input has repeated values, the tree has identical subtrees hanging off sibling edges with equal labels. Sort the input so equal values sit side by side; then, among the children of one node, skip any child whose value equals the previous sibling's.

```text
 [1,2,2] sorted, pick-from-index, children of []:

          []
     /    |     \
   [1]   [2]    [2]   <- same label as left sibling
                x        its subtree would repeat [2]'s
```

The rule is `i > start and nums[i] == nums[i-1]`. The `i > start` part matters: it only compares siblings. Going one level deeper and taking the second 2 right after the first (`[2] -> [2,2]`) is a different child of a different node, and it is allowed.

### Recursion depth and the call stack

Depth equals the length of the path, so it is bounded by n for subsets and permutations, 2n for parentheses, target/min for Combination Sum, and the number of free cells for grid walks. Python's default recursion limit is about 1000, which none of these problems approach except large grid walks.

```text
 time ->   push    push     push    pop     pop     push
 stack:   [d0]  [d0,d1] [d0,d1,d2] [d0,d1] [d0]  [d0,d1']
 path :    []    [1]     [1,2]      [1]     []     [2]
```

The stack and the path grow and shrink together. That is the invariant in motion.

## The invariant

> When a call to `dfs` returns, every piece of shared state is exactly as it was when the call began; and while a call is running, `path` holds precisely the choices on the edges from the root to that call's node.

Everything else follows. Siblings start from identical state, so they see the same "remaining", the same "used", the same board. The recorded answers are correct because the path at a node is the node.

```text
 LEGAL (back at node [1] after exploring child [1,2])
   path   = [1]
   used   = [T, F, F]
   stack  = dfs@[] , dfs@[1]
   -> next sibling [1,3] starts clean

 ILLEGAL (forgot to pop / unmark)
   path   = [1, 2]        <- 2 still there
   used   = [T, T, F]     <- 2 still marked
   stack  = dfs@[] , dfs@[1]
   -> next "sibling" becomes [1,2,3], and 2 is
      never offered again at this level
```

A useful self-check while coding: every line that changes shared state before the recursive call has a mirror line after it, in reverse order.

## How to picture it

Carry one picture: **a decision tree and a pencil line**. The root is "nothing decided". Each level is one decision. The pencil is on the current node; its line back to the root is `path`. The call stack is the pencil line seen from the side, one frame per segment.

Then add scissors. A prune is a cut on an edge just below a node: the scissors remove the whole hanging subtree. The skill in harder problems is finding cuts that are high in the tree (cutting near the root saves exponentially more) and cheap to test.

The traces in this book draw that picture with a fixed legend:

```text
 legend for every "Watch it work" tree
   *[1,2]    node on the current path (pencil line)
   <- here   the node the top stack frame is at
   [2]       finished: visited, pencil already erased
   ?         not visited yet
   x         pruned: the subtree is never entered
```

Two more mental images help:

- **Count the tree to know the cost.** Time is (number of nodes visited) x (work per node). Subsets: 2^n nodes. Permutations: about e·n! nodes. Parentheses: Catalan-many leaves. If you cannot estimate the tree's size, you cannot estimate the running time.
- **Tree versus DAG.** If two different paths reach states that behave identically for the rest of the search (same index, same remaining sum, regardless of how you got there), the tree is secretly a DAG and memoisation or DP may beat backtracking. Backtracking is the right tool when the path itself is part of the answer, so the states cannot be merged.

## Signals in a problem statement

Point here:

- "return **all** ...", "list every ...", "generate all ...": the output is a set of configurations.
- "subsets", "combinations", "permutations", "arrangements", "partitions".
- Tiny constraints: n <= 10 for permutations, n <= 20 for subsets, a 9x9 board, a 6x6 grid, 4 cards.
- "each element may be used once" / "unlimited times": decides `i + 1` versus `i` in the recursion.
- "no duplicate combinations" with an input that "may contain duplicates": sort + skip.
- "place ... such that no two attack", "fill the board": constraint satisfaction with undo.
- "path that visits every cell exactly once", "the word can be built from adjacent cells": grid DFS with a visited mark you remove.
- "insert operators", "remove the minimum number of characters", then "return all": search over edits.

Point elsewhere:

- "**how many** ways" with large n (n up to 1000 or more): the count is wanted, not the list; look for DP.
- "minimum/maximum" of something with overlapping subproblems: DP or greedy.
- "shortest path" or "fewest steps" in an unweighted space: BFS, which finds the nearest answer without exploring deep dead ends.
- "does a subset with sum K exist" with n up to 200 and small sums: subset-sum DP over sums, not a 2^n tree.

## Python toolbox

The skeleton, with a closure so `path` and `result` need no passing around:

```python
def solve(nums):
    result, path = [], []
    def dfs(start):
        result.append(path[:])          # copy, not alias
        for i in range(start, len(nums)):
            path.append(nums[i]); dfs(i + 1); path.pop()
    dfs(0)
    return result
```

Brute-force oracles for testing your backtracking against:

```python
from itertools import combinations, permutations, product
subs  = [c for r in range(len(a)+1) for c in combinations(a, r)]
perms = list(permutations(a))
words = ["".join(p) for p in product("abc", "def")]
```

Other quirks worth knowing:

```python
import sys; sys.setrecursionlimit(10_000)   # deep grid walks
nonlocal best                               # rebind an int in a closure
s = "".join(path)                           # O(n) string answer
```

Lists are mutable and shared by reference, which is exactly why one `path` works for the whole walk and exactly why you must copy it when recording. Ints and strings are immutable, so passing `remaining - x` or `prefix + ch` as an argument "un-chooses" for free: the caller's value never changed.

## Mistakes people make

1. **Appending `path` instead of a copy.** Every answer aliases one list that ends empty. Fix: `result.append(path[:])`.
2. **Forgetting to pop or unmark.** State leaks into siblings. Fix: mirror every mutation after the recursive call.
3. **Looping from 0 in a combinations problem.** `[1,2]` and `[2,1]` both appear. Fix: loop from `start`.
4. **Recursing with `i + 1` when reuse is allowed (or `i` when it is not).** Fix: `i` means "may take this again", `i + 1` means "move past it".
5. **Skipping duplicates without sorting.** Equal values are not adjacent, the skip misses them. Fix: sort first.
6. **Writing the skip as `i > 0` instead of `i > start`.** Kills legitimate answers like `[2,2]`. Fix: compare only siblings.
7. **`continue` where `break` is valid.** Correct but wastes a scan of hopeless siblings. Fix: after sorting, `break` on the first overflow.
8. **Pruning too late.** Checking validity only at the leaf rebuilds the brute force. Fix: test the constraint at the moment of choosing.
9. **Using `x in path` for "used".** O(n) per check. Fix: a boolean array or a set kept in sync with the path.
10. **Returning `[""]` or `[[]]` for empty input when the problem wants `[]`.** Fix: read the edge case in the statement; handle it before the walk.

## The journey ahead

1. **Subsets**: the decision tree itself, choose/explore/un-choose, and the pick-from-index template where every node is an answer.
2. **Subsets II**: duplicates in the input; sort + skip equal siblings to cut identical subtrees.
3. **Permutations**: the pick-from-set template; a `used` array replaces the `start` index.
4. **Combination Sum**: the first real prune (remaining budget) and reuse via recursing on `i`; sorted order turns `continue` into `break`.
5. **Combination Sum II**: two cuts at once, budget break plus duplicate skip, with `i + 1` because reuse is gone.
6. **Letter Combinations**: a fixed-depth tree with a different alphabet per level; recursion as a variable number of nested loops.
7. **Generate Parentheses**: choices constrained by counters, so every branch taken is a prefix of a valid answer and no dead ends exist.
8. **Word Search**: backtracking on a grid; the "used" set becomes a mark on the board that you erase on the way back.
9. **Unique Paths III**: grid walk that must cover every free cell; counting remaining cells is the prune and the success test.
10. **N-Queens**: row-by-row placement with column and diagonal sets; constraints propagate across the board.
11. **Sudoku Solver**: constraint backtracking with bitmasks and choosing the most constrained cell first, so the tree stays narrow.
12. **Remove Invalid Parentheses**: search over deletions; count the exact removals needed first so the tree has a fixed budget.
13. **Expression Add Operators**: carry a running value and the last operand so multiplication can be undone in O(1).
14. **24 Game**: the state is a shrinking multiset; each step combines two numbers, with real-number tolerance.
15. **Robot Room Cleaner**: backtracking where you cannot see the tree; un-choose is a physical turn-around and step back.
