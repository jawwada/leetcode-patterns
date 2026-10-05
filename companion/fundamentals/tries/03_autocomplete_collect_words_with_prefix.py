"""
Autocomplete: Collect Words with a Prefix - Fundamentals
Chapter: fundamentals/tries
Key operations: walk to the prefix node, DFS below in sorted child order, emit at each end flag

Given a word list and a prefix, return every stored word that starts with the prefix, in sorted
order (duplicates in the input count once). Walk the trie down to the prefix node, then DFS its
subtree visiting children in alphabetical order so the words come out sorted for free.
Example: words [car, card, care, cat, dog], prefix "car" -> [car, card, care]
"""


# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}   # char -> TrieNode
        self.end = False     # a word ends here


# --- algorithm ---
def insert(root, word):
    """Walk down creating missing links, then flag the last node as a word end. O(len)."""
    node = root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]
    node.end = True


def build_trie(words):
    """Insert every word under a fresh root. O(total length)."""
    root = TrieNode()
    for word in words:
        insert(root, word)
    return root


def collect(node, word_so_far, out):
    """DFS below node in alphabetical child order; every end flag emits one word."""
    if node.end:
        out.append(word_so_far)
    for ch in sorted(node.children):   # sorted children -> sorted output for free
        collect(node.children[ch], word_so_far + ch, out)


def words_with_prefix(root, prefix):
    """Walk the prefix (O(len)), then DFS only the matching subtree (O(output size))."""
    node = root
    for ch in prefix:
        if ch not in node.children:
            return []   # the path breaks: nothing starts with this prefix
        node = node.children[ch]
    out = []
    collect(node, prefix, out)   # start the DFS with the prefix already spelled
    return out


# --- try it ---
root = build_trie(["car", "card", "care", "cat", "dog"])
print(words_with_prefix(root, "car"))   # -> ['car', 'card', 'care']
print(words_with_prefix(root, "ca"))    # -> ['car', 'card', 'care', 'cat']
print(words_with_prefix(root, "d"))     # -> ['dog']
print(words_with_prefix(root, "x"))     # -> []
print(words_with_prefix(root, ""))      # -> ['car', 'card', 'care', 'cat', 'dog']
