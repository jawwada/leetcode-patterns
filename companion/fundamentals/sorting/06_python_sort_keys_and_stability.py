"""
Python Sort Keys and Stability - Fundamentals
Chapter: fundamentals/sorting
Key operations: tuple key, negate a field to flip it, two stable passes with the minor key first

Sort records (name, dept, salary) by dept ascending then salary descending. One pass with the tuple
key (dept, -salary) does it. Two passes do it too, minor key FIRST: sort by salary descending, then
by dept; the second sort is stable, so within a dept the salary order survives. Ties keep order.
Example: [("ann", "eng", 100), ("bob", "ops", 90), ("cy", "eng", 120), ("di", "ops", 90)]
      -> [("cy", "eng", 120), ("ann", "eng", 100), ("bob", "ops", 90), ("di", "ops", 90)]
"""


# --- algorithm ---
def dept_then_salary_desc(record):
    """Key for one pass: dept ascending, salary descending (negating flips just that field)."""
    name, dept, salary = record
    return (dept, -salary)


def salary_of(record):
    return record[2]


def dept_of(record):
    return record[1]


def sort_one_pass(records):
    """One sort with a tuple key. O(n log n)."""
    return sorted(records, key=dept_then_salary_desc)


def sort_two_passes(records):
    """Minor key first (salary desc), then major key (dept): the stable second pass keeps it."""
    by_salary = sorted(records, key=salary_of, reverse=True)
    return sorted(by_salary, key=dept_of)   # sort the OUTPUT of the first pass, not the original


# --- try it ---
people = [("ann", "eng", 100), ("bob", "ops", 90), ("cy", "eng", 120), ("di", "ops", 90),
          ("ed", "ops", 130)]
print(sort_one_pass(people))
# -> [('cy', 'eng', 120), ('ann', 'eng', 100), ('ed', 'ops', 130), ('bob', 'ops', 90),
#     ('di', 'ops', 90)]
print(sort_two_passes(people))
# -> the same list: the two ways agree
print(sort_two_passes([("a", "x", 1), ("b", "x", 1)]))   # -> [('a', 'x', 1), ('b', 'x', 1)]  (tie)
print(sort_one_pass([("a", "x", 1), ("b", "x", 2)]))     # -> [('b', 'x', 2), ('a', 'x', 1)]
