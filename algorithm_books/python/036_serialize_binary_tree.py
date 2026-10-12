"""
Serialize and Deserialize a Binary Tree - Preorder with Null Markers

Turn a binary tree into a string and the string back into the same tree: write
the values in preorder, '#' for every missing child, separated by commas:
[1, 2, 3, None, None, 4, 5] -> "1,2,#,#,3,4,#,#,5,#,#".
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Build a tree from a level-order list with None for missing children."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root):
    """Level-order list with None for gaps, trailing Nones removed."""
    values = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            values.append(None)
            continue
        values.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while values and values[-1] is None:
        values.pop()
    return values


# --- algorithm ---
def serialize(root):
    """Preorder with '#' for each missing child, joined by commas. O(n)."""
    tokens = []
    write(root, tokens)
    return ",".join(tokens)


def write(node, tokens):
    """Append the node's value, then its left subtree, then its right."""
    if node is None:
        tokens.append("#")                  # the marker closes a branch
        return
    tokens.append(str(node.val))
    write(node.left, tokens)
    write(node.right, tokens)


def deserialize(data):
    """Read the tokens back in the same preorder with a moving index. O(n)."""
    tokens = data.split(",")
    index = [0]                             # one box all the calls share
    return read(tokens, index)


def read(tokens, index):
    """Build the subtree that starts at tokens[index[0]] and move past it."""
    token = tokens[index[0]]
    index[0] += 1
    if token == "#":
        return None
    node = TreeNode(int(token))
    node.left = read(tokens, index)         # the left subtree eats its tokens
    node.right = read(tokens, index)        # the right one starts after them
    return node


# --- try it ---
data = serialize(build_tree([1, 2, 3, None, None, 4, 5]))
print(data)                                 # -> 1,2,#,#,3,4,#,#,5,#,#
print(tree_to_list(deserialize(data)))      # -> [1, 2, 3, None, None, 4, 5]
print(serialize(build_tree([-7, None, 12])))    # -> -7,#,12,#,#
print(serialize(None))                      # -> #
print(tree_to_list(deserialize("#")))       # -> []
