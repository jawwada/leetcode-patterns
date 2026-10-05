"""
Word Squares (LeetCode 425) - Hard
Chapter: tries
Pattern: Prefix trie + row-by-row backtracking

Given distinct words that all have length n, return every word square: n words (reuse
allowed) such that the k-th row and the k-th column read the same word.
Example: ["area", "lead", "wall", "lady", "ball"] -> [["ball", "area", "lead", "lady"],
["wall", "area", "lead", "lady"]].
"""


# --- brute force ---
def is_symmetric(rows):
    """True if the letter grid reads the same across and down: rows[r][c] == rows[c][r]."""
    n = len(rows)
    for r in range(n):
        for c in range(n):
            if rows[r][c] != rows[c][r]:
                return False
    return True


def fill(words, n, rows, out):
    """Put every word in the next row until n rows are placed, then test the whole square."""
    if len(rows) == n:
        if is_symmetric(rows):              # symmetry is checked only once the square is full
            out.append(rows[:])
        return
    for word in words:
        rows.append(word)
        fill(words, n, rows, out)
        rows.pop()


def brute_force(words):
    """Try every ordered n-tuple of words, repetition allowed. O(W^n * n^2) time."""
    n = len(words[0])
    out = []
    fill(words, n, [], out)
    return out


# --- optimal ---
def candidates(trie, prefix):
    """Indices of the words that start with prefix: walk the trie and read the list stored there."""
    node = trie
    for letter in prefix:
        if letter not in node:
            return []
        node = node[letter]
    return node["$"]


def backtrack(words, n, trie, square, squares):
    """Fill row k with a word whose prefix is column k of the rows placed so far."""
    k = len(square)
    if k == n:
        squares.append(square[:])
        return
    prefix = ""
    for row in square:
        prefix += row[k]                    # column k so far dictates how row k must start
    for i in candidates(trie, prefix):
        square.append(words[i])
        backtrack(words, n, trie, square, squares)
        square.pop()


def word_squares(words):
    """Trie nodes list the words passing through them; backtrack row by row. O(W * n) build."""
    n = len(words[0])
    trie = {"$": list(range(len(words)))}   # the empty prefix (row 0) matches every word
    for i in range(len(words)):
        node = trie
        for letter in words[i]:
            if letter not in node:
                node[letter] = {"$": []}
            node = node[letter]
            node["$"].append(i)             # every prefix node remembers this word
    squares = []
    backtrack(words, n, trie, [], squares)
    return squares


# --- try the brute force ---
print(sorted(brute_force(["area", "lead", "wall", "lady", "ball"])))
# -> [['ball', 'area', 'lead', 'lady'], ['wall', 'area', 'lead', 'lady']]
print(sorted(brute_force(["abat", "baba", "atan", "atal"])))
# -> [['baba', 'abat', 'baba', 'atal'], ['baba', 'abat', 'baba', 'atan']]
print(sorted(brute_force(["ab", "ba", "aa"])))
# -> [['aa', 'aa'], ['aa', 'ab'], ['ab', 'ba'], ['ba', 'aa'], ['ba', 'ab']]
print(sorted(brute_force(["abc", "def"])))                  # -> []


# --- try the optimal ---
print(sorted(word_squares(["area", "lead", "wall", "lady", "ball"])))
# -> [['ball', 'area', 'lead', 'lady'], ['wall', 'area', 'lead', 'lady']]
print(sorted(word_squares(["abat", "baba", "atan", "atal"])))
# -> [['baba', 'abat', 'baba', 'atal'], ['baba', 'abat', 'baba', 'atan']]
print(sorted(word_squares(["ab", "ba", "aa"])))
# -> [['aa', 'aa'], ['aa', 'ab'], ['ab', 'ba'], ['ba', 'aa'], ['ba', 'ab']]
print(sorted(word_squares(["abc", "def"])))                 # -> []
