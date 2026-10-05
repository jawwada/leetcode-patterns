"""
Level Order and Height - Basics
Area: trees
Key operations: for _ in range(len(q)) drains exactly one level, popleft, push children, one level = one unit of height

Return the values of a binary tree level by level, and its height counted in levels (number of nodes
on the longest root-to-leaf path; an empty tree has height 0).
Example: [3, 9, 20, None, None, 15, 7] -> levels [[3], [9, 20], [15, 7]], height 3
"""
from collections import deque


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
    """Recursive height 1 + max(children), then a DFS drops each node into the list of its depth. Two passes, O(n)."""
    def height(n):
        return 1 + max(height(n.left), height(n.right)) if n else 0

    def fill(n, d):
        if n:
            levels[d].append(n.val)
            fill(n.left, d + 1)
            fill(n.right, d + 1)
    levels = [[] for _ in range(height(root))]
    fill(root, 0)
    return levels, height(root)


# --- optimal ---
def solve(root):
    """The queue holds exactly one level; drain len(q) nodes, their children form the next level. O(n)."""
    levels = []
    q = deque([root] if root else [])
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
    return levels, len(levels)


# --- demo ---
def demo():
    return solve(build_tree([3, 9, 20, None, None, 15, 7]))


# --- bugs ---
BUGS = [
    {
        "replace": "        for _ in range(len(q)):",
        "with":    "        while q:",
        "fix": "drain only the nodes that are in the queue when the level starts: for _ in range(len(q))",
        "why": "Children pushed during the level are then popped in the same level, so every node lands in one level and the height is 1: [3, 9, 20] gives [[3, 9, 20]].",
        "decoys": [
            {"line": "            node = q.popleft()", "change": "should be q.pop()"},
            {"line": "        levels.append(level)", "change": "should append inside the for loop"},
            {"line": "    q = deque([root] if root else [])", "change": "should be deque([root])"},
        ],
    },
    {
        "replace": "    return levels, len(levels)",
        "with":    "    return levels, len(levels) - 1",
        "fix": "height in levels equals the number of levels; subtract 1 only for height in edges",
        "why": "Mixing up height in nodes with height in edges: a single node has 1 level, not 0, and an empty tree would report -1.",
        "decoys": [
            {"line": "            level.append(node.val)", "change": "should append node"},
            {"line": "        level = []", "change": "should be created once before the while loop"},
            {"line": "            if node.right:", "change": "should be elif node.right"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
