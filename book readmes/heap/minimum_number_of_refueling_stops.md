# Minimum Number of Refueling Stops

*LeetCode 871 · Hard · Pattern: Greedy with a max-heap of passed-but-unused options (refuel only when stuck) · Reading time ~12 min*

## The problem

A car starts with startFuel litres and must reach position target, using one litre per mile. stations[i] = [position,
fuel] are sorted by position and lie before the target. Return the minimum number of refuelling stops, or -1 if the
target is unreachable; the tank is unlimited.

```text
Example: target=100, startFuel=10,
  stations=[[10,60],[20,30],[30,30],[60,40]] -> 2 (stop at 10
  for 60 litres, then at 60 for 40).
```

## What the problem is really asking

A car drives along a straight road from mile 0 to mile `target`. It burns one litre per mile, starts with `startFuel` litres, and has a tank with no upper limit. Gas stations sit along the road, sorted by position, each offering a fixed amount of fuel that you take all at once if you stop there. You want the smallest number of stops that still gets you to the target, or `-1` if no set of stops does.

The answer is a single count. The object you are choosing, though, is a *subset of stations*, and the count is the size of the smallest subset that works. That is what makes it look hard: whether a stop at mile 10 is a good idea seems to depend on what is waiting at mile 60, so it feels like you need to see the future before committing.

One small fact simplifies everything. Because the car uses one litre per mile and starts at mile 0, the total fuel you have ever collected is exactly the farthest mile you can reach. "Fuel" and "reach" are the same number. We will use the two words interchangeably.

Here is the example we will carry through the chapter: `target = 100`, `startFuel = 10`, stations at miles 10, 20, 30, 60 offering 60, 30, 30, 40 litres.

```text
 mile  0    10   20   30             60                   100
       |----S1---S2---S3-------------S4--------------------T
 fuel       60   30   30             40
 reach [=========]                         start: reach = 10
```

The answer is 2: stop at mile 10 (reach becomes 70), stop at mile 60 (reach becomes 110).

## Do it by hand first

Do what anyone would do with a pencil. Start at mile 0 with reach 10. You can get exactly to S1 at mile 10 and no farther, because S2 is at mile 20. So you have no choice: you must have taken S1's 60 litres. Reach is now 70.

With reach 70 you roll past S2 (mile 20), S3 (mile 30) and S4 (mile 60) without needing anything. But the target is at 100, beyond 70. Now look back over your shoulder: which stations did you drive past without using? S2 (30), S3 (30), S4 (40). Pick the biggest, S4, and reach becomes 110. Done, two stops.

```text
 after S1 is taken: reach 70
 mile  0    10   20   30             60        70         100
       |----S1---S2---S3-------------S4--------|          T
            used 30   30             40        ^ stuck before T
 passed but unused: {30, 30, 40}  -> take the 40 -> reach 110
```

Notice what your hand kept track of. It was not a plan. It was a *pile of tanks you drove past and did not use yet*, and the only question you ever asked the pile was "which one is biggest?" A pile you only ever ask for its biggest item is a max-heap. That is the seed.

Notice also *when* you asked. Never at a station. Only at the moment you were about to run dry.

## The first honest attempt

The obvious brute force: try every subset of stations. For each subset, drive the road, add fuel at the chosen stations, check you never run dry before the next chosen station or the target, and keep the smallest subset that survives. With `n` stations there are `2^n` subsets and each simulation is `O(n)`, so `O(2^n · n)` time.

Where does the waste live? Whether the car can get past mile `x` depends only on how much fuel was collected before `x`, not on which particular stations supplied it. Yet the brute force simulates the same prefix over and over:

```text
 subset {S1,S4}      : 0 -> S1(+60) -> ...S4(+40) -> T
 subset {S1,S2,S4}   : 0 -> S1(+60) -> S2(+30) -> ...
 subset {S1,S3,S4}   : 0 -> S1(+60) -> ... S3(+30) -> ...
 subset {S1,S2,S3,S4}: 0 -> S1(+60) -> S2(+30) -> ...
                          \________/
              the same "take S1, reach 70" prefix,
              re-driven in half of all 2^n subsets
```

A smarter candidate says "DP": let `best[k]` be the farthest reach using exactly `k` stops, and update it station by station from high `k` down to low. That is `O(n^2)` and correct. It still treats every station as a decision to make *at the station*. The heap solution removes even that.

## The turning point

**Claim: you never have to decide at a station. A station you drove past stays available, and you can choose to "have stopped there" later, at the moment you would otherwise run dry.**

Why is this legal? A stop is only invalid if you could not reach the station. If you drove past it, you reached it. The fuel it gives pours into the same tank as every other litre, and fuel collected behind you is spent on miles ahead of you. Whether you physically poured it in at mile 20 or you "retroactively" decide at mile 70 that you did, the car's reach for every mile from here on is identical. Behind the car, fuel is fungible: only the *total* you collected matters, and the *count* of stops you used to collect it.

So restructure the drive:

1. Drive forward without stopping. Every station you reach goes onto a pile of unused tanks.
2. When the next point (a station or the target) is beyond your reach, you are stuck. You must commit to one more stop from the pile.
3. Which one? Each stop costs exactly one unit of the thing you are minimising, and buys some amount of reach. Spend that unit on the largest tank. Repeat until the next point is reachable, or the pile is empty (answer `-1`).

The structure falls out immediately. The pile only receives pushes (one per station reached) and only answers "give me the largest and remove it". That is a max-heap; in Python, a min-heap of negated amounts.

Two small design choices keep the loop clean. First, treat the target as one more station at position `target` offering 0 litres, so "can I reach the target?" is the same question as "can I reach the next station?". Second, the check is `fuel < pos` *before* pushing the current station's fuel, because you cannot use a station's fuel to reach that same station.

That is the whole algorithm: lazy commitment plus "biggest first". The laziness is what turns an exponential choice into a greedy one: by the time you commit, you know every option that could possibly help you right now, so you can rank them.

## Watch it work

The heap is drawn as the set of passed-but-unused tanks (largest first). `reach` equals fuel collected.

Frame 1: Start. Reach 10. The next point is S1 at mile 10, which is reachable.

```text
 pos:   0   10   20   30   60   100
        |---S1---S2---S3---S4---T
 car    ^
 reach  10       heap []       stops 0
```

Nothing is stuck, so nothing is committed.

Frame 2: Arrive at S1 (mile 10). Push its 60.

```text
 car       ^ S1
 reach  10       heap [60]     stops 0
```

S1 is now an option, not a decision.

Frame 3: Next point is S2 at mile 20, but reach is 10. Stuck. Pop the largest (60).

```text
 stuck: 10 < 20
 pop 60 -> reach 70            stops 1
 then arrive at S2, push 30
 reach  70       heap [30]
```

The first commitment happens only when it is forced, and it takes the best tank available.

Frame 4: S3 (mile 30) and S4 (mile 60) are both within 70. Push 30, then 40.

```text
 car                    ^ S4
 reach  70       heap [40, 30, 30]   stops 1

 as a triangle (max on top)     as stored (negated)
          40                    [-40, -30, -30]
         /  \                     [0]  [1]  [2]
       30    30
```

We drove past three stations and committed to none of them.

Frame 5: Next point is the target at 100. Reach 70 is short. Pop 40.

```text
 stuck: 70 < 100
 pop 40 -> reach 110           stops 2
 arrive at T, push 0
 reach 110       heap [30, 30, 0]
```

The two 30-litre tanks are never used. The answer is 2.

Across every frame two things held: every tank in the heap belongs to a station the car has already reached, and the stop count only went up at a moment when the car could not otherwise continue.

## Why it is correct

Two facts carry the proof.

**Fact 1: every stop greedy counts was necessary at the moment it was counted.** Greedy pops only when the next point is out of reach with the stops taken so far. So greedy never pays for a stop it could have skipped *given the stops it already has*.

**Fact 2 (the exchange argument): when a stop is forced, taking the largest available tank is never worse than taking any other.** Suppose greedy has made `j - 1` pops, has reach `R`, and is stuck before the next point `p > R`. Take any optimal plan `O` that agrees with greedy's first `j - 1` stops. With only those stops, `O` would also be stuck before `p`, so `O` must use at least one more station that lies within `R` (no other station is reachable yet). Call it `o`. Greedy pops `g`, the largest tank among all reached-and-unused stations, so `fuel(g) >= fuel(o)`.

Now swap: replace `o` by `g` in `O`. Is the new plan still feasible? Every mile up to `R` was already covered by the shared `j - 1` stops, so removing `o` breaks nothing there, and both `o` and `g` lie within that stretch. Every mile beyond `R` is covered by total fuel, and the total went *up* by `fuel(g) - fuel(o) >= 0`. So the swapped plan reaches every point `O` reached, with the same number of stops. It is still optimal, and it now agrees with greedy on `j` stops.

Repeat the swap for `j = 1, 2, ...` and you transform any optimal plan into greedy's plan without ever increasing the count. So greedy's count equals the optimum.

The same argument gives a clean invariant to remember: **after `j` pops, greedy's reach is the largest reach any `j`-stop plan can achieve.** And if the heap is empty while stuck, every reached station is already used; no plan with any number of stops can go farther, so `-1` is correct.

## Cost

- **Time `O(n log n)`.** Each station is pushed once and popped at most once, each heap operation `O(log n)`.
- **Space `O(n)`.** The heap can hold every station.

For comparison, the `best[k]` DP is `O(n^2)` time and `O(n)` space; the brute force is `O(2^n · n)`.

## Variations you will meet

- **Gas Station (LeetCode 134).** A circular route where you *must* use every station once. No choice of which tanks to take, so no heap; the question becomes where to start, solved by a running-sum argument.
- **Jump Game II (LeetCode 45).** Same shape: minimise the number of "commitments" to reach the end, where each index offers a jump. Because the options behind you form a contiguous range, you can track the best one with a single variable instead of a heap (BFS by layers).
- **Bounded tank capacity.** If the tank had a maximum, fuel would no longer be fungible across time: a tank taken too early could overflow. The retroactive trick breaks, and you fall back to DP over (station, fuel) states.
- **IPO (the previous problem).** The mirror image: there you *must* commit `k` times and want the most capital; here you want the fewest commitments to reach a goal. Both keep a max-heap of "unlocked" options and take the biggest.

## What to carry forward

Procrastinate: drive past options, pile them in a max-heap, and commit only when stuck, taking the largest. The next problem, Course Schedule III, uses the same heap of past choices, but there you take everything first and *undo* the worst choice when a deadline is broken.
