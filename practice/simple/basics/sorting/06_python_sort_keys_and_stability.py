"""
Python Sort Keys and Stability (basics: sorting)
Sort (name, dept, salary) records by dept ascending, then by salary descending.
  (ann, eng, 100) (bob, ops, 90) (cy, eng, 120) (di, ops, 90) (ed, ops, 130)
  ->  (cy, eng, 120) (ann, eng, 100) (ed, ops, 130) (bob, ops, 90) (di, ops, 90)

Idea: tuple keys compare field by field; negating salary flips just that field (one pass).
      Python's sort is stable (ties keep their order, even with reverse=True), so sorting by
      salary FIRST and then by dept keeps the salary order inside each dept (two passes).

Pseudocode:
  one pass:   sorted(records, key=(dept, -salary))
  two passes: by_salary = sorted(records, key=salary, reverse=True)   # minor key first
              sorted(by_salary, key=dept)                             # sort pass 1's OUTPUT

Time O(n log n), space O(n).
"""


def sort_one_pass(records):
    return sorted(records, key=lambda r: (r[1], -r[2]))            # dept asc, salary desc


def sort_two_passes(records):
    by_salary = sorted(records, key=lambda r: r[2], reverse=True)  # minor key first
    return sorted(by_salary, key=lambda r: r[1])                   # stable: salary order kept


if __name__ == "__main__":
    staff = [("ann", "eng", 100), ("bob", "ops", 90), ("cy", "eng", 120),
             ("di", "ops", 90), ("ed", "ops", 130)]
    print([name for name, _, _ in sort_one_pass(staff)])    # ['cy', 'ann', 'ed', 'bob', 'di']
    print([name for name, _, _ in sort_two_passes(staff)])  # ['cy', 'ann', 'ed', 'bob', 'di']
