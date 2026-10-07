## Error Count Tracker — Practice

Practice combining a dictionary per service with a time window. The Hit Counter notebook contains the prerequisite bucketed-queue technique.

<!-- cell -->

### Practice contract



Design `ErrorTracker(window)` with `record(service, t)` and `count(service, t)`.
Count **all** recorded errors for that service in `(t - window, t]`; a count for an unknown
service is 0. Calls use nondecreasing integer timestamps; equal times may repeat.

```py
errors = ErrorTracker(10)
errors.record("auth", 1)
errors.record("auth", 1)
errors.record("billing", 2)
assert errors.count("auth", 10) == 2
assert errors.count("billing", 10) == 1
assert errors.count("auth", 11) == 0
assert errors.count("unknown", 11) == 0
assert errors.count("billing", 12) == 0
```

<details>
<summary>Hint for B</summary>

Combine a service dictionary with HitCounter's bucketed queue and running total, but make
the duration configurable. Clean up on both record and count. A query for a missing service
can return 0 without creating stored state. This tracker never rejects an event.

</details>

<!-- cell -->

```python
# Implement ErrorTracker here, then copy the contract checks into this cell.
```
