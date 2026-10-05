"""
Tree Traversals, Recursive and Iterative - Basics
Area: trees
Key operations: visit before/between/after the children, push right then left for preorder, push-left-then-pop for inorder

Return the preorder, inorder and postorder of a binary tree. One recursive walk records all three;
an explicit stack reproduces preorder (push the right child before the left) and inorder (walk left
pushing, pop, visit, go right).
Example: [1, 2, 3, 4, 5, None, 6] -> preorder [1, 2, 4, 5, 3, 6], inorder [4, 2, 5, 1, 3, 6],
postorder [4, 5, 2, 6, 3, 1]
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


def tops(stack):
    """Trace only: stack contents top -> bottom."""
    return [n.val for n in reversed(stack)]


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
    """Build each order by list concatenation, [node] + left + right. O(n^2) copying on a chain."""
    def pre(n):
        return [n.val] + pre(n.left) + pre(n.right) if n else []

    def ino(n):
        return ino(n.left) + [n.val] + ino(n.right) if n else []

    def post(n):
        return post(n.left) + post(n.right) + [n.val] if n else []
    return {"preorder": pre(root), "inorder": ino(root), "postorder": post(root)}


# --- optimal ---
def solve(root):
    """One recursive walk records all three orders; two stack loops rebuild pre/inorder and must agree. O(n)."""
    pre, ino, post = [], [], []

    def rec(node):
        if node is None:
            return
        pre.append(node.val)
        log(f"  down at {node.val}: preorder  {pre}")
        rec(node.left)
        ino.append(node.val)
        log(f"  between children of {node.val}: inorder   {ino}")
        rec(node.right)
        post.append(node.val)
        log(f"  up from {node.val}: postorder {post}")
    rec(root)
    log("preorder with a stack (push right, then left, so left pops first):")
    it_pre, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        it_pre.append(node.val)
        stack.extend(c for c in (node.right, node.left) if c)
        log(f"  pop {node.val} visit; push {[c.val for c in (node.right, node.left) if c]}; stack top->bottom {tops(stack)}; order {it_pre}")
    log("inorder with a stack (walk left pushing, pop, visit, go right):")
    it_in, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            log(f"  push {node.val}, go left; stack top->bottom {tops(stack)}")
            node = node.left
        node = stack.pop()
        it_in.append(node.val)
        log(f"  pop {node.val} visit, go right; order {it_in}")
        node = node.right
    assert it_pre == pre and it_in == ino, "stack versions must match recursion"
    return {"preorder": pre, "inorder": ino, "postorder": post}


# --- demo ---
def demo():
    return solve(build_tree([1, 2, 3, 4, 5, None, 6]))


# --- tests ---
def random_tree(rng, n):
    """Random shape with unique values 0..n-1: attach each new node to a random free slot."""
    nodes = [TreeNode(i) for i in range(n)]
    for i in range(1, n):
        while True:
            p = nodes[rng.randrange(i)]
            if p.left is None or p.right is None:
                break
        side = rng.choice([s for s in ("left", "right") if getattr(p, s) is None])
        setattr(p, side, nodes[i])
    return nodes[0] if n else None


def tests():
    assert solve(build_tree([1, 2, 3, 4, 5, None, 6])) == {
        "preorder": [1, 2, 4, 5, 3, 6], "inorder": [4, 2, 5, 1, 3, 6], "postorder": [4, 5, 2, 6, 3, 1]}
    assert solve(None) == {"preorder": [], "inorder": [], "postorder": []}
    assert solve(build_tree([7])) == {"preorder": [7], "inorder": [7], "postorder": [7]}
    assert solve(build_tree([3, 2, None, 1]))["inorder"] == [1, 2, 3]          # left chain
    assert solve(build_tree([1, None, 2, None, 3]))["postorder"] == [3, 2, 1]  # right chain
    assert solve(build_tree([1, 2, 3]))["preorder"] == [1, 2, 3]
    import random
    rng = random.Random(1)
    for _ in range(200):
        root = random_tree(rng, rng.randint(0, 12))
        assert solve(root) == brute_force(root)


# --- bugs ---
BUGS = [
    {
        "replace": "        stack.extend(c for c in (node.right, node.left) if c)",
        "with":    "        stack.extend(c for c in (node.left, node.right) if c)",
        "fix": "push the RIGHT child first so the left child is on top and pops next",
        "why": "A stack pops the last push, so pushing left last makes it pop first; pushing right last visits right subtrees before left ones: [1, 2, 3] comes out 1, 3, 2.",
        "decoys": [
            {"line": "    it_pre, stack = [], [root] if root else []", "change": "should start with an empty stack"},
            {"line": "        pre.append(node.val)", "change": "should append after rec(node.left)"},
            {"line": "    rec(root)", "change": "should be rec(root.left)"},
        ],
    },
    {
        "replace": "    while stack or node:",
        "with":    "    while stack:",
        "fix": "loop while there is a node to walk down from OR something left on the stack",
        "why": "The stack starts empty, so the loop never runs and the iterative inorder is []; even after a fix to seed it, the loop would stop early whenever the stack empties with a right subtree still pending.",
        "decoys": [
            {"line": "            node = node.left", "change": "should be node.right"},
            {"line": "        it_in.append(node.val)", "change": "should append before the pop"},
            {"line": "        node = node.right", "change": "should be node.left"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
