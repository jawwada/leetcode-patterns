"""
Trie: Delete a Word with Pruning - Basics
Area: tries
Key operations: walk down recording the path, clear the end flag, unwind pruning children that are empty and not word ends, stop at a shared node

Insert words into a trie, then delete some of them. Deleting a word clears its end flag and removes
every node below the last shared point that no other word needs; a node is kept if it still has
children or ends another word. Return the final trie as a nested dict ("$": True marks a word end).
Example: words [apple, app, ape], delete [apple, app, cat] -> {'a': {'p': {'e': {'$': True}}}}
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.end = False    # a word ends here

def to_dict(node):  # nested dict view; "$" marks a word end
    d = {"$": True} if node.end else {}
    d.update((c, to_dict(n)) for c, n in node.children.items())
    return d


# --- brute force ---
def brute_force(words: List[str], removals: List[str]) -> dict:
    """Rebuild the nested dict from scratch out of the words that survive. O(total length)."""
    root = {}
    for w in set(words) - set(removals):
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True
    return root


# --- optimal ---
def insert(root: TrieNode, word: str) -> None:
    node = root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]
    node.end = True

def delete(root: TrieNode, word: str) -> bool:
    """Record the path down; clear the flag; walk back up deleting nodes that are empty and end no word. O(len)."""
    path = [root]
    for ch in word:
        if ch not in path[-1].children:
            log(f"delete '{word}': path breaks at '{ch}', nothing to do")
            return False
        path.append(path[-1].children[ch])
    if not path[-1].end:
        log(f"delete '{word}': path exists but no word ends there, nothing to do")
        return False
    path[-1].end = False
    log(f"delete '{word}': walked {' -> '.join(word)}, cleared end flag")
    for i in range(len(word) - 1, -1, -1):
        node, child = path[i], path[i + 1]
        if child.children or child.end:
            log(f"    keep '{word[i]}': {'has children' if child.children else 'ends another word'}; stop")
            break
        del node.children[word[i]]
        log(f"    prune '{word[i]}': empty and ends no word")
    return True

def solve(words: List[str], removals: List[str]) -> dict:
    """Insert everything, delete each removal (missing words are no-ops), return the trie as a nested dict."""
    root = TrieNode()
    for w in words:
        insert(root, w)
    log(f"after inserts: {to_dict(root)}")
    for w in removals:
        delete(root, w)
        log(f"    trie now {to_dict(root)}")
    return to_dict(root)


# --- demo ---
def demo():
    return solve(["apple", "app", "ape"], ["apple", "app", "cat"])


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # the demo already showed the trace; keep the test run silent
    assert solve(["apple", "app", "ape"], ["apple", "app", "cat"]) == {"a": {"p": {"e": {"$": True}}}}
    assert solve(["cat"], ["cat"]) == {}                                     # whole branch pruned to the root
    assert solve(["cat", "car"], ["cat"]) == {"c": {"a": {"r": {"$": True}}}}  # shared prefix survives
    assert solve(["app", "apple"], ["app"]) == {"a": {"p": {"p": {"l": {"e": {"$": True}}}}}}  # only the flag
    assert solve(["apple"], ["app"]) == {"a": {"p": {"p": {"l": {"e": {"$": True}}}}}}  # prefix is not a word
    assert solve(["a"], ["a", "a"]) == {}                                     # second delete is a no-op
    assert solve([], ["x"]) == {}
    import random
    rng = random.Random(7)
    for _ in range(200):
        words = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 3))) for _ in range(rng.randint(0, 5))]
        removals = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 3))) for _ in range(rng.randint(0, 4))]
        assert solve(words, removals) == brute_force(words, removals), (words, removals)


# --- bugs ---
BUGS = [
    {
        "replace": "        if child.children or child.end:",
        "with":    "        if child.children:",
        "fix": "a node that ends another word must survive even when it has no children",
        "why": "Deleting 'apple' after inserting 'app' prunes the second 'p' node and erases 'app' with it.",
        "decoys": [
            {"line": "        del node.children[word[i]]", "change": "should delete child.children[word[i]]"},
            {"line": "    path[-1].end = False", "change": "should be path[-1].end = None"},
            {"line": "        path.append(path[-1].children[ch])", "change": "should append path[-1]"},
        ],
    },
    {
        "replace": "    for i in range(len(word) - 1, -1, -1):",
        "with":    "    for i in range(len(word) - 1, 0, -1):",
        "fix": "the unwind must reach i = 0 so the root's own child can be pruned",
        "why": "Stopping at i = 1 never removes the first letter: deleting the only word 'cat' leaves an empty 'c' node behind.",
        "decoys": [
            {"line": "        node, child = path[i], path[i + 1]", "change": "should be path[i - 1], path[i]"},
            {"line": "    if not path[-1].end:", "change": "should be if path[-1].children:"},
            {"line": "    path = [root]", "change": "should start as an empty list"},
        ],
    },
    {
        "replace": "    if not path[-1].end:",
        "with":    "    if path[-1].end:",
        "fix": "bail out when NO word ends at the final node; an inverted test refuses to delete real words",
        "why": "Every real word is rejected with False, and deleting a non-word prefix clears nothing but may prune its branch.",
        "decoys": [
            {"line": "        if ch not in path[-1].children:", "change": "should test path[0].children"},
            {"line": "            return False", "change": "should return True"},
            {"line": "            break", "change": "should be continue"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
