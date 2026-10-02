"""
Word Search II (LeetCode 212)  — Hard
Pattern: Trie-guided grid backtracking

Problem
-------
Given an m x n board of letters and a list of words, return every word
that can be spelled by a path of horizontally/vertically adjacent cells
without reusing a cell.
Example: board=[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],
["i","f","l","v"]], words=["oath","pea","eat","rain"] -> ["eat","oath"].

Brute force
-----------
Run Word Search I for every word: from every cell start a backtracking
search for that specific word. O(W * m * n * 4^L) time. The repeated work
is enormous: words sharing a prefix ("oath", "oats") re-explore the exact
same board paths from scratch, and every start cell is revisited once per
word even when no word begins with that letter.

From brute force to optimal
---------------------------
The board paths are the expensive part, so explore them ONCE and check
all words simultaneously. Put the words in a trie; a DFS from each cell
descends the trie in lockstep with the path, so a cell whose letter is
not a child of the current trie node is pruned immediately, and reaching
a node that stores a word emits it. Three refinements keep it fast: store
the word at its terminal node and pop it when found (so duplicates are
never emitted and the search for that word stops), mark visited cells in
place with a sentinel instead of a visited set, and delete trie branches
that have become empty so later cells do not re-walk dead paths.
Invariant: the current trie node corresponds exactly to the letters on
the current path.

Intuition
---------
Backtracking explores paths; a trie tells you after every step whether
ANY remaining word could still match, so dead paths die at the first
wrong letter. Each board path is walked at most once for all words
together instead of once per word.

Geometric view
--------------
Two structures move together: a path snaking through the grid and a
pointer walking down a branching trie diagram. Every grid step must have
a matching trie edge; when the trie pointer lands on a node holding a
word, that word is harvested and the node is emptied, and empty branches
are pruned so the trie shrinks as words are found.

Steps
-----
1. Build the trie; at each word's last node store node["$"] = word.
2. For every cell whose letter is a child of the trie root, call dfs(r, c, trie).
3. dfs: node = parent[letter]; if "$" in node pop it and record the word.
4. Mark board[r][c] = "#", recurse into the 4 neighbours whose letter is in node, restore.
5. If node is now empty, delete it from parent (prune).
6. Return the collected words.

Complexity: O(m * n * 4 * 3^(L-1)) time worst case, O(total word characters)
space — each cell starts a DFS of depth at most L with at most 3 onward
choices per step; the trie bounds depth and prunes most branches.
Pitfalls: not restoring the cell after backtracking; emitting a word twice
when it appears on two paths; forgetting to stop descending when the trie
has no matching child; using a set of visited cells (slow) instead of an
in-place marker.
"""
from typing import List


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        trie: dict = {}
        for w in words:
            node = trie
            for ch in w:
                node = node.setdefault(ch, {})
            node["$"] = w                      # store the whole word at its terminal node

        rows, cols = len(board), len(board[0])
        found: List[str] = []

        def dfs(r: int, c: int, parent: dict) -> None:
            ch = board[r][c]
            node = parent[ch]
            word = node.pop("$", None)         # harvest once; the word can never be re-emitted
            if word is not None:
                found.append(word)
            board[r][c] = "#"                  # in-place visited marker for this path
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                    dfs(nr, nc, node)
            board[r][c] = ch
            if not node:                       # branch exhausted: prune it from the trie
                del parent[ch]

        for r in range(rows):
            for c in range(cols):
                if board[r][c] in trie:
                    dfs(r, c, trie)
        return found


def brute_force(board: List[List[str]], words: List[str]) -> List[str]:
    # Word Search I for every word independently: each restarts backtracking from every cell.
    rows, cols = len(board), len(board[0])

    def exists(r: int, c: int, word: str, i: int) -> bool:
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False
        saved, board[r][c] = board[r][c], "#"
        ok = any(exists(nr, nc, word, i + 1)
                 for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))
        board[r][c] = saved
        return ok

    return [w for w in words
            if any(exists(r, c, w, 0) for r in range(rows) for c in range(cols))]


if __name__ == "__main__":
    s = Solution()
    board1 = [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]]
    cases = [(board1, ["oath", "pea", "eat", "rain"], ["eat", "oath"]),
             (board1, ["oath", "oat", "oa", "o"], ["o", "oa", "oat", "oath"]),   # shared prefixes
             ([["a", "b"], ["c", "d"]], ["abcb"], []),                            # cell reuse forbidden
             ([["a"]], ["a"], ["a"]),
             ([["a", "a"]], ["aaa"], []),
             ([["a", "b"], ["c", "d"]], ["ab", "cb", "ad", "bd", "ac", "ca", "da", "bc", "db", "abdc", "abb", "acb"],
              ["ab", "abdc", "ac", "bd", "ca", "db"])]                           # diagonals are not adjacent
    for board, words, want in cases:
        assert sorted(s.findWords([row[:] for row in board], words)) == want, words
        assert sorted(brute_force([row[:] for row in board], words)) == want, words
    print("ok")
