---
rank: 21
slug: best_time_stock
---

Given a stock's price on each day, buy on one day and sell on a later day so that the profit is as large as possible, or return `0` when no trade makes money. For `[7, 1, 5, 3, 6, 4]` the answer is `5`: buy at `1` on day 1 and sell at `6` on day 4.

The brute force pairs every buy day with every later sell day, `O(n²)` pairs. Yet a sale on a given day does not care about all the earlier days, only about the cheapest of them: the best trade that sells today bought at the minimum price so far. So walk the days once, carry that running minimum, and price each day as a sale against it; the answer is the largest of those daily profits. The running minimum is the whole memory of the past. It is updated before today's sale, which at worst prices a same-day trade at `0`, the same as not trading.

Picture the price chart as a mountain range. A trade is a climb from one point to a later, higher point, and the answer is the tallest such climb. The running minimum is a floor that only ever drops, sitting at the lowest valley behind the walker, and each day's profit is the height of that day's point above the floor. A new low never hurts, because it lowers the floor for every later day. When transactions are unlimited (LC 122), the answer is instead the sum of every positive day-to-day rise: a long climb earns exactly the sum of its steps, and every step up can be taken on its own.

```text
price
  7      ●
  6                              ●   best sale: 6 - 1 = 5
  5                  ●           │
  4                  │           │     ●
  3                  │     ●     │     │
  2                  │     │     │     │
  1            ●─────┴─────┴─────┴─────┴   floor = running minimum
         d0    d1    d2    d3    d4    d5
  min    7     1     1     1     1     1
  profit 0     0     4     2     5     3
  best   0     0     4     4     5     5
```

```pseudo
FUNCTION MaxProfit(prices)
    min_price ← ∞                          // cheapest price so far
    best ← 0                               // no trade at all earns 0
    FOR EACH price IN prices
        IF price < min_price               // a cheaper day to have bought on
            min_price ← price
        profit ← price - min_price         // sell today, bought at the minimum
        IF profit > best
            best ← profit
    RETURN best
```

One pass with constant work per day gives `O(n)` time and `O(1)` space. Reach for the running minimum whenever a problem asks for the best `a[j] - a[i]` with `i < j`: the best partner for every `j` is one number carried forward. Run on the day-to-day price differences, this is Kadane's algorithm (#20) with `best` started at `0`, the mistake there but correct here, because not trading is allowed. The fee and cooldown versions (LC 714, LC 309) carry a few running balances instead of one minimum, the best cash while holding a share and while not holding one, plus a resting state for the cooldown. The classic mistake is answering `max(prices) - min(prices)`, which ignores the order of the days: on `[7, 6, 4, 3, 1]` it reports `6`, but the price only falls and the answer is `0`.

*Practice:* LC 121 Best Time to Buy and Sell Stock · LC 122 Best Time to Buy and Sell Stock II · LC 714 Best Time to Buy and Sell Stock with Transaction Fee · LC 309 Best Time to Buy and Sell Stock with Cooldown
