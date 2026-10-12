"""
Word Search II - Trie-Guided Grid Backtracking

Given a grid of letters and a list of words, return every word that can be
spelled along a path of adjacent cells (up, down, left, right), each cell
used at most once per word: grid oaan / etae / ihkr / iflv with words
oath, pea, eat, rain -> ['oath', 'eat'] (any order).
"""


# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}              # letter -> TrieNode
        self.word = None                # the whole word, at its last node


# --- algorithm ---
def build_trie(words):
    """Insert every word; its last node keeps the word. O(total letters)."""
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = word
    return root


def dfs(board, row, col, parent, found):
    """Step onto (row, col) only if the trie goes on with its letter."""
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        return
    ch = board[row][col]
    if ch not in parent.children:
        return                          # no word goes this way (or a '#')
    node = parent.children[ch]
    if node.word is not None:
        found.append(node.word)
        node.word = None                # record each word only once
    board[row][col] = "#"               # mark: on the current path
    for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        dfs(board, row + d_row, col + d_col, node, found)
    board[row][col] = ch                # unmark on the way back
    if len(node.children) == 0:
        del parent.children[ch]         # prune: no word is left below


def find_words(board, words):
    """One trie, one DFS from every cell. O(m * n * 3^L), L the longest."""
    root = build_trie(words)
    found = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            dfs(board, row, col, root, found)
    return found


# --- try it ---
board = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
print(find_words(board, ["oath", "pea", "eat", "rain"]))  # -> ['oath', 'eat']
print(find_words(board, ["oat", "oath", "eath"]))  # -> ['oat', 'oath', 'eath']
print(find_words([list("ab")], ["ab", "ba", "aba"]))      # -> ['ab', 'ba']
print(find_words([list("ab"), list("cd")], ["abcb"]))     # -> []
