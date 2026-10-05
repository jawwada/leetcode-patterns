"""
Word Search II (LeetCode 212) - Hard
Chapter: tries
Pattern: Trie-guided grid backtracking

Given an m x n board of letters and a list of words, return every word that can be spelled
by a path of horizontally or vertically adjacent cells without reusing a cell.
Example: board [[o,a,a,n],[e,t,a,e],[i,h,k,r],[i,f,l,v]], words [oath,pea,eat,rain] -> [eat, oath].
"""


# --- helpers ---
STEPS = [(1, 0), (-1, 0), (0, 1), (0, -1)]      # down, up, right, left


# --- brute force ---
def exists(board, row, col, word, i):
    """True if word[i:] can be spelled starting at (row, col) without reusing cells."""
    if i == len(word):
        return True
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        return False
    if board[row][col] != word[i]:
        return False
    saved = board[row][col]
    board[row][col] = "#"                   # mark the cell used while this path is alive
    for step_row, step_col in STEPS:
        if exists(board, row + step_row, col + step_col, word, i + 1):
            board[row][col] = saved
            return True
    board[row][col] = saved                 # undo the mark before trying another path
    return False


def found_anywhere(board, word):
    """Word Search I: start a backtracking search for this one word from every cell."""
    for row in range(len(board)):
        for col in range(len(board[0])):
            if exists(board, row, col, word, 0):
                return True
    return False


def brute_force(board, words):
    """Run Word Search I once per word, re-exploring the board each time. O(W * m * n * 4^L)."""
    found = []
    for word in words:
        if found_anywhere(board, word):
            found.append(word)
    return found


# --- optimal ---
def dfs(board, row, col, parent, found):
    """Walk the board and the trie together; parent is the trie node for the path so far."""
    letter = board[row][col]
    node = parent[letter]
    if "$" in node:
        found.append(node["$"])             # harvest the word once ...
        del node["$"]                       # ... and never emit it again
    board[row][col] = "#"                   # in-place visited marker
    for step_row, step_col in STEPS:
        next_row = row + step_row
        next_col = col + step_col
        if next_row < 0 or next_row >= len(board) or next_col < 0 or next_col >= len(board[0]):
            continue
        if board[next_row][next_col] in node:       # only follow letters the trie still wants
            dfs(board, next_row, next_col, node, found)
    board[row][col] = letter
    if len(node) == 0:
        del parent[letter]                  # this branch is exhausted: prune it from the trie


def find_words(board, words):
    """Explore the board once with a trie of all words guiding the search. O(m * n * 4^L)."""
    trie = {}
    for word in words:
        node = trie
        for letter in word:
            if letter not in node:
                node[letter] = {}
            node = node[letter]
        node["$"] = word                    # the whole word sits at its last node
    found = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] in trie:     # no word starts with this letter: skip the cell
                dfs(board, row, col, trie, found)
    return found


# --- try the brute force ---
board = [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]]
small = [["a", "b"], ["c", "d"]]
print(sorted(brute_force(board, ["oath", "pea", "eat", "rain"])))   # -> ['eat', 'oath']
print(sorted(brute_force(board, ["oath", "oat", "oa", "o"])))       # -> ['o', 'oa', 'oat', 'oath']
print(sorted(brute_force(small, ["abcb"])))                         # -> []
print(sorted(brute_force(small, ["ab", "cb", "bd", "ca", "abdc"])))  # -> ['ab', 'abdc', 'bd', 'ca']


# --- try the optimal ---
board = [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]]
small = [["a", "b"], ["c", "d"]]
print(sorted(find_words(board, ["oath", "pea", "eat", "rain"])))    # -> ['eat', 'oath']
print(sorted(find_words(board, ["oath", "oat", "oa", "o"])))        # -> ['o', 'oa', 'oat', 'oath']
print(sorted(find_words(small, ["abcb"])))                          # -> []
print(sorted(find_words(small, ["ab", "cb", "bd", "ca", "abdc"])))   # -> ['ab', 'abdc', 'bd', 'ca']
