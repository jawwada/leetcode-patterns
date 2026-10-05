"""
Trie: Delete a Word with Pruning - Fundamentals
Chapter: fundamentals/tries
Key operations: path down, clear end flag, prune empty non-end nodes upward, stop at a shared node

Insert words into a trie, then delete some of them. Deleting a word clears its end flag and
removes every node below the last shared point that no other word needs; a node is kept if it
still has children or ends another word. The trie is shown as a nested dict ("$" marks a word end).
Example: words [apple, app, ape], delete [apple, app, cat] -> {'a': {'p': {'e': {'$': True}}}}
"""


# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}   # char -> TrieNode
        self.end = False     # a word ends here


def trie_to_dict(node):
    """Nested dict view of the trie; "$" marks a word end."""
    view = {}
    if node.end:
        view["$"] = True
    for ch in node.children:
        view[ch] = trie_to_dict(node.children[ch])
    return view


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


def delete(root, word):
    """Record the path down, clear the end flag, prune empty non-end nodes upward. O(len)."""
    path = [root]
    node = root
    for ch in word:
        if ch not in node.children:
            return False   # the word is not in the trie
        node = node.children[ch]
        path.append(node)
    if not node.end:
        return False   # the prefix exists but no word ends here
    node.end = False
    for i in range(len(word) - 1, -1, -1):   # unwind from the deepest node toward the root
        parent = path[i]
        child = path[i + 1]
        if child.children or child.end:   # another word still needs this node: stop pruning
            break
        del parent.children[word[i]]
    return True


# --- try it ---
root = build_trie(["app", "ape"])
print(trie_to_dict(root))     # -> {'a': {'p': {'p': {'$': True}, 'e': {'$': True}}}}
insert(root, "apple")
print(delete(root, "apple"))  # -> True   (prunes 'l' and 'e'; 'app' still ends a word)
print(delete(root, "app"))    # -> True   (only the flag goes; 'ape' still needs 'a' and 'p')
print(delete(root, "cat"))    # -> False  (not in the trie)
print(delete(root, "ap"))     # -> False  (a prefix, not a stored word)
print(trie_to_dict(root))     # -> {'a': {'p': {'e': {'$': True}}}}
