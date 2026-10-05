"""
Daily Temperatures (LeetCode 739) - Medium
Area: monotonic stack
Key operations: push index, pop while top is colder, answer = i - popped index

Given daily temperatures, return answer where answer[i] is how many days you wait after
day i for a warmer temperature, or 0 if there is none.
Example: [73, 74, 75, 71, 69, 72, 76, 73] -> [1, 1, 4, 2, 1, 1, 0, 0]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(temps: List[int]) -> List[int]:
    """For each day scan forward until a warmer day. O(n^2): the same cold days are rescanned
    from every earlier start."""
    n = len(temps)
    ans = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temps[j] > temps[i]:
                ans[i] = j - i
                break
    return ans


# --- optimal ---
def solve(temps: List[int]) -> List[int]:
    """Stack of indices still waiting for a warmer day; their temperatures decrease bottom to top.
    Each index is pushed once and popped once: O(n)."""
    n = len(temps)
    answer = [0] * n
    waiting = []  # indices; temps[waiting] is decreasing from bottom to top
    for i, t in enumerate(temps):
        log(f"day {i} temp {t:3d} | waiting top->bottom {[(j, temps[j]) for j in reversed(waiting)]}")
        while waiting and temps[waiting[-1]] < t:
            j = waiting.pop()
            answer[j] = i - j
            log(f"    pop day {j} ({temps[j]} < {t}): answer[{j}] = {i} - {j} = {answer[j]}")
        waiting.append(i)
        log(f"    push day {i}; answer so far {answer}")
    return answer


# --- demo ---
def demo():
    return solve([73, 74, 75, 71, 69, 72, 76, 73])


# --- tests ---
def tests():
    assert solve([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert solve([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert solve([30, 60, 90]) == [1, 1, 0]
    assert solve([5, 5, 5]) == [0, 0, 0]  # equal is not warmer
    assert solve([90, 80, 70]) == [0, 0, 0]
    assert solve([]) == []
    assert solve([42]) == [0]
    import random
    for _ in range(200):
        a = [random.randint(1, 20) for _ in range(random.randint(0, 12))]
        assert solve(a) == brute_force(a), a


# --- bugs ---
BUGS = [
    {
        "replace": "        while waiting and temps[waiting[-1]] < t:",
        "with":    "        while waiting and temps[waiting[-1]] <= t:",
        "fix": "should be strict <, equal is not warmer",
        "why": "With <= an equal day pops the waiting day and records a wait, so [5, 5, 5] gives [1, 1, 0] instead of [0, 0, 0].",
        "decoys": [
            {"line": "            answer[j] = i - j", "change": "should be answer[j] = i - j + 1"},
            {"line": "        waiting.append(i)", "change": "should push the temperature t, not the index"},
            {"line": "    answer = [0] * n", "change": "should start as [-1] * n"},
        ],
    },
    {
        "replace": "            answer[j] = i - j",
        "with":    "            answer[j] = i - j - 1",
        "fix": "should be i - j, nothing to subtract",
        "why": "Day j is resolved on day i, so the wait is exactly i - j; subtracting one makes consecutive warmer days report 0.",
        "decoys": [
            {"line": "        while waiting and temps[waiting[-1]] < t:", "change": "should be > so the stack stays increasing"},
            {"line": "        waiting.append(i)", "change": "should run only when the stack is empty"},
            {"line": "    waiting = []  # indices; temps[waiting] is decreasing from bottom to top", "change": "should start with index 0 already pushed"},
        ],
    },
    {
        "replace": "        waiting.append(i)",
        "with":    "        waiting.insert(0, i)",
        "fix": "should be append(i), the top is waiting[-1]",
        "why": "Inserting at the front puts the newest day at the bottom, so the top compared on the next day is the oldest day, and waits are attributed to the wrong days.",
        "decoys": [
            {"line": "            j = waiting.pop()", "change": "should be waiting.pop(0)"},
            {"line": "        while waiting and temps[waiting[-1]] < t:", "change": "should check temps[waiting[0]]"},
            {"line": "    return answer", "change": "should return answer[::-1]"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
