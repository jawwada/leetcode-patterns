"""
Serialize and Deserialize N-ary Tree (LeetCode 428) - Hard
Chapter: trees
Pattern: Preorder with child counts, consumed by a single cursor

Design Codec.serialize(root) -> str and Codec.deserialize(data) -> root for an N-ary tree
in which each node has a value and a list of children. Any format works as long as
deserialize(serialize(t)) rebuilds t.
Example: 1 -> [3 -> [5, 6], 2, 4] must round-trip, and so must the empty tree.
"""
from collections import deque


# --- helpers ---
class Node:
    def __init__(self, val=0):
        self.val = val
        self.children = []


def build_nary(spec):
    """Nested list [value, child_spec, child_spec, ...] -> tree; [] is the empty tree."""
    if len(spec) == 0:
        return None
    node = Node(spec[0])
    for child_spec in spec[1:]:
        node.children.append(build_nary(child_spec))
    return node


def nary_to_list(root):
    """Tree -> the same nested list form, so the demo can print it."""
    if root is None:
        return []
    out = [root.val]
    for child in root.children:
        out.append(nary_to_list(child))
    return out


def round_trip(codec, spec):
    """Build the tree, serialize it, deserialize the text, and show the result as a nested list."""
    text = codec.serialize(build_nary(spec))
    return nary_to_list(codec.deserialize(text))


# --- brute force ---
class BruteForce:
    """Nested parentheses like "1(3(5,6),2,4)"; decoding rescans for depth-0 commas. O(n^2)."""

    def serialize(self, root):
        if root is None:
            return ""
        parts = []
        for child in root.children:
            parts.append(self.serialize(child))
        return str(root.val) + "(" + ",".join(parts) + ")"

    def deserialize(self, data):
        if data == "":
            return None
        open_at = data.index("(")               # the value ends where its bracket opens
        node = Node(int(data[:open_at]))
        inner = data[open_at + 1:-1]            # the text between the outer brackets
        depth = 0
        start = 0
        for i in range(len(inner)):             # rescan the whole remainder for split points
            if inner[i] == "(":
                depth += 1
            elif inner[i] == ")":
                depth -= 1
            elif inner[i] == "," and depth == 0:      # a comma between siblings, not inside one
                node.children.append(self.deserialize(inner[start:i]))
                start = i + 1
        if inner != "":
            node.children.append(self.deserialize(inner[start:]))
        return node


# --- optimal ---
def write(node, out):
    """Preorder: the value, then HOW MANY children, then each child's own tokens."""
    out.append(str(node.val))
    out.append(str(len(node.children)))         # the count replaces brackets
    for child in node.children:
        write(child, out)


def read(tokens):
    """Take a value and a count from the front of the queue, then build exactly count children."""
    node = Node(int(tokens.popleft()))
    count = int(tokens.popleft())
    for i in range(count):
        node.children.append(read(tokens))      # each call consumes exactly one subtree
    return node


class Codec:
    """Preorder 'value count' pairs read by one forward cursor. O(n) both ways."""

    def serialize(self, root):
        out = []
        if root is not None:
            write(root, out)
        return " ".join(out)

    def deserialize(self, data):
        if data == "":
            return None
        tokens = deque(data.split(" "))         # deque: popleft is O(1)
        return read(tokens)


# --- try the brute force ---
codec = BruteForce()
print(round_trip(codec, [1, [3, [5], [6]], [2], [4]]))    # -> [1, [3, [5], [6]], [2], [4]]
print(round_trip(codec, []))                              # -> []
print(round_trip(codec, [-7]))                            # -> [-7]
print(round_trip(codec, [1, [2, [3, [4]]]]))              # -> [1, [2, [3, [4]]]]


# --- try the optimal ---
codec = Codec()
print(round_trip(codec, [1, [3, [5], [6]], [2], [4]]))    # -> [1, [3, [5], [6]], [2], [4]]
print(round_trip(codec, []))                              # -> []
print(round_trip(codec, [-7]))                            # -> [-7]
print(round_trip(codec, [1, [2, [3, [4]]]]))              # -> [1, [2, [3, [4]]]]
