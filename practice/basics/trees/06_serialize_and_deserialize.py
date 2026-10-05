"""
Serialize and Deserialize Binary Tree (LeetCode 297) - Basics
Area: trees
Key operations: preorder emit with '#' for None, consume tokens with one shared iterator, build left then right

Turn a binary tree into a string and the string back into the same tree. Preorder with an explicit
'#' for every missing child is unambiguous, so decoding can consume the tokens in the same order.
Example: [1, 2, 3, None, None, 4, 5] -> "1,2,#,#,3,4,#,#,5,#,#" -> the same tree
"""
import sys
from collections import deque

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build_tree(vals):  # level order, None = missing child (LeetCode style)
    nodes = [TreeNode(v) if v is not None else None for v in vals]
    kids = iter(nodes[1:])
    for node in nodes:
        if node:
            node.left, node.right = next(kids, None), next(kids, None)
    return nodes[0] if nodes else None


# --- brute force ---
def brute_force(root):
    """Level-order list in the LeetCode input format (the inverse of build_tree): BFS with None placeholders, trailing Nones trimmed. O(n) but needs a queue and None bookkeeping."""
    out, q = [], deque([root])
    while q:
        node = q.popleft()
        out.append(node.val if node else None)
        if node:
            q.extend((node.left, node.right))
    while out and out[-1] is None:
        out.pop()
    return out


# --- optimal ---
def serialize(root):
    """Preorder tokens, '#' for a missing child, joined by commas. O(n)."""
    out = []

    def rec(node):
        if node is None:
            out.append("#")
            log(f"  emit # (missing child)      -> {','.join(out)}")
            return
        out.append(str(node.val))
        log(f"  emit {node.val} then its children -> {','.join(out)}")
        rec(node.left)
        rec(node.right)
    rec(root)
    return ",".join(out)


def deserialize(data):
    """One iterator shared by every call consumes the tokens in preorder; '#' closes a branch. O(n)."""
    tokens = iter(data.split(","))

    def rec():
        tok = next(tokens)
        if tok == "#":
            log("  read #: empty subtree")
            return None
        node = TreeNode(int(tok))
        log(f"  read {tok}: make the node, now build its left subtree, then its right")
        node.left = rec()
        node.right = rec()
        return node
    return rec()


def solve(root):
    """Round trip: encode, decode, encode again; the two strings must match."""
    data = serialize(root)
    log(f"serialized: {data}")
    again = serialize(deserialize(data))
    assert again == data, (data, again)
    return data


# --- demo ---
def demo():
    return solve(build_tree([1, 2, 3, None, None, 4, 5]))


# --- tests ---
def random_tree(rng, n):
    """Random shape with random values in -50..99 (multi-digit and negative values must survive)."""
    nodes = [TreeNode(rng.randint(-50, 99)) for _ in range(n)]
    for i in range(1, n):
        while True:
            p = nodes[rng.randrange(i)]
            if p.left is None or p.right is None:
                break
        side = rng.choice([s for s in ("left", "right") if getattr(p, s) is None])
        setattr(p, side, nodes[i])
    return nodes[0] if n else None


def tests():
    assert solve(build_tree([1, 2, 3, None, None, 4, 5])) == "1,2,#,#,3,4,#,#,5,#,#"
    assert solve(None) == "#"
    assert deserialize("#") is None
    assert solve(build_tree([7])) == "7,#,#"
    assert solve(build_tree([12, -3])) == "12,-3,#,#,#"                   # multi-digit and negative
    assert solve(build_tree([1, None, 2, None, 3])) == "1,#,2,#,3,#,#"    # right chain
    assert brute_force(deserialize("1,2,#,#,3,4,#,#,5,#,#")) == [1, 2, 3, None, None, 4, 5]
    import random
    rng = random.Random(6)
    for _ in range(200):
        root = random_tree(rng, rng.randint(0, 12))
        back = deserialize(solve(root))
        assert brute_force(back) == brute_force(root)        # same shape and values, checked by an independent encoding


# --- bugs ---
BUGS = [
    {
        "replace": "    tokens = iter(data.split(\",\"))",
        "with":    "    tokens = data.split(\",\")",
        "fix": "wrap the token list in iter() so every recursive call consumes from the same position",
        "why": "next() on a plain list raises TypeError; the deeper mistake is that without one shared iterator each call would have to pass an index around.",
        "decoys": [
            {"line": "        node.left = rec()", "change": "should build the right subtree first"},
            {"line": "        tok = next(tokens)", "change": "should be next(tokens, '#')"},
            {"line": "        node = TreeNode(int(tok))", "change": "should keep tok as a string"},
        ],
    },
    {
        "replace": "    return \",\".join(out)",
        "with":    "    return \"\".join(out)",
        "fix": "join the tokens with a separator so multi-digit and negative values stay distinct tokens",
        "why": "Without commas '12,-3' becomes '12-3##' and split(',') returns one unparsable token: int('12-3###') raises.",
        "decoys": [
            {"line": "            out.append(\"#\")", "change": "should append None"},
            {"line": "        out.append(str(node.val))", "change": "should append after the children"},
            {"line": "    rec(root)", "change": "should be rec(root.left)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
