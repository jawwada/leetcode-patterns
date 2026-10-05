"""
Generate Parentheses (LeetCode 22) - Medium
Chapter: backtracking
Pattern: Backtracking with validity-preserving constraints (open/close counts)

Given n pairs of parentheses, return all strings of n "(" and n ")" that are well-formed.
Example: n=3 -> ["((()))","(()())","(())()","()(())","()()()"]. Example: n=1 -> ["()"].
"""
from itertools import product     # every string of a given length over some characters


# --- brute force ---
def brute_force(n):
    """Every string of 2n brackets (4^n of them), keep the balanced ones. O(4^n * n)."""
    out = []
    for chars in product("()", repeat=2 * n):
        balance = 0
        for ch in chars:
            if ch == "(":
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                break                    # a ")" with nothing open: invalid
        if balance == 0:                 # checked only once the whole string is built
            out.append("".join(chars))
    return out


# --- optimal ---
def generate_parenthesis(n):
    """DFS: add "(" while some are left, add ")" only when one is open. O(Catalan(n) * n)."""
    result = []
    dfs(n, 0, 0, [], result)
    return result


def dfs(n, opened, closed, path, result):
    if len(path) == 2 * n:
        result.append("".join(path))
        return
    if opened < n:                       # still have "(" left to place
        path.append("(")
        dfs(n, opened + 1, closed, path, result)
        path.pop()
    if closed < opened:                  # may only close something that is open
        path.append(")")
        dfs(n, opened, closed + 1, path, result)
        path.pop()


# --- try the brute force ---
print(brute_force(3))        # -> ['((()))', '(()())', '(())()', '()(())', '()()()']
print(brute_force(1))        # -> ['()']
print(brute_force(0))        # -> ['']
print(len(brute_force(5)))   # -> 42


# --- try the optimal ---
print(generate_parenthesis(3))        # -> ['((()))', '(()())', '(())()', '()(())', '()()()']
print(generate_parenthesis(1))        # -> ['()']
print(generate_parenthesis(0))        # -> ['']
print(len(generate_parenthesis(5)))   # -> 42
