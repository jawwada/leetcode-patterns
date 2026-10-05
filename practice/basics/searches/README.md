# Searches

Two families of search, one idea: **shrink the set of places the answer can still be, and never look at a place twice.**

- **Binary search** works on anything monotone: a sorted array, or a yes/no predicate that flips exactly once over a range of candidate answers. Each probe halves the range.
- **Graph search** (BFS and DFS) explores reachable states. BFS uses a queue and finds the fewest steps; DFS uses recursion or a stack and finds reachability, components and orderings. A visited set makes each state enter the frontier once.

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| binary search probe `mid = (lo + hi) // 2` | O(1) | halves the range; O(log n) probes in total |
| binary search on an answer | O(log(hi - lo)) calls of `feasible` | `feasible` must be monotone: once true, true for everything larger |
| BFS | O(V + E) | each vertex enqueued once, each edge looked at once; grid: O(m*n) |
| DFS (recursive or stack) | O(V + E) | recursion depth up to V, so a long chain can need an explicit stack |
| connected components | O(V + E) | one search per unvisited vertex; the number of searches is the answer |
| multi-source BFS | O(V + E) | enqueue every source at distance 0 before the loop; one BFS instead of one per source |

## Drawn example: lower_bound of 2 in [1, 2, 2, 2, 5, 7]

The half-open range `[lo, hi)` holds every index that might still be the first value `>= 2`; `hi = len(nums)` means "maybe none".

```
    1    2    2    2    5    7    |
   ^L             ^M             ^H     nums[3] = 2 >= 2: mid could be it, keep it -> hi = mid = 3
    1    2    2    2    5    7    |
   ^L   ^M        ^H                    nums[1] = 2 >= 2: keep it                  -> hi = 1
    1    2    2    2    5    7    |
  ^LM   ^H                              nums[0] = 1 <  2: answer is right of mid   -> lo = mid + 1 = 1
lo == hi == 1: lower_bound = 1.  upper_bound uses <= instead of < and gives 4.  count = 4 - 1 = 3.
```

The classic "find x" search uses the closed range `[lo, hi]` and `while lo <= hi`, because the range may hold one last candidate when `lo == hi`. Binary search on an answer is the same loop with `feasible(mid)` in place of the comparison: feasible means `hi = mid` (mid may be the answer), infeasible means `lo = mid + 1`.

## Drawn example: BFS on a grid, 0 free and 1 wall

```
start (0,0), distance counted in cells

layer 1  frontier [(0,0)]       1 2 #      push (0,1); (1,0) is a wall
layer 2  frontier [(0,1)]       # . .
layer 3  frontier [(1,1)]       # # .
                                1 2 #
layer 4  frontier [(1,2)]       # 3 4
layer 5  frontier [(2,2)]       # # 5      target popped at layer 5 -> answer 5
```

Everything in the queue at the start of a layer has the same distance; its children form the next layer. A cell gets its distance **when it is pushed**, so nobody can push it again with a bigger one. Multi-source BFS (01 Matrix) is the same picture with every source placed in layer 0.

## DFS: recursion and the explicit stack

```
graph 0: [1, 2]   1: [3]   2: [3]   3: []            recursive order 0 1 3 2

stack [0]      pop 0 visit  push 2 then 1  (reversed, so 1 is on top)
stack [1, 2]   pop 1 visit  push 3
stack [3, 2]   pop 3 visit
stack [2]      pop 2 visit  push 3
stack [3]      pop 3        already visited, skip
```

To match the recursion the stack version pushes the neighbours **reversed** and marks a node **when it is popped**, skipping stale copies. That is the opposite of BFS, where marking happens on push; mixing the two habits is the most common DFS/BFS bug.

## The invariants to say out loud

- Binary search: "`lo` is the first index that might still be the answer, `hi` is the first index that cannot be; the answer is in `[lo, hi)` and the range shrinks every turn."
- Binary search on an answer: "Everything below `lo` is infeasible, `hi` is feasible or the upper limit; the smallest feasible value is in between."
- BFS: "Mark visited when you enqueue. The queue holds one layer; the first time a state is popped, its distance is final."
- DFS with a stack: "Push the neighbours reversed, mark when you pop, skip what is already marked."
- Components: "Every time I have to start a new search, I have found a new component."

## Exercises

| File | Drills |
|---|---|
| `01_binary_search_variants.py` | classic search on `[lo, hi]`, lower_bound / upper_bound on `[lo, hi)`, count = upper - lower |
| `02_binary_search_on_answer.py` | LeetCode 1011: monotone `feasible(cap)`, smallest feasible capacity in `[max, sum]` |
| `03_bfs_grid_shortest_path.py` | layer-by-layer BFS on a 0/1 grid, mark on push, four directions with a bounds check |
| `04_dfs_recursive_and_iterative.py` | recursive DFS and the explicit stack that reproduces its order (reversed pushes, mark on pop) |
| `05_connected_components.py` | adjacency list from edges in both directions, one BFS per unvisited node |
| `06_multi_source_bfs_01_matrix.py` | LeetCode 542: enqueue every zero first, the layer of first arrival is the distance |
