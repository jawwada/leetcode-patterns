"""
Autocomplete: Collect Words with a Prefix - Basics
Area: tries
Key operations: walk to the prefix node, DFS below it in sorted child order, emit a word at every end flag

Given a word list and a prefix, return every stored word that starts with the prefix, in sorted order
(duplicates in the input count once). Walk the trie down to the prefix node, then depth-first search
its subtree visiting children in alphabetical order so the words come out sorted for free.
Example: words [car, card, care, cat, dog], prefix "car" -> [car, card, care]
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
def brute_force(words: List[str], prefix: str) -> List[str]:
    """Test every word with startswith and sort the survivors. O(total length + k log k)."""
    return sorted(w for w in set(words) if w.startswith(prefix))


# --- optimal ---
def insert(root: TrieNode, word: str) -> None:
    node = root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]
    node.end = True

def solve(words: List[str], prefix: str) -> List[str]:
    """Build the trie, walk the prefix (O(len)), then DFS only the matching subtree (O(output size))."""
    root = TrieNode()
    for w in words:
        insert(root, w)
    log(f"trie {to_dict(root)}")
    node = root
    for ch in prefix:
        if ch not in node.children:
            log(f"prefix breaks at '{ch}': no matches")
            return []
        node = node.children[ch]
        log(f"follow '{ch}' -> subtree {to_dict(node)}")
    out = []

    def dfs(node, path):
        log(f"    {'  ' * (len(path) - len(prefix))}at '{path}'{' (word)' if node.end else ''}, children {sorted(node.children)}")
        if node.end:
            out.append(path)
        for ch in sorted(node.children):
            dfs(node.children[ch], path + ch)
    dfs(node, prefix)
    return out


# --- demo ---
def demo():
    return solve(["car", "card", "care", "cat", "dog"], "car")


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # the demo already showed the trace; keep the test run silent
    assert solve(["car", "card", "care", "cat", "dog"], "car") == ["car", "card", "care"]
    assert solve(["car", "card", "care", "cat", "dog"], "ca") == ["car", "card", "care", "cat"]
    assert solve(["car", "card", "care", "cat", "dog"], "x") == []
    assert solve(["car", "card", "care", "cat", "dog"], "") == ["car", "card", "care", "cat", "dog"]  # all
    assert solve(["b", "a", "ab"], "") == ["a", "ab", "b"]              # sorted, not insertion order
    assert solve(["a", "a"], "a") == ["a"]                              # duplicates once
    assert solve([], "a") == []
    import random
    rng = random.Random(7)
    for _ in range(200):
        words = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 3))) for _ in range(rng.randint(0, 6))]
        prefix = "".join(rng.choice("ab") for _ in range(rng.randint(0, 2)))
        assert solve(words, prefix) == brute_force(words, prefix), (words, prefix)


# --- bugs ---
BUGS = [
    {
        "replace": "        for ch in sorted(node.children):",
        "with":    "        for ch in node.children:",
        "fix": "visit children in sorted order; a dict iterates in insertion order, which is the order words were added",
        "why": "Words [b, a] with prefix '' come out as [b, a]; the output is only sorted when the children are visited alphabetically.",
        "decoys": [
            {"line": "        if node.end:", "change": "should be if not node.children:"},
            {"line": "            out.append(path)", "change": "should append path + ch"},
            {"line": "            return []", "change": "should return [prefix]"},
        ],
    },
    {
        "replace": "    dfs(node, prefix)",
        "with":    "    dfs(node, \"\")",
        "fix": "the path accumulated by the DFS must start with the prefix already walked, otherwise only suffixes are collected",
        "why": "For prefix 'car' the output is ['', 'd', 'e'] instead of ['car', 'card', 'care'].",
        "decoys": [
            {"line": "            dfs(node.children[ch], path + ch)", "change": "should pass path"},
            {"line": "    for ch in prefix:", "change": "should iterate prefix[1:]"},
            {"line": "    out = []", "change": "should be out = [prefix]"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
