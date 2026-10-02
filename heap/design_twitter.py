"""
Design Twitter (LeetCode 355)  — Medium
Pattern: k-way merge with a heap (merge k sorted feeds)

Problem
-------
Implement postTweet(userId, tweetId), follow(a, b), unfollow(a, b) and getNewsFeed(userId),
which returns the 10 most recent tweet ids posted by the user or anyone they follow, newest first.
Example: post(1,5); feed(1)=[5]; follow(1,2); post(2,6); feed(1)=[6,5]; unfollow(1,2); feed(1)=[5].

Brute force
-----------
Store every tweet in one global list in posting order. getNewsFeed walks the whole list from the
newest end, keeping tweets whose author is the user or someone they follow, until 10 are found.
O(T) per feed where T is all tweets ever posted, O(T) space. The waste: the scan touches tweets
from every user on the platform, almost all of which are irrelevant to this reader.

From brute force to optimal
---------------------------
The redundancy is scanning other people's tweets. Observation: if each user keeps their OWN
tweet list (newest last, stamped with a global timestamp), each followee's list is already sorted
by time, so a feed is just "merge k sorted lists, take the first 10". A max-heap seeded with
the latest tweet of each followee lets us repeatedly pull the globally newest tweet in O(log k)
and replace it with that author's next-older tweet. We stop after 10 pops, so the cost is
O(k + 10 log k) instead of O(T).

Intuition
---------
Each followee's timeline is a sorted deck; put the top card of each deck in a heap, draw the
newest, and refill from the same deck. Ten draws build the feed.

Geometric view
--------------
k horizontal rows (one per followee) each sorted newest->oldest from left to right, with a
pointer at the leftmost card. The heap triangle above them holds just the k pointed-at cards;
pop the apex, advance that row's pointer one step right, push the newly exposed card. The
frontier of pointers sweeps right exactly 10 steps in total.

Steps
-----
1. Keep a global decreasing counter as the timestamp; store per-user lists of (time, tweetId).
2. follow / unfollow update a set; a user always implicitly follows themselves.
3. getNewsFeed: for each followee with tweets, push (time, tweetId, userId, index-of-next) for
   their newest tweet.
4. Pop up to 10 times; after each pop, push that author's next-older tweet if any.

Complexity: O(k + 10 log k) per feed where k = number of followees, O(T + F) space for all
tweets and follow edges.
Pitfalls: Forgetting that a user sees their own tweets; unfollow of self or of a non-followed
user must not crash (use set.discard); mixing up the timestamp sign so the heap is a min-heap.
"""
import heapq
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self):
        self.time = 0                                   # decreasing: smaller == newer
        self.tweets = defaultdict(list)                 # user -> [(time, tweetId)] newest last
        self.follows = defaultdict(set)                 # user -> set of followees

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time -= 1
        self.tweets[userId].append((self.time, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        heap = []
        for u in self.follows[userId] | {userId}:       # self is implicitly followed
            if self.tweets[u]:
                i = len(self.tweets[u]) - 1
                t, tid = self.tweets[u][i]
                heap.append((t, tid, u, i - 1))         # i-1 = index of next-older tweet
        heapq.heapify(heap)
        feed = []
        while heap and len(feed) < 10:
            t, tid, u, i = heapq.heappop(heap)
            feed.append(tid)
            if i >= 0:                                  # refill from the same author
                nt, ntid = self.tweets[u][i]
                heapq.heappush(heap, (nt, ntid, u, i - 1))
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].discard(followeeId)


class BruteForce:
    def __init__(self):
        self.tweets = []                                # global (userId, tweetId) in post order
        self.follows = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets.append((userId, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        allowed = self.follows[userId] | {userId}
        feed = []
        for u, tid in reversed(self.tweets):            # scans every tweet on the platform
            if u in allowed:
                feed.append(tid)
                if len(feed) == 10:
                    break
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].discard(followeeId)


if __name__ == "__main__":
    for cls in (Twitter, BruteForce):
        t = cls()
        t.postTweet(1, 5)
        assert t.getNewsFeed(1) == [5]
        t.follow(1, 2)
        t.postTweet(2, 6)
        assert t.getNewsFeed(1) == [6, 5]
        t.unfollow(1, 2)
        assert t.getNewsFeed(1) == [5]
        assert t.getNewsFeed(3) == []                   # user with no tweets or follows
        for i in range(15):                             # feed is capped at 10, newest first
            t.postTweet(1, 100 + i)
        assert t.getNewsFeed(1) == [114 - i for i in range(10)]
        t.unfollow(1, 99)                               # unfollowing a stranger is a no-op
    print("ok")
