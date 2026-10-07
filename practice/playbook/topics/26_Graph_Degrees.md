## Graph Degrees

Indegree counts incoming edges; outdegree counts outgoing edges. Find the Town Judge asks for someone trusted by all n − 1 others who trusts nobody. Add one for incoming trust and subtract one for outgoing trust; the judge has score n − 1.

<!-- cell -->

```python
def find_judge(n, trust):                         # degrees only: trusted by n - 1 people, trusts nobody
    score = [0] * (n + 1)
    for a, b in trust:
        score[a] -= 1                             # trusting anyone disqualifies a
        score[b] += 1
    return next((i for i in range(1, n + 1) if score[i] == n - 1), -1)

print(find_judge(3, [[1, 3], [2, 3]]), find_judge(3, [[1, 3], [2, 3], [3, 1]]), find_judge(1, []))               # 3 -1 1
```
