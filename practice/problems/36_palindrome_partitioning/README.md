# Palindrome Partitioning (LeetCode 131)

**Area:** backtracking · **Difficulty:** Medium · **Key operations:** choose a palindromic prefix, recurse on the rest, record at the end, undo the choice

## Problem

Given a string `s`, return every way to split `s` into pieces such that each piece is a palindrome. Any order of partitions is accepted; the practice script returns them sorted so the result is deterministic.

## Example

```
s = "aab"
cuts:  a|a|b   -> ["a", "a", "b"]   all palindromes
       aa|b    -> ["aa", "b"]       all palindromes
       a|ab    -> "ab" is not a palindrome
       aab     -> not a palindrome
answer: [["a", "a", "b"], ["aa", "b"]]
```

## Brute force

There are `n - 1` gaps between characters and each gap either has a cut or not: `2^(n-1)` cut masks. Build the pieces for every mask and keep the masks whose pieces are all palindromes.

O(2^n · n) time. The wasted work: a mask whose *first* piece is not a palindrome is still fully built and checked, and so are all `2^k` masks that share that first piece. `"abc..."` with a first piece `"ab"` can never work, yet half of the masks starting that way are enumerated one by one.

## From brute force to optimal

Decide the cuts left to right instead of all at once. At position `start`, the next piece is some prefix `s[start:end]`. If that prefix is not a palindrome, no partition beginning with it can succeed, so skip it and all its continuations in one stroke. If it is, commit to it, solve the rest of the string recursively, and then **undo** the choice to try the next prefix. Reaching `start == len(s)` means the whole string has been consumed by palindromic pieces: record a copy of the current path.

This is backtracking: the brute force explores all leaves of the cut tree; the backtracking explores only the branches whose every piece so far is a palindrome, pruning dead subtrees at their root.

## Intuition

Picture a tree of choices. The root is "nothing chosen yet, standing at position 0". Each child is "I take this prefix as the next piece"; a child is only grown if the piece is a palindrome. A leaf is reached when the position hits the end of the string, and the path from the root to that leaf *is* one partition. `path` is the list of pieces along the current branch: push a piece when stepping down, pop it when stepping back up. Because `path` is reused and mutated, record `path[:]`, a snapshot, not `path` itself. The palindrome test is a plain two-pointer scan from both ends; no table is needed.

## Walkthrough

Indentation is the depth of the recursion (the length of `path`).

```
at 0: path []
try 'a': palindrome
    choose 'a'                 path ['a']
    at 1
    try 'a': palindrome
        choose 'a'             path ['a', 'a']
        at 2
        try 'b': palindrome
            choose 'b'         path ['a', 'a', 'b']
            at 3 = len(s)  ->  record ['a', 'a', 'b']
            undo 'b'           path ['a', 'a']
        undo 'a'               path ['a']
    try 'ab': not a palindrome, skip        (prunes every partition starting a | ab...)
    undo 'a'                   path []
try 'aa': palindrome
    choose 'aa'                path ['aa']
    at 2
    try 'b': palindrome
        choose 'b'             path ['aa', 'b']
        at 3 = len(s)  ->  record ['aa', 'b']
        undo 'b'               path ['aa']
    undo 'aa'                  path []
try 'aab': not a palindrome, skip
result (sorted): [['a', 'a', 'b'], ['aa', 'b']]
```

As a tree:

```
                 []
          /       |        \
       'a'       'aa'      'aab' x
      /    \       |
    'a'   'ab' x  'b'  -> record ['aa','b']
     |
    'b'  -> record ['a','a','b']
```

## Steps

1. `result = []`, `path = []`. Define `backtrack(start)`.
2. If `start == len(s)`: `result.append(path[:])` and return.
3. For `end` from `start + 1` to `len(s)` inclusive: `piece = s[start:end]`.
4. If `piece` is a palindrome (two pointers): `path.append(piece)`, `backtrack(end)`, `path.pop()`.
5. Call `backtrack(0)`; return `result`.

## Complexity

O(n · 2^n) time in the worst case (all characters equal: every cut mask is a valid partition and each costs O(n) to copy and check). O(n) extra space for the recursion depth and `path`, not counting the output.

## Pitfalls

- **Recording `path` instead of `path[:]`.** Every recorded partition is the same list object, which the backtracking empties again on the way out; the result is a list of empty lists.
- **`range(start + 1, len(s))` instead of `len(s) + 1`.** The last character can never be included in a piece, `backtrack(len(s))` is never reached, nothing is recorded.
- **Right pointer starting at `len(piece)`.** Off by one in the palindrome check: IndexError on the first non-empty piece. It starts at `len - 1`.
- **Forgetting the `path.pop()`.** Pieces from one branch leak into the next; partitions come out with extra pieces.
- **Reaching for a memo table of palindromes.** Fine for a speed-up, but it is dynamic programming; the two-pointer check keeps the solution a pure backtracking exercise and the asymptotic bound is unchanged.
