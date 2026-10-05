"""
Recover a Tree From Preorder Traversal (LeetCode 1028) - Hard
Chapter: trees
Pattern: Stack of ancestors indexed by depth

A tree was serialised by preorder DFS: each node is written as D dashes followed by its
value, where D is its depth (the root has none). A node with a single child always has it
on the left. Rebuild the tree.
Example: "1-2--3--4-5--6--7" gives [1, 2, 5, 3, 4, 6, 7].
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


def read_tokens(traversal):
    """Split the string into (depth, value) pairs: depth = number of dashes before the digits."""
    tokens = []
    i = 0
    while i < len(traversal):
        depth = 0
        while traversal[i] == "-":
            depth += 1
            i += 1
        j = i
        while j < len(traversal) and traversal[j] != "-":
            j += 1
        tokens.append((depth, int(traversal[i:j])))    # values may have several digits
        i = j
    return tokens


# --- brute force ---
def build_from(tokens):
    """tokens[0] is the root; scan for the second token one level deeper to split its subtrees."""
    if len(tokens) == 0:
        return None
    depth, value = tokens[0]
    node = TreeNode(value)
    split = len(tokens)
    for k in range(2, len(tokens)):         # tokens[1] starts the left subtree
        if tokens[k][0] == depth + 1:       # the next token at depth + 1 starts the right one
            split = k
            break
    node.left = build_from(tokens[1:split])
    node.right = build_from(tokens[split:])
    return node


def brute_force(traversal):
    """Tokenise, then recursively rescan each slice for its right subtree. O(n^2) on a chain."""
    return build_from(read_tokens(traversal))


# --- optimal ---
def recover_from_preorder(traversal):
    """Keep the root-to-node path on a stack; stack[d] is the ancestor at depth d. O(n) time."""
    stack = []
    for depth, value in read_tokens(traversal):
        node = TreeNode(value)
        while len(stack) > depth:           # climb back up: deeper ancestors are finished
            stack.pop()
        if len(stack) > 0:
            parent = stack[-1]              # the most recent node at depth - 1
            if parent.left is None:
                parent.left = node          # preorder: the left child always comes first
            else:
                parent.right = node
        stack.append(node)
    if len(stack) == 0:
        return None
    return stack[0]                         # the bottom of the stack is the root


# --- try the brute force ---
print(tree_to_list(brute_force("1-2--3--4-5--6--7")))      # -> [1, 2, 5, 3, 4, 6, 7]
print(tree_to_list(brute_force("1-401--349---90--88")))    # -> [1, 401, None, 349, 88, 90]
print(tree_to_list(brute_force("10-20--30---40")))         # -> [10, 20, None, 30, None, 40]
print(tree_to_list(brute_force("1-2-3")))                  # -> [1, 2, 3]


# --- try the optimal ---
print(tree_to_list(recover_from_preorder("1-2--3--4-5--6--7")))     # -> [1, 2, 5, 3, 4, 6, 7]
print(tree_to_list(recover_from_preorder("1-401--349---90--88")))  # -> [1, 401, None, 349, 88, 90]
print(tree_to_list(recover_from_preorder("10-20--30---40")))       # -> [10, 20, None, 30, None, 40]
print(tree_to_list(recover_from_preorder("1-2-3")))                 # -> [1, 2, 3]
