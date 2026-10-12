# Letter Combinations of a Phone Number (LeetCode 17)

**Area:** backtracking · **Difficulty:** Medium · **Key operations:** one recursion level per digit, append a letter, recurse to the next digit, pop on return

## Problem

Given a string of digits 2-9, return every string the digits could spell on a phone keypad (2 = abc, 3 = def, 4 = ghi, 5 = jkl, 6 = mno, 7 = pqrs, 8 = tuv, 9 = wxyz). The empty string gives `[]`.

## Example

```
"23" -> ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
```

Three letters for 2, three for 3, so 3 × 3 = 9 strings.

## Brute force

Take the Cartesian product of the letter groups (`itertools.product("abc", "def")`) and join each tuple. Equivalently, grow a list level by level: start with `[""]`, and for each digit replace the list with every existing string extended by every letter of that digit.

O(n · 4^n) time, which is the size of the output, so the time cannot be beaten. The waste is in memory: every intermediate level is fully materialised (3 strings, then 9, then 27, ...) and every extension copies its whole prefix, so the high-water mark is the entire previous level plus the output, O(4^n).

## From brute force to optimal

The choices form a tree of depth n with 3 or 4 children per node. A depth-first walk only ever needs the one prefix on the current root-to-node path. Keep that prefix in a single shared list: append a letter on the way down, recurse, pop it on the way back up. Every leaf is emitted with O(1) incremental work and O(n) auxiliary memory. Time is still O(n · 4^n) because that is how many characters the answer has; what the recursion buys is constant extra space and the template that extends naturally when some branches must be skipped.

## Intuition

You want n nested for-loops, one per digit, but n is only known at run time. Recursion is how you write a variable-depth nested loop: level `i` owns `digits[i]` and tries each of its letters, delegating the remaining digits to level `i + 1`. The shared path is the pencil line from the root to where you are; it grows by one letter going down and shrinks by one coming back up. There is no pruning here, every leaf is an answer, so the whole tree is walked.

## Walkthrough

`digits = "23"`. Indentation is the recursion depth.

```
level 0, digit 2
  choose 'a'       path [a]
    level 1, digit 3
      choose 'd'   path [a, d]   depth 2 == len -> record "ad"
      pop          path [a]
      choose 'e'   path [a, e]   record "ae"
      pop          path [a]
      choose 'f'   path [a, f]   record "af"
      pop          path [a]
  pop              path []
  choose 'b'       path [b]
    level 1, digit 3
      'd' -> "bd", 'e' -> "be", 'f' -> "bf"   (same dance: push, record, pop)
  pop              path []
  choose 'c'       path [c]
    level 1, digit 3
      'd' -> "cd", 'e' -> "ce", 'f' -> "cf"
  pop              path []
result: [ad, ae, af, bd, be, bf, cd, ce, cf]
```

The path never holds more than two letters even though nine strings are produced.

## Steps

1. If `digits` is empty, return `[]`. Map each digit to its letters.
2. `dfs(i)`: if `i == len(digits)`, record `"".join(path)` and return.
3. For each letter of `digits[i]`: append it, call `dfs(i + 1)`, pop it.
4. Call `dfs(0)`; return `result`.

## Complexity

O(n · 4^n) time: up to 4^n leaves, each joined in O(n). O(n) extra space for the path and the recursion stack, beyond the output.

## Pitfalls

- **Stopping at `len(digits) - 1`.** The leaf is reached when every digit has a letter, which is `i == len(digits)`. One level early records prefixes: `"23"` returns `["a", "b", "c"]`.
- **`pop(0)` instead of `pop()`.** The letter chosen at this level is the last one; popping the front removes the first digit's letter and leaves this level's in place, so after `"ad"` the next leaf reads `"de"`.
- **Returning `[""]` for empty input.** The empty string has no combinations; LeetCode expects `[]`.
- **Forgetting that 7 and 9 have four letters.** Hard-coding 3 per digit undercounts.
- **`dfs(i)` instead of `dfs(i + 1)`.** Infinite recursion.
