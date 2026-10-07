<a id="tokens"></a>

## Token Bucket Rate Limiter

**Interview variant; explicit contract:** `TokenBucket(capacity, rate).allow(t)` uses one token
per accepted request. The bucket starts full, holds at most `capacity` tokens, and refills at
`rate` tokens/second. This object governs **one client or one shared budget**.
Capacity is a positive integer; rate is positive and finite. Times are finite, nonnegative
numbers in nondecreasing order. Rejections spend no token.

**Q10.** Capacity 2, rate 0.5 tokens/second. Two requests at time 0 pass and empty the bucket.
When is the next request first eligible? **A.** Time 1 · **B.** Time 2 · **C.** Time 10

**Derive the state:** We need two numbers: available tokens and the last time refill was accounted for.
No request history or timer is necessary: calculate how much a timer would have added.

```text
tokens = min(capacity, tokens + elapsed_seconds * rate)
if tokens >= 1: spend 1 and accept
otherwise: reject
```

**Invariant:** After each call, `0 <= tokens <= capacity`, and `last_time` is the time through
which refill has already been counted. Update `last_time` even on rejection, because partial
refill has already been added to `tokens`.

<!-- cell -->

```python
from math import isfinite


class TokenBucket:
    def __init__(self, capacity: int, rate: float):
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        if not isfinite(rate) or rate <= 0:
            raise ValueError("rate must be positive and finite")
        self.capacity = capacity
        self.rate = rate
        self.tokens = float(capacity)          # Initially full.
        self.last_time = None

    def allow(self, t: float) -> bool:
        if not isfinite(t) or t < 0:
            raise ValueError("time must be finite and nonnegative")
        if self.last_time is not None:
            if t < self.last_time:
                raise ValueError("timestamps must be nondecreasing")
            elapsed = t - self.last_time
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_time = t                    # Includes refill counted on rejected calls.
        if self.tokens < 1:
            return False
        self.tokens -= 1
        return True


bucket = TokenBucket(capacity=2, rate=0.5)
answers = []
for t in [0, 0, 0, 1, 2, 2, 4]:
    allowed = bucket.allow(t)
    answers.append(allowed)
    print(f"t={t}: {str(allowed):5}  remaining tokens={bucket.tokens:g}")
assert answers == [True, True, False, False, True, False, True]
assert [bucket.allow(100) for _ in range(3)] == [True, True, False]  # Capacity caps refill.

partial = TokenBucket(1, 0.5)
assert partial.allow(0) is True
assert partial.allow(1) is False               # 0.5 token accrued.
assert partial.allow(1.5) is False             # 0.75 token, not 1.25: no double refill.
assert partial.allow(2) is True
```

<!-- cell -->

**Cost:** O(1) time and space per call for this one budget.

**Crux:** This policy allows an initial burst and then refills. It does not enforce the same
promise as a strict sliding window. With capacity 2 and rate 0.2, two requests at time 0 and
another at time 5 can all pass; a sliding-window limit of 2 per 10 seconds would reject the third.
Choose the policy from the required behavior before choosing the implementation.

For multiple clients, map each client to its own bucket. For exact fractional accounting,
use integer time/token units or rational arithmetic; ordinary floating-point refill can round
near a boundary. The examples use exactly representable values so their boundaries are unambiguous.

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
elif str(answer).strip().upper() == 'B':
    print("Correct. " + 'One token takes 1 / 0.5 = 2 seconds to refill.')
else:
    print("Try again. " + 'One token takes 1 / 0.5 = 2 seconds to refill.')
```

<!-- cell -->

### Your implementation space

Write the state and invariant first, then implement this API without looking at the solution.

<!-- cell -->

```python
# State:
# Invariant:
# Your implementation:
```
