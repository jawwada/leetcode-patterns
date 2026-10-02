"""
Longest Valid Parentheses (LeetCode 32)  — Hard
Pattern: Stack of indices with a barrier

Problem
-------
Given a string of '(' and ')', return the length of the longest well-formed contiguous
substring. Example: "(()" -> 2; ")()())" -> 4 ("()()"); "" -> 0.

Brute force
-----------
For every start index i scan right keeping a balance counter: '(' adds 1, ')' subtracts 1; each
time the balance returns to 0 the substring s[i..j] is valid, record j-i+1; stop when the
balance goes negative. O(n^2) time, O(1) space. The wasted work: starting the scan at i+1 or
i+2 re-reads the same characters and re-discovers the same matched pairs that the scan from i
already found.

From brute force to optimal
---------------------------
The redundancy is re-matching pairs. Observation: a ')' matches the most recent UNMATCHED '(',
so one left-to-right pass with a stack of '(' indices matches every pair exactly once. The
remaining question is "how long is the valid run ending at this ')'", and it is answered by
the stack too: after popping the partner '(', whatever index sits on top of the stack is the
last position that is NOT part of the current valid run (an unmatched '(' still waiting, or an
unmatched ')' that broke the string). So length = i - stack[-1]. Seed the stack with -1 as the
initial barrier and, whenever a ')' finds nothing to match, replace the barrier with its own
index. Each index is pushed/popped once: O(n).

Intuition
---------
The stack bottom is a wall: the start of the current stretch of possibly-valid text. Above it
sit the open '(' still waiting. Popping on ')' closes a pair; the new top is either another open
'(' (the run goes right up to it) or the wall (the run goes right up to the wall). Either way
the run's length is "current index minus the top". An unmatched ')' is a new wall.

Geometric view
--------------
   s:  ) ( ) ( ) )
   i:  0 1 2 3 4 5
   i=0 ')' nothing to match -> barrier = 0   stack [0]
   i=1 '(' push             stack [0,1]
   i=2 ')' pop 1, len = 2-0 = 2   stack [0]
   i=3 '(' push             stack [0,3]
   i=4 ')' pop 3, len = 4-0 = 4   stack [0]   <- best
   i=5 ')' nothing -> barrier = 5 stack [5]
The stack is a staircase of open brackets standing on a wall; the wall slides right only when a
stray ')' knocks everything down.

Steps
-----
1. stack = [-1] (barrier), best = 0.
2. For i, c: if c == '(' push i.
3. Else if the stack has more than the barrier: pop (match), best = max(best, i - stack[-1]).
4. Else: stack[0] = i (this ')' is the new barrier).
5. Return best.

Complexity: O(n) time, O(n) space — each index is pushed and popped at most once.
Pitfalls: computing length as i - popped_index + 1 (misses chained runs like "()()"; measure
to the new top instead); forgetting the -1 barrier so the first full match has no reference;
popping the barrier itself.
"""


class Solution:
    def longestValidParentheses(self, s: str) -> int:
        stack = [-1]                                 # indices; stack[0] is the barrier
        best = 0
        for i, c in enumerate(s):
            if c == "(":
                stack.append(i)
            elif len(stack) > 1:                     # an open "(" is waiting: match it
                stack.pop()
                best = max(best, i - stack[-1])      # run extends back to the new top
            else:
                stack[0] = i                         # stray ")": new barrier
        return best


def brute_force(s: str) -> int:
    best = 0
    for i in range(len(s)):                          # restart the balance from every index
        balance = 0
        for j in range(i, len(s)):
            balance += 1 if s[j] == "(" else -1
            if balance < 0:
                break
            if balance == 0:
                best = max(best, j - i + 1)
    return best


if __name__ == "__main__":
    s = Solution()
    assert s.longestValidParentheses("(()") == 2
    assert s.longestValidParentheses(")()())") == 4
    assert s.longestValidParentheses("") == 0
    assert s.longestValidParentheses("()(()") == 2
    assert s.longestValidParentheses("()(())") == 6
    assert s.longestValidParentheses("((()))())") == 8
    assert s.longestValidParentheses("(((") == 0
    import random
    random.seed(4)
    for _ in range(300):
        w = "".join(random.choice("()") for _ in range(random.randint(0, 14)))
        assert s.longestValidParentheses(w) == brute_force(w), w
    print("ok")
