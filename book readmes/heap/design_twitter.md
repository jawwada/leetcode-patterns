# Design Twitter

*LeetCode 355 · Medium · Pattern: k-way merge with a heap (merge k sorted feeds) · Reading time ~8 min*

## The problem

Implement postTweet(userId, tweetId), follow(a, b), unfollow(a, b) and getNewsFeed(userId), which returns the 10 most
recent tweet ids posted by the user or anyone they follow, newest first.

```text
Example: post(1,5); feed(1)=[5]; follow(1,2); post(2,6);
  feed(1)=[6,5]; unfollow(1,2); feed(1)=[5].
```

## What the problem is really asking

Build a tiny social network with four operations. `postTweet(user, tweetId)` records a tweet. `follow(a, b)` and `unfollow(a, b)` edit who `a` follows. `getNewsFeed(user)` returns up to 10 tweet ids, newest first, drawn from the user's own tweets and the tweets of everyone they follow.

The answer to a feed call is a short list, at most 10 ids. The hard part is not the size of the answer but where it comes from: the newest 10 among possibly millions of tweets, restricted to a set of authors that changes over time. You have to pick a storage layout that makes the feed query cheap without making posting or following expensive.

```text
user 1 follows {2, 3}  (and always sees self)

timelines (oldest -> newest):
  user 1:  11 (t1)   12 (t3)
  user 2:  21 (t2)   22 (t5)
  user 3:  31 (t4)

feed(1) = newest first, max 10:
  22  31  12  21  11
```

## Do it by hand first

If you were assembling that feed from paper, you would lay out each followed person's timeline as a column with the newest tweet on top. Then you would repeatedly look at the three top tweets, take the newest, and uncover the next one in that person's column. You stop at 10 or when every column is empty.

```text
 user1   user2   user3
  12@3    22@5    31@4     take 22 (newest top)
  11@1    21@2
          ----
 tops: 12@3  21@2  31@4    take 31
 tops: 12@3  21@2  -       take 12
 ...
```

Your hand kept one top card per followed author and kept asking "which top is newest?". That is the k-way merge from the last three problems, with "newest" in place of "smallest", and you stop after 10 pops.

## The first honest attempt

Keep one global list of `(author, tweetId)` in posting order. For a feed, walk it backwards from the newest end, keep tweets whose author is the user or a followee, and stop once you have 10.

Posting and following are O(1). The feed is the problem. It costs O(T) in the worst case, where `T` is every tweet ever posted on the platform. A user who follows two quiet accounts forces a scan through every celebrity's tweets to find 10 relevant ones:

```text
global log (newest at right):
 ... u7 u9 u7 u2 u9 u9 u7 u3 u9 u7 u9 u9 u7
     x  x  x  ^  x  x  x  ^  x  x  x  x  x
 only u2, u3 matter for this reader; every x is wasted work
```

The repeated work is reading other people's tweets, again on every feed call.

## The turning point

**Claim: store tweets per author, and each author's list is already sorted by time, so a feed is "merge the followees' sorted lists and take the first 10".**

Appending to a per-author list keeps it in posting order for free, since time only moves forward. Once you have that, the feed is a k-way merge over `k` = number of followees plus self. You seed a heap with each author's newest tweet. You pop the newest overall, push that author's next-older tweet, and stop after 10 pops. Other authors' tweets are never touched.

Two implementation choices make the heap simple:

- **A global decreasing counter as the timestamp.** Each post does `time -= 1`, so newer tweets get smaller numbers. Python's min-heap then pops the newest first, with no negation at query time.
- **Heap entries `(time, tweetId, author, nextIndex)`.** `nextIndex` points at the author's next-older tweet in their list (`-1` when there is none). Timestamps are unique, so the tuple comparison never reaches the later fields.

Follows live in `user -> set of followees`. A set makes follow O(1), and `discard` makes unfollowing a stranger a harmless no-op. A user is not stored as following themselves. The feed simply uses `follows[user] | {user}`, so a user can never "unfollow" their own tweets out of their feed.

## Watch it work

Posts in order: `post(1,11)`, `post(2,21)`, `post(1,12)`, `post(3,31)`, `post(2,22)`. Then `follow(1,2)`, `follow(1,3)`, `getNewsFeed(1)`. The counter gives times -1 to -5. Heap entries are drawn as `tweet@time`.

Frame 1: seed with each author's newest tweet.

```text
store:  1: [11@-1, 12@-3]
        2: [21@-2, 22@-5]
        3: [31@-4]
            22@-5
           /     \
       12@-3     31@-4
array: [22@-5, 12@-3, 31@-4]       feed: []
```

The root is the most negative time, which is the newest tweet.

Frame 2: pop `22@-5` (user 2), push user 2's next-older tweet `21@-2`.

```text
            31@-4
           /     \
       12@-3     21@-2
array: [31@-4, 12@-3, 21@-2]       feed: [22]
```

User 2's finger moved one step down their own list.

Frame 3: pop `31@-4` (user 3, no older tweet, nothing pushed).

```text
            12@-3
           /
       21@-2
array: [12@-3, 21@-2]              feed: [22, 31]
```

The heap shrank because user 3's timeline ran out.

Frame 4: pop `12@-3` (user 1), push `11@-1`.

```text
            21@-2
           /
       11@-1
array: [21@-2, 11@-1]              feed: [22, 31, 12]
```

Frame 5: pop `21@-2`, then pop `11@-1`. The heap is empty, so stop.

```text
array: [ ]                feed: [22, 31, 12, 21, 11]

then unfollow(1, 2); getNewsFeed(1):
seed [31@-4, 12@-3] ...   feed: [31, 12, 11]
```

After the unfollow, user 2's list is simply not seeded. Nothing was deleted.

Across the frames the heap held at most one tweet per followed author, always that author's newest tweet not yet in the feed. The feed came out newest first.

## Why it is correct

**Invariant.** Before each pop, for each followed author (including self) with tweets not yet in the feed, the heap holds that author's newest such tweet, and nothing else.

Every remaining tweet of an author is older than that author's heap entry, because each author's list is in posting order. So the heap root, the newest entry, is the newest of all remaining relevant tweets. Popping it and pushing the same author's next-older tweet restores the invariant. The feed is therefore the relevant tweets in newest-first order, cut at 10. Unfollow is correct because the feed recomputes the author set on every call. No cached feed exists that could go stale.

## Cost

- **postTweet, follow, unfollow: O(1)**: a list append or a set add/discard.
- **getNewsFeed: O(k + 10 log k)**, where `k` is the number of followees. Building the seed list and heapifying is O(k), and each of at most 10 pops and pushes is O(log k).
- **Space: O(T + F)** for all tweets and follow edges. The heap is O(k) per call.

The brute force was O(T) per feed. The per-author layout replaces "all tweets" with "number of followees".

## Variations you will meet

- **Feed of size `n` with paging ("load more").** Keep the heap (or the per-author cursors) between calls and resume popping. It is the same merge, made lazy.
- **Huge follower counts (fan-out on write).** Real systems often push each tweet into every follower's precomputed feed at post time, so reads are O(1). That is costly for celebrities, so production systems mix the two: push for ordinary users, merge on read for accounts with huge followings. Interviewers like this trade-off discussion.
- **Only keep the last 10 tweets per author.** No feed can use an author's 11th-newest tweet, so trim each list to 10. Space becomes O(10 U) and the merge is unchanged.
- **Merge k Sorted Lists (LeetCode 23).** The same algorithm without the stop at 10. If this problem feels new, re-read that one.

## What to carry forward

Design questions often hide a familiar algorithm. Store data per source, in a naturally sorted order, and a query becomes a short k-way merge that stops early. A decreasing timestamp turns a min-heap into a newest-first heap.

The next problem, Find Median from Data Stream, is also a class with a stream of updates, but it uses two heaps facing each other instead of one heap of feed heads. One holds the smaller half and the other the larger half, and the median sits at the seam between them.
