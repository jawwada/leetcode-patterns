<a id="logger"></a>

## Logger Rate Limiter

**Contract:** `shouldPrintMessage(timestamp, message)` returns `True` if this message may
be printed now. After a successful print, the same message must wait 10 seconds.
Calls have nondecreasing integer timestamps. Different messages have independent cooldowns.

**Q1.** `"error"` prints at time 1 and is rejected at time 9. When is it next eligible?
**A.** 10 · **B.** 11 · **C.** 19

**Derive the state:** Scanning all previous prints would work, but only the latest successful
print of this message can block it. Store `next_allowed[message]`.

**Invariant:** Each stored value is the earliest time this message can next print.
Rejected calls leave that value unchanged.

| Call | Next allowed before | Return | Next allowed after |
|---|---:|---|---:|
| `shouldPrintMessage(1, "error")` | absent | True | 11 |
| `shouldPrintMessage(9, "error")` | 11 | False | 11 |
| `shouldPrintMessage(11, "error")` | 11 | True | 21 |

<!-- cell -->

```python
class Logger:
    def __init__(self):
        self.next_allowed = {}                 # message -> earliest allowed time

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if message in self.next_allowed and timestamp < self.next_allowed[message]:
            return False                      # Rejection must not extend the cooldown.
        self.next_allowed[message] = timestamp + 10
        return True


logger = Logger()
calls = [(1, "error"), (2, "warning"), (9, "error"), (11, "error")]
answers = [logger.shouldPrintMessage(t, message) for t, message in calls]
print(answers)                                # [True, True, False, True]
assert answers == [True, True, False, True]

edge = Logger()
assert edge.shouldPrintMessage(0, "x") is True
assert edge.shouldPrintMessage(0, "x") is False
assert edge.shouldPrintMessage(9, "x") is False
assert edge.shouldPrintMessage(10, "x") is True  # Exact boundary; rejection did not reset it.
```

<!-- cell -->

**Cost:** O(1) per call; O(M) space for M distinct messages ever seen.

**Crux:** The dictionary key is the message; the remembered event is its last **successful** print.
Updating the cooldown before returning `False` would keep delaying a frequently retried message.

**Follow-up:** This basic dictionary retains idle messages. To reclaim expired entries, add a
queue of expiry records and remove them as time advances. Only delete a dictionary entry if
its current expiry still matches the record being removed.

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
    print("Correct. " + 'A successful print at 1 permits another at 11. A rejection at 9 does not reset the cooldown.')
else:
    print("Try again. " + 'A successful print at 1 permits another at 11. A rejection at 9 does not reset the cooldown.')
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
