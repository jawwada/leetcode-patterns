## Python Toolkit

> Python hands you a hash map, a min-heap, a double-ended queue and binary search for free. Turning an idea into code fast is mostly knowing **what each operation costs**, and the handful of traps that silently turn O(1) into O(n) or a correct idea into a wrong answer.

[From Idea to Code](#s01) turned an idea into seven decisions and their lines. Those lines lean on a handful of containers, and this section is what each one costs and where it bites.

Read the trap list once, then come back to a container's cell when you hesitate; every cell runs, so change the inputs and run it again. Which structure an idea needs is in [From Idea to Code](#s01) and [Design Problems](#s24), and the string tools, from `split` to `ord`, `chr` and slicing, are in [Strings](#s20).

### Read this first: the traps

Each trap is one line long and costs minutes to find under pressure, which is why the list comes first. Most of them are shown in a cell or a **Try it** below.

1. **`a.pop(0)`, `a.insert(0, x)` or `x in a_list` inside a loop** cost O(n) each: O(n²) in total. Use a `deque` or a `set`.
2. **Reading a missing key of a `defaultdict` inserts it**: lengths change and loops crash. Test with `in` or `.get`.
3. **`count[x] -= 1` leaves a zero entry**, and `len(count)` still counts it. Delete the key at 0 when `len` means "distinct".
4. **A full `deque(maxlen=k)` drops its oldest item silently**: a running total has to subtract it.
5. **Heap tuples that tie compare their next field**, and objects without `<` crash: push `(priority, counter, item)`.
6. **`bisect_*(a, x, key=f)` applies `f` to the list items only**, so pass `x` as a key; `insort(a, x, key=f)` applies it to `x` too.
7. **A `cmp_to_key` comparator must return a negative number for "x first"**; one that returns a bool never does, so nothing moves.
8. **`a.sort()` returns `None`**: `a = a.sort()` loses the list.
9. **`-7 // 2 == -4`**: Python floors; C and Java truncate toward zero (`trunc_div` below).
10. **`a[(lo + hi) / 2]`**: `/` always makes a float, and a float index raises `TypeError`. Use `//`.
11. **`[[0] * C] * R`** repeats one row object; **`res.append(path)`** stores the path object itself. Copy.
12. **A mutable default argument** (`def f(x, seen=[])`) is shared by every call. Default to `None`.
13. **Assigning to an outer variable inside a nested function** needs `nonlocal`, or you get `UnboundLocalError`.
14. **State created in the class body** (`seen = set()`) is shared by every instance, and an attribute named like a method hides the method. Create state in `__init__` with `self.`.
15. **`max = 0`** (or `sum`, `list`, `id`, ...) shadows the builtin: `max([1, 2])` then raises `TypeError`.
16. **Recursion deeper than about 1000 calls** raises `RecursionError`: use an explicit stack.
17. **`a[i], a[a[i]] = a[a[i]], a[i]`**: targets are assigned left to right. Compute the index first.
18. **`s += c` in a loop** may copy the whole string every time: collect the parts, `"".join` them once.

### What each operation costs

Decision 1 picks a structure; this table says what each of its operations costs, so that an O(n) idea stays O(n) in code. Look things up here, and read the cells below for the traps in context.

| Container | Operation | Cost |
|---|---|---|
| any built-in | `len(x)` | O(1) |
| list | `a[i]`, `a[i] = x`, `a.append(x)`, `a.pop()` | O(1); append and pop are amortised |
| list | `a.pop(0)`, `a.insert(0, x)`, `a.pop(i)`, `a.insert(i, x)` | O(n): every item after `i` shifts |
| list | `x in a`, `a.index(x)`, `a.remove(x)`, `a.count(x)`, `min(a)`, `sum(a)` | O(n): a scan |
| list | `a[i:j]`, `a + b`, `a[::-1]`, `list(a)` | O(size of the result): a copy |
| list | `a.sort()`, `sorted(a)` | O(n log n) |
| dict | `d[k]`, `d[k] = v`, `k in d`, `del d[k]`, `d.get(k, 0)`, `d.pop(k)` | O(1) average |
| dict | loop over `d` or `d.items()`, `max(d, key=d.get)` | O(n); insertion order is kept |
| set | `s.add(x)`, `s.discard(x)`, `x in s` / union, intersection, difference | O(1) average / at most O(len(s) + len(t)) |
| Counter | `Counter(a)` / `c.most_common(k)` | O(n) / O(n log k) |
| deque | `append`, `appendleft`, `pop`, `popleft`, `q[0]`, `q[-1]` / `q[i]` in the middle, `x in q` | O(1) / O(n) |
| OrderedDict | `move_to_end(k)`, `popitem(last=False)` | O(1) |
| heapq | `h[0]` (the min) / `heappush`, `heappop` / `heapify(a)` | O(1) / O(log n) / O(n) |
| heapq | `nlargest(k, a)`, `nsmallest(k, a)` | O(n log k) |
| heapq | remove an arbitrary item | not supported: O(n) search + re-heapify, or lazy deletion |
| bisect | `bisect_left`, `bisect_right` / `insort(a, x)` | O(log n) / O(n): the insert shifts |
| str | `s[i]` / `s + t`, `s[i:j]`, `s == t`, `"".join(parts)` | O(1) / O(the lengths involved) |
| str | `s in t`, `t.find(s)`, `t.count(s)` | O(len(t) · len(s)) as the safe worst case |

*Amortised* O(1) means that an occasional `append` copies the whole list into a bigger block, but averaged over all the appends each one costs O(1).

"O(1)" for a dict or set means O(1) *hashes*, and hashing a `str` or `tuple` key costs O(its length). A `str` caches its hash after the first time. A `tuple` is rehashed on every lookup up to Python 3.13, and from 3.14 it caches its hash too.

### Lists, dicts and sets

A list is a row of slots: taking from the **end** touches one slot, taking from the **front** makes every other item slide over. A set jumps straight to an item's hash slot, while `x in a_list` compares x with `a[0]`, `a[1]`, ... in turn.

The cell does each of these once and prints what came out, then turns to a dict: the two ways to read a key that may be missing, and the fact that insertion order is kept. Remember that `{}` is an empty dict; an empty set is `set()`.

```python
a = [5, 3, 8]
a.append(1)                          # O(1): add at the end
last = a.pop()                       # O(1): remove from the end
first = a.pop(0)                     # O(n): every other item shifts one slot left
print(a, last, first)                # [3, 8] 1 5

seen = set(a)                        # build once: O(n)
print(8 in seen, 8 in a)             # True True   (same answer: the set looks up, the list scans)

d = {"x": 1}
print(d.get("y", 0), "y" in d)       # 0 False     (get never raises and never inserts)
d.setdefault("y", []).append(7)      # insert a default only if missing, then use it
d["x"] += 1
print(d, list(d))                    # {'x': 2, 'y': [7]} ['x', 'y']   (insertion order is kept)
```

**Try it**
- Time the shift: `import time`, then drain `list(range(20_000))` with `pop(0)` and `deque(range(20_000))` with `popleft()`, timing each with `time.perf_counter()`. The deque is dozens of times faster, and doubling the size makes the list roughly 5 times slower (quadratic) but the deque only twice as slow (linear).
- `d["z"]` raises `KeyError: 'z'`, while `d.get("z")` quietly returns `None`. Use `[]` when a missing key is a bug, `.get` when it is normal.
- `a.remove(8)` deletes only the first 8 and leaves `[3]`; a second `a.remove(8)` raises `ValueError`. On the set, `seen.discard(8)` never raises, and `seen.add(3)` for an item already there changes nothing.

### collections: Counter, defaultdict, deque, OrderedDict

`Counter` and `defaultdict` remove the "is the key there yet?" branch, and `deque` and `OrderedDict` give O(1) moves at both ends. Group Anagrams is the classic use of a `defaultdict`: words made of the same letters go in one group, `["eat", "tea", "tan", "ate", "nat"] → [["eat", "tea", "ate"], ["tan", "nat"]]`, and a group's key is its words' sorted letters.

LRU Cache is the classic use of an `OrderedDict`: a cache of fixed size evicts the key that has gone unused for longest, so the key just used moves to the end and the oldest key leaves from the front. The cell counts the letters of a word, groups the anagrams, keeps a window of the last three items with a bounded deque, and ends with that LRU move.

```python
count = Counter("mississippi")
print(count["s"], count["z"], len(count))     # 4 0 4   (a missing key reads as 0 and is NOT added)
print(count.most_common(2))                   # [('i', 4), ('s', 4)]

groups = defaultdict(list)                    # a missing key starts as a fresh empty list
for word in ["eat", "tea", "tan", "ate", "nat"]:
    groups["".join(sorted(word))].append(word)    # anagram key: the sorted letters
print(list(groups.values()))                  # [['eat', 'tea', 'ate'], ['tan', 'nat']]
seen_count = defaultdict(int)
print(seen_count["ghost"], len(seen_count))   # 0 1     (READING a missing key inserted it!)

recent = deque(maxlen=3)                      # a fixed-size window: old items fall off the far end
for x in range(6):
    recent.append(x)
print(recent)                                 # deque([3, 4, 5], maxlen=3)
od = OrderedDict.fromkeys("abc")              # keys a, b, c in insertion order
od.move_to_end("a")                           # "a" was just used: it becomes the newest
print(list(od), od.popitem(last=False))       # ['b', 'c', 'a'] ('b', None)   the OLDEST leaves: an LRU eviction
```

**Try it**
- `c = Counter("aab")`, then `c["b"] -= 1`: `c` is `Counter({'a': 2, 'b': 0})` and `len(c)` is still 2. When `len` means "distinct values", `del c["b"]` as soon as it reaches 0.
- Keep a running total next to `q = deque(maxlen=3)`: append 5, 1, 1, 1, doing `total += x` each time. `total` is 8 but `sum(q)` is 3, because the 5 fell off silently. Subtract the item that is about to fall off, or run the window yourself with `popleft()`.
- Replace `defaultdict(list)` with `{}` and rerun: `KeyError: 'aet'` on the very first word.
- Predict `od.popitem()` after the cell (the default `last=True` pops the newest): `('a', None)`.

### heapq: a min-heap that lives in a plain list

A heap answers "the smallest, again and again" in O(log n) per operation, and Python's lives in a plain list:

```text
h = [1, 2, 8, 3, 5]          the list IS the tree: the children of index i are 2i+1 and 2i+2

            1                h[0] is always the smallest
          /   \              nothing else is sorted: each parent is just
         2     8             <= its own children
        / \
       3   5
```

For a max-heap, push `-x` and negate again on the way out. Python 3.14 adds `heapq.heappush_max` and friends, but negation works on every version.

Tuples compare field by field, so when two priorities tie, Python compares the *next* field. If that field is an object without `<`, a node or a dict, the heap crashes, but only on a tie, which is why small tests miss it. The cell builds a heap, takes its minimum, flips it into a max-heap, then shows the tie crash and the counter that settles it.

```python
h = [5, 1, 8, 3, 2]
heapq.heapify(h)                          # O(n), in place: h[0] is now the minimum
heapq.heappush(h, 0)
print(h[0], heapq.heappop(h), heapq.heappop(h))    # 0 0 1
print(heapq.nlargest(2, [5, 1, 8, 3]), heapq.nsmallest(2, [5, 1, 8, 3]))   # [8, 5] [1, 3]

max_heap = [-x for x in [5, 1, 8]]       # max-heap: store -x, negate again on the way out
heapq.heapify(max_heap)
print(-max_heap[0])                       # 8


class Job:                                # an object that defines no "<"
    def __init__(self, name):
        self.name = name


jobs = [(1, Job("a"))]
try:
    heapq.heappush(jobs, (1, Job("b")))   # equal priorities -> Python compares the two Jobs
except TypeError as e:
    print("TypeError:", e)                # TypeError: '<' not supported between instances of 'Job' and 'Job'

jobs, order = [], 0
for name in ["a", "b", "c"]:
    heapq.heappush(jobs, (1, order, Job(name)))   # a unique counter settles every tie
    order += 1
print([heapq.heappop(jobs)[2].name for _ in range(3)])   # ['a', 'b', 'c']  (first in, first out on ties)
```

**Try it**
- Print `h` right after `heapq.heapify(h)`: `[1, 2, 8, 3, 5]`, the tree in the picture. Only `h[0]` is promised to be the smallest.
- Drop the minus sign on the way out (`print(max_heap[0])`): `-8`. Negate on the way in *and* on the way out.
- Give `Job` a `priority` and a `__lt__` that compares priorities, then push four Jobs a, b, c, d with the same priority and no counter: no `TypeError`, but they pop as a, c, b, d. A heap is not stable; only the counter gives first in, first out.

### bisect: binary search you don't have to write

When the state is a sorted list, `bisect` is the lookup, and the only question is which of its two functions to call:

```text
a = [1, 2, 2, 2, 5]
     0  1  2  3  4  5        the numbers under the items are insertion points

bisect_left(a, 2)  = 1      first index with a[i] >= 2   =  how many items are <  2
bisect_right(a, 2) = 4      first index with a[i] >  2   =  how many items are <= 2
                            the 2s live in a[1:4]: 4 - 1 = 3 copies
```

The cell counts the copies of a value and the items in a range with the two functions, and finds the largest item at most x. It ends with the lookup that Time Based Key-Value Store is built on: values are stored with rising timestamps, and `get` returns the latest value at or before a given time.

```python
a = [1, 2, 2, 2, 5]
print(bisect.bisect_left(a, 2), bisect.bisect_right(a, 2))    # 1 4
print(bisect.bisect_right(a, 2) - bisect.bisect_left(a, 2))   # 3   copies of 2
print(bisect.bisect_left(a, 3), bisect.bisect_right(a, 3))    # 4 4  (3 is absent: both give its insertion point)


def count_between(a, lo, hi):             # how many items x with lo <= x <= hi
    return bisect.bisect_right(a, hi) - bisect.bisect_left(a, lo)


def floor_item(a, x):                     # the largest item <= x, or None
    i = bisect.bisect_right(a, x) - 1
    return a[i] if i >= 0 else None


print(count_between(a, 2, 5), floor_item(a, 4), floor_item(a, 0))   # 4 2 None

times = [(1, "a"), (4, "b"), (9, "c")]    # key= (Python 3.10+) is applied to the ITEMS, not to x
i = bisect.bisect_right(times, 5, key=lambda p: p[0])
print(i, times[i - 1][1])                 # 2 b   (the latest entry with time <= 5)
```

**Try it**
- In `count_between`, use `bisect_left` for the `hi` end too: `count_between(a, 2, 5)` drops to 3, because the 5 itself is no longer counted.
- In `floor_item`, use `bisect_left` instead of `bisect_right`: `floor_item(a, 2)` returns 1 instead of 2 (it stops before the first 2).
- `bisect.insort(times, (6, "z"), key=lambda p: p[0])` works, because `insort` applies the key to the new item too. `bisect.bisect_right(times, (6, "z"), key=lambda p: p[0])` raises `TypeError: '<' not supported between instances of 'tuple' and 'int'`: pass the key `6`, not the record.
- Write `ceil_item(a, x)`, the smallest item `>= x`: `i = bisect.bisect_left(a, x)`, valid while `i < len(a)`. Check `ceil_item(a, 3) == 5` and `ceil_item(a, 6) is None`.

**Python has no TreeMap**, the sorted map with O(log n) insert, delete and nearest-key lookups that Java and C++ offer. A sorted list plus `bisect` stands in for it: each insert is O(n), but it is one fast memory move, and 100,000 random `insort`s take under half a second.

When you only ever need the min or the max, a heap with lazy deletion is enough: it leaves a removed item in place and skips it when it reaches the top. And if the interviewer allows the library, `sortedcontainers.SortedList` is the real thing.

### Sorting: keys and stability

`key=` turns each item into the thing to compare. Tuples compare field by field, so a tuple key is a multi-level sort, and negating a number flips just that level. An order that depends on the pair rather than on one item needs `cmp_to_key`; Largest Number, which arranges numbers so that their concatenation is the largest, is taken apart in [Sorting & Selection](#s23).

Python's sort is **stable**: items with equal keys keep their input order. The cell sorts four people oldest first, with names breaking ties, then by age alone, where stability keeps each tie in input order. It ends with the trap of `.sort()`, which returns `None`.

```python
people = [("ann", 30), ("bob", 25), ("cy", 30), ("di", 25)]
print(sorted(people, key=lambda p: (-p[1], p[0])))   # [('ann', 30), ('cy', 30), ('bob', 25), ('di', 25)]
print(sorted(people, key=lambda p: p[1]))            # [('bob', 25), ('di', 25), ('ann', 30), ('cy', 30)]

print([3, 1, 2].sort(), sorted([3, 1, 2]))         # None [1, 2, 3]   (.sort() works in place and returns None)
```

**Try it**
- Age ascending, name *descending* (you can't negate a string): sort twice, minor key first, and let stability keep it: `sorted(sorted(people, key=lambda p: p[0], reverse=True), key=lambda p: p[1])` gives `[('di', 25), ('bob', 25), ('cy', 30), ('ann', 30)]`.
- `sorted(people, key=lambda p: p[1], reverse=True)` keeps `ann` before `cy` (both 30): `reverse=True` reverses the comparison, not the order of ties.
- Sort `["bb", "a", "cc", "d"]` by `len`: `['a', 'd', 'bb', 'cc']`, ties in input order.
- Hand `cmp_to_key` a comparator that returns a bool: `sorted([3, 1, 2], key=cmp_to_key(lambda x, y: x > y))` gives `[3, 1, 2]`, unchanged and with no error. A bool is never negative, so no item ever counts as smaller; return -1, 1 or 0.

### Numbers: division, modulo, infinity

Integer division and modulo are where Python quietly disagrees with C and Java, and index arithmetic and binary search depend on them. The cell shows which way `//` and `%` round, a division that truncates toward zero without touching floats, and how `math.inf`, `min(..., default=)` and `math.isclose` stand in for "nothing found yet" and "equal enough".

```python
print(7 // 2, -7 // 2, int(-7 / 2))      # 3 -4 -3   // floors toward -inf; int() truncates toward 0
print(-7 % 3, 7 % -3, divmod(-7, 3))     # 2 -2 (-3, 2)   the remainder takes the divisor's sign
print((0 - 1) % 5)                        # 4   wrap-around index: one step left of 0 is 4


def trunc_div(a, b):                      # C/Java-style division, no floats involved
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


print(trunc_div(-7, 2), trunc_div(7, -2), trunc_div(7, 2))   # -3 -3 3

print(min(math.inf, 7), math.inf > 10**100, min([], default=-1))   # 7 True -1   (inf = "nothing found yet")
print(0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3), round(2.5))  # False True 2   (ties round to even)
```

**Try it**
- Run `6 // -132` and `trunc_div(6, -132)`: `-1` and `0`. The problem Evaluate Reverse Polish Notation, which computes a postfix expression given as a list of tokens, divides toward zero, so it expects the `0`.
- `int(a / b)` also truncates, but through a float: `int(10**18 / 3)` is `333333333333333312`, while `10**18 // 3` is `333333333333333333`.
- In a binary search, `a[(lo + hi) / 2]` raises `TypeError: list indices must be integers or slices, not float`. In Python 3, `/` always makes a float.
- `min([])` without `default=` raises `ValueError`. And `2**31 - 1 + 1` prints `2147483648`: Python never overflows, so when a problem says "32-bit integer", compare against `2**31 - 1` yourself.

### Copying and aliasing

Two names for one object is the trap behind most wrong grids and wrong backtracking answers. `bad = [[0] * 3] * 2` makes **one** row object and lists it twice; a comprehension makes a fresh row per iteration. The second half of the cell shows the three kinds of copy: an alias, a shallow copy that shares the inner lists, and a deep copy that shares nothing.

```python
bad = [[0] * 3] * 2                      # ONE row object, listed twice
bad[0][0] = 1
good = [[0] * 3 for _ in range(2)]       # a fresh row per iteration
good[0][0] = 1
print(bad, good)                          # [[1, 0, 0], [1, 0, 0]] [[1, 0, 0], [0, 0, 0]]

import copy
a = [1, [2, 3]]
alias, shallow, deep = a, a[:], copy.deepcopy(a)   # list(a) and a.copy() are shallow, like a[:]
a[0] = 9                                  # replace slot 0: only the alias sees it
a[1].append(4)                            # change the inner list: the shallow copy shares it
print(alias, shallow, deep)               # [9, [2, 3, 4]] [1, [2, 3, 4]] [1, [2, 3]]
```

**Try it**
- Print `[id(row) for row in bad]` and `[id(row) for row in good]`: two equal ids, then two different ones.
- The same trap in backtracking: `res, path = [], []`, then `for x in [1, 2]: path.append(x); res.append(path)` gives `[[1, 2], [1, 2]]`. Append `path[:]` to record a snapshot: `[[1], [1, 2]]`.
- `rows = [[]] * 3`, then `rows[0].append(1)`: `[[1], [1], [1]]`. The inner `[0] * 3` was safe only because ints can't change.

### Functions and classes: state that is shared by accident

A mutable default argument and a rebinding inside a nested function are the two ways a function keeps state you did not mean it to keep. The default list below is created once, at `def` time, and every call appends to the same one; the fix is a `None` default and a fresh list inside. The leaf counter needs `nonlocal`, because `leaves += 1` rebinds the name, and without the declaration Python treats `leaves` as a new local of `dfs`.

```python
def add_item(x, bucket=[]):              # BUG: the default list is created ONCE, at def time
    bucket.append(x)
    return bucket


def add_item_fixed(x, bucket=None):
    bucket = [] if bucket is None else bucket   # a new list on every call
    bucket.append(x)
    return bucket


print(add_item(1), add_item(2), add_item_fixed(1), add_item_fixed(2))   # [1, 2] [1, 2] [1] [2]


def count_leaves(tree, root):             # tree: node -> list of children
    leaves = 0

    def dfs(node):
        nonlocal leaves                   # leaves += 1 REBINDS the name, so declare it
        if not tree[node]:
            leaves += 1
        for child in tree[node]:
            dfs(child)

    dfs(root)
    return leaves


print(count_leaves({"r": ["a", "b"], "a": ["c"], "b": [], "c": []}, "r"))   # 2
```

**Try it**
- Delete the `nonlocal leaves` line: `UnboundLocalError`, because assigning to `leaves` inside `dfs` makes it a new local name there.
- Print `add_item.__defaults__` after the calls: `([1, 2],)`. The shared list lives on the function object itself.
- Use a one-item box instead, `leaves = [0]` with `leaves[0] += 1` (and `return leaves[0]`): it works without `nonlocal`, because you change the list's content, not the name. In a class, `self.leaves` does the same job.
- Shadow a builtin: `max = 0`, then `max([1, 2])` raises `TypeError: 'int' object is not callable`. `del max` brings the builtin back; in a notebook, one stray `max = ...` or `list = ...` breaks every later cell.

A design question is a class, and classes have their own ways of sharing state by accident. A set created in the class body is one set for every instance, and an attribute named like a method hides the method. Both are in the cell.

```python
class Tracker:
    seen = set()                          # BUG: a class attribute: ONE set shared by every Tracker

    def __init__(self):
        self.mine = set()                 # instance state: create it in __init__, with self.

    def add(self, x):
        self.seen.add(x)
        self.mine.add(x)


t1, t2 = Tracker(), Tracker()
t1.add(1)
print(t2.seen, t2.mine)                   # {1} set()   <- t2 never added anything


class Bits:
    def __init__(self, size):
        self.count = 0                    # BUG: this attribute hides the method below

    def count(self):
        return self.count


try:
    Bits(3).count()
except TypeError as e:
    print("TypeError:", e)                # TypeError: 'int' object is not callable
```

**Try it**
- Move `seen = set()` into `__init__` as `self.seen = set()`: `t2.seen` prints `set()`.
- Rename the attribute to `self.ones` (and `return self.ones`): `Bits(3).count()` returns 0.
- Forget `self.`: in a class `Forgot` whose `__init__` says `hits = deque()`, the first method that touches `self.hits` raises `AttributeError: 'Forgot' object has no attribute 'hits'`. The deque was a local variable of `__init__` and vanished.

### Recursion: the limit and the iterative rewrite

Python stops recursion at about 1000 nested calls, and a linked list or a path-shaped tree with 10^5 nodes is far deeper. `sys.setrecursionlimit(10**5)` is the quick fix people use on LeetCode; an explicit stack is the robust answer, and the one to give in an interview.

The cell first hits the limit on a 10,000-deep chain, then rewrites DFS with an explicit stack. The iterative `dfs_order` visits the same nodes as a recursive DFS, and on a tree in the same order. On a graph whose nodes share neighbours the order can differ, which is fine for reachability and flood fill but not for an order-sensitive DFS such as cycle detection by colouring or a postorder topological sort.

```python
def length_recursive(node):              # node = (value, next_node) or None
    return 0 if node is None else 1 + length_recursive(node[1])


chain = None
for v in range(10_000):                   # 10,000 deep: past the default limit of 1000
    chain = (v, chain)
try:
    length_recursive(chain)
except RecursionError:
    print("RecursionError")               # RecursionError


def dfs_order(graph, start):              # iterative DFS: an explicit stack, no depth limit
    seen, order, stack = {start}, [], [start]
    while stack:
        node = stack.pop()
        order.append(node)
        for nxt in reversed(graph[node]): # reversed: on a tree, children pop left to right
            if nxt not in seen:
                seen.add(nxt)             # marked when pushed, so each node is pushed once
                stack.append(nxt)
    return order


print(dfs_order({1: [2, 3], 2: [4], 3: [], 4: []}, 1))   # [1, 2, 4, 3]
```

**Try it**
- Build a chain of 500 instead and print `length_recursive(chain)`: 500. The limit is about depth, not speed.
- Run `dfs_order({"a": ["b", "c"], "b": ["c", "d"], "c": [], "d": []}, "a")`: `['a', 'b', 'd', 'c']`, while a recursive DFS visits a, b, c, d. The node "c" was marked when "a" pushed it, so "b" skipped it.
- Change `stack.pop()` to `stack.pop(0)` *and* remove `reversed`: `[1, 2, 3, 4]`. Taking from the front turned the stack into a queue, and DFS into BFS.

### Small idioms: loops, unpacking, swaps

The last cell is the small change that interview code is made of: `enumerate` with a start, a countdown `range`, `zip` for neighbouring pairs, star unpacking and the swap. It ends with the one swap that goes wrong, because the targets of an assignment are filled left to right.

```python
letters = ["x", "y", "z"]
print(list(enumerate(letters, start=1)))                  # [(1, 'x'), (2, 'y'), (3, 'z')]
print(list(range(4, -1, -1)), list(zip([1, 2, 3], "ab")))   # [4, 3, 2, 1, 0] [(1, 'a'), (2, 'b')]  zip stops at the shorter
nums = [1, 4, 9, 16]
print([b - a for a, b in zip(nums, nums[1:])])           # [3, 5, 7]   neighbouring pairs
first, *rest = nums
x, y = 1, 2
x, y = y, x                                               # swap: the right side is built first
print(first, rest, x, y)                                  # 1 [4, 9, 16] 2 1

arr, i = [2, 0, 1], 0
arr[i], arr[arr[i]] = arr[arr[i]], arr[i]                 # BUG: the targets are assigned left to right
print(arr)                                                # [1, 2, 1]   arr[arr[i]] used the NEW arr[i]
```

**Try it**
- Freeze the index first: `arr = [2, 0, 1]`, `j = arr[i]`, then `arr[i], arr[j] = arr[j], arr[i]` gives `[1, 0, 2]`.
- Change `range(4, -1, -1)` to `range(4, 0, -1)`: the 0 disappears, because the stop value is never included.
- `list(zip([1, 2, 3], "ab", strict=True))` (Python 3.10+) raises `ValueError` instead of silently dropping the 3.
- Remove items while looping over the same list: with `vals = [1, 3, 5, 6]`, a loop `for v in vals:` whose body is `if v % 2: vals.remove(v)` leaves `[3, 6]`. Loop over a copy (`vals[:]`) or build a new list.

### lru_cache, only as a convenience

`@lru_cache(maxsize=None)` on a recursive function is a memo dict you didn't have to write, `arguments -> result`. The arguments become dict keys, so they must be hashable: pass a tuple, not a list. The cache also outlives the call, so when the function reads outside data, define it inside the solving function or call `f.cache_clear()`.

Be ready to write the dict yourself: `if args in memo: return memo[args]`, compute, store, return. Memoised recursion is the bridge to dynamic programming, which [Dynamic Programming](#s25) maps.

### Self-check

1. In a sorted list, which call counts the items `<= x`, and which counts the items `< x`?
<details><summary>Answer</summary><code>bisect_right(a, x)</code> counts the items <code>&lt;= x</code> (it lands just past the last copy of x); <code>bisect_left(a, x)</code> counts the items <code>&lt; x</code> (it lands on the first copy).</details>

2. `heapq.heappush(h, (dist, node))`, where `node` is a `ListNode`, works on small tests and crashes on a big one. Why, and what is the fix?
<details><summary>Answer</summary>Two entries tied on <code>dist</code>, so Python compared the <code>ListNode</code> objects, which define no <code>&lt;</code>. Ints and strings would tie safely; objects don't. Push <code>(dist, counter, node)</code> with a unique counter so every tie is settled before reaching the node.</details>

3. Two instances of your `HitCounter` class report each other's hits. What is the most likely line to look for?
<details><summary>Answer</summary>State created in the class body, e.g. <code>hits = deque()</code> directly under <code>class HitCounter:</code>. That is one deque shared by every instance. Create it in <code>__init__</code> as <code>self.hits = deque()</code>.</details>
