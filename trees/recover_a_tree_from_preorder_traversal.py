"""
Recover a Tree From Preorder Traversal (LeetCode 1028)  — Hard
Pattern: Stack of ancestors indexed by depth

Problem
-------
A tree was serialised by preorder DFS: each node is written as D dashes
followed by its value, where D is its depth (the root has 0 dashes). A
node with one child always has it as the LEFT child. Rebuild the tree.
Example: "1-2--3--4-5--6--7" -> [1,2,5,3,4,6,7].
Example: "1-401--349---90--88" -> [1,401,null,349,88,90].

Brute force
-----------
Tokenise into (depth, value) pairs. Then build recursively: the first
token is the root; scan forward to find the token that starts the right
subtree (the second token with depth == root_depth + 1); everything before
it is the left subtree, everything from it onward is the right subtree;
recurse on both slices. O(n^2) time in the worst case (a left-leaning
chain makes every level rescan nearly the whole remaining list), O(n)
space. The wasted work is the scan: finding where a subtree ends by
re-reading tokens whose depths we already parsed.

From brute force to optimal
---------------------------
Preorder visits a node immediately after its parent's subtree starts, so
when we meet a token at depth d, its parent is the most recent token at
depth d - 1, and everything deeper than d - 1 that we have seen is
finished. Keep a stack of the current root-to-node path: its length is
the current depth. On a new token at depth d, pop until the stack has d
entries; the top is the parent. Attach as the left child if the parent
has none yet, else as the right child (the "single child is left" rule
guarantees this is unambiguous). Each token is pushed and popped once, so
the scan disappears and the whole rebuild is a single linear pass.

Intuition
---------
Depth tells you exactly how many ancestors a node has. Maintain the
ancestor chain explicitly as a stack; the dash count says how far to cut
it back before hanging the new node on. Left fills first, right second,
because preorder lists the left subtree entirely before the right one.

Geometric view
--------------
Read the string left to right as a hiker reporting altitude: "--3" means
"I am two levels below the root". The stack is the rope of ancestors
tied to the hiker; when the altitude decreases, the rope is shortened by
popping, when it increases by one the hiker steps down to a new child.
The rope never has to be longer than the tree is tall.

Steps
-----
1. Scan the string: count dashes to get depth, then read the digits.
2. Create the node. While len(stack) > depth: pop (those ancestors are done).
3. If stack is non-empty: parent = stack[-1]; attach as left if free, else right.
4. Push the node. Continue until the string ends.
5. Return stack[0], the root.

Complexity: O(n) time, O(h) space — each character is read once and each
node is pushed/popped once; the stack holds one root-to-node path.
Pitfalls: multi-digit values (read all digits, not one); attaching to the
right when the left is empty; forgetting that the stack must be cut back
BEFORE the parent is read; using recursion with slicing (quadratic).
"""
from collections import deque
from typing import List, Optional, Tuple


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def recoverFromPreorder(self, traversal: str) -> Optional[TreeNode]:
        stack: List[TreeNode] = []                 # stack[i] is the current ancestor at depth i
        i, n = 0, len(traversal)
        while i < n:
            depth = 0
            while traversal[i] == "-":
                depth += 1
                i += 1
            j = i
            while j < n and traversal[j] != "-":
                j += 1
            node = TreeNode(int(traversal[i:j]))   # multi-digit values
            i = j
            while len(stack) > depth:              # cut the ancestor chain back to depth-1
                stack.pop()
            if stack:
                parent = stack[-1]
                if parent.left is None:            # preorder: the left subtree always comes first
                    parent.left = node
                else:
                    parent.right = node
            stack.append(node)
        return stack[0] if stack else None


def brute_force(traversal: str) -> Optional[TreeNode]:
    # Tokenise, then recursively split each subtree's token list by scanning for the right child: O(n^2).
    tokens: List[Tuple[int, int]] = []
    i, n = 0, len(traversal)
    while i < n:
        depth = 0
        while traversal[i] == "-":
            depth, i = depth + 1, i + 1
        j = i
        while j < n and traversal[j] != "-":
            j += 1
        tokens.append((depth, int(traversal[i:j])))
        i = j

    def build_from(toks: List[Tuple[int, int]]) -> Optional[TreeNode]:
        if not toks:
            return None
        depth, val = toks[0]
        node = TreeNode(val)
        split = len(toks)
        for k in range(2, len(toks)):              # second token at depth+1 starts the right subtree
            if toks[k][0] == depth + 1:
                split = k
                break
        node.left = build_from(toks[1:split])
        node.right = build_from(toks[split:])
        return node

    return build_from(tokens)


def to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Tree -> LeetCode level-order list with trailing Nones stripped."""
    out: List[Optional[int]] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    s = Solution()
    cases = [("1-2--3--4-5--6--7", [1, 2, 5, 3, 4, 6, 7]),
             ("1-2--3---4-5--6---7", [1, 2, 5, 3, None, 6, None, 4, None, 7]),
             ("1-401--349---90--88", [1, 401, None, 349, 88, 90]),
             ("1", [1]),                                                 # single node
             ("10-20--30---40----50", [10, 20, None, 30, None, 40, None, 50]),   # left chain, multi-digit
             ("1-2-3", [1, 2, 3])]                                      # two children of the root
    for text, want in cases:
        assert to_list(s.recoverFromPreorder(text)) == want, text
        assert to_list(brute_force(text)) == want, text
    print("ok")
