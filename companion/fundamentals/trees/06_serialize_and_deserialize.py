"""
Serialize and Deserialize Binary Tree (LeetCode 297) - Fundamentals
Chapter: fundamentals/trees
Key operations: preorder emit, '#' for None, consume tokens from one queue, build left then right

Turn a binary tree into a string and the string back into the same tree. Preorder with an explicit
'#' for every missing child is unambiguous, so decoding consumes the tokens in the same order: take
one token, build the node, then its left subtree, then its right subtree.
Example: [1, 2, 3, None, None, 4, 5] -> "1,2,#,#,3,4,#,#,5,#,#" -> the same tree
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


# --- algorithm ---
def emit(node, tokens):
    """Preorder: the value, then the left subtree, then the right; '#' marks a missing child."""
    if node is None:
        tokens.append("#")                  # the explicit None is what makes decoding unambiguous
        return
    tokens.append(str(node.val))
    emit(node.left, tokens)
    emit(node.right, tokens)


def serialize(root):
    """Tree -> comma-joined preorder tokens. O(n)."""
    tokens = []
    emit(root, tokens)
    return ",".join(tokens)                 # a separator keeps 12 and -3 apart from 1, 2, 3


def consume(tokens):
    """Take the next token from the shared queue; '#' closes a branch, anything else is a node."""
    token = tokens.popleft()                # every call eats from the same queue, in preorder
    if token == "#":
        return None
    node = TreeNode(int(token))
    node.left = consume(tokens)             # the left subtree uses up its tokens first ...
    node.right = consume(tokens)            # ... then the right subtree starts where it stopped
    return node


def deserialize(data):
    """Comma-joined tokens -> tree, consumed in the same preorder they were emitted. O(n)."""
    tokens = deque(data.split(","))         # deque: popleft is O(1)
    return consume(tokens)


# --- try it ---
print(serialize(build_tree([1, 2, 3, None, None, 4, 5])))              # -> 1,2,#,#,3,4,#,#,5,#,#
print(tree_to_list(deserialize("1,2,#,#,3,4,#,#,5,#,#")))      # -> [1, 2, 3, None, None, 4, 5]
print(serialize(build_tree([12, -3])))                                 # -> 12,-3,#,#,#
print(tree_to_list(deserialize(serialize(build_tree([12, -3])))))      # -> [12, -3]
print(serialize(build_tree([])))                                       # -> #
print(tree_to_list(deserialize("#")))                                  # -> []
