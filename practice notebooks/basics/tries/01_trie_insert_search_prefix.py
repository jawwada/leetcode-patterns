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
from typing import List, Optional, Tuple


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
        node = node.children[ch]
    node.end = True

def find(root: TrieNode, s: str) -> Optional[TrieNode]:
    node = root
    for ch in s:
        if ch not in node.children:
            return None
        node = node.children[ch]
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
        if op == "insert":
            insert(root, word)
        elif op == "search":
            out.append(search(root, word))
        else:
            out.append(starts_with(root, word))
    return out


# --- demo ---
def demo():
    return solve([("insert", "apple"), ("search", "apple"), ("search", "app"),
                  ("startsWith", "app"), ("insert", "app"), ("search", "app")])


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
    print("result:", demo())
