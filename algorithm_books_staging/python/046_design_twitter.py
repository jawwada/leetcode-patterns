"""
Design Twitter - Merge the Followees' Feeds with a Heap

Users post tweets and follow each other; get_news_feed(user) returns the ids of
the 10 most recent tweets by the user or anyone they follow, newest first.
Users 1, 2, 3, 2, 1, 3 post 11, 21, 31, 22, 12, 32 and user 1 follows 2 and 3
-> the feed of user 1 is [32, 12, 22, 31, 21, 11].
"""
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class Twitter:
    """Per-user tweet lists stamped by one global clock; a feed merges them."""

    def __init__(self):
        self.clock = 0              # stamps tweets: higher means newer
        self.tweets = {}            # user -> list of (time, tweet_id)
        self.following = {}         # user -> set of the users they follow

    def post_tweet(self, user, tweet_id):
        """Append the tweet, stamped with the next clock value. O(1)."""
        if user not in self.tweets:
            self.tweets[user] = []
        self.tweets[user].append((self.clock, tweet_id))    # oldest first
        self.clock += 1

    def follow(self, follower, followee):
        """Add followee to the follower's set. O(1)."""
        if follower == followee:
            return                  # your own tweets always count anyway
        if follower not in self.following:
            self.following[follower] = set()
        self.following[follower].add(followee)

    def unfollow(self, follower, followee):
        """Remove followee from the follower's set, if it is there. O(1)."""
        if follower in self.following:
            self.following[follower].discard(followee)  # no error if absent

    def get_news_feed(self, user):
        """Merge the sources' lists with a max-heap seeded with each newest
        tweet; stop after 10 pops. O(k log k) for k sources."""
        sources = [user]
        if user in self.following:
            for followee in self.following[user]:
                sources.append(followee)
        heap = []                   # max-heap by time: times go in negated
        for source in sources:
            if source in self.tweets:
                index = len(self.tweets[source]) - 1        # its newest tweet
                time, tweet_id = self.tweets[source][index]
                heapq.heappush(heap, (-time, tweet_id, source, index))
        feed = []
        while len(heap) > 0 and len(feed) < 10:
            neg_time, tweet_id, source, index = heapq.heappop(heap)
            feed.append(tweet_id)   # the newest tweet not yet taken
            if index > 0:           # that source has an older tweet
                time, older_id = self.tweets[source][index - 1]
                heapq.heappush(heap, (-time, older_id, source, index - 1))
        return feed


# --- try it ---
twitter = Twitter()
posts = [(1, 11), (2, 21), (3, 31), (2, 22), (1, 12), (3, 32)]
for user, tweet_id in posts:
    twitter.post_tweet(user, tweet_id)
print(twitter.get_news_feed(1))             # -> [12, 11]
twitter.follow(1, 2)
twitter.follow(1, 3)
print(twitter.get_news_feed(1))             # -> [32, 12, 22, 31, 21, 11]
twitter.unfollow(1, 3)
twitter.unfollow(1, 1)                      # cannot unfollow yourself
print(twitter.get_news_feed(1))             # -> [12, 22, 21, 11]
print(twitter.get_news_feed(2), twitter.get_news_feed(5))   # -> [22, 21] []
for tweet_id in range(40, 52):
    twitter.post_tweet(4, tweet_id)
feed = twitter.get_news_feed(4)
print(len(feed), feed[0], feed[9])          # -> 10 51 42
