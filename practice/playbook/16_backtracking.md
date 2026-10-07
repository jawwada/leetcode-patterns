## Backtracking

> Backtracking walks a decision tree that it never builds. One shared list, `path`, is the pencil line from the root to where you stand. At each node you **choose** an option (append), **explore** everything below it (recurse), then **un-choose** it (pop), so the next option starts from exactly the same place. Pruning rubs out a whole subtree the moment its beginning cannot work.

**Reach for it when** the problem says "return **all**" (subsets, combinations, permutations, partitions, boards, expressions), or asks whether something can be arranged under rules, and the input is small: n ≤ ~15, a 9×9 board, a grid of ~20 cells.

Tiny limits are the interviewer telling you that an exponential search is expected. Rough limits: 2^n is fine up to n ≈ 20, n! up to n ≈ 10. "In how many ways" with a *large* n is counting, not search: that is DP or combinatorics, and [Dynamic Programming](#s25), at the end of this notebook, shows how it grows out of backtracking.

**In this repo:** `backtracking/` (15 problems) · bank: `practice/simple/36_palindrome_partitioning.py`, `practice/simple/37_combination_sum_ii.py`, `practice/simple/38_letter_combinations_of_a_phone_number.py`, `practice/simple/39_word_search.py`, `practice/simple/40_n_queens.py` · basics: `practice/simple/basics/backtracking/01_subsets.py`, `practice/simple/basics/backtracking/02_subsets_with_duplicates.py`, `practice/simple/basics/backtracking/03_combinations_n_choose_k.py`, `practice/simple/basics/backtracking/04_combination_sum.py`, `practice/simple/basics/backtracking/05_permutations.py`, `practice/simple/basics/backtracking/06_permutations_with_duplicates.py`, `practice/simple/basics/backtracking/07_generate_parentheses.py`

### The picture

Subsets is the smallest complete example: every subset of `[1, 2, 3]`, eight of them. Each node of the tree below is a subset, and the walk visits every node once.

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

Every backtracking problem is this picture with different answers to three questions. Q1 asks what a partial solution is: the path, plus a cheap summary of it. Q2 asks which choices a node offers, and Q3 asks when a path is complete.

It is fast enough because the brute force builds every complete candidate and checks it only at the end: all 2^n bitmasks, all n^n sequences, every grid walk of length L. Backtracking checks the rules at every node instead, so a bad beginning is rejected once, together with every completion it would have had, and the subtree below it is never entered.

The earlier a rule is tested, the higher in the tree the cut lands: the sharper the check, the smaller the tree. And one shared `path` with append and pop makes each step O(1), where the brute force copies a list per candidate.

The search stays exponential when the answer is exponential: there really are 2^n subsets to print. Generate Parentheses, every well-formed string of n pairs of brackets, is the ideal case: its checks are perfect, so it never enters a dead prefix.

Say the complexity in words: the nodes visited times the work per node, plus the cost of copying each recorded answer; the extra space is the recursion depth. Name the size of the tree from the reference below, then add that pruning makes it much smaller in practice. The seven searches are the ones you will meet: subsets and k-combinations of a list, its orderings, the words a phone number spells, a word traced through a grid, queens on a board, and bracket strings.

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

The seven decisions have fixed answers here. The **state** is one shared list, `path`, plus where you stand in the tree, `start` or the `used[i]` flags, plus a summary that keeps every check O(1), such as `remaining` or the attack sets. By **definition**, `path` holds the choices from the root to this node, `start` is the smallest index this node may pick, and `remaining` is `target - sum(path)`. The **invariant** is that `dfs` leaves all state as it found it: every append is matched by a pop, every mark by an unmark.

A **step** chooses, by appending or marking, and explores, by calling `dfs` on the smaller problem; the **fix** un-chooses, by popping or unmarking, which restores the invariant. The **record** is a copy, `path[:]`, taken when the path is complete: on entry for subsets, where every node is an answer, and at the leaf otherwise. **Init** is the empty root, `result, path = [], []`, with the root call `dfs(0)` or `dfs(0, target)`. **Return** gives `result`, `[]` when nothing was found, or a count, or `True` once a branch succeeds.

Each sentence of the idea is one line of code. The partial solution is `path`, one list shared by every call, and the choices at this level are `for i in range(start, len(nums)):`. A choice that cannot work is skipped with `continue`, or ends the loop with `break` when the list is sorted and every later choice is worse too.

Choosing is `path.append(nums[i])` and un-choosing is `path.pop()`, with `used[i] = True` and `used[i] = False` beside them when order matters; on a grid the pair is `saved, board[r][c] = board[r][c], "#"` and `board[r][c] = saved`. Exploring is `dfs(i + 1)` when each item may be used once and `dfs(i)` when it may be reused, and a summary rides along as an argument: `dfs(i + 1, remaining - x)`.

A complete path is saved with `result.append(path[:])`, a copy and never `path` itself. "Found one, stop" is `if dfs(...): return True` inside the loop and `return False` after it; "how many ways" is `count += dfs(...)` inside the loop and `return count` after it.

Two prunes come up again and again. After sorting, a value equal to the sibling before it is skipped with `if i > start and nums[i] == nums[i - 1]: continue`; in permutations of a list with repeats the twin rule is `if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]): continue`, which takes equal values left to right. Too few items left for the open slots ends the loop: `if len(nums) - i < k - len(path): break`.

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

For each piece of state decide: argument or shared? An argument such as `start`, `remaining`, `k`, `expr + s` or `rest + [v]` is un-chosen automatically when the call returns, because the caller still holds its own value. Shared state such as `path`, `used`, the attack sets or the board needs a *mirror line*: the line after the call that undoes what the line before it did.

Six core problems show how differently the blanks fill. Subsets, every subset of distinct numbers, passes `start`, chooses any `i` from `start` on, and is complete at every node. Combination Sum II, the combinations that sum to a target with each index used at most once, passes `start` and `remaining`, chooses from the sorted list while skipping equal siblings, and is complete when `remaining == 0`.

Permutations, every ordering of the numbers, passes nothing and shares `used[]`: any unused `i` is a choice, and the path is complete at `len(path) == n`. Letter Combinations of a Phone Number, the words a digit string spells, passes `i` and chooses among the letters of `digits[i]` until `i == len(digits)`.

Palindrome Partitioning, cutting a string into palindromes, passes `start` and chooses each `end` whose piece `s[start:end]` is a palindrome, until `start == len(s)`. Word Search, tracing a word through a grid, passes `r, c, k` from every cell, chooses among the four neighbours, and is complete at `k == len(word)`.

The `start` index is how "order does not matter" becomes code: indices only increase along a path, so {1, 2} is built once as `[1, 2]` and never as `[2, 1]`. Permutations *are* the orders, so any unused item may come next, and `used[]` remembers which ones are taken.

The order of the tagged lines is a decision too. Subsets RECORD first, because a node is an answer before any child is tried. The FIX, the pop, comes after the explore, or the children would never see the item.

The template below solves three problems, and a flag adds a fourth. Subsets asks for every subset of distinct numbers: `[1, 2, 3]` has eight, from `[]` to `[1, 2, 3]`. Combination Sum II asks for every combination that sums to a target, each index used at most once and nothing listed twice: `[10, 1, 2, 7, 6, 1, 5]` with target 8 gives `[1, 1, 6]`, `[1, 2, 5]`, `[1, 7]` and `[2, 6]`.

With `reuse=True` the same function is Combination Sum, where a candidate may be taken again and again: `[2, 3, 6, 7]` with target 7 gives `[2, 2, 3]` and `[7]`. Permutations asks for every ordering of distinct numbers, six for `[1, 2, 3]`. The code is one skeleton three times: `subsets` records at every node and only ever looks to the right, `combination_sum` adds a running `remaining` and two cuts, and `permute` swaps the start index for `used[]` flags, because order matters.

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
- Delete `used[i] = False` in `permute` and run `permute([1, 2, 3])`: only `[[1, 2, 3]]` comes back, since every number stays "used" after its first trip.
- Print `path` on entry to `dfs` in `subsets([1, 2, 3])`: the eight prints are the walk in the picture, in the same order as the output.

### Watch it work

The trace below runs `combination_sum` on `[3, 1, 2, 1]` with target 3, whose answers are `[1, 2]` and `[3]`, and prints every event, one line each, indented by depth in the tree. Watch for three things: break, when the list is sorted and nothing to the right can fit; skip, when a second `1` beside the first would rebuild `[1, 2]`; and every un-choose putting `path` back exactly as it was.

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
3. **Looping from 0 instead of `start`.** `combination_sum([2, 3, 6, 7], 7, reuse=True)` then returns `[2, 2, 3]`, `[2, 3, 2]` and `[3, 2, 2]` as three answers. Subsets has no brake but `start`, so `subsets([1])` recurses until Python raises `RecursionError`.
4. **`dfs(start + 1)` instead of `dfs(i + 1)`.** The next level starts after the item just chosen: with `start + 1`, `subsets([1, 2, 3])` returns 16 lists, including `[1, 3, 3]` and `[3, 2]`.
5. **`i > 0` instead of `i > start` in the duplicate rule.** That also blocks a copy right below its twin, so `[1, 1, 6]` vanishes from `combination_sum([10, 1, 2, 7, 6, 1, 5], 8)`. The rule is about *siblings* only.
6. **Duplicate rule or `break` without sorting.** Equal values must be neighbours for `nums[i] == nums[i - 1]` to see them, and `break` is only safe when every later number is larger: unsorted `[5, 1]` with target 1 breaks at 5 and misses `[1]`.
7. **`dfs(i)` versus `dfs(i + 1)`.** `i` lets the same item be taken again (39), `i + 1` does not (40, Subsets). With `dfs(i)` where reuse is not allowed, `combination_sum([1], 2)` returns `[[1, 1]]`, using the single 1 twice.
8. **Reading before testing "complete".** A finished path calls `dfs` once more with `k == len(word)`, often on an off-grid neighbour, so test `k == len(word)` *before* anything reads `word[k]`. Swapped, `word_search([["A"]], "A")` is False and `word_search([list("AB")], "AB")` raises `IndexError`.
9. **Restoring on only one way out.** In a grid search, a `return True` placed before the restore leaves the board scribbled on: after `word_search(board, "ABCCED")` succeeds, a second search for `"SEE"` on the same board answers False. Compute `found`, restore, then return. Sudoku, which fills a 9×9 board in place, is the deliberate exception: its scribbles are the answer.
10. **`count += 1` in a nested `dfs` without `nonlocal`.** Assigning to `count` makes it a local of `dfs`, so a subset counter that runs `count += 1` on entry raises `UnboundLocalError` on its first call, even for `[]`. `result.append(...)` is fine, because it changes the list without rebinding the name. Fix: `nonlocal count`, or return counts and add them up, `count += dfs(...)`. Why an assignment makes a local is in [Python Toolkit](#s02).
11. **Floats and leading zeros.** The 24 Game, which combines four cards with `+ - * /` into 24, must compare with a tolerance: `8 / (3 - 8 / 3)` is `23.99999999999999` in floats. A number built from digits must reject `"05"` while accepting `"0"`: without that check, `add_operators("105", 5)` also returns `'1*05'`.

### Edge cases to say out loud

Empty input (`[[]]` for subsets and permutations, but `[]` for phone letters of `""`) · no answer at all (unreachable target) · target 0 (the empty combination: ask) · all values equal · one element · a grid of one cell · a word longer than the grid has cells.

Say these before you code, and ask about target 0, because whether the empty combination counts is the interviewer's call. The asserts below hold the three template functions to the cases that apply to them.

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

Every variation keeps the skeleton and changes one thing: the shape of the tree, the test on a choice, or what "complete" means. The table is the overview; the paragraphs below take the shapes in order, each with its problem and its code.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Subsets, loop tree** | record on entry to every node; recurse with `i + 1` | Subsets (78) |
| **Subsets, take/skip tree** | one level per item, two edges (take, skip); record at depth n | Subsets (78) |
| **Fixed size k** | record at `len(path) == k`; `break` when too few items are left for the open slots | Combinations (77): every k-subset of 1..n |
| **Duplicates in the input** | sort; skip `i > start and nums[i] == nums[i - 1]` | Subsets II (90): every distinct subset of a list with repeats; Combination Sum II (40) |
| **Sum target** | sort, `break` once `nums[i] > remaining`; reuse allowed: recurse with `i` | Combination Sum (39), Combination Sum II (40) |
| **Permutations** | no `start`; `used[i]` flags (duplicates: the twin rule) | Permutations (46), Permutations II (47): every distinct ordering of a list with repeats |
| **Two options per position** | keep or change this letter; keep it or abbreviate it: take/skip in disguise | Letter Case Permutation (784): every upper/lower-case spelling of a string; Generalized Abbreviation (320): every way to replace runs of letters by their length |
| **Build a string under counts** | "(" while `opened < n`, ")" while `closed < opened` | Generate Parentheses (22) |
| **One level per position** | level i picks a letter for `digits[i]`; complete at `i == len(digits)` | Letter Combinations of a Phone Number (17) |
| **Cut the string** | the choice is where the next piece ends; each piece must pass a test | Palindrome Partitioning (131), Restore IP Addresses (93): read a digit string as four numbers 0..255 |
| **Grid paths** | 4 neighbours; mark the cell in place, restore it after | Word Search (79) |
| **Board + many words** | walk the board once with a trie of all the words: [Tries](#s12) | Word Search II (212): which of many words are on the board; Word Squares (425): a grid of words whose rows and columns read the same |
| **Constraint sets** | sets of taken columns and diagonals answer "attacked?" in O(1) | N-Queens (51): every placement of n queens on an n×n board with no two attacking; N-Queens II (52): only count the boards |
| **Items into k buckets** | level i places item i; skip buckets that look alike | Partition to K Equal Sum Subsets (698): split the numbers into k groups of equal sum; Matchsticks to Square (473): use every stick to form the four equal sides of a square |
| *Second pass:* **running value and last term** | carry the value so far and the last term; `*x` takes the last term back out | Expression Add Operators (282): every way to put `+`, `-`, `*` between the digits to reach a target |
| *Second pass:* **cells still owed** | word search plus a counter of empty cells left; the end counts only at zero | Unique Paths III (980): the walks from start to end that step on every empty cell once |
| *Second pass:* **row, column and box sets** | the sets of N-Queens, one per row, column and 3×3 box; stop at the first solution | Sudoku Solver (37): fill a 9×9 board so every row, column and box holds 1 to 9 once |
| *Second pass:* **count the budget first** | one balance pass fixes how many `(` and `)` must go; the search picks which | Remove Invalid Parentheses (301): every valid string left after the fewest deletions |
| *Second pass:* **shrink the multiset** | replace two numbers by one result; recurse on the shorter list | 24 Game (679): can four cards make 24 with `+ - * /` and brackets |
| *Second pass:* **walk back to un-choose** | the robot's position is the state; un-choose = turn around, step, turn around | Robot Room Cleaner (489): clean every reachable cell of a room you cannot see |

The loop tree of the picture records at every node, because every node is a subset. There is a second way to draw the same search, and it comes first because every later variation is one of the two shapes.

The take/skip tree has one level per item and two edges, take it or skip it. A node is a half-made decision, so it records only at the bottom: the same 2^n answers in a different shape. Take/skip is the shape that grows into "which bucket gets this item" later in this section.

Combinations asks for every k-subset of 1..n: `n = 4, k = 2` gives the six pairs from `[1, 2]` to `[3, 4]`. It is the loop tree with a size limit: record once the path holds k numbers, and never start a branch with too few numbers left to fill the open slots. In the code, `subsets_take_skip` asks one item at a time "in or out?", and `combine` stops at k items and never starts a branch it cannot finish.

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

Strings come next because a string is a path of characters: the same skeleton, with `"".join(path)` as the copy. Generate Parentheses asks for every well-formed string of n pairs of brackets, five for n = 3, from `((()))` to `()()()`. Two counters replace `used[]`: a `(` may go in while fewer than n are placed, a `)` while one is still open, so every branch is the start of a valid answer and nothing is filtered at the end.

Letter Combinations of a Phone Number asks for every word a digit string spells on a keypad, where 2 is `abc`, 3 is `def` and so on: `"23"` gives nine words, `ad` to `cf`, and the empty string gives `[]`. Here recursion is a nested `for` loop whose depth is only known at run time: level i picks a letter for `digits[i]`, and each loop is nested inside the one before.

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

Cutting a string is the next shape: the path is a list of pieces, and a choice is where the next piece ends. Palindrome Partitioning asks for every way to cut a string so that each piece reads the same both ways: `"aab"` gives `["a", "a", "b"]` and `["aa", "b"]`. Restore IP Addresses asks for every way to read a digit string as four numbers from 0 to 255 with no leading zero: `"25525511135"` gives `255.255.11.135` and `255.255.111.35`.

Each piece must pass its test before it is chosen, and the IP version also fixes the number of pieces, so "complete" means four pieces and no digits left over. In the code, `partition_palindromes` tries every end for the next piece and keeps the ends that make a palindrome; `restore_ip_addresses` does the same with pieces of one to three digits, exactly four of them.

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

Grids come next, because now the shared state is the board itself. The path is a snake of cells, and a cell on the snake must not be stepped on twice. Flood fill in [Graphs I](#s17), which paints every cell connected to a start cell, asks whether a cell can be reached, so a visited cell stays visited and the cost is O(cells). A path search asks which cells form this path, so a cell is free again once the path backs off it.

Word Search asks whether a word can be traced through side-by-side cells, each used once: on the board `ABCE / SFCS / ADEE`, `"ABCCED"` can be traced and `"ABCB"` cannot, because it would stand on the same B twice. Instead of a `visited` set, stand on a cell only if it shows the letter you need, cover it with `#`, ask the four neighbours for the next letter, and put the letter back on the way out.

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

N-Queens comes next because a choice is checked against everything placed so far, not only the last item. It asks for every way to place n queens on an n×n board so that no two share a row, column or diagonal, drawn as strings: n = 4 has two boards, n = 1 has one, and n = 2 and n = 3 have none.

A queen at `(r, c)` owns one column, one `\` diagonal, where every square has the same `r - c`, and one `/` diagonal, where every square has the same `r + c`. Three sets answer "attacked?" in O(1), so a bad square is never even entered. In the code, fill the board one row at a time, and a column is a choice only if no earlier queen owns that column or either diagonal through the square.

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

The last medium shape turns take/skip into a k-way choice: level i decides which bucket gets item i. Partition to K Equal Sum Subsets asks whether the numbers can be split into k groups with equal sums: `[4, 3, 2, 3, 5, 2, 1]` with k = 4 can, as 5, 4+1, 3+2 and 3+2. Matchsticks to Square is the same question with k = 4 and every stick used.

Two prunes make it fast. Big items go first, so a dead end shows up near the root. And if item i failed in an empty bucket, it fails in every other empty bucket too, because empty buckets are interchangeable, so stop trying. In the code, the items are sorted biggest first, each bucket the item still fits in is tried, and once the item has failed in an empty bucket no other empty bucket is offered.

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

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic. Each one is the same skeleton with heavier bookkeeping.

Expression Add Operators asks for every way to put `+`, `-` or `*` between the digits of a string, or nothing, to make a longer number, so that the expression equals a target: `"123"` with target 6 gives `1+2+3` and `1*2*3`. The search carries the value so far and the last term, because `*` binds tighter than `+` and `-`: `*x` takes the last term back out and puts it back multiplied.

```text
expr      value   last
2           2       2       "+x": value + x, last x       "-x": value - x, last -x
2-3        -1      -3       "*x": value - last + last * x, last last * x
2-3*4     -10     -12       -1 - (-3) + (-12) = -10, the same as 2 - 12
```

At each position the choice is how many digits the next number takes and which operator goes in front of it. The running value and the last term travel as arguments, so a `*` is fixed up without re-reading the expression, and a number with a leading zero ends the loop, because every longer piece from the same start has one too.

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
- Add `print(expr, value, last)` inside `if value == target:` and run `add_operators("234", -10)`: it prints `2-3*4 -10 -12`, the last row of the picture, and returns `['2-3*4']`.

Unique Paths III counts the walks from the start cell, marked 1, to the end cell, marked 2, that step on every empty cell, marked 0, exactly once and never touch an obstacle, marked −1: the grid `[[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]]` has two such walks.

It is word search plus a counter of cells still owed, which starts at the number of empty cells plus one for the end cell itself. Block each cell while you stand on it and unblock it on the way out. The end cell counts a walk only when nothing is owed, and every other cell returns the sum of what its neighbours return: `count += dfs(...)`, the "how many ways" shape.

Sudoku Solver fills the `.` cells of a 9×9 board so that every row, column and 3×3 box holds each digit once. It is the constraint sets of N-Queens with more bookkeeping: one set of used digits per row, per column and per box, where the box of `(r, c)` is `r // 3 * 3 + c // 3`, and each empty cell tries only the digits in none of its three sets.

It stops at the first solution and leaves the board filled in, the deliberate exception from trap 9: wrong guesses are taken back, but the right ones are the answer. The repo version keeps the sets as bitmasks and always fills the cell with the fewest legal digits first.

Remove Invalid Parentheses asks for every string you get by deleting the fewest brackets that make the input valid: `"()())()"` gives `(())()` and `()()()`. It counts first, then searches: one balance pass tells you how many `(` and `)` must go, so the search only decides which ones, and never lets the open count drop below zero. In the code, each bracket is deleted if the budget allows and kept if the string stays valid so far.

The 24 Game asks whether four cards make exactly 24 with `+`, `-`, `*`, `/` and brackets, each card used once: `[4, 1, 8, 7]` can, as (8 − 4) · (7 − 1), and `[1, 2, 1, 2]` cannot. Any such expression is three steps of "replace two numbers by one result", so the code tries every pair and each of its six results, which covers every bracketing, and recurses on three numbers, then two, then one.

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

Robot Room Cleaner hands you a robot in an unknown room with only four calls, `move()`, `turnLeft()`, `turnRight()` and `clean()`, and asks you to clean every reachable cell; you know neither the map nor the position nor the heading. It has physical moves and no undo button: the robot's position is the state, so "un-choose" means walking back.

The parent cell is right behind the robot, so "turn around, step, turn around" restores both position and heading, and turning right after each of the four tries brings the heading back to where it started. Every caller finds the robot exactly as it left it: the backtracking invariant, enforced with motors.

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

> "This is Combination Sum II: every combination of the candidates that sums to the target, each index used at most once. Can candidates repeat, can one be reused, and may answers come in any order?
>
> The brute force tries all 2^n index subsets, sums each, and dedupes with a set of sorted tuples: O(n·2^n), and it finishes subsets whose first numbers already overshoot.
>
> I'll build combinations one number at a time instead: one shared path, choices from `start` on so each combination is built in one order only, complete when the remaining sum is zero. I sort first, so I can `break` once a number exceeds what's left, and skip a value equal to its left sibling so nothing is built twice.
>
> Worst case is still O(n·2^n), at most 2^n nodes and O(n) to copy each answer, but most branches die early. Extra space is O(n)."

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
