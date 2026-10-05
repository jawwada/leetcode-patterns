"""
Remove Invalid Parentheses (LeetCode 301) - Hard
Chapter: backtracking
Pattern: Backtracking with counted removals and balance pruning

Remove the minimum number of parentheses so the string becomes valid and return every
distinct result; letters are kept as they are.
Example: "()())()" -> ["(())()", "()()()"]; "(a)())()" -> ["(a())()", "(a)()()"]; ")(" -> [""].
"""


# --- brute force ---
def brute_force(s):
    """Try every subset of characters to keep, collect valid ones, keep the longest. O(2^n n)."""
    n = len(s)
    kept = set()
    for mask in range(1 << n):                    # bit i on = keep s[i]
        candidate = ""
        for i in range(n):
            if mask >> i & 1:
                candidate += s[i]
        if is_valid(candidate):
            kept.add(candidate)
    longest = 0
    for t in kept:
        longest = max(longest, len(t))
    result = []
    for t in kept:
        if len(t) == longest:                     # longest valid = fewest removals
            result.append(t)
    return result


def is_valid(t):
    balance = 0
    for c in t:
        if c == "(":
            balance += 1
        elif c == ")":
            balance -= 1
        if balance < 0:
            return False
    return balance == 0


# --- optimal ---
def remove_invalid_parentheses(s):
    """Count the forced removals first, then DFS over which brackets to drop; prune balance < 0."""
    left = 0                                      # how many '(' must go
    right = 0                                     # how many ')' must go
    for c in s:
        if c == "(":
            left += 1
        elif c == ")":
            if left > 0:
                left -= 1
            else:
                right += 1
    results = set()                               # deleting different copies gives the same string
    choose(s, 0, 0, left, right, "", results)
    return list(results)


def choose(s, i, open_count, left, right, path, results):
    if i == len(s):
        if open_count == 0 and left == 0 and right == 0:
            results.add(path)
        return
    c = s[i]
    if c == "(" and left > 0:                     # option: delete this '('
        choose(s, i + 1, open_count, left - 1, right, path, results)
    if c == ")" and right > 0:                    # option: delete this ')'
        choose(s, i + 1, open_count, left, right - 1, path, results)
    if c == "(":                                  # option: keep it
        choose(s, i + 1, open_count + 1, left, right, path + c, results)
    elif c == ")":
        if open_count > 0:                        # keeping ')' needs something open, else prune
            choose(s, i + 1, open_count - 1, left, right, path + c, results)
    else:
        choose(s, i + 1, open_count, left, right, path + c, results)


# --- try the brute force ---
# any order is accepted, so the demos print the results sorted
print(sorted(brute_force("()())()")))    # -> ['(())()', '()()()']
print(sorted(brute_force("(a)())()")))   # -> ['(a())()', '(a)()()']
print(sorted(brute_force(")(")))         # -> ['']
print(sorted(brute_force("n")))          # -> ['n']


# --- try the optimal ---
# any order is accepted, so the demos print the results sorted
print(sorted(remove_invalid_parentheses("()())()")))    # -> ['(())()', '()()()']
print(sorted(remove_invalid_parentheses("(a)())()")))   # -> ['(a())()', '(a)()()']
print(sorted(remove_invalid_parentheses(")(")))         # -> ['']
print(sorted(remove_invalid_parentheses("n")))          # -> ['n']
