"""
Fibonacci - Recursion, Memo, Iteration, Fast Doubling

F(0) = 0, F(1) = 1, and every later term is the sum of the two before it:
0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55. Compute F(n): n = 10 -> 55.
"""


# --- algorithm ---
def fib_naive(n):
    """Two calls per call: 2F(n + 1) - 1 calls, growing like 1.618^n."""
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n, memo):
    """The same recursion, but each F(k) is solved once. O(n) time and space."""
    if n < 2:
        return n
    if n in memo:
        return memo[n]                  # solved before: skip the whole subtree
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_iter(n):
    """Slide a window of two neighbors n steps. O(n) time, O(1) space."""
    prev = 0
    curr = 1
    for i in range(n):                  # prev = F(i), curr = F(i + 1)
        nxt = prev + curr
        prev = curr
        curr = nxt
    return prev


def fib_pair(n):
    """Return (F(n), F(n + 1)) from the pair at n // 2. O(log n) calls."""
    if n == 0:
        return (0, 1)
    a, b = fib_pair(n // 2)             # a = F(k), b = F(k + 1) with k = n // 2
    even = a * (2 * b - a)              # F(2k)
    odd = a * a + b * b                 # F(2k + 1)
    if n % 2 == 0:
        return (even, odd)
    return (odd, even + odd)            # n = 2k + 1: one step further


def fib_fast(n):
    """Fast doubling: F(n) is the first value of the pair. O(log n) steps."""
    pair = fib_pair(n)
    return pair[0]


# --- try it ---
print(fib_naive(10))                    # -> 55
print(fib_memo(50, {}))                 # -> 12586269025
print(fib_iter(90))                     # -> 2880067194370816120
print(fib_fast(100))                    # -> 354224848179261915075
