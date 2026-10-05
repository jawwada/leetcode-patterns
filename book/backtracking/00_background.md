# Backtracking

*15 problems · Reading time ~27 min*

## The chapter

Backtracking enumerates configurations by making a choice, recursing, and undoing the choice. This chapter teaches the
one skeleton behind subsets, permutations, combinations, constrained strings, grid paths, piece placement and puzzle
solving: name the choice, the constraint that prunes, and the undo.

Problems, in reading order:

1. [Subsets](subsets.md) · Medium
2. [Subsets II](subsets_ii.md) · Medium
3. [Permutations](permutations.md) · Medium
4. [Combination Sum](combination_sum.md) · Medium
5. [Combination Sum II](combination_sum_ii.md) · Medium
6. [Letter Combinations of a Phone Number](letter_combinations_of_a_phone_number.md) · Medium
7. [Generate Parentheses](generate_parentheses.md) · Medium
8. [Word Search](word_search.md) · Medium
9. [Unique Paths III](unique_paths_iii.md) · Hard
10. [N-Queens](n_queens.md) · Hard
11. [Sudoku Solver](sudoku_solver.md) · Hard
12. [Remove Invalid Parentheses](remove_invalid_parentheses.md) · Hard
13. [Expression Add Operators](expression_add_operators.md) · Hard
14. [24 Game](twenty_four_game.md) · Hard
15. [Robot Room Cleaner](robot_room_cleaner.md) · Hard

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

## Advanced patterns

The skeleton above solves every Medium in this chapter. The Hards use the same skeleton, but each adds one idea about *what the state is* or *where to cut*. These are the ideas to recognise on sight.

### 1. Constraint state updated incrementally

**When it shows up**: placement problems where a new piece must not conflict with any piece already placed (queens on a board, digits in a sudoku row), and checking "against everything so far" would cost O(n) per node.

**The intuition**: do not re-check the board; keep a summary of *what is already forbidden* and update it on choose and un-choose. The trick is finding a label so that "these two squares conflict" becomes "these two squares have the same key". For queens, every square on a down-right diagonal has the same `r - c`, and every square on a down-left diagonal has the same `r + c`. So the whole attack picture is three sets of integers: columns, `r - c` values, `r + c` values. Placing a queen adds three keys; lifting it removes the same three. The test at a node is three O(1) lookups, and it happens at the moment of choosing, so an illegal partial board is never extended.

```text
 queen at (r=1, c=2) on 4x4; keys it owns:
    c0  c1  c2  c3
 r0  .   \   .   /     col  2  : every square in col 2
 r1  .   .   Q   .     r-c -1  : the "\" line
 r2  .   /   .   \     r+c  3  : the "/" line
 r3  /   .   .   .
 sets: cols={2}  diag={-1}  anti={3}
 square (3,0): c=0 ok, r-c=3 ok, r+c=3 HIT -> pruned
```

**Where you'll use it**: N-Queens (column and diagonal sets), Sudoku Solver (row, column and box sets). Beyond the chapter: N-Queens II and Valid Sudoku use the same keys without the search.

### 2. Bitmasks as the used set

**When it shows up**: the universe of things that can be "used" is small (9 digits, n <= 15 columns, a grid with <= 20 free cells), and you test, add and remove members at every node.

**The intuition**: a set of small integers is one integer, bit `k` set meaning "k is in". Union is `|`, membership is `>> k & 1`, adding a known-absent member is `|=`, removing it is `^=`. The real win is that *all the candidates at once* come out of one expression: for sudoku, `~(row | col | box) & 0x3FE` is the set of legal digits for a cell; for queens, `~(cols | dr | dl) & full` is the set of safe columns in the next row. Then `low = free & -free` peels off one candidate at a time. For queens there is an extra gift: shifting the diagonal masks left and right by one moves every attack one row down, so the diagonals need no `r - c` arithmetic at all. A bitmask is also hashable, which is what lets a search over "which cells are used" turn into a memo table when the same mask keeps reappearing.

```text
 4-queens, queen placed in row 0 at col 1 (col 0 leftmost)
 moving to row 1:     c0 c1 c2 c3
   cols (same col)    0  1  0  0
   dr   (moves right) 0  0  1  0   attack down-right
   dl   (moves left)  1  0  0  0   attack down-left
   OR                 1  1  1  0
   free = ~OR         0  0  0  1   only col 3 is safe
 full 4-queens search: 17 nodes visited, versus 341 in the
 unpruned 4-ary tree of depth 4
```

**Where you'll use it**: Sudoku Solver (nine-bit masks per row, column, box), N-Queens (bitmask variant); Unique Paths III when you memoise `(cell, visited mask)`. Beyond: Shortest Path Visiting All Nodes (847) and Partition to K Equal Sum Subsets (698).

### 3. Most constrained first, and forced moves

**When it shows up**: you are free to choose *which* variable to decide next (any empty sudoku cell, any unplaced piece), and the branching factor differs a lot from variable to variable.

**The intuition**: the order of decisions does not change the set of solutions (every empty cell needs some digit eventually), but it changes the shape of the tree enormously. Branch on the cell with the fewest candidates. If that number is 0, the board is already dead, and you learn it now instead of after ten more guesses elsewhere. If it is 1, the move is forced: a tree level with a single child costs nothing, and filling it often leaves another cell with one candidate, so forced moves chain. Only when every cell has two or more options do you really guess, and then you guess where the odds are best and a wrong guess is refuted soonest. Put generally: cut high in the tree, because one cut near the root removes exponentially more than one near the leaves.

```text
 one empty cell, its three masks (bit d = digit d used)
   row  {3,5,7}       0 0 1 0 1 0 1 0 0    digits 1..9
   col  {1,6,8,9}     1 0 0 0 0 1 0 1 1
   box  {3,5,6,8,9}   0 0 1 0 1 1 0 1 1
   used = OR          1 0 1 0 1 1 1 1 1
   cand = ~used       . 2 . 4 . . . . .  -> 2 candidates
 MRV scans all empty cells: counts 2, 4, 1, 3 ...
 pick the "1" (forced), then rescan; a "0" ends the branch
```

**Where you'll use it**: Sudoku Solver is the chapter's showcase. N-Queens uses a fixed row order, which is safe because each row needs exactly one queen. Beyond: exact-cover solvers (Algorithm X picks the least-covered constraint), graph colouring.

### 4. Count the minimum first, then search with a budget

**When it shows up**: the answers must be optimal ("remove the **minimum** number", "fewest changes") and you are asked to list all of them. Searching over every number of edits and keeping the best is the trap.

**The intuition**: split the problem into a cheap counting pass and a search. For parentheses, one left-to-right scan with a balance counter tells you exactly how many `(` and how many `)` must go: every `)` that would drive the balance negative forces one deletion, and every `(` still open at the end forces one more. These counts are necessary and sufficient, so the search no longer asks "how many?", only "which ones?". The budget caps the depth of deletion, and a second fence (the running balance may never go negative) cuts bad prefixes at their first wrong character. A leaf is accepted only with both budgets at exactly zero, so every answer is minimal by construction. The same "count what is still owed" idea appears in Unique Paths III: a `todo` counter of unvisited cells turns the "covered everything?" check into one integer comparison at the end cell.

```text
 s = ( ) ( ) ) ( )     scan: balance 1 0 1 0 -1 ...
     0 1 2 3 4 5 6           index 4 cannot match: right=1
 budget: left=0, right=1   (one ")" must go, no "(")

 delete idx 1 -> ( ( ) ) ( )   valid   "(())()"
 delete idx 3 -> ( ) ( ) ( )   valid   "()()()"
 delete idx 4 -> ( ) ( ) ( )   same string: dedupe
 keep 0..4    -> balance -1 at idx 4: pruned on the spot
```

**Where you'll use it**: Remove Invalid Parentheses (removal budgets plus balance fence), Unique Paths III (cells-still-owed counter). Duplicate answers can still appear from deleting either of two equal adjacent brackets; collect into a set, or skip deleting a bracket equal to the one just kept.

### 5. Carry an undoable aggregate: running value plus last operand

**When it shows up**: each choice extends an expression or a sequence, and the prefix has a value you need at the leaf, but the next choice can retroactively change how the prefix evaluates (multiplication binds tighter than the `+` before it).

**The intuition**: never re-evaluate the prefix string; carry its value down as an argument. The difficulty is precedence: in `1 + 2 * 3`, the `*3` must act on the `2`, not on the `3` already summed. Treat the expression as a sum of terms, where `+` and `-` start a new term and `*` grows the current one. Carry `value` (the whole prefix) and `last` (the signed last term). Then `*x` is "take the last term out, put `last * x` back": `value - last + last * x`. The sign must live inside `last`, or `2 - 3 * 4` goes wrong. Because the pair is passed as arguments, un-choose is free: the caller's copies never changed.

```text
 building 2 - 3 * 4 + 5, state after each step
 step   value              last
 2      2                  2
 -3     2 - 3      = -1    -3
 *4     -1 + 3 - 12 = -10  -12   undo -3, add -3*4
 +5     -10 + 5    = -5    5
 check: 2 - 12 + 5 = -5    (O(1) work per edge)
```

**Where you'll use it**: Expression Add Operators. Beyond: Basic Calculator II (227) uses the same `last` trick to evaluate, not search; Target Sum (494) drops `*` and collapses into DP.

### 6. Shrink the state instead of extending a path

**When it shows up**: any two items may combine in any order (bracket placement is free), so there is no left-to-right prefix to build. "Use these numbers with `+ - * /` and any parentheses" is the classic shape.

**The intuition**: every expression tree is evaluated by repeatedly taking two values that are ready and replacing them with one. So the state is the multiset of values on the table, and one move is "pick a pair, pick an operation, recurse on a table one smaller". Parentheses never appear explicitly: which pair you merge first *is* the bracketing. Because the state shrinks, the depth is fixed (k values, k - 1 merges) and the tree is small enough to walk fully: for four cards, at most 36 x 18 x 6 = 3,888 leaves. Two details matter. Subtraction and division are not commutative, so for a pair `(a, b)` you try `a-b`, `b-a`, `a/b` and `b/a`. And real division means floats, so the leaf test is `|x - 24| < 1e-6`.

```text
 table [4, 1, 8, 7]
   merge 8,4 with "-"  -> [1, 7, 4]
   merge 7,1 with "-"  -> [4, 6]
   merge 4,6 with "*"  -> [24]      leaf: |24-24| < 1e-6
 expression recovered: (8 - 4) * (7 - 1)
```

**Where you'll use it**: 24 Game. Contrast with Expression Add Operators: if the order of items is fixed, carry a prefix (pattern 5); if any pair may go first, shrink a multiset. Memoising on the sorted table helps when the card count grows.

### 7. Relative coordinates and a physical undo

**When it shows up**: you cannot see the search space. You are an agent with "move forward, turn, is there a wall?" and no map, and every un-choose must be carried out by actions in the world.

**The intuition**: you do not need the true map to remember where you have been; you need a consistent frame. Call the starting cell `(0, 0)` and the starting heading "up", and track your own position and heading as you move; the visited set uses these invented coordinates. Un-choose is now a sequence of commands: when the child returns, the parent is directly behind the robot, so "turn twice, move, turn twice" puts it back on the parent cell *facing the same way as before*. That last detail is the contract that makes the recursion work: every call hands the robot back to its caller on the same cell with the same heading, so the parent's loop of "try ahead, turn right" stays in sync with the code's idea of direction.

```text
 invented frame: start S = (0,0), facing up = dir 0
 dirs: 0 up (-1,0)  1 right (0,1)  2 down (1,0)  3 left (0,-1)

  row -1    A      robot on S facing up; ahead is A
            ^      A unvisited, move() ok -> dfs(A, up)
  row  0    S      A's subtree done: turn, turn, move,
          col 0    turn, turn -> on S, facing up again
                   turnRight -> now trying dir 1 (right)
```

**Where you'll use it**: Robot Room Cleaner. Beyond: Minimum Path Cost in a Hidden Grid (1810), which first maps the room this way and then runs Dijkstra on the map.

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
import sys; sys.setrecursionlimit(10_000)  # deep grid walks
nonlocal best                              # rebind outer int
s = "".join(path)                          # O(n) string answer
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

The fifteen problems climb in four stages. The first stage builds the three templates; the second learns to cut; the third moves the walk onto a board; the last changes what the state *is*. Each problem adds one idea to the previous one, so the order matters.

### Stage 1: the three tree shapes

**Subsets.** The plainest possible question, and the right place to meet the tree: there are 2^n answers, so no algorithm can beat listing them, and the only question is how to list each exactly once with no wasted work. It teaches choose/explore/un-choose with a single shared `path`, the pick-from-index template where every node is an answer, and the habit of copying the path when you record it.

**Subsets II.** Add one repeated value and the same code prints `[1,2]` twice. The tempting fix is a set of tuples at the end, which still builds every duplicate subtree. The new idea is to stop duplicates where they are born: sort, then skip a child whose value equals its left sibling's, with the `i > start` guard that keeps `[2,2]` legal.

**Permutations.** Now order matters, so the start index stops working: after choosing 3 you still need to be able to choose 1. The puzzle is what replaces it, and the answer is a `used` flag per element, which turns pick-from-index into pick-from-set. This `used` array is the ancestor of every visited mark and attack set later in the chapter.

### Stage 2: learning to cut

**Combination Sum.** The first problem where most of the tree is hopeless: once the running sum overshoots, nothing below can come back. That gives the first real prune (a remaining budget), and two small twists worth understanding: recursing on `i` rather than `i + 1` allows reuse, and sorting turns `continue` into `break`, cutting a whole fan of siblings with one comparison.

**Combination Sum II.** Two earlier ideas meet: the duplicate skip from Subsets II and the budget break from Combination Sum, with reuse switched off (`i + 1`). The interesting question is whether the two cuts interfere; they do not, because one compares siblings and the other compares against the budget.

**Letter Combinations.** A breather with a new shape: the depth is fixed by the input, and each level has its own alphabet. The idea it teaches is that recursion is a way to write a variable number of nested loops, which is exactly what you need when you do not know at coding time how many loops there will be.

**Generate Parentheses.** Here the prune is so good that there are no dead ends at all. Two counters (opens used, closes used) decide which characters are allowed next, so every branch taken is a prefix of some valid answer. It is the first taste of "make illegal states impossible to enter" rather than "detect them and back off".

### Stage 3: the walk moves onto a board

**Word Search.** Backtracking on a grid: the tree's children are the four neighbours, and the `used` flag becomes a mark written on the board itself and erased on the way back. The puzzle is why you cannot just keep a global visited set as in an ordinary flood fill: a cell used by one failed path must be free for the next one.

**Unique Paths III.** The walk must cover every free cell and end on a specific square. Checking coverage at the end would be the brute force; the new idea is a `todo` counter that is both the prune and the success test, which is the "count what is still owed" pattern in its simplest form. Watch the off-by-one for the end cell.

**N-Queens.** The first Hard, and the first problem where a choice constrains distant parts of the state. Placing row by row removes the row conflict for free; the new idea is labelling diagonals by `r - c` and `r + c`, so that the conflict test becomes three set lookups at the moment of choosing (Advanced pattern 1).

**Sudoku Solver.** N-Queens with nine values per line and a free choice of which cell to fill. Two ideas arrive together: bitmasks that produce all candidates of a cell in one expression, and branching on the most constrained cell, which turns most of the puzzle into forced moves (patterns 2 and 3).

### Stage 4: the state itself changes shape

**Remove Invalid Parentheses.** The answers must be minimal, and the naive search tries every number of deletions. The new idea is to count the exact number of `(` and `)` deletions first, then search only over *which* ones, with a balance fence pruning bad prefixes (pattern 4).

**Expression Add Operators.** Each edge appends an operator and an operand, and the puzzle is precedence: a `*` must reach back into the term you already added. The idea is to carry `value` and the signed `last` term so that multiplication is undone and redone in O(1) (pattern 5).

**24 Game.** Same flavour of "operators between numbers", but now any pair may be combined first and parentheses are free. A prefix no longer describes the state; the multiset of remaining values does. The search becomes "merge two, recurse on the smaller table", with float tolerance at the leaf (pattern 6).

**Robot Room Cleaner.** The final step removes the map. You explore through a robot's API, so the tree is invisible and un-choose is a physical action that must leave the robot on the same cell with the same heading. Relative coordinates and the turn-around return trip close the chapter (pattern 7): if you can backtrack here, you understand exactly what "restore the state" means.
