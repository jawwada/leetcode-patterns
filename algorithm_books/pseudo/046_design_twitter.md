---
rank: 46
slug: design_twitter
---

Design a small Twitter with four calls: `post_tweet(user, tweet_id)`, `follow(follower, followee)`, `unfollow(follower, followee)` and `get_news_feed(user)`, which returns the ids of the 10 most recent tweets posted by the user or by anyone the user follows, newest first. Users always see their own tweets and cannot unfollow themselves. If users 1, 2, 3, 2, 1 and 3 post tweets 11, 21, 31, 22, 12 and 32 in that order, the first digit naming the author, and user 1 follows users 2 and 3, the feed of user 1 is `[32, 12, 22, 31, 21, 11]`; after `unfollow(1, 3)` it is `[12, 22, 21, 11]`.

The brute force keeps one global list of every tweet and walks it from the newest end, keeping the tweets by the user or a followee until it has ten, so one small feed can read the history of the whole platform. Instead, give every user a private list of `(time, tweet_id)` pairs, stamped by one global clock that ticks once per tweet. Appending keeps each list sorted by time, so a feed is the newest end of k sorted lists merged together: the k-way merge of #20, run backward in time. A max-heap holds one entry per source, the newest tweet not yet taken from it. Each pop yields the newest tweet left anywhere, and the popped source pushes its next older tweet in its place. Ten pops fill the feed.

Picture the users as rows on a shared time axis. The feed reads the axis from right to left, and the heap keeps one finger on each row; every pop moves one finger a step to the left, and a row whose finger falls off its oldest tweet drops out of the merge.

```text
time      0     1     2     3     4     5     tweets[user], oldest first
user 1    11                      12          [(0, 11), (4, 12)]
user 2          21          22                [(1, 21), (3, 22)]
user 3                31                32    [(2, 31), (5, 32)]

get_news_feed(1), following 2 and 3: heap starts (5, 32) (4, 12) (3, 22)
pop (time, id)   push its older tweet    heap after, newest first
(5, 32)          (2, 31) of user 3       (4, 12) (3, 22) (2, 31)
(4, 12)          (0, 11) of user 1       (3, 22) (2, 31) (0, 11)
(3, 22)          (1, 21) of user 2       (2, 31) (1, 21) (0, 11)
(2, 31)          user 3 is done          (1, 21) (0, 11)
(1, 21)          user 2 is done          (0, 11)
(0, 11)          user 1 is done          empty
feed = the pops in order = [32, 12, 22, 31, 21, 11]
after unfollow(1, 3) only rows 1 and 2 merge: [12, 22, 21, 11]
```

```pseudo
CLASS Twitter
    FUNCTION Init()
        self.clock ← 0                      // stamps tweets: higher is newer
        self.tweets ← empty map             // user → list of (time, tweet_id)
        self.following ← empty map          // user → set of users they follow

    FUNCTION PostTweet(user, tweet_id)
        IF user NOT IN self.tweets
            self.tweets[user] ← empty list
        self.tweets[user].append((self.clock, tweet_id))     // oldest first
        self.clock ← self.clock + 1

    FUNCTION Follow(follower, followee)
        IF follower = followee
            RETURN                          // your own tweets always count
        IF follower NOT IN self.following
            self.following[follower] ← empty set
        self.following[follower].add(followee)

    FUNCTION Unfollow(follower, followee)
        IF follower IN self.following
            self.following[follower].remove(followee)    // no-op if absent

    FUNCTION GetNewsFeed(user)
        sources ← [user]
        IF user IN self.following
            FOR EACH followee IN self.following[user]
                sources.append(followee)
        heap ← empty max-heap        // of (time, tweet_id, source, index)
        FOR EACH source IN sources
            IF source IN self.tweets
                index ← len(self.tweets[source]) - 1        // its newest tweet
                (time, tweet_id) ← self.tweets[source][index]
                heap.push((time, tweet_id, source, index))
        feed ← empty list
        WHILE len(heap) > 0 AND len(feed) < 10
            (time, tweet_id, source, index) ← heap.pop()
            feed.append(tweet_id)           // the newest tweet not yet taken
            IF index > 0                    // that source has an older tweet
                (time, older_id) ← self.tweets[source][index - 1]
                heap.push((time, older_id, source, index - 1))
        RETURN feed
```

`post_tweet`, `follow` and `unfollow` cost `O(1)`. `get_news_feed` costs `O(k log k)` to seed the heap with the newest tweet of each of its `k` sources (`O(k)` with heapify), plus `O(log k)` for each of at most 10 pops, so it reads at most `k + 10` tweets however long the histories are. Memory is one pair per tweet and one set entry per follow. Reach for this merge whenever a result is assembled from many sources that are each already sorted and only its first few items are wanted: feeds, merged logs, the k smallest pair sums. The global clock is what makes "most recent" well defined, and the classic mistake is ordering by tweet id instead: ids are labels, not times, and nothing promises that a later tweet has a larger id. The other slip is the user's own tweets, either forgotten or merged twice after a self-follow; here `follow` ignores a self-follow and the user is always the first source. In system-design terms this read-time merge is fan-out on read. The usual design at scale fans out on write instead, pushing each new tweet into a cached timeline per follower so that a read is one lookup, and merges at read time only for celebrities, whose millions of followers would turn each post into millions of writes.

*Practice:* LC 355 Design Twitter · LC 23 Merge k Sorted Lists · LC 378 Kth Smallest Element in a Sorted Matrix
