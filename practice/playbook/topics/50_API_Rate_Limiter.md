<a id="limiter"></a>

## Sliding-Window API Rate Limiter

**Interview variant; explicit contract:** `RateLimiter(limit, window).allow(client, t)` returns
whether this request is accepted. Each client may have at most `limit` **accepted** requests
in **`(t - window, t]`**. Rejected requests consume no quota. Use integer seconds,
positive integer `limit` and `window`, and nondecreasing timestamps across all calls.

**Q4.** Limit 2, window 10: client A calls at times `1, 2, 3, 11, 11`.
Which results are correct?

**A.** `T, T, F, T, F` · **B.** `T, T, F, F, F` · **C.** `T, T, T, T, T`

**Derive the state:** The last accepted time alone cannot enforce a budget larger than one.
We need the accepted timestamps still in the window, separately for each client.

**Invariant:** After a client's call, its deque contains exactly its accepted timestamps
inside the current window, in order; its length never exceeds `limit`.

| Call | Expire | Remaining accepted times | Decision | Stored afterward |
|---|---|---|---|---|
| `allow("A", 1)` | nothing | `[]` | accept | `[1]` |
| `allow("A", 2)` | nothing | `[1]` | accept | `[1, 2]` |
| `allow("A", 3)` | nothing | `[1, 2]` | reject | `[1, 2]` |
| `allow("A", 11)` | `1` | `[2]` | accept | `[2, 11]` |
| `allow("A", 11)` | nothing | `[2, 11]` | reject | `[2, 11]` |

The method has three steps: **expire → check budget → record only if accepted**.

<!-- cell -->

```python
from collections import deque


class RateLimiter:
    def __init__(self, limit: int, window: int):
        if type(limit) is not int or type(window) is not int or limit <= 0 or window <= 0:
            raise ValueError("limit and window must be positive integers")
        self.limit = limit
        self.window = window
        self.accepted = {}                     # client -> deque of accepted timestamps
        self.last_time = None

    def allow(self, client: str, t: int) -> bool:
        if type(t) is not int:
            raise ValueError("timestamps must be integer seconds")
        if self.last_time is not None and t < self.last_time:
            raise ValueError("timestamps must be nondecreasing")
        self.last_time = t
        if client not in self.accepted:
            self.accepted[client] = deque()
        q = self.accepted[client]

        while q and q[0] <= t - self.window:    # Step 1: remove expired accepted requests.
            q.popleft()
        if len(q) >= self.limit:               # Step 2: reject if the budget is full.
            return False
        q.append(t)                           # Step 3: only an acceptance consumes quota.
        return True


limiter = RateLimiter(limit=2, window=10)
calls = [("A", 1), ("A", 2), ("A", 3), ("B", 3), ("A", 11), ("A", 11), ("A", 12)]
answers = []
for client, t in calls:
    allowed = limiter.allow(client, t)
    answers.append(allowed)
    print(f"{client} at {t:2}: {str(allowed):5}   accepted={list(limiter.accepted[client])}")
assert answers == [True, True, False, True, True, False, True]

edge = RateLimiter(2, 10)
assert [edge.allow("A", 5) for _ in range(3)] == [True, True, False]
assert edge.allow("A", 14) is False
assert edge.allow("A", 15) is True           # Both hits at 5 expire together.
assert edge.allow("A", 1000) is True         # Long idle gap.
try:
    edge.allow("A", 999)
except ValueError:
    pass
else:
    raise AssertionError("Backward time must be rejected")
```

<!-- cell -->

**Cost:** O(1) amortized per request; one call can remove O(L) entries where L is the limit.
O(U × L) space for U clients ever seen. Each accepted request enters and leaves a deque at most once.

**Memory detail:** A quiet client's stored timestamps remain until that client calls again.
This implementation does not automatically remove idle dictionary keys. For unbounded client IDs,
add scheduled/global expiry cleanup, validating expiry records before deleting a client's state.

**Why a single count fails:** A count tells us the budget is full, but not when the next slot becomes free.
**Why recording rejections fails:** It charges requests that the contract says should consume no quota.

**Three policies with different promises:**

| Policy | State per client | Promise / trade-off |
|---|---|---|
| Fixed window | Window ID and count | L per aligned window; allows a burst across a boundary |
| Sliding log, above | Accepted timestamps | At most L in every trailing W-second window |
| [Token bucket](56_Token_Bucket.ipynb) | Tokens and last refill time | Controlled bursts with continuous refill |

For a fixed-window limit of 2 per 10 seconds, two requests at time 9 and two at time 10
can all pass because they occupy different aligned windows. This sliding limiter rejects the last two.
In a concurrent service, the complete expire/check/append operation must be atomic for a client.
The class here teaches the sequential algorithm; shared state across processes needs shared atomic storage.

<!-- cell -->

### Check your prediction

Set `answer` to your letter, then run the next cell. The feedback applies to this notebook's question.

<!-- cell -->

```python
answer = None  # Enter "A", "B", or "C".
```

<!-- cell -->

```python
if answer is None:
    print("Choose an answer above, then rerun this cell.")
elif str(answer).strip().upper() == 'A':
    print("Correct. " + 'Only acceptances are recorded. At 11, the request at 1 expires; one slot opens.')
else:
    print("Try again. " + 'Only acceptances are recorded. At 11, the request at 1 expires; one slot opens.')
```

<!-- cell -->

### Practice: implement it yourself



Implement `MyRateLimiter(limit, window).allow(client, t)` using this notebook's contract.
Use these checks once your class is ready:

```py
r = MyRateLimiter(2, 10)
assert r.allow("alice", 1) is True
assert r.allow("alice", 2) is True
assert r.allow("alice", 3) is False
assert r.allow("bob", 3) is True
assert r.allow("alice", 11) is True
assert r.allow("alice", 11) is False
assert r.allow("alice", 12) is True
```

Explain why a single timestamp is insufficient, why rejections do not append,
and why the expiration comparison uses `<=`.

<!-- cell -->

### Your implementation space

Write the state and invariant first, then implement this API without looking at the solution.

<!-- cell -->

```python
# State:
# Invariant:
# Your implementation:
```
