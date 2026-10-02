"""
Valid Parentheses (LeetCode 20)  — Easy
Pattern: Stack matching

Problem
-------
Given a string of the characters ()[]{} decide whether it is valid: every opener is closed by
the same type of bracket, and brackets close in the correct (nested) order.
Example: "()[]{}" -> True; "([)]" -> False; "{[]}" -> True.

Brute force
-----------
Repeatedly scan the string for an adjacent matched pair "()", "[]" or "{}", delete it, and
restart; the string is valid iff it shrinks to "". O(n^2) time (n/2 deletions, each an O(n)
scan and copy), O(n) space. The wasted work: every pass rescans from the beginning even
though only the characters around the last deletion could have formed a new pair.

From brute force to optimal
---------------------------
The redundancy is rescanning a prefix that cannot contain a new pair. Observation: a closer
is valid only if it matches the most recent still-open opener -- the innermost one -- which
is exactly last-in-first-out order. So walk the string once, pushing openers; on a closer,
pop and compare. The stack is the "unfinished business" that the brute force kept re-reading;
keeping it explicitly makes each character cost O(1).

Intuition
---------
Nesting is LIFO: the bracket opened most recently must be the first one closed. A stack
remembers open brackets in exactly that order, so each closer has one legal partner: the top.

Geometric view
--------------
Picture the string as a path going "down" a level on each opener and "up" on each closer.
The stack is the trail of openers above you; a closer must match the one you are directly
beneath. The path must end back at ground level (empty stack) and never go above ground
(closer with empty stack).

Steps
-----
1. pairs = {")": "(", "]": "[", "}": "{"}, stack = [].
2. For each ch: if it is a closer, the stack must be non-empty and its top must equal
   pairs[ch]; pop it. Otherwise push ch.
3. Return True iff the stack is empty at the end.

Complexity: O(n) time, O(n) space — one push or pop per character.
Pitfalls: Forgetting the empty-stack check on a closer ("]" alone); forgetting that leftover
openers mean invalid ("(("); matching only counts instead of types ("([)]" has equal counts).
"""


class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for ch in s:
            if ch in pairs:                                   # closer must match the top
                if not stack or stack.pop() != pairs[ch]:
                    return False
            else:
                stack.append(ch)
        return not stack                                      # leftover openers = invalid


def brute_force(s: str) -> bool:
    changed = True
    while changed:                                            # rescan from scratch each pass
        changed = False
        for pair in ("()", "[]", "{}"):
            if pair in s:
                s = s.replace(pair, "", 1)
                changed = True
    return s == ""


if __name__ == "__main__":
    s = Solution()
    cases = ["()", "()[]{}", "(]", "([)]", "{[]}", "", "((", "]"]
    assert s.isValid("()") is True
    assert s.isValid("()[]{}") is True
    assert s.isValid("(]") is False
    assert s.isValid("([)]") is False
    assert s.isValid("{[]}") is True
    assert s.isValid("((") is False
    assert s.isValid("]") is False
    for c in cases:
        assert s.isValid(c) == brute_force(c)
    print("ok")
