"""
Tree Traversals, Recursive and Iterative - Fundamentals
Chapter: fundamentals/trees
Key operations: visit before/between/after the children, push right then left, push-left-then-pop

Return the preorder, inorder and postorder of a binary tree. One recursive walk records all three;
an explicit stack reproduces preorder (push the right child before the left) and inorder (walk left
pushing, pop, visit, go right).
Example: [1, 2, 3, 4, 5, None, 6] -> preorder [1, 2, 4, 5, 3, 6], inorder [4, 2, 5, 1, 3, 6],
postorder [4, 5, 2, 6, 3, 1]
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


# --- algorithm ---
def traverse(node, preorder, inorder, postorder):
    """One recursive walk; where the visit sits relative to the child calls picks the order."""
    if node is None:
        return
    preorder.append(node.val)                 # before both children
    traverse(node.left, preorder, inorder, postorder)
    inorder.append(node.val)                  # between the children
    traverse(node.right, preorder, inorder, postorder)
    postorder.append(node.val)                # after both children


def all_orders(root):
    """Run the walk once and return (preorder, inorder, postorder)."""
    preorder = []
    inorder = []
    postorder = []
    traverse(root, preorder, inorder, postorder)
    return preorder, inorder, postorder


def preorder_iterative(root):
    """Explicit stack: pop a node, visit it, push its children right then left. O(n)."""
    order = []
    stack = []
    if root is not None:
        stack.append(root)
    while len(stack) > 0:
        node = stack.pop()
        order.append(node.val)
        if node.right is not None:            # push the RIGHT child first ...
            stack.append(node.right)
        if node.left is not None:             # ... so the left child is on top and pops next
            stack.append(node.left)
    return order


def inorder_iterative(root):
    """Walk left pushing every node, pop and visit the top, then move to its right child. O(n)."""
    order = []
    stack = []
    node = root
    while len(stack) > 0 or node is not None:  # a node to walk down from OR a node still pending
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        order.append(node.val)
        node = node.right
    return order


# --- try it ---
root = build_tree([1, 2, 3, 4, 5, None, 6])
print(all_orders(root))   # -> ([1, 2, 4, 5, 3, 6], [4, 2, 5, 1, 3, 6], [4, 5, 2, 6, 3, 1])
print(preorder_iterative(root))     # -> [1, 2, 4, 5, 3, 6]
print(inorder_iterative(root))      # -> [4, 2, 5, 1, 3, 6]
print(all_orders(build_tree([1, None, 2, 3])))      # -> ([1, 2, 3], [1, 3, 2], [3, 2, 1])
print(inorder_iterative(build_tree([1, None, 2, 3])))   # -> [1, 3, 2]
print(preorder_iterative(build_tree([])))           # -> []
