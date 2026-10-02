"""
Minimum Remove to Make Valid Parentheses (LeetCode 1249)  — Medium
Pattern: Stack matching

Problem
-------
Given a string of lowercase letters and parentheses, remove the minimum number of parentheses
so the result is valid (every '(' has a matching ')' after it). Return any valid result.
Example: "lee(t(c)o)de)" -> "lee(t(c)o)de"; "a)b(c)d" -> "ab(c)d"; "))((" -> "".

Brute force
-----------
Scan left to right with a depth counter; the first ')' that drives depth negative is
unmatched -- delete it and rescan from the beginning. Repeat until no such ')' exists, then
do the mirror image from the right for unmatched '('. O(n^2) time (each deletion is an O(n)
rebuild plus rescan), O(n) space. The wasted work: after deleting one bad ')', the rescan
re-walks the prefix whose depth profile we already know.

From brute force to optimal
---------------------------
The redundancy is rescanning after each deletion. Observation: a ')' is unmatched exactly
when there is no open '(' to pair it with, and a '(' is unmatched exactly when it never gets
closed -- both facts are decidable in one left-to-right pass if we keep the indices of
currently-open '(' on a stack. A ')' pops when possible and is marked for deletion otherwise;
whatever is left on the stack at the end is the set of never-closed '(' to delete. One pass
plus one join; every character handled O(1) times.

Intuition
---------
Match parentheses as you read: ')' pairs with the most recent open '('. Anything that cannot
be paired -- a ')' with no partner, or a '(' still waiting at the end -- is exactly the
minimum set to remove, because every removed character was genuinely unmatchable.

Geometric view
--------------
Draw depth over position: '(' steps up, ')' steps down. Every downward step that would go
below zero is a doomed ')' (cut it, the curve stays at zero). At the end, the final height
is the count of doomed '(' -- they are the most recent unclosed openers, which is exactly
what sits on the stack.

Steps
-----
1. chars = list(s), stack = [] (indices of open '(').
2. For i, ch: '(' -> push i. ')' -> pop if stack non-empty, else chars[i] = "" (delete).
3. For every index left on the stack, chars[i] = "".
4. Return "".join(chars).

Complexity: O(n) time, O(n) space — single pass; stack and output list are linear.
Pitfalls: Deleting from the string while iterating (shifts indices) -- mark instead;
removing all leftover '(' is required, not just one; letters never affect the stack.
"""


class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        chars = list(s)
        stack = []                                 # indices of '(' not yet closed
        for i, ch in enumerate(s):
            if ch == "(":
                stack.append(i)
            elif ch == ")":
                if stack:
                    stack.pop()
                else:
                    chars[i] = ""                  # unmatched ')': delete
        for i in stack:                            # '(' never closed: delete
            chars[i] = ""
        return "".join(chars)


def brute_force(s: str) -> str:
    def strip(s: str, open_: str, close: str) -> str:
        changed = True
        while changed:                             # rescan from scratch after each removal
            changed, depth = False, 0
            for i, ch in enumerate(s):
                depth += (ch == open_) - (ch == close)
                if depth < 0:                      # first unmatched closer
                    s, changed = s[:i] + s[i + 1:], True
                    break
        return s
    s = strip(s, "(", ")")                         # drop unmatched ')' left-to-right
    return strip(s[::-1], ")", "(")[::-1]          # drop unmatched '(' right-to-left


if __name__ == "__main__":
    s = Solution()
    cases = ["lee(t(c)o)de)", "a)b(c)d", "))((", "(a(b(c)d)", "abc", "", "(()("]
    assert s.minRemoveToMakeValid("lee(t(c)o)de)") == "lee(t(c)o)de"
    assert s.minRemoveToMakeValid("a)b(c)d") == "ab(c)d"
    assert s.minRemoveToMakeValid("))((") == ""
    assert s.minRemoveToMakeValid("(a(b(c)d)") == "a(b(c)d)"
    assert s.minRemoveToMakeValid("abc") == "abc"
    for c in cases:
        assert s.minRemoveToMakeValid(c) == brute_force(c)
    print("ok")
