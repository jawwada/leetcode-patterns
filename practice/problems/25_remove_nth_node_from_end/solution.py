"""
Remove Nth Node From End of List (LeetCode 19) - Medium
Area: linked list
Key operations: dummy head, open a gap of n+1, slide both pointers, splice slow.next = slow.next.next

Remove the n-th node from the end of a singly linked list and return the head. n is valid
(1 <= n <= length).
Example: 1 -> 2 -> 3 -> 4 -> 5, n = 2 -> 1 -> 2 -> 3 -> 5
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
class ListNode:
    def __init__(self, val, next=None):
        self.val, self.next = val, next


def build_list(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def draw(node, **marks):
    """'dummy[slow] -> 1 -> 2 -> 3[fast] -> None' with a label on every marked node (None included)."""
    out = []
    while node:
        tag = "+".join(k for k, v in marks.items() if v is node)
        out.append(str(node.val) + (f"[{tag}]" if tag else ""))
        node = node.next
    end = "+".join(k for k, v in marks.items() if v is None)
    return " -> ".join(out + ["None" + (f"[{end}]" if end else "")])


# --- brute force ---
def brute_force(head, n):
    """Pass 1 counts the length L, pass 2 walks to node L - n - 1 and unlinks its successor. O(n) time but
    two full traversals; the first exists only to translate 'n from the end' into 'L - n from the start'."""
    length, node = 0, head
    while node:
        length, node = length + 1, node.next
    dummy = ListNode("dummy", head)
    prev = dummy
    for _ in range(length - n):
        prev = prev.next
    prev.next = prev.next.next
    return dummy.next


# --- optimal ---
def solve(head, n):
    """Two pointers n + 1 links apart: when fast falls off the end, slow is just before the victim. The
    dummy lets the same splice delete the head. One pass, O(n) time, O(1) space."""
    dummy = ListNode("dummy", head)
    slow = fast = dummy
    log(f"start:   {draw(dummy, slow=slow, fast=fast)}")
    for _ in range(n + 1):
        fast = fast.next
    log(f"gap {n + 1}:   {draw(dummy, slow=slow, fast=fast)}")
    while fast:
        slow, fast = slow.next, fast.next
        log(f"slide:   {draw(dummy, slow=slow, fast=fast)}")
    log(f"fast is off the end, so slow.next ({slow.next.val}) is node {n} from the end: splice it out")
    slow.next = slow.next.next
    log(f"result:  {draw(dummy, slow=slow)}")
    return dummy.next


# --- demo ---
def demo():
    return to_list(solve(build_list([1, 2, 3, 4, 5]), 2))


# --- tests ---
def tests():
    assert to_list(solve(build_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert to_list(solve(build_list([1]), 1)) == []            # remove the only node
    assert to_list(solve(build_list([1, 2]), 1)) == [1]        # remove the tail
    assert to_list(solve(build_list([1, 2]), 2)) == [2]        # remove the head
    assert to_list(solve(build_list([1, 2, 3]), 3)) == [2, 3]
    assert to_list(solve(build_list([4, 4, 4]), 2)) == [4, 4]
    import random
    random.seed(0)
    for _ in range(200):
        values = [random.randint(0, 9) for _ in range(random.randint(1, 9))]
        n = random.randint(1, len(values))
        got = to_list(solve(build_list(values), n))
        assert got == to_list(brute_force(build_list(values), n)), (values, n)
        assert got == values[:len(values) - n] + values[len(values) - n + 1:], (values, n)


# --- bugs ---
BUGS = [
    {
        "replace": "    for _ in range(n + 1):",
        "with":    "    for _ in range(n):",
        "fix": "open a gap of n + 1 links so slow stops just before the victim",
        "why": "With a gap of n, slow lands on the victim itself and the node after it is removed; for n = 1 slow stops on the tail and slow.next.next reads next of None.",
        "decoys": [
            {"line": "    slow = fast = dummy", "change": "should start both at head"},
            {"line": "        slow, fast = slow.next, fast.next", "change": "should move fast two steps"},
            {"line": "    return dummy.next", "change": "should return slow"},
        ],
    },
    {
        "replace": "    return dummy.next",
        "with":    "    return head",
        "fix": "return dummy.next, which is the new head when the old head was removed",
        "why": "When the victim is the first node the list now starts at dummy.next, not at the old head; [1] with n = 1 returns [1] instead of [].",
        "decoys": [
            {"line": "    dummy = ListNode(\"dummy\", head)", "change": "should be ListNode(\"dummy\", None)"},
            {"line": "        fast = fast.next", "change": "should also move slow"},
            {"line": "    slow.next = slow.next.next", "change": "should be slow = slow.next.next"},
        ],
    },
    {
        "replace": "    while fast:",
        "with":    "    while fast.next:",
        "fix": "slide until fast falls off the end (while fast), not until it reaches the tail",
        "why": "Stopping one link early leaves slow one node too far left, so the (n+1)th node from the end is removed; when n equals the length fast is already None and fast.next crashes.",
        "decoys": [
            {"line": "    for _ in range(n + 1):", "change": "should be range(n + 2)"},
            {"line": "        slow, fast = slow.next, fast.next", "change": "should move slow only when fast.next exists"},
            {"line": "    slow = fast = dummy", "change": "should start fast at dummy.next"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
