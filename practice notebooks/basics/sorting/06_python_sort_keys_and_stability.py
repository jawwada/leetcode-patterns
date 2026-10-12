"""
Python Sort Keys and Stability - Basics
Area: sorting
Key operations: key= returning a tuple, negate a number to flip one field, two stable passes with the minor key first

Sort records (name, dept, salary) by dept ascending then salary descending. One pass with the tuple key
(dept, -salary) does it. Two passes do it too, minor key FIRST: sort by salary descending, then by dept;
the second sort is stable, so within a dept the salary order survives. Records that tie on both keys
stay in input order either way. solve returns the sorted records and checks that both ways agree.
Example: [("ann", "eng", 100), ("bob", "ops", 90), ("cy", "eng", 120), ("di", "ops", 90), ("ed", "ops", 130)]
      -> [("cy", "eng", 120), ("ann", "eng", 100), ("ed", "ops", 130), ("bob", "ops", 90), ("di", "ops", 90)]
"""
from typing import List, Tuple


Record = Tuple[str, str, int]


# --- brute force ---
def brute_force(records: List[Record]) -> List[Record]:
    """Insertion sort on the same tuple key; stable because it shifts only strictly greater keys. O(n^2)."""
    key = lambda r: (r[1], -r[2])  # noqa: E731
    out = []
    for r in records:
        i = len(out)
        while i > 0 and key(out[i - 1]) > key(r):
            i -= 1
        out.insert(i, r)
    return out


# --- optimal ---
def solve(records: List[Record]) -> List[Record]:
    """One tuple-key pass; two stable passes give the same order. O(n log n)."""
    one_pass = sorted(records, key=lambda r: (r[1], -r[2]))
    by_salary = sorted(records, key=lambda r: r[2], reverse=True)
    two_pass = sorted(by_salary, key=lambda r: r[1])
    assert one_pass == two_pass
    return one_pass


# --- demo ---
def demo():
    return solve([("ann", "eng", 100), ("bob", "ops", 90), ("cy", "eng", 120), ("di", "ops", 90), ("ed", "ops", 130)])


# --- bugs ---
BUGS = [
    {
        "replace": "    one_pass = sorted(records, key=lambda r: (r[1], -r[2]))",
        "with":    "    one_pass = sorted(records, key=lambda r: (r[1], r[2]))",
        "fix": "negate the salary inside the key so it sorts descending while dept stays ascending",
        "why": "Without the minus both fields go ascending: ann (100) comes before cy (120) and the two-pass check fails.",
        "decoys": [
            {"line": "    by_salary = sorted(records, key=lambda r: r[2], reverse=True)", "change": "should drop reverse=True and negate instead"},
            {"line": "    assert one_pass == two_pass", "change": "should compare sets"},
            {"line": "    return one_pass", "change": "should return two_pass"},
        ],
    },
    {
        "replace": "    two_pass = sorted(by_salary, key=lambda r: r[1])",
        "with":    "    two_pass = sorted(records, key=lambda r: r[1])",
        "fix": "the second pass must sort the OUTPUT of the first pass; chaining is what makes stability do the work",
        "why": "Sorting the original records by dept keeps input order within a dept, so ann (100) stays before cy (120).",
        "decoys": [
            {"line": "    one_pass = sorted(records, key=lambda r: (r[1], -r[2]))", "change": "should be key (-r[2], r[1])"},
            {"line": "    by_salary = sorted(records, key=lambda r: r[2], reverse=True)", "change": "should sort by r[1] first"},
            {"line": "    assert one_pass == two_pass", "change": "should be removed"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
