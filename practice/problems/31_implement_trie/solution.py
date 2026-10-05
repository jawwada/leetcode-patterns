"""
Implement Trie (Prefix Tree) (LeetCode 208) - Medium
Area: tries
Key operations: walk one node per character, create the missing child on insert, end flag, prefix walk

Design a trie with insert(word), search(word) -> is this exact word stored, and startsWith(prefix)
-> does some stored word begin with prefix. Here solve(ops) runs a list of ("insert" | "search" |
"startsWith", string) operations and returns the results of the search / startsWith calls in order.
Example: insert "apple", search "apple", search "app", startsWith "app", insert "app", search "app"
-> [True, False, True, True]
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
        self.end = False    # a stored word ends at this node


def draw(node: TrieNode, depth=0) -> List[str]:
    """One character per line, indented by depth; * marks the end of a stored word."""
    lines = []
    for ch, child in sorted(node.children.items()):
        lines.append("  " * depth + ch + (" *" if child.end else ""))
        lines += draw(child, depth + 1)
    return lines


# --- brute force ---
def brute_force(ops: List[Tuple[str, str]]) -> List[bool]:
    """Keep a set of words. search is a set lookup, but startsWith rescans every stored word and
    re-reads the letters shared by 'apple', 'apply', 'app' once per word: O(N * L) per prefix query."""
    words, results = set(), []
    for op, s in ops:
        if op == "insert":
            words.add(s)
        elif op == "search":
            results.append(s in words)
        else:
            results.append(any(w.startswith(s) for w in words))
    return results


# --- optimal ---
def solve(ops: List[Tuple[str, str]]) -> List[bool]:
    """Shared prefixes are stored once as a shared path. Every operation walks one node per
    character, so it costs O(L) no matter how many words are stored. Space O(total characters)."""
    root = TrieNode()
    results = []
    for op, s in ops:
        log(f"{op}({s!r})")
        node = root
        found = True
        for i, ch in enumerate(s):
            if ch not in node.children:
                if op != "insert":
                    found = False
                    log(f"    at {s[:i]!r}: no child {ch!r} -> the path breaks")
                    break
                node.children[ch] = TrieNode()
                log(f"    at {s[:i]!r}: create child {ch!r}")
            node = node.children[ch]
            log(f"    walk to {s[:i + 1]!r}  end={node.end}  children {sorted(node.children)}")
        if op == "insert":
            node.end = True
            log("    mark end at " + repr(s) + "; trie now:\n" + "\n".join("        " + l for l in draw(root)))
        elif op == "search":
            results.append(found and node.end)
            log(f"    search: whole word walked={found}, end flag={node.end} -> {found and node.end}")
        else:
            results.append(found)
            log(f"    startsWith: whole prefix walked -> {found}")
    return results


# --- demo ---
def demo():
    return solve([("insert", "apple"), ("search", "apple"), ("search", "app"),
                  ("startsWith", "app"), ("insert", "app"), ("search", "app")])


# --- tests ---
def tests():
    assert solve([("insert", "apple"), ("search", "apple"), ("search", "app"),
                  ("startsWith", "app"), ("insert", "app"), ("search", "app")]) == [True, False, True, True]
    assert solve([("search", "a"), ("startsWith", "a")]) == [False, False]  # empty trie
    assert solve([("insert", "a"), ("search", "a"), ("startsWith", "a"), ("search", "ab")]) == [True, True, False]
    assert solve([("insert", "ab"), ("insert", "ab"), ("search", "ab"), ("search", "a")]) == [True, False]  # duplicate insert
    assert solve([("insert", "app"), ("insert", "apple"), ("search", "appl"), ("startsWith", "appl"),
                  ("search", "app"), ("search", "apple")]) == [False, True, True, True]
    assert solve([("insert", "apple"), ("startsWith", "apple"), ("startsWith", "apples")]) == [True, False]
    import random
    for _ in range(200):
        ops = []
        for _ in range(random.randint(1, 12)):
            w = "".join(random.choice("ab") for _ in range(random.randint(1, 4)))
            ops.append((random.choice(["insert", "search", "search", "startsWith", "startsWith"]), w))
        assert solve(ops) == brute_force(ops), ops


# --- bugs ---
BUGS = [
    {
        "replace": "            results.append(found and node.end)",
        "with":    "            results.append(found)",
        "fix": "search needs found and the end flag on the last node",
        "why": "Walking the whole word only proves it is a prefix of some stored word; after inserting only 'apple', search('app') must be False but returns True.",
        "decoys": [
            {"line": "            results.append(found)", "change": "should be found and node.end"},
            {"line": "        found = True", "change": "should start as False"},
            {"line": "            node.end = True", "change": "should be set before the walk, on root"},
        ],
    },
    {
        "replace": "            results.append(found)",
        "with":    "            results.append(found and node.end)",
        "fix": "startsWith only needs the prefix path, no end flag",
        "why": "Requiring the end flag turns startsWith into search: after inserting 'apple', startsWith('app') returns False instead of True.",
        "decoys": [
            {"line": "            results.append(found and node.end)", "change": "should be just found"},
            {"line": "                node.children[ch] = TrieNode()", "change": "should be node.children[ch] = root"},
            {"line": "        node = root", "change": "should be node = TrieNode()"},
        ],
    },
    {
        "replace": "            if ch not in node.children:",
        "with":    "            if ch not in root.children:",
        "fix": "check the current node's children, not the root's",
        "why": "Checking the root makes every lookup only see first letters: after inserting 'apple', startsWith('app') fails at 'p', and inserting 'app' overwrites the child 'p' under 'a' so 'apple' is lost.",
        "decoys": [
            {"line": "            node = node.children[ch]", "change": "should be node = root.children[ch]"},
            {"line": "                if op != \"insert\":", "change": "should be op == \"insert\""},
            {"line": "                    break", "change": "should be continue"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
