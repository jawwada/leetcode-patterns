---
rank: 54
slug: word_search
---

Given a grid of letters and a word, decide whether the word can be spelled along a path of horizontally or vertically adjacent cells, using each cell at most once. In the grid with rows `ABCE`, `SFCS` and `ADEE`, the word `ABCCED` is there, while `ABCB` is not, because its second `B` would have to reuse a cell.

A path is a sequence of choices, so this is backtracking on the grid. Every cell is tried as the start. From a cell that matches `word[k]`, the search steps to each of the four neighbors looking for `word[k + 1]`, and it succeeds when k reaches the length of the word. The path must not cross itself, so before stepping on, the cell is overwritten with `#`, a character no word contains, and once the search from that cell is over, the letter is written back. The mark replaces a visited set, and it folds the visited test into the letter test, because `#` never equals `word[k]`.

Picture a snake growing through the grid. Its body is the marked cells, its head tries the neighbors in a fixed order (down, up, right, left), and when the head is stuck the snake pulls back one cell and unmarks it, so that a different path may use that cell later.

```text
board       "ABCCED": k on its path       "ABCB": the board when k = 3
A B C E     0 1 2 .                       # # # E    the C at (0,2) needs a B,
S F C S     . . 3 .                       S F C S    and its only B neighbor
A D E E     . 5 4 .                       A D E E    is '#': dead end

ABCCED at k = 5: down is off the grid, up is '#', right is E, left is D ✓
ABCB: unmark C, B, A in turn; the other A, at (2,0), fails at once: false
```

```pseudo
FUNCTION Dfs(board, word, row, col, k)
    IF k = len(word)
        RETURN true                          // every letter matched
    IF row < 0 OR row ≥ len(board) OR col < 0 OR col ≥ len(board[0])
        RETURN false                         // off the grid
    IF board[row][col] ≠ word[k]
        RETURN false                         // wrong letter, or a '#'
    board[row][col] ← '#'                    // mark: on the path now
    found ← false
    FOR EACH (d_row, d_col) IN [(1, 0), (-1, 0), (0, 1), (0, -1)]
        IF Dfs(board, word, row + d_row, col + d_col, k + 1)
            found ← true
            BREAK
    board[row][col] ← word[k]                // unmark on the way back
    RETURN found

FUNCTION Exist(board, word)
    FOR row FROM 0 TO len(board) - 1
        FOR col FROM 0 TO len(board[0]) - 1
            IF Dfs(board, word, row, col, 0)
                RETURN true
    RETURN false
```

Each of the `m · n` starts grows paths of up to L cells, and after the first step the cell behind the head is always marked, so at most three ways lead on: the worst case is `O(m · n · 3^L)`, usually quoted as the looser `O(m · n · 4^L)`, with `O(L)` recursion depth. Two cheap prunes help in practice. Count the letters of the grid first and answer false if the word needs more of some letter than the grid holds; and if the word's last letter is rarer in the grid than its first, search for the reversed word instead, so fewer starts pass the first test. Signals: a grid, a path through adjacent cells, no reuse, one word. For many words at once, the trie-guided version is #63. The classic mistake is forgetting to write the letter back: the `#` stays behind and blocks later paths, and on this grid a failed search for `ABCB` would leave every `A` marked, so a following search for `ABCCED` would wrongly say false.

*Practice:* LC 79 Word Search · LC 212 Word Search II
