"""
Serialize and Deserialize Binary Tree (LeetCode 297)  — Hard
Pattern: Preorder with null sentinels

Problem
-------
Design Codec with serialize(root) -> str and deserialize(str) -> root such
that deserialize(serialize(t)) reproduces t exactly. Any format is allowed.
Example: [1,2,3,null,null,4,5] -> "1,2,#,#,3,4,#,#,5,#,#" -> same tree.

Brute force
-----------
Use LeetCode's own display format: level-order BFS emitting "null" for
every missing child, and decode with a queue that pairs each parent with
the next two tokens. O(n) time and O(n) space, so not asymptotically
slow, but the decoder has to keep a queue of "parents still waiting for
children" and index into the token list by hand, and every leaf costs two
"null" tokens. The bookkeeping (queue + token index + which-child state)
is the overhead: structure is reconstructed by remembering who is waiting
rather than being implied by the order of tokens.

From brute force to optimal
---------------------------
The queue exists only to remember which parent the next tokens belong to.
Recursion remembers that for free: if we emit nodes in PREORDER and write
a sentinel "#" for every null child, the decoder is a single recursive
reader: take the next token; if it is "#" return None; otherwise make a
node, then read its left subtree, then its right subtree. The sentinels
tell the reader exactly where each subtree ends, so no sizes, indices, or
queues are needed. The string is a direct image of the recursion and the
decoder mirrors the encoder line for line. Invariant: when read() returns,
the token stream is positioned just past the subtree it decoded.

Intuition
---------
Preorder alone is ambiguous ([1,2] vs [1,null,2]), but preorder WITH null
markers is a complete description: each "#" says "this branch stops
here". Encoding and decoding are the same traversal in two directions.

Geometric view
--------------
Walk the tree in preorder and write down what you see, including every
empty slot; the output is a flat line of tokens. Decoding replays the
walk: a value token means "step down-left", a "#" means "this branch is
done, step back up and go right". The token iterator is the walker's
position on that line.

Steps
-----
1. serialize: walk(node): None -> append "#"; else append val, walk left, walk right.
   Join with commas.
2. deserialize: tokens = iter(split(",")).
3. read(): tok = next(tokens); if "#" return None.
4. node = TreeNode(int(tok)); node.left = read(); node.right = read(); return node.

Complexity: O(n) time, O(n) space — each node emits one token and one
pair of recursive calls; recursion depth is the height h.
Pitfalls: choosing a separator that can appear in values (negatives need
a real delimiter, not "-"); storing preorder+inorder instead (breaks on
duplicate values); deep recursion on skewed trees of 10^4 nodes (raise
the recursion limit or go iterative).
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        # preorder with '#' for every null child: the structure is implied by the order
        tokens: List[str] = []

        def walk(node: Optional[TreeNode]) -> None:
            if node is None:
                tokens.append("#")
                return
            tokens.append(str(node.val))
            walk(node.left)
            walk(node.right)

        walk(root)
        return ",".join(tokens)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        tokens = iter(data.split(","))

        def read() -> Optional[TreeNode]:
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))
            node.left = read()            # consumes exactly the left subtree's tokens
            node.right = read()
            return node

        return read()


class BruteForce:
    # Level-order with explicit "null" tokens (LeetCode's display format): the decoder
    # needs a queue of waiting parents plus a running token index.
    def serialize(self, root: Optional[TreeNode]) -> str:
        out, queue = [], deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                out.append("null")
                continue
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        return ",".join(out)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        tokens = data.split(",")
        if tokens[0] == "null":
            return None
        root = TreeNode(int(tokens[0]))
        queue, i = deque([root]), 1
        while queue:
            node = queue.popleft()
            for side in ("left", "right"):
                if tokens[i] != "null":
                    child = TreeNode(int(tokens[i]))
                    setattr(node, side, child)
                    queue.append(child)
                i += 1
        return root


def build(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """LeetCode level-order list (None = missing child) -> tree."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = deque([root]), 1
    while queue and i < len(vals):
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


def to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Tree -> LeetCode level-order list with trailing Nones trimmed."""
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    codec, naive = Codec(), BruteForce()
    assert codec.serialize(build([1, 2, 3, None, None, 4, 5])) == "1,2,#,#,3,4,#,#,5,#,#"
    cases = [[1, 2, 3, None, None, 4, 5], [], [1], [1, None, 2, None, 3],
             [-1, 0, -2], [1, 2], [1, None, 2], [5, 5, 5, 5]]          # duplicates must survive
    for vals in cases:
        assert to_list(codec.deserialize(codec.serialize(build(vals)))) == vals, vals
        assert to_list(naive.deserialize(naive.serialize(build(vals)))) == vals, vals
    print("ok")
