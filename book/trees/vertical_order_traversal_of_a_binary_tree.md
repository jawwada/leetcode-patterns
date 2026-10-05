# Vertical Order Traversal of a Binary Tree

*LeetCode 987 · Hard · Pattern: DFS with (column, row) coordinates, then group-sort · Reading time ~11 min*

## The problem

The root is at (row 0, col 0); a left child sits at (row+1, col-1) and a right child at (row+1, col+1). Report the
nodes column by column from left to right. Within a column, order by row, and break ties at the same (row, col) by
value.

```text
Example: [1,2,3,4,5,6,7] returns [[4],[2],[1,5,6],[3],[7]],
  since 5 and 6 share (2,0).
```

## What the problem is really asking

Lay the tree on graph paper. The root sits at `(row 0, col 0)`. Every left child is one row down and one column left, `(row+1, col-1)`; every right child is one row down and one column right, `(row+1, col+1)`. Now read the paper column by column from left to right, and inside each column read top to bottom. If two nodes land on the *same grid point*, read the smaller value first.

The answer is a list of lists: one inner list per column, leftmost column first.

Running example: `[1,2,3,4,6,5,7]`. I swapped 5 and 6 from the LeetCode example on purpose, for a reason that will show up in a moment.

```text
 col:     -2    -1     0     1     2
 row 0                 1
                     /   \
 row 1           2           3
                / \         / \
 row 2         4   6       5   7
                    \     /
                     >(2,0)<   6 and 5 land on the SAME point

 answer: [[4], [2], [1, 5, 6], [3], [7]]
```

Node 6 is the right child of 2: `(1,-1) -> (2,0)`. Node 5 is the left child of 3: `(1,1) -> (2,0)`. They collide. Column 0 therefore reads `1` (row 0), then `5` and `6` (both row 2, ordered by value).

What makes this Hard is not any single step. It is that there are three ordering rules stacked on top of each other (column, then row, then value), and the tree's natural traversal orders respect none of them fully. A DFS visits 6 before 5. A BFS visits row by row, but still visits 6 before 5 because 2 is to the left of 3. Whatever order you walk in, you will have to sort something.

## Do it by hand first

On paper you would not think about traversals at all. You would write each node's coordinate next to it, then fill a table:

```text
 node  (row, col)          column -2 : 4
  1     (0,  0)            column -1 : 2
  2     (1, -1)            column  0 : 1, 6, 5   <- as found
  4     (2, -2)                        1, 5, 6   <- fixed
  6     (2,  0)            column  1 : 3
  3     (1,  1)            column  2 : 7
  5     (2,  0)
  7     (2,  2)
```

Your hand kept two things. A **coordinate per node**, computed from its parent's coordinate. And a **bucket per column**, where nodes were dropped as you found them and tidied at the end. The coordinate is passed down the tree like the depth in the previous problem; the buckets are a dictionary keyed by column.

## The first honest attempt

A natural first plan works one column at a time:

1. Walk the tree once to find the leftmost and rightmost columns, `lo` and `hi`.
2. For each column `c` from `lo` to `hi`, walk the whole tree again, collecting `(row, val)` for every node whose column is `c`. Sort those pairs and emit the values.

It is correct. The cost is `O(n · W + n log n)`, where `W` is the number of columns. In a tree shaped like a long diagonal, `W` is about `n`, so this is `O(n²)`.

The repeated work is easy to draw. Every pass visits all seven nodes to keep one or three of them:

```text
 pass for col -2:  1 2 4 6 3 5 7   keeps 4
 pass for col -1:  1 2 4 6 3 5 7   keeps 2
 pass for col  0:  1 2 4 6 3 5 7   keeps 1 6 5
 pass for col  1:  1 2 4 6 3 5 7   keeps 3
 pass for col  2:  1 2 4 6 3 5 7   keeps 7
                   ^^^^^^^^^^^^^
   five full walks; each node's column was known on
   the first walk and recomputed four more times
```

Every node's column is computed in every pass, and in all but one pass the answer is "not mine, skip".

## The turning point

**Claim: the problem is "sort all nodes by the key `(col, row, val)`, then cut the sorted list wherever `col` changes". Once every node carries its coordinate, the shape of the tree no longer matters.**

Justify it by reading the rules again. Columns go left to right: that is sorting by `col`. Inside a column, top to bottom: sorting by `row` as the second key. Same grid point, smaller value first: sorting by `val` as the third key. Three rules, three keys, in priority order. Python compares tuples exactly this way, left element first, so a tuple *is* the composite key.

That turns a tree problem into a records problem:

- One traversal stamps every node with `(row, col)`. The coordinate of a child comes from its parent in O(1), so it rides down as recursion arguments, exactly like depth did for cousins.
- Drop each record into a bucket keyed by its column: `cols[col].append((row, val))`. A `defaultdict(list)` makes the buckets appear as needed, and negative column numbers are fine as dictionary keys. (A plain list indexed by column would need an offset, a classic bug.)
- At the end, visit the columns in `sorted(cols)` order, and sort each bucket's `(row, val)` tuples. The tuple sort applies "row first, then value" in one go.

Why bucket by column instead of sorting one big list of `(col, row, val)`? Both work and both are `O(n log n)`. Bucketing makes the "cut wherever `col` changes" step trivial: each bucket already is one output list.

**What about BFS?** It is tempting, because BFS hands you nodes row by row, so the row order inside each bucket comes for free. If the problem only said "top to bottom" (that is LeetCode 314, the premium sibling), BFS with `(node, col)` in the queue and no sorting inside buckets would be the whole answer. But this problem adds the tie rule, and BFS does not know about values: in our tree it would put 6 into column 0 before 5, because 2 is dequeued before 3. So with BFS you must still sort within each row of each bucket. Once you are sorting anyway, DFS plus a tuple sort is the simplest form that is obviously correct.

The single line that states the whole post-processing is:

```text
 [[v for _, v in sorted(cols[c])] for c in sorted(cols)]
```

## Watch it work

Tree `[1,2,3,4,6,5,7]`. The DFS visits in preorder: 1, 2, 4, 6, 3, 5, 7. Each frame shows the node being visited with its coordinate and the bucket dictionary after the append.

Frame 1. Visit the root at `(0, 0)`.

```text
 visit 1 at (row 0, col 0)
 cols:  0: [(0,1)]
 recursion: dfs(1,0,0)
```

The root starts column 0. Next call: left child with `(1, -1)`.

Frame 2. Visit 2 at `(1, -1)`, then its left child 4 at `(2, -2)`.

```text
 visit 2 at (1,-1), then 4 at (2,-2)
 cols: -2: [(2,4)]
       -1: [(1,2)]
        0: [(0,1)]
 recursion: dfs(1) -> dfs(2) -> dfs(4)
```

Each step left subtracts one from the column, so new buckets open to the left.

Frame 3. Back at 2, go right: visit 6 at `(2, 0)`.

```text
 visit 6 at (2, 0)        right child of (1,-1)
 cols: -2: [(2,4)]
       -1: [(1,2)]
        0: [(0,1), (2,6)]       <- second record in col 0
 recursion: dfs(1) -> dfs(2) -> dfs(6)
```

Node 6 lands under the root, in column 0.

Frame 4. Back to the root, go right: visit 3 at `(1, 1)`, then 5 at `(2, 0)`.

```text
 visit 3 at (1,1), then 5 at (2,0)
 cols: -2: [(2,4)]
       -1: [(1,2)]
        0: [(0,1), (2,6), (2,5)]   <- 6 before 5: out
        1: [(1,3)]                    of order for now
 recursion: dfs(1) -> dfs(3) -> dfs(5)
```

5 lands on the same grid point as 6 and is appended after it. The bucket is not yet in the required order.

Frame 5. Visit 7 at `(2, 2)`. The traversal is done.

```text
 visit 7 at (2, 2)
 cols: -2: [(2,4)]
       -1: [(1,2)]
        0: [(0,1), (2,6), (2,5)]
        1: [(1,3)]
        2: [(2,7)]
```

Every node has been stamped and bucketed exactly once.

Frame 6. Sort the keys, sort each bucket, strip the rows.

```text
 sorted(cols) = [-2, -1, 0, 1, 2]
 col  0: sorted([(0,1),(2,6),(2,5)])
       = [(0,1),(2,5),(2,6)]   row ties broken by value
 output: [[4], [2], [1, 5, 6], [3], [7]]
```

Throughout, each record's coordinate was correct the moment it was created, and each bucket held exactly the nodes of its column. Only the order inside a bucket was provisional, and the final sort fixed it.

## Why it is correct

Two invariants.

*Coordinates.* The root is called with `(0, 0)`. If a node is called with its true coordinate, its children are called with `(row+1, col-1)` and `(row+1, col+1)`, which are their true coordinates by definition. By induction every node is recorded with its true `(row, col)`.

*Buckets.* Every node is visited exactly once and appended to `cols[col]` for its own column, so after the traversal each bucket contains exactly the nodes of that column, no more and no fewer.

Then the output order is right by construction: iterating `sorted(cols)` gives columns left to right, and sorting a bucket's `(row, val)` tuples orders by row and breaks equal rows by value, which are the problem's second and third rules. Because values are compared only when both row and column match, two nodes with equal values at different rows are still ordered by row, as required.

## Cost

- Time `O(n log n)`: one `O(n)` traversal, then every record is sorted once inside its bucket (total at most `O(n log n)`), plus sorting the `W <= n` column keys.
- Space `O(n)`: one record per node in the buckets, plus `O(h)` recursion.

The brute force was `O(n · W + n log n)`. The win is removing the factor `W`: each node's column is used once, when it is computed.

## Variations you will meet

- **Binary Tree Vertical Order Traversal (LeetCode 314).** Same columns, but nodes on the same grid point are listed in left-to-right BFS order instead of by value. Now BFS with `(node, col)` in the queue is exactly right and no bucket needs sorting. Track `min_col` and `max_col` and the column keys need no sort either: `O(n)`.
- **Top view / bottom view of a tree.** Keep only the first (top) or last (bottom) node seen per column in BFS order. Same coordinates, a smaller bucket.
- **Sort by one big key.** Build a single list of `(col, row, val)` and sort it once, then group consecutive equal `col`s. Same cost; useful when the grouping key is not obvious in advance.
- **Diagonal traversal.** Give left children `d+1` and right children `d+0`; nodes on one diagonal share `d`. Same "stamp a coordinate, then bucket" idea with a different coordinate rule.

## What to carry forward

When the output order is defined by geometry, stamp each node with its coordinate on the way down and turn the tree into keyed records; a tuple sort applies all tie rules at once. The next problem goes back to a single, fixed order defined by the tree itself, inorder, and replaces the hidden recursion stack with one you hold in your hand.
