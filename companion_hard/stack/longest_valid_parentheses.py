"""
Longest Valid Parentheses (LeetCode 32) - Hard
Chapter: stack
Pattern: Stack of indices with a barrier

Given a string of '(' and ')', return the length of the longest well-formed contiguous
substring.
Example: "(()" -> 2; ")()())" -> 4 ("()()"); "" -> 0.
"""


# --- brute force ---
def brute_force(s):
    """Restart a balance counter from every index. O(n^2) time, O(1) space."""
    best = 0
    for start in range(len(s)):
        balance = 0
        for end in range(start, len(s)):        # re-matches pairs the last start already found
            if s[end] == "(":
                balance += 1
            else:
                balance -= 1
            if balance < 0:                     # a ')' with no opener: nothing longer works
                break
            if balance == 0:
                best = max(best, end - start + 1)
    return best


# --- optimal ---
def longest_valid_parentheses(s):
    """Stack of '(' indices over a barrier; length = i - new top. O(n) time, O(n) space."""
    stack = [-1]                                # indices; stack[0] is the barrier
    best = 0
    for i in range(len(s)):
        if s[i] == "(":
            stack.append(i)
        elif len(stack) > 1:                    # an open '(' is waiting: match it
            stack.pop()
            best = max(best, i - stack[-1])     # the run reaches back to the new top
        else:
            stack[0] = i                        # stray ')': it becomes the new barrier
    return best


# --- try the brute force ---
print(brute_force("(()"))          # -> 2
print(brute_force(")()())"))       # -> 4
print(brute_force("()(())"))       # -> 6
print(brute_force("((()))())"))    # -> 8


# --- try the optimal ---
print(longest_valid_parentheses("(()"))          # -> 2
print(longest_valid_parentheses(")()())"))       # -> 4
print(longest_valid_parentheses("()(())"))       # -> 6
print(longest_valid_parentheses("((()))())"))    # -> 8
