"""
Kth Smallest Element in a BST (LeetCode 230) - Medium
Area: trees
Key operations: push the left spine, pop the next smallest, count down k, step to the right child

Given the root of a BST and an integer k, return the k-th smallest value (1-indexed).
Example: [5, 3, 6, 2, 4, None, None, 1], k = 3 -> 3
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
class TreeNode:
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None


def build_tree(values):
    """LeetCode level-order list, None = missing child; only real nodes consume children."""
    nodes = [TreeNode(v) if v is not None else None for v in values]
    kids = iter(nodes[1:])
    for node in nodes:
        if node:
            node.left, node.right = next(kids, None), next(kids, None)
    return nodes[0] if nodes else None


# --- brute force ---
def brute_force(root, k):
    """Collect the complete inorder sequence (already sorted for a BST) and index it. O(n) time and O(n)
    space: every node is visited even when k is 1."""
    def inorder(node):
        return inorder(node.left) + [node.val] + inorder(node.right) if node else []

    return inorder(root)[k - 1]


# --- optimal ---
def solve(root, k):
    """Iterative inorder with an explicit stack: push the whole left spine, pop the next smallest, then
    walk into its right subtree. Stop at the k-th pop. O(h + k) time, O(h) stack."""
    stack, node = [], root
    while True:
        while node:
            stack.append(node)
            log(f"push {node.val}, go left        | stack top->bottom {[n.val for n in reversed(stack)]}")
            node = node.left
        node = stack.pop()
        k -= 1
        log(f"pop {node.val}: {k} still to skip | stack top->bottom {[n.val for n in reversed(stack)]}")
        if k == 0:
            log(f"    {node.val} is the answer")
            return node.val
        node = node.right
        log(f"    step into the right subtree: {node.val if node else 'empty, pop next'}")


# --- demo ---
def demo():
    return solve(build_tree([5, 3, 6, 2, 4, None, None, 1]), 3)


# --- tests ---
def tests():
    assert solve(build_tree([5, 3, 6, 2, 4, None, None, 1]), 3) == 3
    assert solve(build_tree([3, 1, 4, None, 2]), 1) == 1
    assert solve(build_tree([3, 1, 4, None, 2]), 2) == 2
    assert solve(build_tree([3, 1, 4, None, 2]), 4) == 4
    assert solve(build_tree([1]), 1) == 1
    assert solve(build_tree([5, 3, 6, 2, 4, None, None, 1]), 6) == 6     # k = n, the largest
    assert solve(build_tree([1, None, 2, None, 3]), 3) == 3              # right-leaning chain
    assert solve(build_tree([3, 2, None, 1]), 1) == 1                    # left-leaning chain
    import random
    random.seed(0)

    def insert(node, v):
        if node is None:
            return TreeNode(v)
        if v < node.val:
            node.left = insert(node.left, v)
        else:
            node.right = insert(node.right, v)
        return node

    for _ in range(200):
        values = random.sample(range(30), random.randint(1, 9))
        root = None
        for v in values:
            root = insert(root, v)
        k = random.randint(1, len(values))
        assert solve(root, k) == brute_force(root, k) == sorted(values)[k - 1], (values, k)


# --- bugs ---
BUGS = [
    {
        "replace": "        if k == 0:",
        "with":    "        if k == 1:",
        "fix": "k is 1-indexed and was just decremented, so the k-th pop is when k reaches 0",
        "why": "The answer is returned one pop early: the example returns 2 instead of 3, and k = 1 never triggers, so the stack is popped empty.",
        "decoys": [
            {"line": "        k -= 1", "change": "should decrement before the pop"},
            {"line": "    stack, node = [], root", "change": "should start with root already on the stack"},
            {"line": "            return node.val", "change": "should return k"},
        ],
    },
    {
        "replace": "            node = node.left",
        "with":    "            node = node.right",
        "fix": "the spine to push is the left spine: inorder goes left first",
        "why": "Pushing the right spine emits the larger values first, so the order is wrong; the example returns 6 for k = 3.",
        "decoys": [
            {"line": "            stack.append(node)", "change": "should push node.left"},
            {"line": "        node = stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "        node = node.right", "change": "should go to node.right.left"},
        ],
    },
    {
        "replace": "        node = node.right",
        "with":    "        node = node.left",
        "fix": "after emitting a node, continue with its right subtree",
        "why": "Going left again re-pushes the already visited left subtree, so values repeat and the count is off: [3, 1, 4, None, 2] with k = 2 returns 3 instead of 2.",
        "decoys": [
            {"line": "        while node:", "change": "should be while node and node.left"},
            {"line": "        if k == 0:", "change": "should be if k <= 0"},
            {"line": "        k -= 1", "change": "should subtract 1 only when the stack is empty"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
