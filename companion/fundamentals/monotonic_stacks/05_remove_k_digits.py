"""
Remove K Digits (LeetCode 402) - Fundamentals
Chapter: fundamentals/monotonic_stacks
Key operations: pop while top > digit and k remains, push digit, cut the end, strip leading zeros

Remove k digits from the decimal string num so that the remaining number is as small as possible.
Greedy: a bigger digit standing in front of a smaller one should go first, so the kept digits stay
non-decreasing bottom to top while deletions remain; whatever is left of k is cut from the end.
Example: "1432219", k=3 -> "1219"; "10200", k=1 -> "200"; "10", k=2 -> "0"
"""


# --- algorithm ---
def remove_k_digits(num, k):
    """Non-decreasing stack of digits: pop a bigger top before a smaller digit while k > 0."""
    stack = []
    for digit in num:
        while k > 0 and len(stack) > 0 and stack[-1] > digit:   # a bigger digit in front goes
            stack.pop()
            k -= 1
        stack.append(digit)
    while k > 0:                            # leftover deletions: the stack is sorted, cut its end
        stack.pop()
        k -= 1
    result = "".join(stack)
    result = result.lstrip("0")             # "0200" -> "200"
    if result == "":
        return "0"
    return result


# --- try it ---
print(remove_k_digits("1432219", 3))   # -> 1219
print(remove_k_digits("10200", 1))     # -> 200
print(remove_k_digits("10", 2))        # -> 0
print(remove_k_digits("112", 1))       # -> 11
print(remove_k_digits("9", 1))         # -> 0
