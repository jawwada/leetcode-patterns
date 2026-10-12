# Practice bank: file format

Every script in `practice/` is self-contained (standard library only, no local imports), runs with
`python3 <file>` printing a traced demo then `ok`, and runs silently with `python3 <file> --quiet`.
`python3 practice/build_bank.py` validates every file and builds `practice/bank.json` for the drill artifact.

## Script layout (markers are mandatory, in this order)

```python
"""
<Title> (LeetCode <n>) - <Medium | Medium-Hard | Basics>
Area: <area name>
Key operations: <the 2-4 operations this problem drills, comma separated>

<Problem statement in 2-5 lines, with one worked example input -> output.>
"""
import sys
from collections import deque            # only what the file needs

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---            (optional: ListNode, TreeNode, build_list, to_list ...)

# --- brute force ---        (required for problems; optional for basics)
def brute_force(...):
    """One line on the idea and its complexity."""

# --- optimal ---            (required; this is the code the learner studies and debugs)
def solve(...):
    """One line on the idea and its complexity."""

# --- demo ---               (required: calls solve on the docstring example and returns the result)
def demo():
    return solve(...)

# --- tests ---              (required: deterministic asserts first, then a randomized cross-check)
def tests():
    assert solve(...) == ...
    ...

# --- bugs ---               (required: >= 2 variants for problems, >= 1 for basics)
BUGS = [
    {
        "replace": "<one exact line of the optimal section, including indentation>",
        "with":    "<the same line with ONE realistic mistake>",
        "fix": "<how to fix it, one line, no line number>",
        "why": "<what goes wrong and on which input, 1-2 sentences>",
        "decoys": [
            {"line": "<exact correct line>", "change": "<a plausible but wrong change>"},
            {"line": "<exact correct line>", "change": "<...>"},
            {"line": "<exact correct line>", "change": "<...>"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
```

## Rules

- **Trace output.** The optimal section calls `log(...)` after every key operation (push, pop, swap,
  pointer move, heap push/pop, visit, shrink/expand) and prints the structure's state in a readable form:
  a stack top to bottom, a window as `[l..r]` with its contents, a heap as its array, a linked list as
  `1 -> 2 -> 3`, a dict as `{k: v}`. Label the decision taken, as in `pop day 2 (75 < 76)`.
- **`log` is always a standalone statement**, never the only statement in a block and never part of an
  expression. The build strips every line whose code starts with `log(` and the remainder must still
  compile and pass the tests. Multi-line `log(` calls are not allowed.
- **Shown program length** (helpers + optimal without log lines + demo) 15-45 non-blank lines for problems, 10-45 for basics. Aim for an optimal section of 15-30 lines; add a small helper (node class, builder) when the problem needs one.
- **Bug variants.** `replace` must match exactly one line of the shown program (helpers + stripped
  optimal + demo). `with` differs from it by one realistic mistake an experienced engineer makes
  (strictness of a comparison, off by one, wrong order of two statements, mark in the wrong place, stale
  entry not skipped, wrong shrink condition, aliasing, wrong return). Never a syntax error or a renamed
  variable. The build runs the tests against the buggy program and **rejects a variant the tests do not
  catch** (it must assert, raise, or hang past 5 seconds). Each decoy names a *different* correct line
  and a change that would break it or change nothing; the three decoys and the fix should read about the
  same length.
- **Tests** cover the docstring example, the empty/single/duplicate/edge cases, and compare `solve` with
  `brute_force` on ~200 random small inputs (seeded by the build). Tests must finish in under 2 seconds.
- **Brute force** is the obvious method (try everything), written clearly; its docstring states the
  complexity and the wasted work the optimal method removes.
- No dynamic programming anywhere in the bank.

## README.md next to each problem (problems only; basics get one README per area)

```
# <Title> (LeetCode <n>)

**Area:** ... · **Difficulty:** ... · **Key operations:** ...

## Problem
## Example
## Brute force          (idea, complexity, what work is wasted)
## From brute force to optimal   (the observation that removes the waste)
## Intuition            (the mental picture, 3-6 sentences)
## Walkthrough          (the docstring example traced step by step in a code block, drawing the structure after each step)
## Steps                (numbered, as you would say them in the interview)
## Complexity
## Pitfalls             (each bug variant's mistake explained, plus any other classic slip)
```

Area README (`practice/basics/<area>/README.md`): what the structure/technique is, the core operations with
their costs, a drawn example, the invariant to remember, then the exercise list (file, what it drills).
