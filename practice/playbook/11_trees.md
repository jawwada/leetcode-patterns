## Trees

> A tree recursion is a conversation. Each call gets facts from its **parent** (arguments: depth, bounds, the path so far), asks its two **children** for facts about their subtrees (return values: height, sum, "found it"), and may **record** something in a global answer on the side. Decide those three things and the code nearly writes itself.

**Reach for it when** the input is a `TreeNode` (or anything with parents and children); the answer at a node depends on its **subtrees** (height, balance, sums, diameter) or on its **ancestors** (bounds, depth, path sums); the problem says *level*, *row* or *view from the side* (BFS); or it says *BST* (inorder is sorted; compare and go one way).

**In this repo:** `trees/` (28 problems) · bank: `practice/simple/26_binary_tree_level_order_traversal.py`, `practice/simple/27_validate_binary_search_tree.py`, `practice/simple/28_kth_smallest_element_in_a_bst.py`, `practice/simple/29_lowest_common_ancestor_of_a_bst.py`, `practice/simple/30_diameter_of_binary_tree.py` · basics: `practice/simple/basics/trees/` (traversals recursive and iterative, BFS level order and height, BST insert/search/delete, balanced, LCA, serialize/deserialize).

### The picture

Information moves in two directions. **Down**, as arguments: what the ancestors know. **Up**, as return values: what a subtree knows about itself.

```text
tree = [3, 9, 20, None, None, 15, 7]

                  arguments DOWN (depth)        return values UP (height)

        3         depth 0                       3 returns 1 + max(1, 2) = 3
      /   \
     9     20     depth 1                       9 returns 1      20 returns 1 + max(1, 1) = 2
          /  \
        15    7   depth 2                       15 returns 1     7 returns 1
```

Every call is the same small box. It receives arguments from its parent, gets one return value from each child, sends one value up, and may write to a global answer that nobody returns:

```text
                         parent
             arguments  |      ^  return value
       (depth, bounds,  |      |  (height, sum, found node)
        path so far)    v      |
                    +--------------+
                    |     node     |------>  RECORD into a global answer
                    +--------------+         (best, a result list)
                     |  ^      |  ^
                args v  | ret  v  | ret
                    left        right
```

Why it is fast: the brute force usually recomputes a fact about a subtree once for every ancestor (calling `height()` from each node in Balanced or Diameter is O(n²) on a chain), or re-walks the path from the root at every node (Count Good Nodes rescanning the path is O(n·h)). A bottom-up pass computes each subtree fact exactly once and hands it to the parent; a top-down pass hands each node a summary of its ancestors (a running max, a window, a remaining sum) in O(1). Either way every node is visited once: O(n) time, O(h) space for the recursion (h = height).

### From idea to code

**The idea in one sentence:** *write the contract first, "f(node, what comes down) returns what my parent needs about my subtree, and records the answer if it can sit at any node", then write the base case for `None`, recurse into the children, and combine.*

| Decision | Tree-recursion answer |
|---|---|
| **State**: what must I remember? | the arguments (facts from above: depth, bounds, remaining sum, the path), the return value (a fact about this subtree), and maybe one global (`best`, a result list) |
| **Definition**: what exactly does each variable mean? | one sentence per function, as a comment: `height(node)` = number of nodes on the longest downward path from `node`; 0 for `None` |
| **Invariant**: what is true at the end of every step? | trust the recursion: when a child's call returns, its answer is correct for that child's *whole* subtree |
| **Step**: how does one node change the state? | base case → recurse into the children (with updated arguments) → combine their two answers with `node.val` |
| **Record**: when is the answer updated? | when the problem's answer is *not* what the parent needs (a path that bends at this node, a finished level, a matching path): write it to the global inside the call |
| **Init**: starting values | the answer for an empty tree (`0`, `True`, `None`), the root's arguments (`-inf, inf`, depth 0), and `best` = the worst possible (`0` for lengths, `-math.inf` for sums) |
| **Return**: what comes back? | `f(root)` or the recorded global, translated if needed (`height(root) != -1`) |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "an empty tree" | `if node is None: return 0` (or `True`, or `None`: the neutral answer) |
| "a leaf" | `if node.left is None and node.right is None:` |
| "ask both children" | `left, right = f(node.left), f(node.right)` |
| "tell my children what I know" | `f(node.left, depth + 1)`, `valid(node.left, low, node.val)` |
| "my answer from theirs" | `return 1 + max(left, right)` |
| "my parent needs two facts" | `return depth, node` (a tuple) |
| "remember the best seen anywhere" | `nonlocal best`, then `best = max(best, left + right)` |

**Write the contract before any code.** Four questions turn an unseen problem into a signature:

```text
1. DOWN    To judge ONE node, what must I know about the nodes ABOVE it?
           -> arguments: path max, window, remaining sum, depth, parent
2. UP      What must my PARENT know about my subtree?
           -> the return value; if it needs two facts, return a tuple
3. RECORD  Is the problem's answer what the root returns? If the answer can sit at ANY node
           (a bend, a count, a list of paths) -> record it on the side
4. EDGES   What does None return? What does the root receive?
           -> the neutral value and the starting arguments
contract:  f(node, <down>) -> <up> about node's subtree; records <global>; f(None) = <neutral>
```

If the parent needs exactly what the problem asks for, just return it; if not, return what the parent needs and record the answer on the side. The contracts of this section:

| Problem | Down (from the parent) | Up (return value) | Recorded globally |
|---|---|---|---|
| Balanced (110) | – | height, or -1 = "unbalanced below" | – |
| Diameter (543) | – | height (one arm) | `best = max(best, left + right)` |
| Max path sum (124) | – | best one-arm sum going down (the parent clips a negative one to 0) | `best = max(best, val + left + right)` |
| Longest univalue path (687) | – | the longest same-value arm, in edges | `best = max(best, left + right)` |
| Distribute coins (979) | – | coins to send up (negative: coins needed) | `moves += abs(left) + abs(right)` |
| Subtree with all deepest (865) | – | a tuple: (depth of the deepest leaf, the answer for this subtree) | – |
| Validate BST (98) | open window `(low, high)` | `True` / `False` | – |
| Count good nodes (1448) | largest value on the path | number of good nodes in this subtree | – |
| Path Sum II (113) | remaining sum, the shared `path` | – | copies of the matching paths |
| Right side view (199) | depth | – | the first value seen at each depth |
| LCA (236) | – | `p`, `q`, the LCA, or `None` | – |

First the node, and two helpers: build a tree from LeetCode's level-order list (`None` = no child) and turn a tree back into that list.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build_tree(values):                      # LeetCode level order, None = no child
    nodes = [None if v is None else TreeNode(v) for v in values]
    kids = iter(nodes[1:])
    for node in nodes:
        if node:                             # each real node takes the next two slots
            node.left, node.right = next(kids, None), next(kids, None)
    return nodes[0] if nodes else None


def tree_to_list(root):                      # the inverse: tree -> LeetCode list
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        out.append(node.val if node else None)
        if node:
            queue.extend([node.left, node.right])
    while out and out[-1] is None:           # LeetCode trims the trailing Nones
        out.pop()
    return out


root = build_tree([3, 9, 20, None, None, 15, 7])
print(root.val, root.left.val, root.right.left.val)   # 3 9 15
print(tree_to_list(root))                             # [3, 9, 20, None, None, 15, 7]
```

**Try it**
- Build `[1, None, 2, 3]` and print `root.right.left.val`: 3. The `None` fills only 1's left slot, so 2 is 1's right child and 3 hangs to the left of 2.
- `build_tree([])` is `None` and `tree_to_list(None)` is `[]`: the empty tree round-trips.
- Delete the trimming loop in `tree_to_list`: the example prints `[3, 9, 20, None, None, 15, 7, None, None, None, None]`, two `None`s for each of the two bottom leaves.

The three shapes of tree recursion. Bottom-up (`max_depth`): children answer first, the parent combines. Top-down (`is_valid_bst`): the parent passes a constraint down. Return one thing, record another (`diameter`). Down and up at once is Count Good Nodes (1448): the largest value on the path goes down, the count of good nodes comes up; the drill at the end of the section has the same shape.

**Why recording at every node finds the best path:** every path has exactly one highest node. At that node the path is a left arm plus a right arm, each at most that child's height. Recording `left + right` at every node therefore sees every path at its own highest node. The order of the lines follows: a bottom-up call can only combine after both children have answered (post-order), and the RECORD sits between the children's answers and the RETURN, because it needs both arms while the parent gets only one.

```python
def max_depth(node):                          # bottom-up: the answer comes UP
    if node is None:                          # INIT: an empty tree has depth 0
        return 0
    left = max_depth(node.left)               # STEP: ask both children first ...
    right = max_depth(node.right)
    return 1 + max(left, right)               # RETURN: ... then combine (post-order)


def is_valid_bst(root):                       # top-down: the constraint goes DOWN
    def valid(node, low, high):               # STATE: every value here must be in (low, high)
        if node is None:
            return True                       # an empty subtree breaks nothing
        if not low < node.val < high:
            return False                      # one node outside its window decides it
        return (valid(node.left, low, node.val)         # STEP: going left caps high
                and valid(node.right, node.val, high))  # going right raises low
    return valid(root, -math.inf, math.inf)   # INIT: the root may be anything


def diameter(root):                           # RETURN one thing, RECORD another
    best = 0                                  # STATE: longest path seen anywhere, in edges
    def height(node):
        nonlocal best                         # we reassign best, so nonlocal is required
        if node is None:
            return 0                          # INIT: an empty tree has height 0
        left, right = height(node.left), height(node.right)   # STEP: both children answer first
        best = max(best, left + right)        # RECORD: the path that bends at node
        return 1 + max(left, right)           # RETURN: only one arm can continue upward
    height(root)
    return best                               # RETURN: the recorded answer, not height(root)


tree = build_tree([3, 9, 20, None, None, 15, 7])
print(max_depth(tree), is_valid_bst(tree), diameter(tree))          # 3 False 3
print(is_valid_bst(build_tree([5, 1, 7, None, None, 6, 8])))        # True
print(diameter(build_tree([1, 2, None, 3, 4, 5, None, None, 6])))   # 4  (bends at 2, not at the root)
```

**Try it**
- Count what the problem counts: record `left + right + 1` in `diameter` and try `diameter(build_tree([1, 2, 3]))`: 3 instead of 2. That is the number of *nodes* on the path; the problem counts edges.
- Copy `max_depth` as `min_depth` and change `max` to `min`: `min_depth(build_tree([1, 2]))` gives 1, but the only leaf (2) is at depth 2. An empty side is not a leaf: when one child is `None`, use the other side.
- Replace the window with a parent-only check, `valid(node.left, -math.inf, node.val)` and `valid(node.right, node.val, math.inf)`, then try `is_valid_bst(build_tree([5, 4, 6, None, None, 3, 7]))`: `True`, although the 3 sits in 5's right subtree.
- Ask which side duplicates go. If the problem says left ≤ node < right, check `low < node.val <= high` with the same recursion: `[2, 2]` becomes valid and `[2, None, 2]` stays invalid.

**BFS by level.** A queue visits nodes in order of depth. The one trick for grouping: at the start of a round the queue holds exactly one level, so `len(queue)` is that level's size.

```text
tree [3, 9, 20, None, None, 15, 7]:   queue [3] -> level [3];   [9, 20] -> level [9, 20];   [15, 7] -> level [15, 7]
each popped node puts its children at the BACK of the queue, behind the rest of the current level
```

```python
def level_order(root):
    levels, queue = [], deque([root] if root else [])   # STATE + INIT: queue = one level, left to right
    while queue:
        level = []
        for _ in range(len(queue)):           # snapshot: exactly the nodes of this level
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)       # STEP: children wait behind this level
            if node.right:
                queue.append(node.right)
        levels.append(level)                  # RECORD: one finished level
    return levels                             # RETURN


def right_side_view(root):                    # top-down DFS: the depth goes down
    view = []
    def dfs(node, depth):
        if node is None:
            return
        if depth == len(view):                # the first node to reach this depth
            view.append(node.val)
        dfs(node.right, depth + 1)            # right first, so it claims the level
        dfs(node.left, depth + 1)
    dfs(root, 0)
    return view


print(level_order(build_tree([3, 9, 20, None, None, 15, 7])))    # [[3], [9, 20], [15, 7]]
print(right_side_view(build_tree([1, 2, 3, None, 5, None, 4])))  # [1, 3, 4]
print(right_side_view(build_tree([1, 2, 3, 4])))                 # [1, 3, 4]  (4 is visible: nothing to its right)
```

**Try it**
- Replace `for _ in range(len(queue)):` with `while queue:`: the first tree becomes one level, `[[3, 9, 20, 15, 7]]`. The children joined the round that was still running.
- Print `len(queue)` at the top of each round of `level_order`: 1, 2, 2, the level sizes.
- In `right_side_view`, recurse left before right: `[1, 2, 3, None, 5, None, 4]` now gives `[1, 2, 5]`, the view from the *left*.

### Watch it work

The top-down windows of `is_valid_bst`, printed on the way down. Each window sits inside its parent's, and one broken node stops the walk.

```python
def trace_windows(root):
    def valid(node, low, high, depth):
        if node is None:
            return True
        ok = low < node.val < high
        print(f"{'    ' * depth}{node.val} must be in ({low}, {high}): {'ok' if ok else 'BROKEN'}")
        return ok and valid(node.left, low, node.val, depth + 1) and valid(node.right, node.val, high, depth + 1)
    return valid(root, -math.inf, math.inf, 0)


print(trace_windows(build_tree([5, 1, 7, None, None, 4, 8])))
```

**Try it**
- Delete `ok and` from the return line: the 4 is still printed as BROKEN, yet the answer becomes `True`. A node's own check must be part of what it returns.
- Run `trace_windows(build_tree([5, 1, 7, None, None, 6, 8]))`: every line is ok, and 6's window is (5, 7).
- Run `trace_windows(build_tree([2, 2]))`: the second line is `2 must be in (-inf, 2): BROKEN`. Equal to a bound counts as outside.

### Where it goes wrong

1. **Returning what you should record, or counting the wrong thing.** The parent can extend only one arm: return `1 + max(left, right)` and *record* `left + right`. Returning both arms counts paths that fork, and recording `left + right + 1` counts nodes where the problem counts edges (`[1, 2, 3]` gives 3 instead of 2).
2. **`UnboundLocalError` on the global.** Assigning `best = ...` inside a nested function makes `best` local: add `nonlocal best` (appending to a list needs no `nonlocal`).
3. **Checking only parent and child in a BST.** `[5, 4, 6, None, None, 3, 7]` passes a parent-only check. Pass the window `(low, high)` down instead.
4. **The wrong neutral value.** Max Path Sum with `best = 0` answers 0 for `[-3]` (should be -3): start at `-math.inf`. In Balanced, an empty subtree has height 0; -1 means "unbalanced".
5. **A leaf is not `None`.** Testing `remaining == 0` when you reach `None` makes `[1, 2]` with target 1 succeed through 1's empty right side, and min depth as `1 + min(left, right)` gives 1 instead of 2 on `[1, 2]`. Test leaves explicitly.
6. **Skipping a call that also records.** `if uni(node.left) and uni(node.right):` short-circuits, so Count Univalue Subtrees on `[1, 2, 3, 4]` never visits 3 and answers 1 instead of 2; a Longest Univalue Path that recurses only into children with the same value answers 0 instead of 1 on `[1, 2, None, 2]`. Call both children first, store the results, then combine.
7. **Shared state without the undo.** `paths.append(path)` stores the *same* list again and again (append `path[:]`, and `path.pop()` on the way back); Path Sum III without `seen[prefix] -= 1` lets a sibling see your prefix sums (`[0, 1, 2]`, target 1, gives 3 instead of 2).
8. **Forgetting to re-attach.** A function that returns the new root of a subtree must be called as `node.left = f(node.left, ...)`; calling `f(node.left, key)` alone throws the new subtree away (deleting 2 from `[5, 3, 6, 2, 4, None, 7]` returns the tree unchanged).
9. **Values instead of nodes.** LCA, cousins and "is it the same node" compare identity: `node is p`. An `lca` that compares values answers 1 instead of 3 on `[1, 2, 3, None, None, 2]` with p = the lower 2 and q = 3: the *other* 2 answered for p.

### Edge cases to say out loud

Empty tree (`None`) · a single node · a chain (height = n, recursion depth!) · all values negative · duplicates (BST strictness; compare nodes by identity) · p is an ancestor of q · the answer does not pass through the root · values at the integer limits (use `math.inf` bounds, not a sentinel like `2**31 - 1` that a real value can equal).

```python
assert max_depth(None) == 0 and diameter(None) == 0 and is_valid_bst(None)
assert max_depth(build_tree([1])) == 1 and diameter(build_tree([1])) == 0
chain = build_tree([1, None, 2, None, 3, None, 4])       # every node has only a right child
assert max_depth(chain) == 4 and diameter(chain) == 3 and is_valid_bst(chain)
assert not is_valid_bst(build_tree([2, 2]))              # duplicates break the strict order
assert is_valid_bst(build_tree([2 ** 31 - 1]))           # math.inf bounds never collide with values
assert level_order(None) == [] and right_side_view(None) == []
print("edge cases pass")
```

**Try it**
- Predict, then check: `is_valid_bst(build_tree([1, None, 1]))` is `False`. An equal value may not sit on the right either.
- Build a 10 000-node chain: `deep = node = TreeNode(0)`, then `for i in range(1, 10_000): node.right = TreeNode(i); node = node.right`. `max_depth(deep)` raises `RecursionError`; the explicit-stack versions in the Variations handle it.
- What is the diameter of the "V" `build_tree([1, 2, 3, 4, None, None, 5])`? Write the assert first: 4 (the path 4-2-1-3-5).

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Bottom-up value** | return a fact about the subtree; combine the two children | 104, 226, 110 |
| **Return ≠ record** | return one arm; record the path that bends here | 543, 124, 687 |
| **Sentinel, state or tuple return** | return -1 ("failed below"), a state (needs / covered / camera) or a tuple (depth, node) | 110, 968, 865 |
| **Top-down arguments** | pass a running max (and min), a window, a remaining sum, a depth, a parent | 1448, 1026, 98, 112, 404, 993, 199 |
| **Path state, with undo** | a shared path (copy it at a matching leaf) or a counter of prefix sums on the root path (the counter from [Prefix Sums](#s04)); undo it on the way back | 113, 437 |
| **Found below me** | return `p`/`q`/LCA/`None`; a hit from both sides means "it's me" (if a target may be missing, count the hits) | 236, 1644 |
| **BST: compare and go one way** | a single O(h) descent, no recursion needed | 235 (and BST insert/search) |
| **Rebuild and return the subtree** | every call returns the new root of its subtree; the parent re-attaches it | 450, 701, 1110 |
| **Explicit stack; inorder = sorted** | a lazy inorder generator with a counter or a `prev` node; bottom-up = preorder reversed, a dict for the return values; 272: two lazy iterators, predecessors and successors of the target | 94, 543, 230, 99, 272 |
| **BFS by level** | a queue plus the `len(queue)` snapshot | 102, 199 |
| **Tree as a graph** | record every node's parent, then BFS over left, right *and* parent ([Graphs I](#s17)) | 863 |
| **Coordinates** | DFS carrying `(row, col)`, bucket by column, sort | 987 |
| **Build or encode a tree** | preorder + inorder index map; preorder with `#` for `None`; a stack indexed by depth | 105, 297, 428, 1028, 572 |
| **Two trees at once** | recurse on pairs `(a, b)` | 100, 101, 572 |

**Return one arm and record the bend (124); return two facts at once (865).** Max Path Sum has the skeleton of Diameter, but the arms are sums, and a negative arm is dropped (clipped to 0) because a path doesn't have to use it. Subtree with All the Deepest Nodes needs two facts from each child, how deep its deepest leaf is *and* which node holds all of them, so it returns a tuple. (Balanced sends "this subtree already failed" up the height channel as -1, the same idea with one number.)

```python
def max_path_sum(root):
    best = -math.inf                          # not 0: an all-negative tree still has an answer
    def gain(node):                           # best sum going DOWN from node along one side
        nonlocal best
        if node is None:
            return 0
        left = max(gain(node.left), 0)        # a negative arm is simply left out
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)   # RECORD: the path that bends at node
        return node.val + max(left, right)    # RETURN: only one arm continues up
    gain(root)
    return best


def subtree_with_all_deepest(root):
    def deep(node):                           # UP: (depth of the deepest leaf below, answer node)
        if node is None:
            return 0, None
        (ld, ln), (rd, rn) = deep(node.left), deep(node.right)
        if ld != rd:                          # the deeper side holds all the deepest leaves
            return (ld + 1, ln) if ld > rd else (rd + 1, rn)
        return ld + 1, node                   # deepest leaves on both sides: I hold them all
    return deep(root)[1]


print(max_path_sum(build_tree([-10, 9, 20, None, None, 15, 7])), max_path_sum(build_tree([-3])))   # 42 -3
print(tree_to_list(subtree_with_all_deepest(build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]))))   # [2, 7, 4]
```

**Try it**
- Remove both `max(..., 0)` clips and try `max_path_sum(build_tree([2, -1]))`: 1 instead of 2. Without the clip the path is forced to take the -1 arm.
- Start with `best = 0`: `[-3]` now answers 0, the sum of a path that doesn't exist.
- Predict, then run `subtree_with_all_deepest` on `build_tree([1, 2, 3])`: the whole tree `[1, 2, 3]` (the deepest leaves sit on both sides of the root). On `build_tree([0, 1, 3, None, 2])`: `[2]` (a single deepest leaf is its own answer).

**Lowest common ancestor (236, 235).** Ask every subtree one question, "which of p and q do you contain?", and let the answer be a single node: `None` (neither), `p` or `q` (that one), or the LCA itself (both, already resolved below). The first node that hears a non-`None` answer from *both* sides is where the two paths split. This contract assumes both targets are in the tree. In a BST you don't need to search at all: compare values and walk down one path.

```text
              3               lca(5, 1): 3 hears "5" from the left and "1" from the right:
            /   \                        both sides answered, so 3 is the split point
           5     1
          / \   / \           lca(5, 4): the call on 5 returns 5 at once (it IS p);
         6   2 0   8                     the right side reports nothing, so 3 passes 5 up
            / \
           7   4
```

```python
def lca(root, p, q):                          # returns p, q, their LCA, or None for this subtree
    if root is None or root is p or root is q:
        return root                           # found one (or nothing): report it up
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root                           # one target on each side: I am the split
    return left or right                      # pass up whatever was found


def lca_bst(root, p, q):                      # BST: compare values, walk ONE path down
    lo, hi = min(p.val, q.val), max(p.val, q.val)
    node = root
    while node:
        if hi < node.val:
            node = node.left                  # both targets are smaller
        elif lo > node.val:
            node = node.right                 # both are larger
        else:
            return node                       # lo <= node.val <= hi: they split here


def find_node(root, val):                     # helper: the node holding val
    if root is None or root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


t = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(lca(t, find_node(t, 5), find_node(t, 1)).val, lca(t, find_node(t, 5), find_node(t, 4)).val)   # 3 5
b = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
print(lca_bst(b, find_node(b, 2), find_node(b, 8)).val, lca_bst(b, find_node(b, 3), find_node(b, 5)).val)   # 6 4
```

**Try it**
- Add `print(root.val)` right after the base-case `if` in `lca`, rerun the cell, then call `lca(t, find_node(t, 5), find_node(t, 4))`: only 3, 1, 0 and 8 are printed. Nothing below 5 is visited: the call on 5 returns at once, and since nobody else reports anything, 5 travels up as the answer.
- Ask about a node that isn't in the tree: `lca(t, find_node(t, 5), TreeNode(10)).val` is 5, a wrong answer, because the early return assumed both targets exist. If a target may be missing (1644), don't return early: visit everything, count the hits, and answer only if the count is 2.
- In `lca_bst`, change `hi < node.val` to `hi <= node.val` and ask for 2 and 0: you get 0 instead of 2. When a target *is* the node, the node is the answer (a node counts as its own ancestor).

**Facts that ride down the path (113, 437).** Path Sum II carries the remaining sum down as an argument and keeps ONE list for the current path: append on the way down, pop on the way back, copy it only at a matching leaf. Path Sum III counts paths that may start anywhere: keep a counter of the prefix sums on the current root path (the trick from [Prefix Sums](#s04)); a path ending here sums to the target exactly when `prefix - target` was a prefix higher up. The counter is shared, so undo your entry on the way back.

```python
def path_sum_all(root, target):
    paths, path = [], []
    def dfs(node, remaining):
        if node is None:
            return
        path.append(node.val)                 # STEP: going down, extend the path
        remaining -= node.val
        if node.left is None and node.right is None:
            if remaining == 0:
                paths.append(path[:])         # RECORD a COPY: path keeps changing
        else:
            dfs(node.left, remaining)
            dfs(node.right, remaining)
        path.pop()                            # FIX: coming back up, undo
    dfs(root, target)
    return paths


def path_sum_iii(root, target):
    seen = Counter({0: 1})                    # prefix sums on the current root path
    def dfs(node, prefix):
        if node is None:
            return 0
        prefix += node.val
        count = seen[prefix - target]         # downward paths that end here
        seen[prefix] += 1                     # STEP: join the path ...
        count += dfs(node.left, prefix) + dfs(node.right, prefix)
        seen[prefix] -= 1                     # FIX: ... and leave it on the way back up
        return count
    return dfs(root, 0)


t = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
print(path_sum_all(t, 22))                                                  # [[5, 4, 11, 2], [5, 8, 4, 5]]
print(path_sum_iii(build_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]), 8))   # 3
```

**Try it**
- Replace `paths.append(path[:])` with `paths.append(path)`: `[[], []]`. Both entries are the same list object, emptied by the pops on the way back.
- Delete `path.pop()`: the sums are still checked correctly (`remaining` travels as an argument), but the paths keep stale nodes: the first answer becomes `[5, 4, 11, 7, 2]`.
- Delete `seen[prefix] -= 1` and try `path_sum_iii(build_tree([0, 1, 2]), 1)`: 3 instead of 2. The prefix 1 from the left branch is still in the counter when the right branch asks.

**Explicit stacks, and inorder is sorted (94, 230, 99).** Preorder, inorder and postorder are one walk; they differ only in *when* you write the node down. The recursion keeps a hidden stack of nodes waiting for you to come back, and you can keep it yourself. Written as a generator, the inorder walk becomes a lazy iterator: `yield` hands out one node and pauses until the caller asks for the next. On a BST that walk is sorted: Kth Smallest stops after k nodes, and Recover BST compares each node with the one before it. Two swapped values make the sorted walk dip once if they were neighbours, twice if far apart (`1 5 3 4 2 6` dips at 5 > 3 and at 4 > 2): swap the bigger value of the first dip with the smaller value of the last. Finally, any bottom-up recursion becomes a loop, which answers "what about depth 10⁵?": an iterative preorder (pop a node, push its children) puts every parent before its children, so the reversed preorder puts every child before its parent, and a dict replaces the return values.

```text
            1            preorder  (node, left, right):  1 2 4 5 3 6    node BEFORE its children
          /   \          inorder   (left, node, right):  4 2 5 1 3 6    node BETWEEN them
         2     3         postorder (left, right, node):  4 5 2 6 3 1    node AFTER them
        / \     \        (iterative postorder = node-right-left preorder, reversed)
       4   5     6
```

```python
def inorder_nodes(root):                      # yields the nodes in inorder, lazily
    stack, node = [], root
    while node or stack:                      # both: a right subtree may still be pending
        while node:                           # slide down the left edge, leaving breadcrumbs
            stack.append(node)
            node = node.left
        node = stack.pop()                    # its left side is done: hand it out
        yield node
        node = node.right                     # then do its right subtree the same way


def kth_smallest(root, k):
    for i, node in enumerate(inorder_nodes(root), 1):
        if i == k:
            return node.val                   # stop early: the rest is never visited


def recover_bst(root):
    first = second = prev = None
    for node in inorder_nodes(root):
        if prev and prev.val > node.val:      # a dip in what should be increasing
            if first is None:
                first = prev                  # the bigger value of the FIRST dip
            second = node                     # the smaller value of the LAST dip
        prev = node
    first.val, second.val = second.val, first.val


def diameter_iterative(root):
    order, stack = [], [root] if root else []
    while stack:                              # preorder: every parent before its children
        node = stack.pop()
        order.append(node)
        stack.extend(c for c in (node.left, node.right) if c)
    height, best = {None: 0}, 0
    for node in reversed(order):              # reversed: every child before its parent
        left, right = height[node.left], height[node.right]
        best = max(best, left + right)
        height[node] = 1 + max(left, right)   # the dict plays the return value
    return best


t = build_tree([1, 2, 3, 4, 5, None, 6])
print([n.val for n in inorder_nodes(t)], diameter_iterative(t), diameter(t))   # [4, 2, 5, 1, 3, 6] 4 4
print(kth_smallest(build_tree([5, 3, 6, 2, 4, None, None, 1]), 3))           # 3
bst = build_tree([3, 1, 4, None, None, 2])
recover_bst(bst)
print(tree_to_list(bst))                                                      # [2, 1, 4, None, None, 3]
```

**Try it**
- In `inorder_nodes`, move `yield node` up into the `while node:` loop, right after the push: the first printed list becomes `[1, 2, 4, 5, 3, 6]`, the preorder. Handing a node out on arrival is preorder; handing it out once its left side is done is inorder.
- Add `print(node.val)` after `stack.append(node)` and call `kth_smallest(build_tree([5, 3, 6, 2, 4, None, None, 1]), 1)`: only 5, 3, 2, 1 are ever pushed. The walk stops as soon as the answer is known: O(h + k).
- Make `recover_bst` stop at the first dip (`break` right after `second = node`) and repair `build_tree([4, 5, 6, 1, 3, 2])`, where 2 and 5 were swapped far apart: it swaps 5 with 3, and the inorder becomes `[1, 3, 5, 4, 2, 6]` instead of `[1, 2, 3, 4, 5, 6]`.
- On the 10 000-node chain from the edge cases, `diameter_iterative(deep)` is 9999 while `diameter(deep)` raises `RecursionError` (`sys.setrecursionlimit(30_000)` also lets it through; set it back to 1000 afterwards). Loop over `order` instead of `reversed(order)` and you get `KeyError`: a parent asks for a child's height before the child has one.

**Rebuild and return the subtree (450), and the tree as a graph (863).** When a call may *replace* its subtree (delete, insert, trim), its contract is "return the new root of my subtree", and the parent re-attaches whatever comes back: `node.left = delete(node.left, key)`. When the question looks *up* as well as down ("all nodes at distance k from the target"), a parent pointer is just one more edge: remember every node's parent in one pass, then BFS outwards from the target over left, right and parent, one ring per step.

```python
def delete_bst(node, key):                    # returns the new root of this subtree
    if node is None:
        return None
    if key < node.val:
        node.left = delete_bst(node.left, key)      # re-attach whatever comes back
    elif key > node.val:
        node.right = delete_bst(node.right, key)
    else:
        if node.left is None:
            return node.right                       # 0 or 1 child: it takes my place
        if node.right is None:
            return node.left
        succ = node.right                           # 2 children: copy the successor in ...
        while succ.left:
            succ = succ.left
        node.val = succ.val
        node.right = delete_bst(node.right, succ.val)   # ... and delete it below
    return node


def distance_k(root, target, k):
    parent, stack = {root: None}, [root]
    while stack:                                    # one pass: remember every node's parent
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    seen, ring = {target}, [target]
    for _ in range(k):                              # BFS rings over left, right AND parent
        nxt = []
        for node in ring:
            for nb in (node.left, node.right, parent[node]):
                if nb and nb not in seen:
                    seen.add(nb)
                    nxt.append(nb)
        ring = nxt
    return [n.val for n in ring]


print(tree_to_list(delete_bst(build_tree([5, 3, 6, 2, 4, None, 7]), 3)))   # [5, 4, 6, 2, None, None, 7]
t = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(sorted(distance_k(t, find_node(t, 5), 2)))                            # [1, 4, 7]
```

**Try it**
- In `delete_bst`, call `delete_bst(node.left, key)` without `node.left = ...` and delete 2 from `[5, 3, 6, 2, 4, None, 7]`: the tree comes back unchanged. The new subtree was returned and thrown away.
- In `distance_k`, drop the `seen` check: the k = 2 answer becomes `[1, 4, 5, 5, 5, 7]`. The walk goes back to the target, and three different two-step paths lead there.
- Leave out the parent edge (`for nb in (node.left, node.right)`): only `[4, 7]`. The 1 is two steps away *up and over*, through 3.

**Build a tree from its traversals (105) and serialize it (297).** Preorder says *who* the root is (the first unused value); inorder says *how many* nodes are on its left (everything before the root). A dict finds the root's inorder position in O(1), and one iterator walks preorder, because building left-then-right uses preorder in exactly its own order. To *store* a tree, preorder alone is ambiguous, but preorder with `#` for every missing child is complete: each `#` says "this branch stops here", so the reader can replay the walk.

```text
 preorder = [3 | 9 | 20, 15, 7]      the next unused preorder value is the root: 3
 inorder  = [9 | 3 | 15, 20, 7]      left of 3 in inorder: [9]  -> left subtree; [15, 20, 7] -> right
 serialize [1, 2, 3, None, None, 4, 5]:   1,2,#,#,3,4,#,#,5,#,#   (# = "nothing here")
```

```python
def build_from_pre_in(preorder, inorder):
    where = {v: i for i, v in enumerate(inorder)}     # value -> inorder index (values unique)
    next_root = iter(preorder)                        # roots come out in preorder order
    def make(lo, hi):                                 # builds the subtree that owns inorder[lo:hi]
        if lo >= hi:
            return None
        root = TreeNode(next(next_root))
        mid = where[root.val]
        root.left = make(lo, mid)                     # left FIRST: it uses the next preorder values
        root.right = make(mid + 1, hi)
        return root
    return make(0, len(inorder))


def serialize(root):                                  # preorder, "#" where a branch ends
    if root is None:
        return "#"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"


def deserialize(data):
    tokens = iter(data.split(","))                    # one cursor shared by every call
    def read():
        token = next(tokens)
        if token == "#":
            return None
        node = TreeNode(int(token))
        node.left = read()                            # consumes exactly the left subtree's tokens
        node.right = read()
        return node
    return read()


print(tree_to_list(build_from_pre_in([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])))   # [3, 9, 20, None, None, 15, 7]
s = serialize(build_tree([1, 2, 3, None, None, 4, 5]))
print(s, tree_to_list(deserialize(s)))        # 1,2,#,#,3,4,#,#,5,#,# [1, 2, 3, None, None, 4, 5]
```

**Try it**
- Print `serialize(build_tree([1, 2]))` and `serialize(build_tree([1, None, 2]))`: `1,2,#,#,#` and `1,#,2,#,#`. Strip the `#`s and both read `1,2`: the markers are what tell a left child from a right one.
- `serialize(None)` is `"#"` and `deserialize("#")` is `None`: the empty tree round-trips too.
- Build from `preorder=[1, 2]` with `inorder=[2, 1]`, then with `inorder=[1, 2]`: `[1, 2]` versus `[1, None, 2]`. Same preorder; inorder decides the side.
- Swap the two recursive lines in `make` (right subtree first): the build hands preorder values to the wrong subtrees and stops with `StopIteration`, asking for more roots than there are.

**Coordinates (987).** Give every node a position on graph paper: the root at (row 0, col 0), a left child at (row + 1, col − 1), a right child at (row + 1, col + 1). Once each node carries its coordinates, the tree shape no longer matters: bucket by column, then sort each bucket by (row, value), so two nodes in the same cell come out smaller value first.

```python
def vertical_order(root):
    columns = defaultdict(list)               # col -> [(row, val), ...]
    def dfs(node, row, col):
        if node is None:
            return
        columns[col].append((row, node.val))
        dfs(node.left, row + 1, col - 1)
        dfs(node.right, row + 1, col + 1)
    dfs(root, 0, 0)
    return [[val for _, val in sorted(columns[c])] for c in sorted(columns)]


print(vertical_order(build_tree([3, 9, 20, None, None, 15, 7])))   # [[9], [3, 15], [20], [7]]
print(vertical_order(build_tree([1, 2, 3, 4, 6, 5, 7])))           # [[4], [2], [1, 5, 6], [3], [7]]
```

**Try it**
- Sort each column by value only (`sorted(columns[c], key=lambda rv: rv[1])`) and try `build_tree([5, 1, 9, None, 3])`: column 0 becomes `[3, 5]`, but 5 is above 3. The row decides first; the value only breaks ties.
- Print `dict(columns)` before the `return` for the second tree: column 0 holds `(0, 1), (2, 6), (2, 5)`. 6 and 5 share a grid cell, so the sort uses their values.
- Predict `vertical_order(build_tree([1, 2, 3]))` before running: `[[2], [1], [3]]`, one node per column.

<details><summary>Binary Tree Cameras (968): a state per node</summary>

Each subtree reports one of three states to its parent: "needs" (dark), "covered" (lit from below, no camera of its own) or "camera". `None` reports "covered", so leaves report "needs" and never hold a camera: a camera on the parent covers the leaf, the parent and the parent's other neighbours. A node takes a camera exactly when a child "needs" one, is "covered" when a child has a camera, and otherwise "needs". If the root still "needs" at the end, add one camera for it.

</details>

### Your turn: Maximum Difference Between Node and Ancestor

*Return the largest `|a.val - b.val|` where `a` is an ancestor of `b`.* `[8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13] → 7` (8 and 1) · `[1, None, 2, None, 0, 3] → 3` (0 and 3)

Answer the four contract questions on paper first, then open the answers.

<details><summary>The contract</summary>

**Down:** the smallest and the largest value on the path above the node. **Up:** the widest gap on any path below. **Record:** nothing, the root's return value is the answer. **Edges:** `None` returns `hi - lo` (its path is finished); the root starts with `lo = hi = root.val`.

</details>

Now write it in the cell below and run the cell; the checker tests the examples and 300 random trees against a brute force.

```python
def max_ancestor_diff(root):
    # write the contract first: what comes DOWN, what goes UP, what is recorded, what None returns
    return None


def check_max_ancestor_diff(fn):
    if fn(build_tree([1, None, 2])) is None:
        print("not written yet: fill in max_ancestor_diff and run this cell again")
        return
    for values, want in [([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], 7), ([1, None, 2, None, 0, 3], 3)]:
        got = fn(build_tree(values))
        print(("ok   " if got == want else "FAIL ") + f"{values} -> {got} (expected {want})")
    below = lambda n: [] if n is None else [n.val] + below(n.left) + below(n.right)
    brute = lambda n: 0 if n is None else max([abs(n.val - v) for v in below(n)] + [brute(n.left), brute(n.right)])
    rng = random.Random(0)                    # brute: every node against every node below it
    for _ in range(300):
        values = [rng.randint(0, 20)] + [None if rng.random() < 0.25 else rng.randint(0, 20) for _ in range(rng.randint(1, 11))]
        if fn(build_tree(values)) != brute(build_tree(values)):
            print(f"FAIL on random tree {values}: expected {brute(build_tree(values))}")
            return
    print("all random checks pass")


check_max_ancestor_diff(max_ancestor_diff)
```

**Try it**
- Write your solution, run the cell and read the checker's lines. If a random tree fails, draw it and trace your function on it.
- If you pass only the *largest* value down, the second example fails: 3's widest partner above it is the smaller value 0. A node needs both the smallest and the largest value above it.
- Both contracts below work: report from `None` (as in the answer), or record `best = max(best, abs(node.val - lo), abs(node.val - hi))` at every node. Write the other one and run the checker again.

<details><summary>One solution</summary>

```py
def max_ancestor_diff(root):
    def dfs(node, lo, hi):                    # DOWN: the smallest and largest value above node
        if node is None:
            return hi - lo                    # a finished path reports its widest pair
        lo, hi = min(lo, node.val), max(hi, node.val)
        return max(dfs(node.left, lo, hi), dfs(node.right, lo, hi))   # UP: the best below
    return dfs(root, root.val, root.val)
```

</details>

### Say it in the interview

> "I'll write one recursive function and state its contract: given a node and what comes down from its parent, it returns what the parent needs about its subtree, and it records the answer outside when the answer can sit at any node; an empty tree returns a neutral value. Correctness by induction: if my children's calls are right for their subtrees, combining them is right for mine, and every candidate answer is seen at exactly one node (for a path, its highest node), where I record it. One visit per node: O(n) time, O(h) stack, O(n) on a chain."

Before typing, say the contract out loud, then point at the base case, the line that combines the children and the line that records. Be ready for the follow-ups:

- *Depth 10⁵?* Raise the recursion limit, or turn the recursion into the reversed-preorder loop (`diameter_iterative`).
- *Return the path itself, not its length?* Remember the node where the best bend happened, then walk down its taller arm on each side.
- *p or q may be missing?* Don't return early; count the hits and answer only if both were found (1644).
- *The tree is a BST?* Compare and go one way: O(h), one path.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Balanced Binary Tree | `trees/balanced_binary_tree.py` | return the height, or -1 as soon as any subtree is unbalanced; the -1 travels up |
| Binary Tree Cameras | `trees/binary_tree_cameras.py` | post-order states needs/covered/camera; `None` is covered; camera only when a child needs one; check the root |
| Binary Tree Inorder Traversal | `trees/binary_tree_inorder_traversal.py` | the stack holds the left edge: push lefts, pop = visit, go right; loop while node or stack |
| Binary Tree Level Order Traversal | `trees/binary_tree_level_order_traversal.py` · `practice/simple/26_binary_tree_level_order_traversal.py` | BFS; `len(queue)` at the start of a round is the size of one level |
| Binary Tree Maximum Path Sum | `trees/binary_tree_maximum_path_sum.py` | record val + left + right; return val + max(left, right); clip negative arms to 0; best starts at -inf |
| Binary Tree Right Side View | `trees/binary_tree_right_side_view.py` | right-first DFS with depth; record when depth == len(view) |
| Closest Binary Search Tree Value II | `trees/closest_binary_search_tree_value_ii.py` | two lazy inorder stacks (values ≤ target, values > target); merge k times by distance |
| Construct Binary Tree from Preorder and Inorder Traversal | `trees/construct_binary_tree_from_preorder_and_inorder_traversal.py` | preorder gives the root, an inorder index map splits left/right; build left first with one preorder pointer |
| Count Good Nodes in Binary Tree | `trees/count_good_nodes_in_binary_tree.py` | pass the path maximum down; good iff val ≥ path max |
| Cousins in Binary Tree | `trees/cousins_in_binary_tree.py` | carry (parent, depth) down; cousins = same depth, different parent |
| Diameter of Binary Tree | `trees/diameter_of_binary_tree.py` · `practice/simple/30_diameter_of_binary_tree.py` | return the height; record left + right (edges) at every node |
| Invert Binary Tree | `trees/invert_binary_tree.py` | swap the two children at every node (tuple swap); pre-order, post-order or BFS all work (in-order swaps one side twice) |
| Kth Smallest Element in a BST | `trees/kth_smallest_element_in_a_bst.py` · `practice/simple/28_kth_smallest_element_in_a_bst.py` | inorder is sorted: iterative inorder, stop at the k-th pop |
| Lowest Common Ancestor of a Binary Tree | `trees/lowest_common_ancestor_of_a_binary_tree.py` | return p/q/LCA/None per subtree; hits from both sides make this node the LCA (both targets guaranteed) |
| Lowest Common Ancestor of a BST | `trees/lowest_common_ancestor_of_a_bst.py` · `practice/simple/29_lowest_common_ancestor_of_a_bst.py` | walk down while both values are on one side; the first node between them (inclusive) is the LCA |
| Maximum Depth of Binary Tree | `trees/maximum_depth_of_binary_tree.py` | 1 + max(depth(left), depth(right)); `None` is 0 |
| Path Sum | `trees/path_sum.py` | pass the remaining sum down; test it only at a leaf |
| Path Sum II | `trees/path_sum_ii.py` | one shared path: append on entry, pop on exit, copy at a matching leaf |
| Recover a Tree From Preorder Traversal | `trees/recover_a_tree_from_preorder_traversal.py` | stack of ancestors; dash count = depth; pop until len(stack) == depth; fill left before right |
| Recover Binary Search Tree | `trees/recover_binary_search_tree.py` | inorder dips: first = prev of the first dip, second = node of the last dip; swap the values |
| Same Tree | `trees/same_tree.py` | recurse on pairs: both None → True; one None or different values → False |
| Serialize and Deserialize Binary Tree | `trees/serialize_and_deserialize_binary_tree.py` | preorder with `#` for None; the reader replays the walk with one shared iterator |
| Serialize and Deserialize N-ary Tree | `trees/serialize_and_deserialize_n_ary_tree.py` | preorder "value, child count"; the reader builds exactly that many children |
| Subtree of Another Tree | `trees/subtree_of_another_tree.py` | serialize both with null markers and a delimiter; a subtree is a substring |
| Sum of Left Leaves | `trees/sum_of_left_leaves.py` | pass "I am a left child" down; add the leaves that have it |
| Symmetric Tree | `trees/symmetric_tree.py` | mirror(a, b): equal values, mirror(a.left, b.right) and mirror(a.right, b.left) |
| Validate Binary Search Tree | `trees/validate_binary_search_tree.py` · `practice/simple/27_validate_binary_search_tree.py` | pass an open window (low, high) down; left caps high, right raises low |
| Vertical Order Traversal of a Binary Tree | `trees/vertical_order_traversal_of_a_binary_tree.py` | DFS with (row, col); bucket by column; sort each bucket by (row, value) |

### Self-check

1. In Diameter, why is the value you return different from the value you record, and why does recording at every node find the best path?
<details><summary>Answer</summary>The parent can extend a path through only one of your arms (a path can't fork), so it needs <code>1 + max(left, right)</code>. The answer may bend at you and use both arms: <code>left + right</code>. Every path has exactly one highest node, where it is a left arm plus a right arm, so recording <code>left + right</code> at every node sees every path once.</details>

2. How do you decide what a recursive function returns?
<details><summary>Answer</summary>Ask what the <em>parent</em> needs to know about your subtree to do its own job. If it needs two facts (a depth and a node), return a tuple. If the problem's answer can sit at any node rather than at the root, return what the parent needs and record the answer on the side.</details>
