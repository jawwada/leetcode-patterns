"""
Linked List Cycle II (LeetCode 142) - Medium
Area: linked list
Key operations: slow/fast race, meeting check by identity, reset one pointer to head, same-speed walk to the entry

Given the head of a linked list, return the index of the node where the cycle begins, or -1 if there
is no cycle. Use O(1) extra space and do not modify the list.
Example: values [3, 2, 0, -4] with the tail linked back to index 1 -> 1 (the node holding 2).
"""


# --- helpers ---
class ListNode:
    def __init__(self, val):
        self.val, self.next = val, None


def build_list(values, pos):
    """Chain the values; the tail points back to index pos (-1 for no cycle). Returns the node list."""
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes


def draw(nodes, pos, **marks):
    """'3 -> 2[slow] -> 0 -> -4[fast] -> back to 2' with a label on every marked node."""
    tags = {id(n): "+".join(k for k, v in marks.items() if v is n) for n in nodes}
    cells = [str(n.val) + (f"[{tags[id(n)]}]" if tags[id(n)] else "") for n in nodes]
    return (" -> ".join(cells) or "(empty)") + (f" -> back to {nodes[pos].val}" if pos >= 0 else " -> None")


# --- brute force ---
def brute_force(values, pos):
    """Walk from the head remembering every node seen; the first repeat is the entry. O(n) time but
    O(n) memory spent only to answer 'have I been here?', which two pointers can answer in O(1)."""
    nodes = build_list(values, pos)
    seen = set()
    node = nodes[0] if nodes else None
    while node and id(node) not in seen:
        seen.add(id(node))
        node = node.next
    return nodes.index(node) if node else -1


# --- optimal ---
def solve(values, pos):
    """Floyd: slow (1 step) and fast (2 steps) must meet inside the loop; then a walker from the head and
    one from the meeting point, both 1 step, meet exactly at the entry. O(n) time, O(1) extra space."""
    nodes = build_list(values, pos)
    head = nodes[0] if nodes else None
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            break
    else:
        return -1
    ptr = head
    while ptr is not slow:
        ptr, slow = ptr.next, slow.next
    return nodes.index(ptr)


# --- demo ---
def demo():
    return solve([3, 2, 0, -4], 1)


# --- bugs ---
BUGS = [
    {
        "replace": "        if slow is fast:",
        "with":    "        if slow.val == fast.val:",
        "fix": "compare the nodes by identity with is, not their values",
        "why": "Two different nodes may hold the same value: on [1, 1, 1, 1] with no cycle the race 'meets' at once, phase 2 walks off the end and crashes.",
        "decoys": [
            {"line": "        slow, fast = slow.next, fast.next.next", "change": "should move fast three steps"},
            {"line": "    ptr = head", "change": "should start ptr at head.next"},
            {"line": "    return nodes.index(ptr)", "change": "should return nodes.index(fast)"},
        ],
    },
    {
        "replace": "    while fast and fast.next:",
        "with":    "    while fast:",
        "fix": "also require fast.next, since fast moves two steps",
        "why": "When the list has no cycle fast lands on the last node, and fast.next.next reads next of None; [1] with no cycle crashes.",
        "decoys": [
            {"line": "        if slow is fast:", "change": "should test this before moving the pointers"},
            {"line": "        return -1", "change": "should return 0"},
            {"line": "    while ptr is not slow:", "change": "should loop while ptr is not fast"},
        ],
    },
    {
        "replace": "    while ptr is not slow:",
        "with":    "    while ptr is not fast:",
        "fix": "walk ptr toward the moving slow pointer, not the frozen meeting point",
        "why": "fast stays parked on the meeting point, so ptr stops there and the meeting index is reported as the entry; [3, 2, 0, -4] with pos 1 gives 3 instead of 1.",
        "decoys": [
            {"line": "    slow = fast = head", "change": "should start fast at head.next"},
            {"line": "        ptr, slow = ptr.next, slow.next", "change": "should move slow two steps"},
            {"line": "        return -1", "change": "should return None"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
