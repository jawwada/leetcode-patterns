# Companion code files: format

One file per problem at `companion/<topic>/<slug>.py`. Standard library only, no local imports. Running
`python3 companion/<topic>/<slug>.py` prints the brute force demo and then the optimal demo; the two demos
use the same inputs and must print the same lines. `python3 site/build_companion.py --check <file>...`
validates a file; `python3 site/build_companion.py` builds the artifact page from all of them.

## Layout (markers are mandatory, in this order; `# --- helpers ---` is optional)

```python
"""
<Title> (LeetCode <n>) - <Easy | Medium>
Chapter: <topic folder name>
Pattern: <the pattern line from site/problems.json>

<Problem statement in 2-4 lines, ending with one example: input -> output.>
"""
from collections import deque      # only what the file needs


# --- helpers ---
class TreeNode:                    # node classes, build_tree / tree_to_list, build_list / list_to_array ...
    ...


# --- brute force ---
def brute_force(nums):
    """One line: the idea and its complexity, e.g. 'Try every pair. O(n^2) time, O(1) space.'"""
    ...


# --- optimal ---
def two_sum(nums, target):         # a plain function named after the problem (a class for design problems)
    """One line: the idea and its complexity."""
    ...


# --- try the brute force ---
print(brute_force([2, 7, 11, 15], 9))   # -> [0, 1]
print(brute_force([3, 3], 6))           # -> [0, 1]


# --- try the optimal ---
print(two_sum([2, 7, 11, 15], 9))       # -> [0, 1]
print(two_sum([3, 3], 6))               # -> [0, 1]
```

## Python style: simple on purpose

The reader's Python is sketchy. The code exists to show the gist of the algorithm, not to be clever.

- Plain functions in snake_case, no type hints, no `class Solution`. A class only for design problems
  (LRU cache, trie, min stack ...) and for list/tree nodes.
- One idea per line. Write loops out: no list comprehensions beyond `[0] * n`, no generator expressions,
  no `lambda`, no ternary `a if c else b`, no walrus, no `*args`, no chained method calls, no slicing
  tricks beyond `a[i:j]` and `a[::-1]`, no `any(...)`/`all(...)` over a generator (write the loop and
  return early), no `setdefault`/`defaultdict`/`Counter` (use `if key not in d: d[key] = ...` and
  `d.get(key, 0) + 1`), no `zip` of three things, no nested functions except one recursive helper when
  recursion is the algorithm (give it explicit parameters, write it at top level in the same section).
- Allowed toolbox, with a short comment the first time it appears in a file: `deque` (popleft is O(1)),
  `heapq` (heappush / heappop keep the smallest at index 0), `sorted` / `.sort()`, `bisect` only in the
  binary search chapter, `math` for inf/ceil.
- Descriptive names (`left`, `right`, `count`, `best`, `seen`), not `l`, `r`, `c`.
- A short `#` comment on each key step (the step a reader would get wrong), not on every line.
- Each function at most about 25 lines. Brute force is the obvious method written clearly; optimal is the
  standard interview solution.
- Demos: 2 to 4 inputs, each a one-line `print(...)` followed by `# -> expected`. Trees and linked lists
  are built from Python lists with the helpers and printed back as lists. Design classes: a short
  sequence of operations with a print after each query. The brute force demo and the optimal demo use the
  same inputs in the same order and print exactly the same lines.

## Fundamentals files: `companion/fundamentals/<area>/<name>.py`

The data structure operations and classic algorithms (sorting, BFS/DFS, topological sort, union find,
Kruskal, Prim, Dijkstra, heap mechanics, KMP ...). Same simple style, but there is no brute force: one
algorithm section and one demo. Markers, in this order (`# --- helpers ---` optional):

```python
"""
<Title> - Fundamentals
Chapter: fundamentals/<area>
Key operations: <the 2-4 operations this file drills, comma separated>

<What the algorithm does and when you reach for it, 2-4 lines, ending with one example: input -> output.>
"""
import heapq


# --- helpers ---
...


# --- algorithm ---
def kruskal(n, edges):
    """One line: idea and complexity."""
    ...


# --- try it ---
print(kruskal(4, [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4)]))   # -> (7, [(0, 1, 1), (1, 2, 2), (2, 3, 4)])
```

A file may define several small functions when the topic is a set of operations (e.g. get / set / clear a
bit, or insert / search / delete in a BST); the demo then exercises each one with a print.
