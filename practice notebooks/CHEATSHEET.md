# Python LeetCode Cheatsheet

One-page reminder. The full guide (intuition, idea-to-code decisions, traps, edge cases, variations and
runnable experiments for every technique) has one notebook per topic in `practice/LeetCode_Playbook/`,
built from `practice/playbook/topics/` (start with [the topic index](LeetCode_Playbook/00_Topic_Index.ipynb)).

## Built-ins you'll use constantly
```python
from collections import Counter, defaultdict, deque
import heapq, bisect, math
cnt = Counter(s); cnt.most_common(k)      # freq map, top k
g = defaultdict(list); g[u].append(v)     # adjacency / grouping
q = deque([x]); q.append(y); q.popleft()  # O(1) queue
a.sort(key=lambda x: (x[0], -x[1]))       # multi-key sort
bisect.bisect_left(a, x)                  # first index with a[i] >= x
float('inf'), -float('inf'); divmod(a, b); ord(c) - ord('a')
for i, x in enumerate(a); for x, y in zip(a, b); grid = [[0]*C for _ in range(R)]
```

## Hashing / counting  - "have I seen X?" in O(1)
```python
seen = {}                                # value -> index
for i, x in enumerate(nums):
    if target - x in seen: return [seen[target - x], i]
    seen[x] = i
groups[tuple(sorted(w))].append(w)       # anagram key = sorted letters
```

## Prefix sum + hashmap  - "subarray sums to k"
```python
count, total, seen = 0, 0, {0: 1}        # prefix value -> times seen
for x in nums:
    total += x
    count += seen.get(total - k, 0)      # earlier prefix that cuts out sum k
    seen[total] = seen.get(total, 0) + 1
```

## Two pointers  - sorted array / pair / shrink from both ends
```python
l, r = 0, len(a) - 1
while l < r:
    s = a[l] + a[r]
    if s == target: return [l, r]
    if s < target: l += 1                # need bigger -> move left up
    else: r -= 1                         # need smaller -> move right down
```

## Sliding window  - longest/shortest substring with a condition
```python
l, best, window = 0, 0, {}
for r, c in enumerate(s):
    window[c] = window.get(c, 0) + 1     # 1. grow: add s[r]
    while window[c] > 1:                 # 2. shrink while invalid
        window[s[l]] -= 1; l += 1
    best = max(best, r - l + 1)          # 3. record valid window
```

## Binary search  - sorted input OR "smallest x that works"
```python
lo, hi = 0, len(a) - 1                   # find exact target
while lo <= hi:
    mid = (lo + hi) // 2
    if a[mid] == t: return mid
    if a[mid] < t: lo = mid + 1
    else: hi = mid - 1

lo, hi = min_ans, max_ans                # binary search on the answer
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid): hi = mid           # works -> try smaller
    else: lo = mid + 1
return lo
```

## Stack / monotonic stack  - matching brackets, "next greater element"
```python
stack, res = [], [0] * len(t)            # stack of indices, values decreasing
for i, x in enumerate(t):
    while stack and t[stack[-1]] < x:    # x is the answer for everything smaller
        j = stack.pop(); res[j] = i - j
    stack.append(i)
```

## Linked list  - dummy head, reverse, fast/slow
```python
dummy = ListNode(0, head)                # avoids head edge cases
prev, cur = None, head                   # reverse
while cur: cur.next, prev, cur = prev, cur, cur.next
slow = fast = head                       # middle / cycle
while fast and fast.next:
    slow, fast = slow.next, fast.next.next
    if slow is fast: break               # cycle found
```

## Trees  - DFS recursion, BFS by level
```python
def dfs(node):                           # return info up from children
    if not node: return 0
    l, r = dfs(node.left), dfs(node.right)
    return 1 + max(l, r)

q, levels = deque([root]), []            # level order
while q:
    level = []
    for _ in range(len(q)):              # exactly one level
        n = q.popleft(); level.append(n.val)
        if n.left: q.append(n.left)
        if n.right: q.append(n.right)
    levels.append(level)
# BST: inorder = sorted; validate with (low, high) bounds passed down
```

## Trie  - prefix lookups
```python
root = {}
def insert(w):
    node = root
    for c in w: node = node.setdefault(c, {})
    node['$'] = True                     # end-of-word marker
```

## Heap  - top k, k-way merge, running median
```python
h = []
for x in nums:
    heapq.heappush(h, x)                 # min-heap of size k keeps k LARGEST
    if len(h) > k: heapq.heappop(h)      # root = kth largest
heapq.heappush(h, (-dist, i))            # max-heap: negate; tuples sort by first item
# median: max-heap `low` (negated) + min-heap `high`, keep len(low) == len(high) or +1
```

## Intervals  - sort by start, merge or sweep
```python
intervals.sort()
out = [intervals[0]]
for s, e in intervals[1:]:
    if s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)   # overlap -> extend
    else: out.append([s, e])
# rooms needed: min-heap of end times; pop if heap[0] <= start; push end; answer = max len
```

## Backtracking  - choose / explore / un-choose
```python
res = []
def bt(start, path):
    res.append(path[:])                  # record (or only when complete)
    for i in range(start, len(nums)):
        if i > start and nums[i] == nums[i-1]: continue   # skip dups (sorted input)
        path.append(nums[i])             # choose
        bt(i + 1, path)                  # explore (i for reuse, i+1 for no reuse)
        path.pop()                       # un-choose
bt(0, [])
```

## Graphs  - grid BFS/DFS, topo sort, union-find, Dijkstra
```python
DIRS = [(1,0), (-1,0), (0,1), (0,-1)]
q, seen = deque([(r0, c0)]), {(r0, c0)}  # BFS = shortest steps in unweighted graph
while q:
    r, c = q.popleft()
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen and grid[nr][nc] == '1':
            seen.add((nr, nc)); q.append((nr, nc))   # mark when ADDING

indeg = [0] * n                          # topo sort (Kahn)
for u, v in edges: g[u].append(v); indeg[v] += 1
q = deque(i for i in range(n) if indeg[i] == 0); order = []
while q:
    u = q.popleft(); order.append(u)
    for v in g[u]:
        indeg[v] -= 1
        if indeg[v] == 0: q.append(v)
# cycle exists iff len(order) < n

parent = list(range(n))                  # union-find
def find(x):
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False            # already connected -> cycle edge
    parent[ra] = rb; return True

dist, h = {src: 0}, [(0, src)]           # Dijkstra (non-negative weights)
while h:
    d, u = heapq.heappop(h)
    if d > dist.get(u, float('inf')): continue        # stale entry
    for v, w in g[u]:
        if d + w < dist.get(v, float('inf')):
            dist[v] = d + w; heapq.heappush(h, (d + w, v))
# Prim MST: same loop, push (edge weight, v) instead of (d + w, v); skip visited
```

## Bits
```python
x & 1 (odd?)   x >> 1 (÷2)   x & (x-1) (drop lowest 1)   x & -x (lowest 1)
a ^ a == 0  -> XOR all to find the single number     bin(x).count('1')
for mask in range(1 << n): [nums[i] for i in range(n) if mask >> i & 1]  # all subsets
```

## Pick the technique
| Clue in the problem | Reach for |
|---|---|
| pair/complement, "seen before", grouping | hashmap |
| contiguous subarray sum = k (negatives allowed) | prefix sum + hashmap |
| sorted array, pairs/triplets | two pointers |
| longest/shortest substring or window | sliding window |
| sorted / rotated / "minimum max" / "smallest speed" | binary search (on answer) |
| next greater/smaller, histogram | monotonic stack |
| top k, kth largest, merge k sorted | heap |
| all combos / permutations / partitions | backtracking |
| grid regions, shortest steps | BFS / DFS |
| prerequisites, ordering | topological sort |
| connectivity, redundant edge | union-find |
| weighted shortest path | Dijkstra |
| overlapping ranges | sort + merge / heap of ends |
