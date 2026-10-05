"""
Serialize and Deserialize Binary Tree (LeetCode 297) - Hard
Chapter: trees
Pattern: Preorder with null sentinels

Design a Codec with serialize(root) -> str and deserialize(str) -> root such that
deserialize(serialize(t)) reproduces t exactly; any format is allowed.
Example: [1, 2, 3, None, None, 4, 5] -> "1,2,#,#,3,4,#,#,5,#,#" and back.
"""
from collections import deque


# --- helpers ---
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(vals):
    """Level-order list (None = missing child) -> tree, the LeetCode input format."""
    if len(vals) == 0 or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])          # deque: popleft is O(1)
    i = 1
    while len(queue) > 0 and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root):
    """Tree -> level-order list with None for missing children, trailing Nones removed."""
    out = []
    queue = deque([root])
    while len(queue) > 0:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while len(out) > 0 and out[-1] is None:
        out.pop()
    return out


def round_trip(codec, vals):
    """Build the tree, serialize it, deserialize the text, and show the result as a list."""
    text = codec.serialize(build_tree(vals))
    return tree_to_list(codec.deserialize(text))


# --- brute force ---
class BruteForce:
    """Level-order text with "null" for every missing child, decoded with a queue of parents."""

    def serialize(self, root):
        out = []
        queue = deque([root])
        while len(queue) > 0:
            node = queue.popleft()
            if node is None:
                out.append("null")
                continue
            out.append(str(node.val))
            queue.append(node.left)             # pushed even when missing: it becomes a "null"
            queue.append(node.right)
        return ",".join(out)

    def deserialize(self, data):
        tokens = data.split(",")
        if tokens[0] == "null":
            return None
        root = TreeNode(int(tokens[0]))
        queue = deque([root])                   # parents still waiting for their two children
        i = 1
        while len(queue) > 0:
            node = queue.popleft()
            if tokens[i] != "null":
                node.left = TreeNode(int(tokens[i]))
                queue.append(node.left)
            i += 1
            if tokens[i] != "null":             # the next token is always this node's right child
                node.right = TreeNode(int(tokens[i]))
                queue.append(node.right)
            i += 1
        return root


# --- optimal ---
def write(node, tokens):
    """Preorder: the node, then its left subtree, then its right; "#" marks an empty child."""
    if node is None:
        tokens.append("#")
        return
    tokens.append(str(node.val))
    write(node.left, tokens)
    write(node.right, tokens)


def read(tokens):
    """Consume exactly one subtree from the front of the token queue and return it."""
    tok = tokens.popleft()
    if tok == "#":
        return None
    node = TreeNode(int(tok))
    node.left = read(tokens)        # the left subtree's tokens come right after the node
    node.right = read(tokens)       # when that returns, the queue sits at the right subtree
    return node


class Codec:
    """Preorder with "#" sentinels; the decoder mirrors the encoder. O(n) both ways."""

    def serialize(self, root):
        tokens = []
        write(root, tokens)
        return ",".join(tokens)

    def deserialize(self, data):
        tokens = deque(data.split(","))         # deque: popleft is O(1)
        return read(tokens)


# --- try the brute force ---
codec = BruteForce()
print(round_trip(codec, [1, 2, 3, None, None, 4, 5]))     # -> [1, 2, 3, None, None, 4, 5]
print(round_trip(codec, []))                              # -> []
print(round_trip(codec, [1, None, 2, None, 3]))           # -> [1, None, 2, None, 3]
print(round_trip(codec, [5, 5, 5, 5]))                    # -> [5, 5, 5, 5]


# --- try the optimal ---
codec = Codec()
print(round_trip(codec, [1, 2, 3, None, None, 4, 5]))     # -> [1, 2, 3, None, None, 4, 5]
print(round_trip(codec, []))                              # -> []
print(round_trip(codec, [1, None, 2, None, 3]))           # -> [1, None, 2, None, 3]
print(round_trip(codec, [5, 5, 5, 5]))                    # -> [5, 5, 5, 5]
