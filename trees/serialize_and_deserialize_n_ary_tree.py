"""
Serialize and Deserialize N-ary Tree (LeetCode 428)  — Hard
Pattern: Preorder with child counts, consumed by a single cursor

Problem
-------
Design Codec.serialize(root) -> str and Codec.deserialize(str) -> root
for an N-ary tree (each node has a value and a list of children). Any
format is allowed as long as deserialize(serialize(t)) rebuilds t.
Example: the tree 1 -> [3 -> [5, 6], 2, 4] round-trips; so must the empty
tree and a single node.

Brute force
-----------
Write each node as "val(child,child,...)", a nested-parentheses string
such as "1(3(5,6),2,4)". To deserialize, read the value, then split the
inside of the outer parentheses at the commas that sit at bracket depth 0
and recurse on each piece. O(n^2) time in the worst case (a deep chain
1(2(3(4(...)))) rescans the almost-whole remainder at every level to find
its matching bracket), O(n) space. The wasted work is the rescanning:
every level re-reads characters that a deeper level will read again to
discover where a subtree ends.

From brute force to optimal
---------------------------
The rescan exists only to find where a subtree ends. Preorder gives a
cheaper signal: if each node records HOW MANY children it has, a reader
knows exactly how many subtrees to consume next and never has to look
ahead. Serialize as "val count val count ..." in preorder; deserialize
with one cursor (an iterator over the tokens) that reads a value, reads
the count, then recursively builds exactly that many children. Each token
is consumed once, so the rebuild is a single O(n) pass and the string has
no brackets to balance. (An equivalent trick is a sentinel "#" after the
last child; the count version avoids the extra token per node.)

Intuition
---------
A binary tree is serialised with null markers because every node has
exactly two slots; an N-ary node has no fixed number of slots, so the
missing information is "how many children follow". Store that number
next to the value and preorder becomes self-delimiting: the stream tells
the reader when each subtree is complete without any lookahead.

Geometric view
--------------
Picture the tree flattened into a tape: 1 3 | 3 2 | 5 0 | 6 0 | 2 0 | 4 0.
The reader is a single head moving right. Each "count" is a promise of
how many complete subtrees come next; the recursion stack keeps the
outstanding promises, and when a promise hits zero the head is already
positioned at the next sibling. The head never moves backwards.

Steps
-----
1. serialize: DFS preorder; for each node append str(val) and
   str(len(children)); join with spaces. Empty tree -> "".
2. deserialize: if the string is empty return None; make an iterator of
   the tokens.
3. build(): val = next(it); count = next(it); node = Node(val);
   node.children = [build() for _ in range(count)]; return node.
4. Return build().

Complexity: O(n) time, O(n) space — each node emits and consumes two
tokens; the output string and recursion stack are linear.
Pitfalls: forgetting the empty-tree case (serialize to "" and check for
it); splitting on "," inside a nested format without tracking depth;
relying on recursion for a 10^4-deep chain (switch to an explicit stack
if the depth limit bites).
"""
import random
from typing import List, Optional


class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List["Node"]] = None):
        self.val = val
        self.children = children if children is not None else []


class Codec:
    def serialize(self, root: Optional[Node]) -> str:
        out: List[str] = []

        def dfs(node: Node) -> None:
            out.append(str(node.val))
            out.append(str(len(node.children)))    # the child count makes preorder self-delimiting
            for child in node.children:
                dfs(child)

        if root is not None:
            dfs(root)
        return " ".join(out)

    def deserialize(self, data: str) -> Optional[Node]:
        if not data:
            return None
        tokens = iter(data.split())                # a single forward-moving cursor

        def build() -> Node:
            node = Node(int(next(tokens)))
            count = int(next(tokens))
            node.children = [build() for _ in range(count)]   # consume exactly `count` subtrees
            return node

        return build()


class BruteForce:
    """Nested parentheses "1(3(5,6),2,4)"; deserialize rescans for depth-0 commas at every level: O(n^2)."""

    def serialize(self, root: Optional[Node]) -> str:
        if root is None:
            return ""
        return f"{root.val}({','.join(self.serialize(c) for c in root.children)})"

    def deserialize(self, data: str) -> Optional[Node]:
        if not data:
            return None
        open_at = data.index("(")
        node = Node(int(data[:open_at]))
        inner = data[open_at + 1:-1]
        depth, start = 0, 0
        for i, ch in enumerate(inner):             # rescan the whole remainder to find split points
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == "," and depth == 0:
                node.children.append(self.deserialize(inner[start:i]))
                start = i + 1
        if inner:
            node.children.append(self.deserialize(inner[start:]))
        return node


def same(a: Optional[Node], b: Optional[Node]) -> bool:
    if a is None or b is None:
        return a is b
    return (a.val == b.val and len(a.children) == len(b.children)
            and all(same(x, y) for x, y in zip(a.children, b.children)))


def random_tree(rng: random.Random, n: int) -> Optional[Node]:
    """Random N-ary tree with n nodes: each new node picks a random existing parent."""
    if n == 0:
        return None
    nodes = [Node(rng.randint(-50, 50))]
    for _ in range(n - 1):
        child = Node(rng.randint(-50, 50))
        rng.choice(nodes).children.append(child)
        nodes.append(child)
    return nodes[0]


if __name__ == "__main__":
    codec, naive = Codec(), BruteForce()
    example = Node(1, [Node(3, [Node(5), Node(6)]), Node(2), Node(4)])
    assert codec.serialize(example) == "1 3 3 2 5 0 6 0 2 0 4 0"
    assert same(codec.deserialize(codec.serialize(example)), example)
    assert same(naive.deserialize(naive.serialize(example)), example)
    assert codec.deserialize(codec.serialize(None)) is None                 # empty tree
    assert naive.deserialize(naive.serialize(None)) is None
    single = Node(-7)
    assert same(codec.deserialize(codec.serialize(single)), single)         # negative single node
    chain = Node(1, [Node(2, [Node(3, [Node(4)])])])                       # one child per level
    assert same(codec.deserialize(codec.serialize(chain)), chain)
    rng = random.Random(428)
    for _ in range(200):
        t = random_tree(rng, rng.randint(0, 40))
        assert same(codec.deserialize(codec.serialize(t)), t)
        assert same(naive.deserialize(naive.serialize(t)), t)
        assert same(codec.deserialize(codec.serialize(t)), naive.deserialize(naive.serialize(t)))
    print("ok")
