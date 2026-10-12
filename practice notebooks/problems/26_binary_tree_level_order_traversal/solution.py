"""
Binary Tree Level Order Traversal (LeetCode 102) - Medium
Area: trees
Key operations: queue of the current level, snapshot len(q), popleft and push children, append the level

Return the node values level by level, left to right, as a list of lists.
Example: [3, 9, 20, None, None, 15, 7] -> [[3], [9, 20], [15, 7]]
"""
from collections import deque


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
def brute_force(root):
    """Compute the height, then run one full DFS per depth d collecting the nodes at exactly depth d.
    O(n * h) time: every pass walks all n nodes to keep a single level."""
    def height(node):
        return 0 if node is None else 1 + max(height(node.left), height(node.right))

    def collect(node, depth, target, out):
        if node is None:
            return
        if depth == target:
            out.append(node.val)
        collect(node.left, depth + 1, target, out)
        collect(node.right, depth + 1, target, out)

    levels = []
    for d in range(height(root)):
        level = []
        collect(root, 0, d, level)
        levels.append(level)
    return levels


# --- optimal ---
def solve(root):
    """BFS with a queue: at the top of each round the queue holds exactly one level, so pop len(q) nodes
    while their children queue up behind. O(n) time, O(width) space."""
    if root is None:
        return []
    levels, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        levels.append(level)
    return levels


# --- demo ---
def demo():
    return solve(build_tree([3, 9, 20, None, None, 15, 7]))


# --- bugs ---
BUGS = [
    {
        "replace": "        for _ in range(len(q)):",
        "with":    "        while q:",
        "fix": "pop exactly len(q) nodes, the size of the level when the round started",
        "why": "Draining the queue keeps popping the children that were just pushed, so every node lands in one level: the example gives [[3, 9, 20, 15, 7]].",
        "decoys": [
            {"line": "    levels, q = [], deque([root])", "change": "should start with an empty deque"},
            {"line": "            level.append(node.val)", "change": "should append the node itself"},
            {"line": "        levels.append(level)", "change": "should append inside the inner loop"},
        ],
    },
    {
        "replace": "            node = q.popleft()",
        "with":    "            node = q.pop()",
        "fix": "pop from the left, the queue must be FIFO",
        "why": "Popping from the right turns the queue into a stack: children of the last node come out before the earlier nodes, so levels mix and reverse; the example gives [[3], [20, 7], [15, 9]].",
        "decoys": [
            {"line": "            if node.left:", "change": "should test node.left is not None"},
            {"line": "        level = []", "change": "should be created once outside the while loop"},
            {"line": "    return levels", "change": "should return levels[::-1]"},
        ],
    },
    {
        "replace": "            if node.right:",
        "with":    "            if node.left:",
        "fix": "guard the right push with node.right (copy-paste slip)",
        "why": "The right child is pushed only when a left child exists and is pushed as None when there is no right child: [1, None, 2] loses the 2 and [1, 2] crashes on None.val.",
        "decoys": [
            {"line": "                q.append(node.left)", "change": "should use appendleft"},
            {"line": "            node = q.popleft()", "change": "should be q[0] without popping"},
            {"line": "    if root is None:", "change": "should be if not root.left and not root.right"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
