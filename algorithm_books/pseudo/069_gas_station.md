---
rank: 69
slug: gas_station
---

Stations sit on a circle. Station `i` gives `gas[i]` fuel, and the drive on to the next station burns `cost[i]`. Starting with an empty tank, return the station from which a full lap is possible, or `-1` if there is none; the input promises at most one such station. With `gas = [4, 1, 2, 5, 1]` and `cost = [3, 3, 3, 1, 2]` the answer is `3`.

The brute force simulates a lap from every station, `O(n²)`. Two facts make one pass enough. First, a lap exists exactly when the total gas covers the total cost, so `sum(gas) < sum(cost)` answers `-1` at once. Second, a failed attempt rules out a whole stretch, not just its first station. Say the tank, started empty at `start`, first runs dry on the drive out of station `i`. Every station `k` in between was reached from `start` with a non-negative tank, because no deficit had happened yet. Starting fresh at `k` means arriving there with an empty tank instead, which is never better, so that attempt also runs dry by station `i`. Every station from `start` to `i` is out, and the next candidate is `i + 1`, with the tank reset to zero.

Picture the running sum of `gas[i] - cost[i]` as a profile over the stations, the bottom row of the picture. A car that starts at station `s` carries exactly the profile's rise since the point just before `s`, so starting right after the lowest point keeps the tank non-negative all the way to the end of the array. Past the wrap, the profile repeats lifted by the total, which is non-negative, so the tank stays non-negative there too. Each deficit in the scan is the profile hitting a new low, and moving `start` to `i + 1` simply follows the low point down.

```text
gas  = [4, 1, 2, 5, 1]   sum 13
cost = [3, 3, 3, 1, 2]   sum 12   13 ≥ 12, so a lap exists

  i   gas - cost   tank   start
  0       1           1     0
  1      -2          -1     0 → 2     deficit: stations 0 and 1 are out
  2      -1          -1     2 → 3     deficit: station 2 is out
  3       4           4     3
  4      -1           3     3         answer 3

running sum   1  -1  -2   2   1
                      ▲ lowest, after station 2: start at 3
```

```pseudo
FUNCTION CanCompleteCircuit(gas, cost)
    IF sum(gas) < sum(cost)                // not enough fuel for any lap
        RETURN -1
    start ← 0
    tank ← 0                               // fuel left since leaving start
    FOR i FROM 0 TO len(gas) - 1
        tank ← tank + gas[i] - cost[i]
        IF tank < 0                        // stranded: start..i are all out
            start ← i + 1
            tank ← 0
    RETURN start
```

One pass plus the two sums gives `O(n)` time and `O(1)` space. Reach for this pattern when a running balance around a loop or along a route must never go negative and the question is where to begin: the answer sits right after the lowest point of the prefix sums. It is the restart of Kadane's algorithm (#28) in another costume, where a run that turned negative is dropped whole. The classic mistake is trusting the scan without the total check: for `gas = [2, 3, 4]` and `cost = [3, 4, 3]` the scan ends on station 2 with fuel to spare, yet no lap is possible, because the total gas `9` is less than the total cost `10`.

*Practice:* LC 134 Gas Station · LC 1413 Minimum Value to Get Positive Step by Step Sum · LC 918 Maximum Sum Circular Subarray
