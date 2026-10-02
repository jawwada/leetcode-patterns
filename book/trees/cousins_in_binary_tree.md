# Cousins in Binary Tree

*LeetCode 993 · Easy · Pattern: DFS carrying path state · Reading time ~6 min*

## What the problem is really asking

All the values in the tree are distinct. You get two of them, `x` and `y`. Their nodes are *cousins* if they sit at the same depth but hang from different parents. Return `True` or `False`.

The answer is a yes/no resting on two facts per target: its **depth** (which layer) and its **parent** (which node it hangs from). Either part can fail: different layers means not cousins, and same layer with the same parent means siblings.

Running example: `root = [1,2,3,null,4,null,5]`, `x = 5`, `y = 4`.

```text
 depth 0            1
                  /   \
 depth 1         2     3
                  \     \
 depth 2           4     5
                   ^     ^
                   y     x
 4: depth 2, parent 2      5: depth 2, parent 3
 same layer, different parents  -> cousins -> True
```

The catch: a `TreeNode` has only `val`, `left`, `right`. Depth and parent belong to the *path* from the root, not to the node.

## Do it by hand first

With the picture in front of you, you do two things. You count down from the top to see which row 4 is on, and which row 5 is on. Then you trace a line upward from each one to see what it hangs from.

```text
 your finger going down the tree:
   at 1 (row 0) -> step to 2 (row 1) -> step to 4 (row 2)
        "4 is on row 2, and I came from 2"
   at 1 (row 0) -> step to 3 (row 1) -> step to 5 (row 2)
        "5 is on row 2, and I came from 3"
```

Notice that your finger already knew both facts on the way down. When it arrived at 4, it knew it had taken two steps, and it knew the node it just left was 2. Your hand kept track of a pair: *(where I came from, how many steps I took)*. That pair is the seed of the algorithm: pass it down as arguments.

## The first honest attempt

Answer the four questions separately. Write `depth(target)`, a search from the root that returns how deep `target` is. Write `parent(target)`, a search that returns the node whose child is `target`. Then call `depth(x)`, `depth(y)`, `parent(x)`, `parent(y)` and compare.

Each search is `O(n)`, so the total is `O(4n)`: still linear, but look at the waste:

```text
 search        nodes walked
 depth(5)      1 2 4 3 5
 depth(4)      1 2 4
 parent(5)     1 2 4 3 5
 parent(4)     1 2 4
               ^ ^ ^
   the top of the tree is walked four times, and every walk
   passes nodes whose depth and parent it could have noted
```

Every walk *sees* the depth and parent of each node it passes and throws that away, except for its one target.

## The turning point

**Claim: a single DFS that carries `(parent, depth)` as arguments knows both facts for every node at the moment it arrives, so one walk answers all four questions.**

This is the "finger" from before. When the recursion calls `dfs(child, node, depth + 1)`, the child receives the exact node it hangs from and its exact layer. Nothing is searched for; it is handed down.

So the algorithm is:

- `dfs(node, parent, depth)` returns immediately on `None`.
- If `node.val` is `x` or `y`, record `info[node.val] = (parent, depth)`.
- Recurse into both children with `(node, depth + 1)`.

After `dfs(root, None, 0)`, compare: depths equal **and** parents different. Compare the parents by identity (`is not`), which says exactly "these are different nodes". The root gets parent `None`, which is fine: if `x` is the root, its depth is 0 and nothing else is at depth 0, so the depth test fails first.

A chapter-wide rule: information flowing *down* (depth, parent, bounds) travels as an argument; information flowing *up* (heights, sums) travels as a return value.

## Watch it work

Tree `[1,2,3,null,4,null,5]`, `x = 5`, `y = 4`. The DFS visits in preorder: 1, 2, 4, 3, 5.

Frame 1. Start at the root with no parent.

```text
 call dfs(1, None, 0)          info = {}
      [1]  <- here, depth 0
     /   \
    2     3
```

The root is neither 4 nor 5, so nothing is recorded; the walk goes left with `(parent=1, depth=1)`.

Frame 2. At node 2.

```text
 call dfs(2, 1, 1)             info = {}
       1
     /   \
   [2]    3     <- here, depth 1, parent 1
     \
      4
```

Node 2 is not a target. Its left child is `None` (returns at once), then the walk goes right with `(parent=2, depth=2)`.

Frame 3. At node 4, which is `y`.

```text
 call dfs(4, 2, 2)             info = {4: (node 2, 2)}
       1
     /   \
    2     3
     \
     [4]        <- here, depth 2, parent 2
```

The pair arrives as arguments and is stored. Both children are `None`.

Frame 4. Back up and over to node 3, then to node 5, which is `x`.

```text
 call dfs(3, 1, 1)
 call dfs(5, 3, 2)             info = {4: (node 2, 2),
       1                               5: (node 3, 2)}
     /   \
    2     3
     \     \
      4    [5]  <- here, depth 2, parent 3
```

Frame 5. Compare.

```text
 x=5: depth 2, parent node 3
 y=4: depth 2, parent node 2
 2 == 2 and (node 3 is not node 2)  -> True
```

What stayed invariant: on entry to every call, `depth` equalled the number of edges from the root to `node`, and `parent` was the node one edge above it. The dictionary only ever held correct facts.

## Why it is correct

By induction on depth: the root is called with `(None, 0)`, which is correct. If a node is called with its correct parent and depth, it calls each child with itself as parent and `depth + 1`, which is correct for the child. So every node, and in particular `x` and `y`, is visited with its true parent and depth. The values are unique, so each target is recorded exactly once. The final test is the definition of cousins word for word.

## Cost

- Time `O(n)`: every node is entered once.
- Space `O(h)`: the recursion is as deep as the tree is tall; the dictionary holds two entries.

## Variations you will meet

- **BFS instead of DFS.** Process one layer at a time with a queue; if a layer contains exactly one of `x`, `y`, answer `False`. To rule out siblings, check whether any node's two children are `x` and `y` together. This uses the layer property directly and can stop early.
- **Non-unique values.** Then `x` and `y` must be given as node references, and you compare nodes by identity, not values.

## What to carry forward

Facts that live on the path, like depth and parent, are passed down as arguments and are free at every node. The next problem passes down a richer coordinate, `(row, col)`, and has to sort the nodes by it.
