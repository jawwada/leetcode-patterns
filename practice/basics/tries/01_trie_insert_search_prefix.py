"""
Trie: Insert, Search, StartsWith - Basics
Area: tries
Key operations: walk or create one child per character, mark the end flag, search checks the end flag, startsWith only needs the path

A trie stores words as a tree of characters: each node has a dict of children and a flag saying
whether a word ends there. Drive a list of ops: ("insert", w) adds w, ("search", w) asks whether the
whole word w was inserted, ("startsWith", p) asks whether any inserted word begins with p.
Return the booleans in order.
Example: insert apple, search apple, search app, startsWith app, insert app, search app
      -> [True, False, True, True]
"""
import sys
from typing import List, Optional, Tuple

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.end = False    # a word ends here

def to_dict(node):  # nested dict view for the trace; "$" marks a word end
    d = {"$": True} if node.end else {}
    d.update((c, to_dict(n)) for c, n in node.children.items())
    return d


# --- brute force ---
def brute_force(ops: List[Tuple[str, str]]) -> List[bool]:
    """Keep the words in a set; startsWith scans every word. O(total length) per prefix query."""
    words, out = set(), []
    for op, w in ops:
        if op == "insert":
            words.add(w)
        elif op == "search":
            out.append(w in words)
        else:
            out.append(any(x.startswith(w) for x in words))
    return out


# --- optimal ---
def insert(root: TrieNode, word: str) -> None:
    node = root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = TrieNode()
            log(f"    create child '{ch}'")
        node = node.children[ch]
    node.end = True
    log(f"    path {' -> '.join(word)}, end flag set; trie {to_dict(root)}")

def find(root: TrieNode, s: str) -> Optional[TrieNode]:
    node = root
    for ch in s:
        if ch not in node.children:
            log(f"    path breaks at '{ch}' (children here: {sorted(node.children)})")
            return None
        node = node.children[ch]
    log(f"    walked {' -> '.join(s) or '(root)'}, end flag {node.end}")
    return node

def search(root: TrieNode, word: str) -> bool:
    node = find(root, word)
    return node is not None and node.end

def starts_with(root: TrieNode, prefix: str) -> bool:
    return find(root, prefix) is not None

def solve(ops: List[Tuple[str, str]]) -> List[bool]:
    """Each op walks at most len(word) nodes: O(len) per op, independent of how many words are stored."""
    root, out = TrieNode(), []
    for op, word in ops:
        log(f"{op} '{word}':")
        if op == "insert":
            insert(root, word)
        elif op == "search":
            out.append(search(root, word))
        else:
            out.append(starts_with(root, word))
        log(f"    -> {out[-1] if op != 'insert' else 'done'}")
    return out


# --- demo ---
def demo():
    return solve([("insert", "apple"), ("search", "apple"), ("search", "app"),
                  ("startsWith", "app"), ("insert", "app"), ("search", "app")])


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # the demo already showed the trace; keep the test run silent
    assert solve([("insert", "apple"), ("search", "apple"), ("search", "app"),
                  ("startsWith", "app"), ("insert", "app"), ("search", "app")]) == [True, False, True, True]
    assert solve([]) == []
    assert solve([("search", "a"), ("startsWith", "a")]) == [False, False]        # empty trie
    assert solve([("insert", "a"), ("search", "ab"), ("startsWith", "ab")]) == [False, False]  # longer than stored
    assert solve([("insert", "ab"), ("startsWith", ""), ("search", "")]) == [True, False]      # empty prefix/word
    assert solve([("insert", "a"), ("insert", "a"), ("search", "a")]) == [True]              # duplicate insert
    import random
    rng = random.Random(7)
    for _ in range(200):
        ops = []
        for _ in range(rng.randint(1, 10)):
            w = "".join(rng.choice("ab") for _ in range(rng.randint(1, 3)))
            ops.append((rng.choice(["insert", "search", "startsWith"]), w))
        assert solve(ops) == brute_force(ops), ops


# --- bugs ---
BUGS = [
    {
        "replace": "    return node is not None and node.end",
        "with":    "    return node is not None",
        "fix": "search must also check the end flag; reaching the node only proves the prefix exists",
        "why": "After inserting 'apple', search('app') walks to the 'p' node and reports True although 'app' was never inserted.",
        "decoys": [
            {"line": "    return find(root, prefix) is not None", "change": "should also check .end"},
            {"line": "    node.end = True", "change": "should be root.end = True"},
            {"line": "        if op == \"insert\":", "change": "should also append True"},
        ],
    },
    {
        "replace": "            return None",
        "with":    "            break",
        "fix": "a missing child means the string is not in the trie: return None, do not fall through to the last node reached",
        "why": "With break, find returns the deepest node matched so far; insert 'a' then search 'ab' returns the 'a' node, whose end flag is True.",
        "decoys": [
            {"line": "            node.children[ch] = TrieNode()", "change": "should be node.children[ch] = node"},
            {"line": "    node = find(root, word)", "change": "should pass word[:-1]"},
            {"line": "            out.append(search(root, word))", "change": "should append find(root, word)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
