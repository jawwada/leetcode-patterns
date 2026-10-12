# 100 Algorithms: entry format

Two books are built from the same 100 entries, in the rank order of `manifest.json`:
the **Pseudocode book** from `pseudo/NNN_slug.md`, the **Python book** from `python/NNN_slug.py`
(`NNN` = rank, zero padded to 3 digits). Titles, subtitles, topics and tiers live only in the
manifest; the build adds headings. Entry #1 (`pseudo/001_two_sum.md`, `python/001_two_sum.py`) is
the reference: match its voice, shape and density.

The reader knows the data structures and is preparing for a Google interview. They learn best from
a connected argument in a confident voice, with a visual or geometric picture of what the algorithm
does to the data. Their Python is sketchy, so the code is simple on purpose.

Run `python3 algorithms_100/check.py <rank> [<rank> ...]` (or `--batch N`, or no args for all). An
entry is done only when it prints `OK`.

## Pseudocode book entry: `pseudo/NNN_slug.md`

```markdown
---
rank: 1
slug: two_sum
---

<Paragraph: the problem, stated plainly with one tiny example. No label, no heading.>

<One or two paragraphs: the idea. When a natural brute force exists, one sentence names it and its
cost, then the insight that beats it. Describe the shape of the data and the motion of the
algorithm (what moves, what is kept, what is the invariant). Declarative sentences, no hedging.>

```text
<The picture: an ASCII diagram or a step-by-step trace of the algorithm on the example from the
first paragraph. 4 to 20 lines. Every number in it must be what the code actually produces.>
```

```pseudo
<The pseudocode, following the conventions below.>
```

<One closing paragraph: the cost with the one-line reason for it, the signals in a problem
statement that call for this algorithm, and the classic mistake.>

*Practice:* LC 1 Two Sum · LC 167 Two Sum II - Input Array Is Sorted · LC 15 3Sum
```

- No headings, no bold labels, no tables, no bullet lists inside the entry. Flowing paragraphs.
- Whole entry roughly 250 to 450 words of prose plus the two code blocks. One printed page is the
  target; two pages only for the big ones (designs, Dijkstra, text justification, ...).
- Use the manifest `brief` for scope: it names the variant, the edge cases and what to mention.
- Inline code uses backticks. Complexity in plain text: `O(n log n)`, `O(V + E)`.
- Cross references by rank: "the sift-down from #41". Only reference ranks that exist.
- *Practice:* line: 2 to 4 real LeetCode problems as `LC <number> <exact official title>`,
  separated by ` · `. Only problems you are certain of; the numbers and titles must match LeetCode.
- Allowed Unicode in code blocks: ← → ↑ ↓ ≤ ≥ ≠ ∞ × · … ² √ ⌊ ⌋ ✓ ✗ ▲ ▼ ● ○ and box drawing
  (─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼). Everything else ASCII. Every code-block line at most 80 characters.

### Pseudocode conventions

```pseudo
FUNCTION TwoSum(nums, target)
    seen ← empty map                       // value → index
    FOR i FROM 0 TO len(nums) - 1
        need ← target - nums[i]
        IF need IN seen
            RETURN [seen[need], i]
        seen[nums[i]] ← i
    RETURN empty list
```

- Keywords in capitals: `FUNCTION`, `CLASS`, `RETURN`, `IF`, `ELSE IF`, `ELSE`, `FOR`,
  `FOR EACH x IN c`, `WHILE`, `BREAK`, `CONTINUE`, `AND`, `OR`, `NOT`, `IN`.
- Blocks by 4-space indentation. No `END` lines, no colons at line ends, no braces.
- `FOR i FROM a TO b` is inclusive; `FOR i FROM b DOWNTO a`; `STEP k` when needed.
- Assignment `←`. Comparison `=`, `≠`, `<`, `≤`, `>`, `≥` (never `==`, `!=`, `<=`, `>=`).
  Arithmetic `+ - * /`, `floor(a / b)`, `a mod b`, `∞` and `-∞`. Literals `true`, `false`, `null`.
- Comments with `//`.
- Containers: `empty map`, `empty set`, `empty list`, `empty stack`, `empty queue`,
  `empty min-heap`, `empty max-heap`, `array of n zeros`, `array of n copies of x`.
  Operations method-style: `list.append(x)`, `stack.push(x)`, `stack.pop()`, `stack.top()`,
  `queue.enqueue(x)`, `queue.dequeue()`, `heap.push(x)`, `heap.pop()`, `heap.top()`, `set.add(x)`,
  `set.remove(x)`, `map[k] ← v`, `k IN map`, `len(x)`, `swap(a[i], a[j])`, `a[i..j]` (inclusive).
- Function names `CamelCase`; variables `snake_case` and the same names as the Python file, so the
  two books line up line by line. Design problems: `CLASS LRUCache` with indented `FUNCTION`s and
  `self.` fields.
- Usually 8 to 35 lines; design classes up to about 60. Several small functions are fine when the
  algorithm has parts (e.g. `SiftDown` + `Heapify`).

## Python book entry: `python/NNN_slug.py`

```python
"""
Two Sum - Hash Map of Complements

Given an array of integers and a target, return the indices of the two numbers
that add up to the target: [2, 7, 11, 15], target 9 -> [0, 1].
"""


# --- algorithm ---
def two_sum(nums, target):
    """Remember each value's index; look up target - x. O(n) time, O(n) space."""
    ...


# --- try it ---
print(two_sum([2, 7, 11, 15], 9))   # -> [0, 1]
```

- Docstring line 1 is exactly `<title> - <subtitle>` from the manifest (ASCII hyphen, spaces
  around it). Then a blank line, then the problem in 2 to 4 lines ending with one example
  `input -> output`. The build prints this paragraph above the code; the rest of the file is shown
  as code.
- Imports (only what is needed) come right after the docstring.
- Markers, in this order: `# --- helpers ---` (optional: node classes, build/print helpers),
  `# --- algorithm ---` (required), `# --- try it ---` (required).
- Every function has a one-line docstring: the idea and its complexity. If it does not fit in 80
  columns, use two or three lines.
- Demo: 2 to 5 lines, each `print(...)` followed by `# -> <exact expected output>`. Each print
  writes exactly one line. Plain statements (building inputs, calling methods on a design object)
  may sit between prints. The checker runs the file and compares the output line by line with the
  `# -> ` comments. Demos are deterministic (seed `random`, or print order-independent results).
- Every line at most 80 characters.

### Simple Python on purpose

- Plain functions in snake_case, no type hints. A class only for design problems (LRU cache, trie,
  median finder, ...) and for list or tree nodes.
- One idea per line. Write loops out: no list/set/dict comprehensions (`[0] * n` and
  `[[0] * m for ...]` style 2D init are the only exceptions; prefer a loop for 2D too), no generator
  expressions, no `lambda`, no ternary `a if c else b`, no walrus, no `*args`/`**kwargs`, no `any`/
  `all` over a generator, no `setdefault`/`defaultdict`/`Counter` (use `if key not in d: d[key] = ...`
  and `d.get(key, 0) + 1`), no chained method calls, no slicing tricks beyond `a[i:j]` and `a[::-1]`.
- No nested functions, except when recursion is the algorithm: then write ONE top-level recursive
  helper with explicit parameters next to the main function.
- Allowed toolbox, each with a short comment the first time it appears: `from collections import
  deque` (popleft is O(1)), `import heapq` (heappush / heappop keep the smallest at index 0),
  `sorted` / `.sort()` (a `key=` argument needs a named top-level function, not a lambda; sorting
  tuples is usually enough), `math` for inf/ceil/sqrt, `random` for randomized algorithms,
  `bisect` only in Binary Search entries (prefer a hand-written search anyway).
- Descriptive names (`left`, `right`, `count`, `best`, `seen`), not `l`, `r`, `c`.
- A short `#` comment on each key step (the step a reader would get wrong), not on every line.
- Functions about 25 lines at most; split helpers out when longer.
- The Python mirrors the pseudocode: same algorithm, same variable names, same order of steps.

## Correctness bar

- The Python is a correct, standard interview-quality implementation, tested beyond the demo
  (edge cases: empty input, one element, duplicates, negatives, ties) and, wherever a brute force
  exists, cross-checked against it on random inputs in a scratch file outside the repo.
- The pseudocode is the same algorithm as the Python; hand-executing it on the example gives the
  demo's answer.
- Every claim in the prose is true: complexities, invariants, "why it works" arguments, the trace
  numbers in the picture, LeetCode numbers and titles.
