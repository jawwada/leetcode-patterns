"""
Serialize and Deserialize Binary Tree (basics: trees)
Turn a binary tree into a string, and that string back into the same tree.
  [1, 2, 3, None, None, 4, 5]  ->  "1,2,#,#,3,4,#,#,5,#,#"  ->  the same tree

Idea: write the tree in preorder with '#' for every missing child. The '#' marks show exactly
      where each branch ends, so the decoder rebuilds it by reading the tokens in the same
      order: the node, then its whole left subtree, then its whole right subtree.

Pseudocode:
  serialize(node):
      if node is None: emit "#"
      else: emit node.val; serialize(node.left); serialize(node.right)
      (join the tokens with ",")

  deserialize(data):
      tokens = one iterator over data.split(","), shared by every call
      build_subtree(): tok = next token
                       if tok == "#": return None
                       node = TreeNode(int(tok))
                       node.left = build_subtree(); node.right = build_subtree()
                       return node

Time O(n), space O(n).
"""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build(values):
    """LeetCode level-order list (None = missing child) -> root."""
    nodes = [TreeNode(v) if v is not None else None for v in values]
    kids = iter(nodes[1:])
    for node in nodes:
        if node:
            node.left, node.right = next(kids, None), next(kids, None)
    return nodes[0] if nodes else None


def serialize(root):
    tokens = []

    def walk(node):
        if node is None:
            tokens.append("#")           # mark the missing child
            return
        tokens.append(str(node.val))     # preorder: node, left, right
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(tokens)


def deserialize(data):
    tokens = iter(data.split(","))       # one iterator shared by every call

    def build_subtree():
        tok = next(tokens)
        if tok == "#":                   # this branch ends here
            return None
        node = TreeNode(int(tok))
        node.left = build_subtree()      # same order as serialize
        node.right = build_subtree()
        return node

    return build_subtree()


if __name__ == "__main__":
    data = serialize(build([1, 2, 3, None, None, 4, 5]))
    print(data)                          # 1,2,#,#,3,4,#,#,5,#,#
    print(serialize(deserialize(data)) == data)  # True
    print(deserialize(data).right.left.val)      # 4
