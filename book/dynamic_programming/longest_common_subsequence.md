# Longest Common Subsequence

*LeetCode 1143 · Medium · Pattern: 2-D DP over two prefixes · Reading time ~7 min*

## The problem

Given two strings text1 and text2, return the length of their longest common subsequence, a sequence of characters
appearing in both in the same order but not necessarily contiguously.

```text
Example: "abcde" and "ace" -> 3 ("ace"); "abc" and "def" -> 0.
```

## What the problem is really asking

Given two strings, find the length of the longest sequence of characters that appears in both, in the same order, but not necessarily next to each other. Deleting characters from either string is allowed; reordering is not.

The answer is a length. What makes it hard is that a string of length `m` has `2^m` subsequences, and matching one string's characters to the other's involves choices: an `a` in the first string might match any of several `a`s in the second, and an early greedy match can block better ones later.

```text
 text1:  a  b  c  d  e
         |     |     |
 text2:  a     c     e        LCS = "ace", length 3

 the matching lines never cross: order is preserved
```

## Do it by hand first

Lay one string down the side and the other across the top, and fill a grid where cell `(i, j)` answers "LCS of the first `i` characters of text1 and the first `j` of text2". An empty prefix gives 0, so the first row and column are zeros. Then fill row by row.

```text
            ""   a    c    e
       ""    0    0    0    0
       a     0    1    1    1
       b     0    1    1    1
       c     0    1    2    2     c = c: 1 + up-left (1)
       d     0    1    2    2
       e     0    1    2    3     e = e: 1 + up-left (2)
```

When the two last characters were equal, your hand added 1 to the diagonal neighbour. When they differed, it copied the larger of the cell above and the cell to the left. Three neighbours, one rule. That grid is the whole algorithm.

## The first honest attempt

Recursion on prefix lengths, looking at the last characters:

- If `text1[i-1] == text2[j-1]`: `lcs(i, j) = 1 + lcs(i-1, j-1)`.
- Otherwise: `lcs(i, j) = max(lcs(i-1, j), lcs(i, j-1))`.
- `lcs(0, j) = lcs(i, 0) = 0`.

Every mismatch branches twice, and each branch shrinks only one string, so the tree can reach about `2^(m+n)` nodes. The repeated work shows up quickly:

```text
                 lcs(4,2)   "abcd" vs "ac"   d != c
               /                     \
        lcs(3,2) "abc","ac"     lcs(4,1) "abcd","a"
        c == c                   d != a
           |                    /        \
        lcs(2,1)  <-- A    lcs(3,1)     lcs(4,0)=0
                           c != a
                          /       \
                     lcs(2,1) <-- B   lcs(3,0)=0

  A and B are the same question: "ab" vs "a"
```

`lcs(i, j)` depends only on the two prefix lengths, and there are only `(m+1)(n+1)` pairs. The recursion re-derives each one from scratch along every route that reaches it.

## The turning point

**Claim: if the last characters match, some LCS ends with that character in both strings; if they do not match, at least one of the two last characters is unused, so dropping one of them loses nothing.**

Justify the match case with an exchange. Suppose `text1[i-1] == text2[j-1] == ch`, and an optimal common subsequence does not pair those two final positions. If it ends with `ch` matched to an earlier position, re-point that match to the last positions; nothing crosses, the length is unchanged. If it does not end with `ch` at all, append `ch` and it gets longer, a contradiction. So pairing the last characters is always safe, and the rest is the LCS of the two shorter prefixes: `1 + dp[i-1][j-1]`.

For the mismatch case: the last characters cannot be paired with each other, and they cannot both be paired with something else (those two lines would cross). So one of them is unused, and the answer is the better of dropping the last of text1 or the last of text2.

- **State:** `dp[i][j]` = LCS length of `text1[:i]` and `text2[:j]`.
- **Recurrence:** match: `dp[i-1][j-1] + 1`; mismatch: `max(dp[i-1][j], dp[i][j-1])`.
- **Base:** row 0 and column 0 are 0.
- **Order:** rows top to bottom, columns left to right, so up, left and up-left are ready.
- **Space:** a row reads only the previous row and itself, so keep two rows. The solution swaps the strings so the columns are the shorter one: O(min(m, n)) space.

```text
            j-1      j
   i-1   [ UL ]  [ U  ]       match:    UL + 1
   i     [ L  ]  [ X  ]       mismatch: max(U, L)

   prev row holds UL and U; cur row holds L as it fills
```

With a single row you would overwrite `UL` before you need it (it is `prev[j-1]`, which became `cur[j-1]` one step ago), so a one-row version must save the diagonal in a temporary. Two rows avoid the trap at the cost of one extra row.

## Watch it work

`text1 = "abcde"` (rows), `text2 = "ace"` (columns). Each frame shows `prev` after a row is finished.

**Frame 1.** Start: `prev = [0, 0, 0, 0]` (the empty prefix of text1).

```text
          ""  a   c   e
 prev:  [ 0,  0,  0,  0 ]
```

Nothing matches an empty string.

**Frame 2.** Row `a`: `a == a` gives `prev[0] + 1 = 1`; then `c`, `e` mismatch and copy the left value 1.

```text
          ""  a   c   e
 row a: [ 0,  1,  1,  1 ]
              ^ diagonal + 1
```

**Frame 3.** Row `b`: no matches; every cell is `max(up, left)`.

```text
          ""  a   c   e
 row b: [ 0,  1,  1,  1 ]
```

The `b` contributes nothing; the best stays "a".

**Frame 4.** Row `c`: column `c` matches, `up-left (1) + 1 = 2`; column `e` copies left, 2.

```text
          ""  a   c   e
 row c: [ 0,  1,  2,  2 ]
                  ^ "ac"
```

**Frame 5.** Row `d`: no matches, a copy of the previous row.

```text
          ""  a   c   e
 row d: [ 0,  1,  2,  2 ]
```

**Frame 6.** Row `e`: column `e` matches, `up-left (2) + 1 = 3`.

```text
          ""  a   c   e
 row e: [ 0,  1,  2,  3 ]  <- answer prev[-1] = 3
```

Invariant across frames: after finishing row `i`, `prev[j]` was the exact LCS of `text1[:i]` and `text2[:j]` for every `j`, and values never decreased moving right or down.

## Why it is correct

Induction in fill order. When cell `(i, j)` is computed, its three neighbours are final and correct. The case split on the last characters is exhaustive: match (pairing them is safe, by the exchange above) or mismatch (one is unused, so the answer is the better of the two drops). So the cell is correct, and the bottom-right cell is the LCS of the full strings.

To recover the subsequence itself, keep the full table and walk back from the corner: on a match step diagonally and record the character; otherwise step toward the larger of up and left. The diagonal steps form a staircase path.

## Cost

- **Brute force:** O(2^(m+n)) time, O(m+n) stack.
- **Full table:** O(m x n) time, O(m x n) space.
- **Two rows:** O(m x n) time, O(min(m, n)) space.

## Variations you will meet

- **Longest Common Substring:** contiguous, so a mismatch resets the cell to 0 and the answer is the maximum cell anywhere, not the corner.
- **Edit Distance (LC 72):** same grid, three operations; mismatch takes `1 + min(up, left, diagonal)`.
- **Delete Operation for Two Strings (LC 583):** `m + n - 2 x LCS`.
- **Shortest Common Supersequence (LC 1092):** build the LCS table, then walk back emitting characters from both strings.

## What to carry forward

Two sequences mean a grid over two prefixes; compare the last characters, take the diagonal on a match, otherwise drop one side. The next problem has only one sequence, and its O(n^2) DP will be beaten by a smarter structure: patience sorting.
