"""
Design Add and Search Words Data Structure (LeetCode 211) - Basics
Area: tries
Key operations: trie insert, DFS search that follows one child per letter, '.' branches into every child, end flag at the last character

Support addWord(word) and search(pattern) where the pattern may contain '.' matching any single
letter. Search is a depth-first walk: a letter follows exactly one child, a '.' tries all of them,
and the pattern matches only if a word ends where the pattern ends.
Example: addWord bad, dad, mad; search pad -> False, bad -> True, ".ad" -> True, "b.." -> True
"""
import sys
from typing import List, Tuple

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
def brute_force(ops: List[Tuple[str, str]]) -> List[bool]:
    """Keep a set of words; a search compares the pattern with every stored word of the same length. O(words * len)."""
    words, out = set(), []
    for op, w in ops:
        if op == "addWord":
            words.add(w)
        else:
            out.append(any(len(x) == len(w) and all(p == "." or p == c for p, c in zip(w, x)) for x in words))
    return out


# --- optimal ---
def insert(root: TrieNode, word: str) -> None:
    node = root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]
    node.end = True

def search(node: TrieNode, word: str, i: int = 0) -> bool:
    """DFS over the pattern: letters follow one child, '.' tries all children. O(26^dots * len) worst case."""
    if i == len(word):
        log(f"    {'  ' * i}pattern exhausted, end flag {node.end}")
        return node.end
    ch = word[i]
    log(f"    {'  ' * i}depth {i} '{ch}': children {sorted(node.children)}")
    if ch == ".":
        return any(search(child, word, i + 1) for child in node.children.values())
    if ch not in node.children:
        log(f"    {'  ' * i}no child '{ch}': dead end")
        return False
    return search(node.children[ch], word, i + 1)

def solve(ops: List[Tuple[str, str]]) -> List[bool]:
    """Drive addWord / search; return the search results in order."""
    root, out = TrieNode(), []
    for op, word in ops:
        if op == "addWord":
            insert(root, word)
            log(f"addWord '{word}': trie {to_dict(root)}")
        else:
            log(f"search '{word}':")
            out.append(search(root, word))
            log(f"    -> {out[-1]}")
    return out


# --- demo ---
def demo():
    return solve([("addWord", "bad"), ("addWord", "dad"), ("addWord", "mad"),
                  ("search", "pad"), ("search", "bad"), ("search", ".ad"), ("search", "b..")])


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # the demo already showed the trace; keep the test run silent
    assert solve([("addWord", "bad"), ("addWord", "dad"), ("addWord", "mad"),
                  ("search", "pad"), ("search", "bad"), ("search", ".ad"), ("search", "b..")]) == [False, True, True, True]
    assert solve([("search", "a"), ("search", ".")]) == [False, False]            # empty structure
    assert solve([("addWord", "bad"), ("search", "ba"), ("search", "b.")]) == [False, False]   # prefix is not a word
    assert solve([("addWord", "bad"), ("search", "bad."), ("search", "....")]) == [False, False]  # too long
    assert solve([("addWord", "a"), ("addWord", "ab"), ("search", "."), ("search", "..")]) == [True, True]
    assert solve([("addWord", "ab"), ("addWord", "ac"), ("search", "a.")]) == [True]
    import random
    rng = random.Random(7)
    for _ in range(200):
        ops = []
        for _ in range(rng.randint(1, 10)):
            if rng.random() < 0.5:
                ops.append(("addWord", "".join(rng.choice("ab") for _ in range(rng.randint(1, 3)))))
            else:
                ops.append(("search", "".join(rng.choice("ab.") for _ in range(rng.randint(1, 3)))))
        assert solve(ops) == brute_force(ops), ops


# --- bugs ---
BUGS = [
    {
        "replace": "        return node.end",
        "with":    "        return True",
        "fix": "reaching the end of the pattern is not enough: a word must END at this node",
        "why": "After addWord('bad'), search('ba') and search('b.') walk to the 'a' node and return True.",
        "decoys": [
            {"line": "    if i == len(word):", "change": "should be i == len(word) - 1"},
            {"line": "    ch = word[i]", "change": "should be word[i + 1]"},
            {"line": "    return search(node.children[ch], word, i + 1)", "change": "should pass i"},
        ],
    },
    {
        "replace": "        return any(search(child, word, i + 1) for child in node.children.values())",
        "with":    "        return any(search(child, word, i + 1) for child in node.children)",
        "fix": "iterate over the child NODES (.values()); iterating a dict yields its keys, the characters",
        "why": "Each child is a one-letter string, so the recursive call touches .children on a str and raises AttributeError on the first '.' pattern.",
        "decoys": [
            {"line": "    if ch not in node.children:", "change": "should be if ch in node.children:"},
            {"line": "        return False", "change": "should return node.end"},
            {"line": "            out.append(search(root, word))", "change": "should pass i = 1"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
