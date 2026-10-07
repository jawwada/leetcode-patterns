## Backtracking

> Backtracking walks a decision tree that it never builds. One shared list, `path`, is the pencil line from the root to where you stand. At each node you **choose** an option (append), **explore** everything below it (recurse), then **un-choose** it (pop), so the next option starts from exactly the same place. Pruning rubs out a whole subtree the moment its beginning cannot work.

**Reach for it when** the problem says "return **all**" (subsets, combinations, permutations, partitions, boards, expressions), or asks whether something can be arranged under rules, and the input is small (n ≤ ~15, a 9×9 board, a grid of ~20 cells). Rough limits: 2^n is fine up to n ≈ 20, n! up to n ≈ 10. Tiny limits are the interviewer telling you that an exponential search is expected; "in how many ways" with a large n is DP or combinatorics, not search.

**In this repo:** `backtracking/` (15 problems) · bank: `practice/simple/36_palindrome_partitioning.py`, `practice/simple/37_combination_sum_ii.py`, `practice/simple/38_letter_combinations_of_a_phone_number.py`, `practice/simple/39_word_search.py`, `practice/simple/40_n_queens.py` · basics: `practice/simple/basics/backtracking/01_subsets.py`, `practice/simple/basics/backtracking/02_subsets_with_duplicates.py`, `practice/simple/basics/backtracking/03_combinations_n_choose_k.py`, `practice/simple/basics/backtracking/04_combination_sum.py`, `practice/simple/basics/backtracking/05_permutations.py`, `practice/simple/basics/backtracking/06_permutations_with_duplicates.py`, `practice/simple/basics/backtracking/07_generate_parentheses.py`

### The picture

```text
nums = [1, 2, 3]      a node is the current path;  an edge is "choose nums[i]" with i >= start

                              []                    record at EVERY node: 8 subsets
                    +1 /   +2 |      \ +3
                [1]          [2]          [3]       [3]: no index after it, a leaf
           +2 /     \ +3      | +3
         [1,2]       [1,3]  [2,3]
        +3 |
        [1,2,3]

the walk:  []  ->  [1]  ->  [1,2]  ->  [1,2,3]         choose:    path.append(x), then recurse
                           [1,2]  <-  [1,2,3]          un-choose: path.pop(), one edge back up
                  [1]  <-  [1,2]
                  [1]  ->  [1,3]  ->  ...              the next sibling starts from the same [1]
```

Every backtracking problem is this picture with different answers to **three questions**: **Q1** what is a partial solution (the path, plus a summary of it), **Q2** what are the choices here, **Q3** when is it complete?

Why it is fast enough: the brute force builds every *complete* candidate (all 2^n bitmasks, all n^n sequences, every grid walk of length L) and checks it only at the end. Backtracking checks the rules at every node, so a bad beginning is rejected **once**, together with every completion it would have had, and sharing one `path` makes each step O(1) instead of a list copy. The search stays exponential when the answer is exponential (there really are 2^n subsets to print), but a prefix stops costing anything the moment a check rejects it, so the earlier and sharper the check, the smaller the tree. Generate Parentheses is the ideal case: its checks are perfect, so it never enters a dead prefix.

**Complexity in words:** (nodes visited) × (work per node), plus the cost of copying each recorded answer; the extra space is the recursion depth. Name the size of the tree, then add "pruning makes it much smaller in practice":

| Search | Size of the search | Say it as |
|---|---|---|
| subsets | 2^n | "every item is in or out" |
| combinations of size k | C(n, k) leaves | "n choose k" |
| permutations | n! leaves | "n choices, then n − 1, then ..." |
| phone letters | ≤ 4^n leaves | "up to 4 letters per digit" |
| word search | O(m·n·3^L) | "any start cell, 4 first moves, then at most 3: the cell behind me is marked" |
| N-queens | ≤ n! leaves | "one queen per row, and a column is never reused" |
| generate parentheses | Catalan(n): 5 for n = 3, 42 for n = 5 | "only valid prefixes survive" |

### From idea to code

**The idea in one sentence:** *at each node, for every choice that is still allowed: choose it, explore below it, un-choose it; when the path is complete, record a copy.*

| Decision | Backtracking answer |
|---|---|
| **State**: what must I remember? | `path` (one shared list), where I am in the tree (`start` = first index still allowed, or `used[i]` flags), and a running summary that makes checks O(1): `remaining`, `opened`/`closed`, attack sets, marked cells |
| **Definition**: what exactly does each variable mean? | `path` = the choices on the way from the root to this node; `start` = the smallest index this node may pick; `remaining = target - sum(path)` |
| **Invariant**: what is true at the end of every step? | when `dfs` returns, every piece of state is exactly as it was when `dfs` was called: each append has its pop, each mark its unmark |
| **Step**: how does one choice change the state? | for each allowed choice: choose (append, mark) → explore (`dfs` on the smaller problem) → un-choose (pop, unmark), always in that order |
| **Record**: when is the answer updated? | when the path is complete: on entry for subsets (every node is an answer), at the leaf otherwise; append a **copy**, `path[:]` |
| **Init**: starting values | `result, path = [], []`, then `dfs(0)` (or `dfs(0, target)`, `dfs(0, 0)`) |
| **Return**: what comes back, and for "not found"? | `result` (maybe `[]`), a count, or `True` the moment one branch succeeds and `False` once every choice failed |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "the partial solution" | `path` (one list shared by every call) |
| "the choices at this level" | `for i in range(start, len(nums)):` |
| "this choice can't work" | `continue` (skip it) or `break` (sorted: every later choice is worse too) |
| "choose it" / "un-choose it" | `path.append(nums[i])` / `path.pop()` (plus `used[i] = True` / `False` when order matters) |
| "explore what follows" | `dfs(i + 1)` (each item at most once) or `dfs(i)` (it may be reused) |
| "state that undoes itself" | pass it as an argument: `dfs(i + 1, remaining - x)` |
| "complete: save it" | `result.append(path[:])`, a copy and never `path` itself |
| "found one, stop" | `if dfs(...): return True` inside the loop, `return False` after it |
| "how many ways" | `count += dfs(...)` inside the loop, `return count` after it |
| "stand on this cell" | `saved, board[r][c] = board[r][c], "#"` ... `board[r][c] = saved` |
| "same value as the sibling before" | `if i > start and nums[i] == nums[i - 1]: continue` (after sorting) |
| "twin not used yet" (permutations) | `if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]): continue` |
| "too few items left for the open slots" | `if len(nums) - i < k - len(path): break` |

Every solution in this section is this skeleton with the blanks filled in. The three questions land on fixed lines:

```text
def solve(data):
    result, path = [], []                    # STATE + INIT: the root is the empty path
    def dfs(pos, summary):                   # Q1: where am I, plus cheap facts about path
        if <complete>:                       # Q3, tested FIRST, before anything reads data[pos]
            result.append(path[:])           # RECORD a copy (subsets: record, but don't return)
            return
        for choice in <choices at pos>:      # Q2
            if <choice breaks a rule>:
                continue                     # or break: sorted, so every later choice is worse
            path.append(choice)              # STEP: choose      } shared state needs a mirror
            dfs(<next pos>, <new summary>)   #       explore     } line after the call;
            path.pop()                       # FIX: un-choose    } arguments undo themselves
    dfs(<first pos>, <starting summary>)     # INIT
    return result                            # RETURN (or True/False, or a count)
```

For each piece of state decide: **argument or shared?** An argument (`start`, `remaining`, `k`, `expr + s`, `rest + [v]`) is un-chosen automatically when the call returns, because the caller still holds its own value. Shared state (`path`, `used`, the attack sets, the board) needs a mirror line after the call.

| Problem | `dfs(...)` arguments | Choices | Complete when |
|---|---|---|---|
| Subsets | `start` | `i` in `range(start, n)` | every node |
| Combination Sum II | `start, remaining` | the same, sorted, skipping equal siblings | `remaining == 0` |
| Permutations | none (`used[]` is shared) | every unused `i` | `len(path) == n` |
| Phone letters | `i` | the letters of `digits[i]` | `i == len(digits)` |
| Palindrome Partitioning | `start` | each `end` whose piece `s[start:end]` is a palindrome | `start == len(s)` |
| Word Search | `r, c, k` (called from every cell) | 4 neighbours | `k == len(word)` |

The `start` index is how "order does not matter" becomes code: indices only increase along a path, so {1, 2} is built once as `[1, 2]` and never as `[2, 1]`. Permutations *are* the orders, so any unused item may come next, and `used[]` remembers which ones are taken. The order of the tagged lines is a decision too: subsets RECORD first, because a node is an answer before any child is tried; the FIX (pop) comes after the explore, or the children would never see the item.

```python
def subsets(nums):
    result, path = [], []                    # STATE + INIT: path = the choices from the root to here
    def dfs(start):                          # STATE: start = first index this node may still choose
        result.append(path[:])               # RECORD first: every node is a subset (append a copy)
        for i in range(start, len(nums)):    # the choices at this level
            path.append(nums[i])             # STEP (choose)
            dfs(i + 1)                       #   explore: only later indices, so no repeats
            path.pop()                       # FIX (un-choose): path is back to how this call found it
    dfs(0)                                   # INIT: the root may choose any index
    return result                            # RETURN


def combination_sum(candidates, target, reuse=False):   # LeetCode 40; reuse=True is LeetCode 39
    nums = sorted(candidates)                # equal values side by side, bigger ones later
    result, path = [], []                    # STATE + INIT
    def dfs(start, remaining):               # STATE: remaining = target - sum(path)
        if remaining == 0:                   # complete
            result.append(path[:])           # RECORD at the leaf
            return
        for i in range(start, len(nums)):
            if nums[i] > remaining:          # prune: too big, and every later number is too
                break
            if i > start and nums[i] == nums[i - 1]:
                continue                     # same value as its left sibling: same subtree
            path.append(nums[i])             # STEP (choose)
            dfs(i if reuse else i + 1, remaining - nums[i])   # explore; i: it may be taken again
            path.pop()                       # FIX (un-choose)
    dfs(0, target)                           # INIT
    return result                            # RETURN


def permute(nums):
    result, path = [], []                    # STATE + INIT
    used = [False] * len(nums)               # STATE: used[i] = nums[i] is already in path
    def dfs():
        if len(path) == len(nums):           # complete: every slot is filled
            result.append(path[:])           # RECORD
            return
        for i in range(len(nums)):           # no start index: order matters
            if used[i]:
                continue
            used[i] = True                   # STEP (choose): two pieces of shared state ...
            path.append(nums[i])
            dfs()                            #   explore
            path.pop()                       # FIX (un-choose): ... so two mirror lines
            used[i] = False
    dfs()                                    # INIT
    return result                            # RETURN


print(subsets([1, 2, 3]))                             # [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
print(combination_sum([10, 1, 2, 7, 6, 1, 5], 8))     # [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
print(combination_sum([2, 3, 6, 7], 7, reuse=True))   # [[2, 2, 3], [7]]
print(permute([1, 2, 3]))                             # [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
```

**Try it**
- Change `result.append(path[:])` to `result.append(path)` and run `subsets([1, 2])`: `[[], [], [], []]`. Four references to one list, which is empty again when the search ends.
- Delete the `path.pop()` in `subsets` and run `subsets([1, 2])`: `[[], [1], [1, 2], [1, 2, 2]]`. The subset `[2]` is gone and a 2 appears twice, because a sibling started from a dirty path.
- Change `dfs(i + 1)` to `dfs(start + 1)` in `subsets`: `subsets([1, 2, 3])` returns 16 lists, including `[1, 3, 3]` and `[3, 2]`. The next level must start after the item just chosen, not after this level's start.
- Delete `used[i] = False` in `permute` and run `permute([1, 2, 3])`: only `[[1, 2, 3]]` comes back, since every number stays "used" after its first trip.

### Watch it work

Each line is one event, indented by depth in the tree. Watch the two cuts, **break** (sorted, so nothing to the right can fit) and **skip** (a second `1` beside the first would rebuild `[1, 2]`), and every **un-choose** putting `path` back exactly as it was.

```python
def trace_combination_sum(candidates, target):
    nums, path = sorted(candidates), []
    print(f"nums={nums}  target={target}")
    def dfs(start, remaining, depth):
        pad = "    " * depth
        if remaining == 0:
            print(f"{pad}record {path}")
            return
        for i in range(start, len(nums)):
            if nums[i] > remaining:
                print(f"{pad}break: {nums[i]} > {remaining} left, and later numbers are no smaller")
                break
            if i > start and nums[i] == nums[i - 1]:
                print(f"{pad}skip {nums[i]}: same value as its left sibling")
                continue
            path.append(nums[i])
            print(f"{pad}choose {nums[i]}  path={path}  left={remaining - nums[i]}")
            dfs(i + 1, remaining - nums[i], depth + 1)
            path.pop()
            print(f"{pad}un-choose {nums[i]}  path={path}")
    dfs(0, target, 0)


trace_combination_sum([3, 1, 2, 1], 3)
```

**Try it**
- Delete the duplicate rule (the `if i > start ...` line and its `continue`) and rerun: `record [1, 2]` now appears twice, once for each copy of 1.
- Change `i > start` to `i > 0` and run `trace_combination_sum([1, 1, 2], 4)`: the only answer, `[1, 1, 2]`, disappears. The second 1 sat one level *below* its twin, not beside it, so it should have been allowed.
- Change `dfs(i + 1, ...)` to `dfs(i, ...)` and rerun the original call: a new `record [1, 1, 1]` appears, the first 1 taken three times.
- Run `trace_combination_sum([2, 3, 6, 7], 7)` and predict the records first: only `[7]`.

### Where it goes wrong

1. **Recording `path` instead of a copy.** Every entry of `result` is then the same list, empty when the search ends: `subsets([1])` gives `[[], []]`. Fix: `result.append(path[:])` (`"".join(path)` already makes a new string).
2. **Un-choosing only part of the state.** Each change made in "choose" needs its mirror in "un-choose": the `pop`, `used[i] = False`, the attack sets, the grid cell. Forget `used[i] = False` and `permute([1, 2])` returns only `[[1, 2]]`.
3. **Looping from 0 instead of `start`.** `combination_sum([2, 3, 6, 7], 7, reuse=True)` then returns `[2, 2, 3]`, `[2, 3, 2]` and `[3, 2, 2]` as three answers. Subsets, whose only brake is `start`, recurses until Python raises `RecursionError`.
4. **`dfs(start + 1)` instead of `dfs(i + 1)`.** The next level starts after the item just chosen: with `start + 1`, `subsets([1, 2, 3])` returns 16 lists, including `[1, 3, 3]` and `[3, 2]`.
5. **`i > 0` instead of `i > start` in the duplicate rule.** That also blocks a copy right below its twin, so `[1, 1, 6]` vanishes from `combination_sum([10, 1, 2, 7, 6, 1, 5], 8)`. The rule is about *siblings* only.
6. **Duplicate rule or `break` without sorting.** Equal values must be neighbours for `nums[i] == nums[i - 1]` to see them, and `break` is only safe when every later number is larger: unsorted `[5, 1]` with target 1 breaks at 5 and misses `[1]`.
7. **`dfs(i)` versus `dfs(i + 1)`.** `i` lets the same item be taken again (39), `i + 1` does not (40, Subsets). With `dfs(i)` where reuse is not allowed, `combination_sum([1], 2)` returns `[[1, 1]]`, using the single 1 twice.
8. **Reading before testing "complete".** A finished path calls `dfs` once more with `k == len(word)`, often on an off-grid neighbour, so test `k == len(word)` *before* anything reads `word[k]`. Swapped, `word_search([["A"]], "A")` is False and `word_search([list("AB")], "AB")` raises `IndexError`.
9. **Restoring on only one way out.** In a grid search, a `return True` placed before the restore leaves the board scribbled on. Compute `found`, restore, then return. (Sudoku is the deliberate exception: its scribbles are the answer.)
10. **`count += 1` in a nested `dfs` without `nonlocal`.** Assigning to `count` makes it a local of `dfs`, so Python raises `UnboundLocalError`; `result.append(...)` is fine because it changes the list without rebinding the name. Fix: `nonlocal count`, or return counts and add them up (`count += dfs(...)`), as `unique_paths_iii` below does.
11. **Floats and leading zeros.** 24 Game must compare with a tolerance (`8 / (3 - 8 / 3)` is `23.99999999999999` in floats); a number built from digits must reject `"05"` while accepting `"0"`.

### Edge cases to say out loud

Empty input (`[[]]` for subsets and permutations, but `[]` for phone letters of `""`) · no answer at all (unreachable target) · target 0 (the empty combination: ask) · all values equal · one element · a grid of one cell · a word longer than the grid has cells.

```python
assert subsets([]) == [[]]                              # the empty set is a subset of anything
assert permute([]) == [[]]                              # exactly one way to order nothing
assert combination_sum([2, 4], 5) == []                 # unreachable target: no answers, no error
assert combination_sum([3, 1], 0) == [[]]               # target 0: the empty combination (ask!)
assert combination_sum([2, 2, 2], 4) == [[2, 2]]        # copies collapse into one answer
assert combination_sum([2], 4) == []                    # i + 1: the 2 can be used once ...
assert combination_sum([2], 4, reuse=True) == [[2, 2]]  # ... i: as often as you like
assert len(subsets(list(range(10)))) == 2 ** 10
assert len(permute([1, 2, 3, 4, 5])) == 120
print("edge cases pass")
```

**Try it**
- Run `subsets([1, 1])`: `[[], [1], [1, 1], [1]]`, because the template has no duplicate rule. Add `nums = sorted(nums)` and the `i > start` skip to get `[[], [1], [1, 1]]`.
- Run `permute([1, 1])`: `[[1, 1], [1, 1]]`. Add `nums = sorted(nums)` as the first line and change `if used[i]:` to `if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]):` (twins are used left to right): now `[[1, 1]]`. Without `i > 0`, index 0 compares with `nums[-1]`, the *last* element, and `permute([1, 1])` returns `[]`.
- Predict, then assert: `combination_sum([1, 1, 1], 2) == [[1, 1]]`.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Subsets, loop tree** | record on entry to every node; recurse with `i + 1` | 78 |
| **Subsets, take/skip tree** | one level per item, two edges (take, skip); record at depth n | 78 |
| **Fixed size k** | record at `len(path) == k`; `break` when too few items are left for the open slots | 77 |
| **Duplicates in the input** | sort; skip `i > start and nums[i] == nums[i - 1]` | 90, 40 |
| **Sum target** | sort, `break` once `nums[i] > remaining`; reuse allowed: recurse with `i` | 39, 40 |
| **Permutations** | no `start`; `used[i]` flags (duplicates: the twin rule) | 46, 47 |
| **Two options per position** | keep or change this letter; keep it or abbreviate it: take/skip in disguise | 784, 320 |
| **Build a string under counts** | "(" while `opened < n`, ")" while `closed < opened` | 22 |
| **One level per position** | level i picks a letter for `digits[i]`; complete at `i == len(digits)` | 17 |
| **Cut the string** | the choice is where the next piece ends; each piece must pass a test | 131, 93 |
| **Grid paths** | 4 neighbours; mark the cell in place, restore it after | 79 |
| **Board + many words** | walk the board once with a trie of all the words: [Tries](#s12) | 212, 425 |
| **Constraint sets** | sets of taken columns and diagonals answer "attacked?" in O(1) | 51, 52 |
| **Items into k buckets** | level i places item i; skip buckets that look alike | 698, 473 |
| Hard ones (at the end) | a running value with a last term; a counter of cells still owed; row/column/box sets; count the budget first; shrink the multiset; walk back to un-choose | 282, 980, 37, 301, 679, 489 |

**Two trees for subsets, and a size limit.** The loop tree above records at every node, because every node is a subset. The take/skip tree has one level per item and two edges, *take it* or *skip it*; a node is a half-made decision, so it records only at the bottom. Same 2^n answers, different shape: take/skip is the one that grows into "which bucket gets this item". For a fixed size k, a branch can stop as soon as too few numbers are left to fill the open slots.

```python
def subsets_take_skip(nums):                 # one level per item, two edges
    result, path = [], []
    def dfs(i):                              # items 0 .. i-1 are decided
        if i == len(nums):
            result.append(path[:])           # RECORD at the leaves: depth n
            return
        path.append(nums[i]); dfs(i + 1); path.pop()   # take nums[i]
        dfs(i + 1)                                     # skip nums[i]
    dfs(0)
    return result


def combine(n, k):                           # every k-subset of 1..n
    result, path = [], []
    def dfs(start):
        if len(path) == k:
            result.append(path[:])
            return
        need = k - len(path)                 # open slots
        for i in range(start, n - need + 2): # i <= n - need + 1 leaves room for need - 1 more
            path.append(i); dfs(i + 1); path.pop()
    dfs(1)
    return result


print(subsets_take_skip([1, 2, 3]))   # [[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []]
print(combine(4, 2))                  # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
```

**Try it**
- Swap the take line and the skip line: the same 8 subsets come out in another order, starting `[[], [3], [2], [2, 3], ...]`.
- Drop the `path.pop()` from the take line and run `subsets_take_skip([1, 2])`: `[[1, 2], [1, 2], [1, 2, 2], [1, 2, 2]]`. The skip branch inherits the taken item.
- In `combine`, change `+ 2` to `+ 1`: `combine(4, 2)` silently loses `[1, 4]`, `[2, 4]` and `[3, 4]`. A bound that is off by one fails quietly, so always test with the largest number in play.

**Building a string, one character per level.** For brackets, two counters replace `used[]`: they say exactly which characters may come next, so every branch is the start of a valid answer and nothing is filtered at the end. For phone letters, recursion is a nested `for` loop whose depth is only known at run time.

```python
def generate_parentheses(n):
    result, path = [], []
    def dfs(opened, closed):                 # the two counts ARE the state
        if len(path) == 2 * n:
            result.append("".join(path))
            return
        if opened < n:                       # a "(" is still available
            path.append("("); dfs(opened + 1, closed); path.pop()
        if closed < opened:                  # only close what is open
            path.append(")"); dfs(opened, closed + 1); path.pop()
    dfs(0, 0)
    return result


KEYPAD = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}

def letter_combinations(digits):
    if not digits:
        return []                            # no digits: no words (not [""])
    result, path = [], []
    def dfs(i):                              # level i picks a letter for digits[i]
        if i == len(digits):
            result.append("".join(path))
            return
        for ch in KEYPAD[digits[i]]:
            path.append(ch); dfs(i + 1); path.pop()
    dfs(0)
    return result


print(generate_parentheses(3))     # ['((()))', '(()())', '(())()', '()(())', '()()()']
print(letter_combinations("23"))   # ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
```

**Try it**
- Change `if closed < opened:` to `if closed < n:` and run `generate_parentheses(2)`: six strings, including `'())('` and `'))(('`. You are now making every arrangement of two of each bracket, valid or not.
- Print `[len(generate_parentheses(n)) for n in range(1, 7)]`: `[1, 2, 5, 14, 42, 132]` (the Catalan numbers), far fewer than the 4^n strings of length 2n.
- Delete the `if not digits` guard and run `letter_combinations("")`: `['']`. The root is already complete (zero digits, zero letters), so the empty path gets recorded.

**Cutting a string into pieces.** Here a choice is *where the next piece ends*, and the piece must pass a test: it reads the same both ways, or it is a number from 0 to 255 without a leading zero. Restore IP Addresses also fixes the number of pieces, so "complete" means four pieces *and* no digits left over.

```python
def partition_palindromes(s):
    result, path = [], []
    def dfs(start):                          # s[:start] is already cut into palindromes
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):   # choice: where the next piece ends
            piece = s[start:end]
            if piece == piece[::-1]:         # only palindromic pieces may be chosen
                path.append(piece); dfs(end); path.pop()
    dfs(0)
    return result


def restore_ip_addresses(s):                 # 4 pieces, each 0..255, no leading zero
    result, path = [], []
    def dfs(start):
        if len(path) == 4:
            if start == len(s):              # complete only if every digit is used
                result.append(".".join(path))
            return
        for end in range(start + 1, min(start + 3, len(s)) + 1):
            piece = s[start:end]
            if (piece[0] == "0" and len(piece) > 1) or int(piece) > 255:
                break                        # a longer piece would be just as bad
            path.append(piece); dfs(end); path.pop()
    dfs(0)
    return result


print(partition_palindromes("aab"))   # [['a', 'a', 'b'], ['aa', 'b']]
print(restore_ip_addresses("25525511135"), restore_ip_addresses("010010"))
# ['255.255.11.135', '255.255.111.35'] ['0.10.0.10', '0.100.1.0']
```

**Try it**
- Remove the palindrome test in `partition_palindromes` (let every piece through) and run it on `"aab"`: 4 partitions, every way to cut 3 letters (2^(n−1)).
- Predict `partition_palindromes("aaa")` before running: `[['a', 'a', 'a'], ['a', 'aa'], ['aa', 'a'], ['aaa']]`.
- Replace `if start == len(s):` with `if True:`: `len(restore_ip_addresses("25525511135"))` becomes 43. Four pieces are not enough; every digit must be used.
- Drop the leading-zero test (keep only `int(piece) > 255`) and run `restore_ip_addresses("010010")`: 10 results, including `'01.0.0.10'`.

**Grids: mark the cell, explore, restore.** The path is a snake of cells, and a cell on the snake must not be stepped on twice. Instead of a `visited` set, overwrite the cell while you stand on it and put the letter back on the way out. Compare flood fill ([Graphs I: BFS & DFS](#s17)): it asks *can I reach this cell?*, so a visited cell stays visited and the cost is O(cells). A path search asks *which cells form this path?*, so a cell is free again once the path backs off it.

```python
def word_search(board, word):
    R, C = len(board), len(board[0])
    def dfs(r, c, k):                        # can word[k:] be traced starting at (r, c)?
        if k == len(word):                   # complete: test this FIRST, before reading word[k]
            return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[k]:
            return False                     # off the grid, on the path already ("#"), or wrong letter
        saved, board[r][c] = board[r][c], "#"           # choose: this cell is on the path
        found = any(dfs(r + dr, c + dc, k + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = saved                  # un-choose, before the only return below
        return found
    return any(dfs(r, c, 0) for r in range(R) for c in range(C))


board = [list("ABCE"), list("SFCS"), list("ADEE")]
print(word_search(board, "ABCCED"), word_search(board, "SEE"), word_search(board, "ABCB"))   # True True False
print(board == [list("ABCE"), list("SFCS"), list("ADEE")])   # True  (every mark was restored)
```

**Try it**
- Replace `saved, board[r][c] = board[r][c], "#"` with `saved = board[r][c]` (remember the letter, but never mark the cell) and run `word_search(board, "ABCB")`: `True`. The walk A→B→C→B stands on the same B twice.
- Swap the two tests at the top of `dfs` (bounds and letter first, `k == len(word)` second) and rerun the cell: `IndexError` on its first search, and `word_search([["A"]], "A")` is now False. A finished path asks for `word[len(word)]`.
- Delete the restore line `board[r][c] = saved` and run `word_search([list("ABB")], "BBA")`: False instead of True. The failed try from the middle B leaves both B's marked, so the try from the right B never gets going.

**Constraint sets: is this square allowed?** A queen at `(r, c)` owns one column, one `\` diagonal (every square on it has the same `r - c`) and one `/` diagonal (same `r + c`). Three sets answer "attacked?" in O(1), so a bad square is never even entered.

```python
def solve_n_queens(n):
    boards, queens = [], []                  # queens[r] = column of the queen in row r
    cols, diag, anti = set(), set(), set()   # taken columns, r - c diagonals, r + c diagonals
    def dfs(r):                              # rows 0 .. r-1 already hold one safe queen each
        if r == n:
            boards.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
            return
        for c in range(n):
            if c in cols or r - c in diag or r + c in anti:
                continue                     # attacked: not a choice
            cols.add(c); diag.add(r - c); anti.add(r + c)
            queens.append(c)
            dfs(r + 1)
            queens.pop()
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)
    dfs(0)
    return boards


print(solve_n_queens(4))                              # [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]
print([len(solve_n_queens(n)) for n in range(1, 9)])  # [1, 0, 0, 2, 10, 4, 40, 92]
```

**Try it**
- Add `print(queens)` just before the `boards.append` line and run `solve_n_queens(4)`: `[1, 3, 0, 2]` and `[2, 0, 3, 1]`. The board strings are only a drawing of that list.
- Delete the line with the three `remove` calls: `solve_n_queens(4)` returns `[]`. Lifted queens keep "attacking", so the search runs out of squares.
- Use `r + c` for `diag` too (in the test, the `add` and the `remove`), so both sets track `/` diagonals: `len(solve_n_queens(4))` becomes 7, the 2 real boards plus 5 with two queens on one `\` diagonal.

**Items into k buckets** (698, 473). Level i decides which bucket gets item i: the take/skip tree with k edges instead of two. Two prunes make it fast. Big items go first, so a dead end shows up near the root. And if item i failed in an empty bucket, it fails in every other empty bucket too (empty buckets are interchangeable), so stop trying.

```python
def can_partition_k(nums, k):
    total = sum(nums)
    if total % k:
        return False
    target, load = total // k, [0] * k       # load[b] = sum of the items in bucket b (shared)
    nums = sorted(nums, reverse=True)        # big items first: dead ends show up early
    def dfs(i):                              # items 0 .. i-1 are placed
        if i == len(nums):
            return True
        for b in range(k):
            if load[b] + nums[i] > target:
                continue
            load[b] += nums[i]               # choose: item i goes into bucket b
            if dfs(i + 1):
                return True
            load[b] -= nums[i]               # un-choose
            if load[b] == 0:
                break                        # it failed in an empty bucket: all empty buckets are alike
        return False
    return dfs(0)


print(can_partition_k([4, 3, 2, 3, 5, 2, 1], 4), can_partition_k([1, 2, 3, 4], 3))   # True False
```

**Try it**
- Count the calls: put `calls = [0]` before `def dfs`, `calls[0] += 1` as its first line, and end with `ok = dfs(0); print(calls[0]); return ok`. `can_partition_k([2, 2, 2, 2, 3, 4, 5], 4)` makes 12 calls; delete the empty-bucket `break` and it makes 233, for the same `False`.
- Matchsticks to Square (473) is this function with k = 4: predict `can_partition_k([1, 1, 2, 2, 2], 4)` (True: 2, 2, 2 and 1 + 1).
- Predict `can_partition_k([1, 1, 1, 1, 6], 2)` before running: False, since the 6 alone is more than the target 5.

**Optional: the Hard ones.** The same skeleton with heavier bookkeeping. Read these once the mediums above feel easy.

Expression Add Operators (282) carries the value so far and the **last term**. `*` binds tighter than `+` and `-`, so `*x` takes the last term back out and puts it back multiplied:

```text
expr      value   last
2           2       2       "+x": value + x, last x       "-x": value - x, last -x
2-3        -1      -3       "*x": value - last + last * x, last last * x
2-3*4     -10     -12       -1 - (-3) + (-12) = -10, the same as 2 - 12
```

```python
def add_operators(num, target):
    out = []
    def dfs(i, expr, value, last):           # value of expr; last = its final term, with its sign
        if i == len(num):
            if value == target:
                out.append(expr)
            return
        for j in range(i + 1, len(num) + 1): # the next operand is num[i:j]
            s = num[i:j]
            if len(s) > 1 and s[0] == "0":
                break                        # "05" is not an operand, and longer ones neither
            x = int(s)
            if i == 0:
                dfs(j, s, x, x)              # the first operand has no operator in front
            else:
                dfs(j, expr + "+" + s, value + x, x)
                dfs(j, expr + "-" + s, value - x, -x)
                dfs(j, expr + "*" + s, value - last + last * x, last * x)   # undo last, redo it times x
    dfs(0, "", 0, 0)
    return out


print(add_operators("123", 6), add_operators("105", 5))   # ['1+2+3', '1*2*3'] ['1*0+5', '10-5']
```

**Try it**
- In the `*` line, replace `value - last + last * x` with `value * x` and run `add_operators("123", 7)`: `[]`, because `1+2*3` is now computed as (1 + 2) · 3 = 9.
- Delete the leading-zero `break` and run `add_operators("105", 5)`: `'1*05'` sneaks in beside `'1*0+5'` and `'10-5'`.
- Check the picture: `add_operators("234", -10)` is `['2-3*4']`.

Unique Paths III (980) is word search plus a counter of cells still owed, and it counts walks by adding up what the children return. Sudoku (37) is constraint sets with one set per row, per column and per 3×3 box; the repo version adds bitmasks and fills the cell with the fewest legal digits first.

```python
def unique_paths_iii(grid):
    R, C = len(grid), len(grid[0])
    todo = sum(row.count(0) for row in grid) + 1        # empty cells + the end cell
    sr, sc = next((r, c) for r in range(R) for c in range(C) if grid[r][c] == 1)
    def dfs(r, c, todo):                     # todo = cells still to step on, the end included
        if grid[r][c] == 2:
            return 1 if todo == 0 else 0     # the end counts only if nothing was skipped
        saved, grid[r][c] = grid[r][c], -1   # choose: block the cell while we stand on it
        count = 0
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] in (0, 2):
                count += dfs(nr, nc, todo - 1)
        grid[r][c] = saved                   # un-choose
        return count
    return dfs(sr, sc, todo)


def solve_sudoku(board):                     # fills board in place; True when solved
    rows, cols, boxes = ([set() for _ in range(9)] for _ in range(3))   # digits used per row / column / box
    empty = [(r, c) for r in range(9) for c in range(9) if board[r][c] == "."]
    for r in range(9):
        for c in range(9):
            if board[r][c] != ".":           # the box of (r, c) is r // 3 * 3 + c // 3
                d = board[r][c]; rows[r].add(d); cols[c].add(d); boxes[r // 3 * 3 + c // 3].add(d)
    def dfs(k):                              # empty[:k] are filled and every rule holds
        if k == len(empty):
            return True
        r, c = empty[k]
        b = r // 3 * 3 + c // 3
        for d in "123456789":
            if d in rows[r] or d in cols[c] or d in boxes[b]:
                continue
            board[r][c] = d; rows[r].add(d); cols[c].add(d); boxes[b].add(d)
            if dfs(k + 1):
                return True                  # first solution: stop, and keep the board
            board[r][c] = "."; rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d)
        return False                         # no digit fits: the caller must change its guess
    return dfs(0)


print(unique_paths_iii([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]]))   # 2
puzzle = [list(row) for row in ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
                                "7...2...6", ".6....28.", "...419..5", "....8..79"]]
print(solve_sudoku(puzzle), "".join(puzzle[0]), "".join(puzzle[8]))   # True 534678912 345286179
```

**Try it**
- In `unique_paths_iii`, drop the `+ 1` from `todo`: the answer becomes 0, because `todo` is -1 instead of 0 when a full walk reaches the end.
- Change `1 if todo == 0 else 0` to `1`: the answer jumps from 2 to 17, since every walk that reaches the end now counts, even one that skipped cells.
- In `solve_sudoku`, delete the undo line after `if dfs(k + 1)` and rerun the cell: it prints `False` and row 0 reads `53127689.`. Wrong guesses that are never taken back stay in the sets and block every later attempt.

Remove Invalid Parentheses (301) **counts first, then searches**: one balance pass tells you *how many* `(` and `)` must go, so the search only decides *which* ones and never lets the open count drop below zero. The 24 Game (679) **shrinks the multiset**: any expression on four cards is three steps of "replace two numbers by one result", so trying every pair and every result covers every bracketing.

```python
def remove_invalid_parentheses(s):
    left = right = 0                         # how many "(" and ")" MUST be removed
    for ch in s:
        if ch == "(":
            left += 1
        elif ch == ")" and left:
            left -= 1                        # this ")" closes an earlier "("
        elif ch == ")":
            right += 1                       # nothing open: this ")" must go
    found, path = set(), []                  # path = the characters kept so far (shared)
    def dfs(i, opened, left, right):
        if i == len(s):
            if opened == 0 and left == 0 and right == 0:
                found.add("".join(path))     # a set: deleting different copies can give one string
            return
        ch = s[i]
        if ch == "(" and left:               # option 1: delete this "("
            dfs(i + 1, opened, left - 1, right)
        if ch == ")" and right:              # option 1: delete this ")"
            dfs(i + 1, opened, left, right - 1)
        if ch != ")" or opened:              # option 2: keep it (a ")" needs an open "(")
            path.append(ch)
            dfs(i + 1, opened + (ch == "(") - (ch == ")"), left, right)
            path.pop()
    dfs(0, 0, left, right)
    return sorted(found)


def judge_point_24(cards):
    def solve(nums):                         # can these numbers be combined into 24?
        if len(nums) == 1:
            return abs(nums[0] - 24) < 1e-6  # floats: compare with a tolerance
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                a, b = nums[i], nums[j]
                rest = [nums[k] for k in range(len(nums)) if k != i and k != j]
                options = [a + b, a - b, b - a, a * b]
                if abs(b) > 1e-6:
                    options.append(a / b)
                if abs(a) > 1e-6:
                    options.append(b / a)
                if any(solve(rest + [v]) for v in options):   # rest + [v] is a new list: nothing to undo
                    return True
        return False
    return solve([float(x) for x in cards])


print(remove_invalid_parentheses("()())()"), remove_invalid_parentheses(")("))   # ['(())()', '()()()'] ['']
print(judge_point_24([4, 1, 8, 7]), judge_point_24([1, 2, 1, 2]), judge_point_24([3, 3, 8, 8]))   # True False True
```

**Try it**
- Delete the `if ch != ")" or opened:` condition (always allow keeping) and run `remove_invalid_parentheses(")()(")`: `['()', ')(']`. The string `")("` has the right counts but dips below zero in the middle.
- Change the leaf test to `nums[0] == 24` and run `judge_point_24([3, 3, 8, 8])`: `False`, because its solution `8 / (3 - 8 / 3)` comes out as `23.99999999999999` in floats.
- Remove `b - a` and `b / a` from the options and rerun `judge_point_24([3, 3, 8, 8])`: `False`. Only pairs with `i < j` are tried, so the reversed order of `-` and `/` must be offered explicitly.

Robot Room Cleaner (489) has **physical moves** and no undo button: the robot's position *is* the state, so "un-choose" means walking back. The parent cell is right behind it, so "turn around, step, turn around" restores both position and heading, and turning right after each of the four tries brings the heading back to where it started. Every caller finds the robot exactly as it left it: the backtracking invariant, enforced with motors.

```text
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]       up, right, down, left: turnRight() means d -> (d + 1) % 4

go_back():   turnRight(); turnRight(); move(); turnRight(); turnRight()      the parent is one step behind

dfs(r, c, d):                     the robot stands on (r, c), facing DIRS[d]; the start is (0, 0)
    visited.add((r, c)); clean()
    for k in 0, 1, 2, 3:
        nd = (d + k) % 4          the direction it faces right now
        dr, dc = DIRS[nd]
        if (r + dr, c + dc) not in visited and move():
            dfs(r + dr, c + dc, nd)     choose = walk in
            go_back()                   un-choose = walk back out, facing nd again
        turnRight()               after the 4th turn it faces d again
```

### Say it in the interview

> "This is Combination Sum II. Can candidates repeat, can one be reused, and may answers come in any order? The brute force tries all 2^n index subsets, sums each, and dedupes with a set of sorted tuples: O(n·2^n), and it finishes subsets whose first numbers already overshoot. I'll build combinations one number at a time instead: one shared path, choices from `start` on so each combination is built in one order only, complete when the remaining sum is zero. I sort first, so I can `break` once a number exceeds what's left, and skip a value equal to its left sibling so nothing is built twice. Worst case is still O(n·2^n), at most 2^n nodes and O(n) to copy each answer, but most branches die early. Extra space is O(n)."

Then point at the three lines *choose / explore / un-choose* ("these three lines are the algorithm, everything else is pruning") and name the invariant: "`dfs` leaves `path` exactly as it found it".

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| 24 Game | `backtracking/twenty_four_game.py` | pick any two numbers, replace them with one of six results, recurse on the shorter list; compare with a tolerance |
| Combination Sum | `backtracking/combination_sum.py` | sorted start-index search; recurse with `i` to allow reuse; `break` once a candidate exceeds what remains |
| Combination Sum II | `backtracking/combination_sum_ii.py` · `practice/simple/37_combination_sum_ii.py` | sort; skip equal siblings (`i > start`); recurse with `i + 1`; `break` on overflow |
| Expression Add Operators | `backtracking/expression_add_operators.py` | carry value and last term; `*x` gives `value - last + last * x`; no operand with a leading zero |
| Generate Parentheses | `backtracking/generate_parentheses.py` | "(" while open < n, ")" while close < open: every branch is a valid prefix |
| Letter Combinations of a Phone Number | `backtracking/letter_combinations_of_a_phone_number.py` · `practice/simple/38_letter_combinations_of_a_phone_number.py` | one recursion level per digit, a nested loop of unknown depth; empty input gives `[]` |
| N-Queens | `backtracking/n_queens.py` · `practice/simple/40_n_queens.py` | one queen per row; sets of columns, `r - c` and `r + c` make "attacked?" O(1) |
| Palindrome Partitioning | `practice/simple/36_palindrome_partitioning.py` | the choice is where the next piece ends; only palindromic pieces may be chosen |
| Permutations | `backtracking/permutations.py` | no start index; `used[i]` marks what is already in the path |
| Remove Invalid Parentheses | `backtracking/remove_invalid_parentheses.py` | count the forced removals first; keep or delete each bracket within budget, balance never below 0 |
| Robot Room Cleaner | `backtracking/robot_room_cleaner.py` | DFS on coordinates relative to the start; un-choose = turn around, move, turn around |
| Subsets | `backtracking/subsets.py` | record at every node; recurse with `i + 1` so indices only increase (or take/skip one item per level) |
| Subsets II | `backtracking/subsets_ii.py` | sort; skip a value equal to its left sibling at the same level (`i > start`) |
| Sudoku Solver | `backtracking/sudoku_solver.py` | row, column and box sets (bitmasks) make legality O(1); fill the most constrained cell first |
| Unique Paths III | `backtracking/unique_paths_iii.py` | grid search marking cells in place; the end counts only when every empty cell was used |
| Word Search | `backtracking/word_search.py` · `practice/simple/39_word_search.py` | test "complete" first; match `word[k]` at depth k; overwrite the cell while on the path, restore it after |

### Self-check

1. Why do subsets use a `start` index while permutations use `used[]`?
<details><summary>Answer</summary>Subsets ignore order, so <code>[1, 2]</code> and <code>[2, 1]</code> are the same answer; forcing indices to increase keeps exactly one ordering of each. Permutations <em>are</em> the orderings, so any unused item may come next, and <code>used[]</code> remembers which items are already placed.</details>

2. In Subsets II, why `i > start` and not `i > 0`?
<details><summary>Answer</summary>The rule only stops <em>siblings</em> (choices at the same level) from repeating a value. <code>i == start</code> is the first choice at this level, and taking a copy right after its twin, one level deeper, is how <code>[2, 2]</code> is built. <code>i > 0</code> would forbid that too.</details>

3. Which state needs a mirror line after the recursive call, and which does not?
<details><summary>Answer</summary>Shared, mutable state does: <code>path</code>, <code>used</code>, the attack sets, the board, the bucket loads. Each change made before the call is undone after it. State passed as an argument (<code>start</code>, <code>remaining</code>, <code>expr + s</code>) undoes itself, because the caller still holds its own value when the call returns.</details>

4. In Expression Add Operators the expression so far is `2-3`. What are `value` and `last`, and what do they become after `*4`?
<details><summary>Answer</summary>Before: value = -1, last = -3. After: value = -1 - (-3) + (-3)·4 = -10 and last = -12. Check: 2 - 3·4 = -10.</details>
