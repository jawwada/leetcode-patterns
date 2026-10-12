---
rank: 2
slug: rate_limiter
---

A rate limiter decides whether each request's sender is still within an agreed allowance. A free-plan API key may make 10 requests a second with bursts of 20; the 21st request of a sudden burst gets `429 Too Many Requests` and a `Retry-After` header, and the backend never sees it. Limits protect services from overload and abuse, and because the check runs on every request it must be fast, shared and cheap. Three questions decide the design: which algorithm counts, how hundreds of gateways share one count without a race or a slow round trip, and what happens when the counter store fails or a client spans regions.

### Requirements

Operators write rules that cap how fast a client may call, keyed by API key, user, client IP or a combination, scoped to a route, method or plan, and expressed as a rate with a burst or as a count per window; contract overrides adjust particular keys, and expensive requests may cost several tokens. The gateway checks every matching rule, forwards the request or answers 429, and reports the remaining allowance in `X-RateLimit-*` headers. Rule changes apply within seconds without a deploy, and a new rule can first run in shadow mode, logging what it would have refused.

The limiter sits in the path of a million requests a second at peak, so it may add at most 2 ms at the 99th percentile and must never be the reason the API is down. Limits hold within a few percent: a few extra requests for a second are fine, twice the limit at a window boundary is not. Counters are ephemeral, and a global limit holds approximately across three regions, with remote usage visible within a second. Network-layer DDoS, bot detection and billing-grade metering are out of scope.

### Estimates

```text
peak traffic   1 M requests/s over 3 regions; busiest region 40% → 400,000/s
gateways       400,000 / 2,000 requests/s per gateway = 200 in that region
decisions      2 identities per request (API key, client IP) → 800,000 calls/s
Redis shards   800,000 / 50,000 scripts/s planned per shard = 16 + 16 replicas
bucket state   up to 10 M live (client, rule) buckets × ~150 B ≈ 1.5 GB
hourly log     400,000/s × 3,600 s = 1.44 × 10^9 entries × ~100 B ≈ 144 GB
latency        same-zone Redis round trip ≈ 0.5 ms; budget 2 ms at p99
global check   cross-region round trip ≈ 100 ms = 50 × the whole budget
```

Three conclusions follow. The counter store is sized by operations, not memory: sixteen shards per region carry 800,000 decisions a second while each holds under 100 MB of buckets. The algorithm decides the memory, since a sliding log for one hourly rule over all traffic needs about a hundred times what buckets need. And a synchronous global check is out of the question, because one cross-region round trip costs fifty times the whole latency budget; each region decides locally and learns of remote usage asynchronously.

### API

```text
GET  /v1/search?q=...                        Authorization: Bearer <api key>
     200 OK                 X-RateLimit-Limit: 20   X-RateLimit-Remaining: 7
                            X-RateLimit-Reset: 2
     429 Too Many Requests  Retry-After: 1   X-RateLimit-Remaining: 0
                            {"error": "rate_limited", "rule": "free-search"}

PUT  /admin/v1/rules/free-search                     If-Match: "<version>"
     {"match": {"route": "GET /v1/search", "plan": "free"}, "key": "api_key",
      "algorithm": "token_bucket", "rate_per_s": 10, "burst": 20,
      "mode": "shadow", "on_error": "open"}
     200 {"version": 43}      400 invalid rule      412 version changed

Decide(descriptors, cost) → {allowed, remaining, reset_s, retry_after_s}
     descriptors [("api_key", "k_9f2"), ("ip", "203.0.113.7")], cost 1
```

The headers describe the token bucket: `Limit` is its size, `Remaining` the whole tokens left, `Reset` the seconds until it is full and `Retry-After` the seconds until the next token, all relative, so clients never depend on their own clocks. The `X-` names are a convention; an IETF draft defines the same information as `RateLimit-Policy` and `RateLimit`. Caches must not store a 429 (RFC 6585), and a 429 is not a 503, which says the server is overloaded whoever is asking. Through `If-Match`, concurrent rule edits fail with 412 rather than overwrite each other, and `Decide` is the gateway's internal call, one per request.

### Data Model

```text
rules       rule_id PK | match (route, method, plan) | key_type | algorithm
            | rate_per_s | burst | window_s | mode | on_error | version
            SQL, a few thousand rows; every gateway holds a snapshot in memory
overrides   (rule_id, key_value) PK → rate_per_s, burst       contract limits
counters    Redis, one key per (client, rule); shard = hash of the {client}
  bucket    rl:{k_9f2}:free-search          HASH tokens=7.3 ts=1791795600.412
            TTL = burst / rate, the time an empty bucket takes to fill
  window    rl:{k_9f2}:hourly:1791795600    INT 412, two live windows, TTL 2 h
  log       rl:{acct:8812}:login            ZSET member=request id, score=time
  remote    rl:{k_9f2}:global:<window>:from-B   INT, written by the sync worker
decisions   Kafka topic: denials, shadow denials, per-minute allow counts
```

Rules are small, read on every request and rarely changed, so they live in an ordinary SQL table and every gateway keeps the whole set in memory, indexed by route. Counters are tiny, rewritten on every request and worthless within seconds or hours, which is what Redis is for; each carries a TTL, so idle clients cost nothing, and an expired bucket reads exactly like a full one. The braces mark the hashed part of the key, so all of one client's counters, remote counts included, share a shard and one script can check them together; in Redis Cluster the braces are its hash-tag syntax. Only denials, shadow denials and per-minute totals reach Kafka, since logging all 800,000 decisions a second would cost more than making them.

### Architecture

```dot
rankdir=TB;
client [label="clients\napps, SDKs, scripts", class=client];
ops    [label="operators", class=client];
pop    [label="CDN / WAF edge\ncoarse per-IP limits", class=edge];
rules  [label="rules service", class=service];
rdb    [label="rules DB", class=store];
subgraph cluster_a {
  label="Region A"; style="rounded,dashed"; color="#9CA3AF";
  lb     [label="load balancer", class=edge];
  gw     [label="API gateways\n+ limiter library", class=service];
  redis  [label="Redis counters\nsharded by client", class=cache];
  svc    [label="backend services\nconcurrency limits", class=service];
  events [label="decision log", class=queue];
  usage  [label="usage + alerts job", class=worker];
}
regb [label="Region B\ngateways + Redis", class=service];
sync [label="cross-region\nusage sync", class=worker];
client -> pop [label=" HTTPS"];
pop -> lb;
pop -> regb;
lb -> gw;
gw -> redis [label=" EVALSHA"];
gw -> svc [label=" allowed"];
gw -> events [label=" async", style=dashed];
events -> usage;
ops -> rules [label=" PUT rule"];
rules -> rdb;
rules -> gw [label=" push snapshot", style=dashed];
rules -> regb [style=dashed];
regb -> sync [style=dashed, dir=both];
sync -> redis [style=dashed, dir=both];
{rank=same; client; ops}
{rank=same; pop; rules; rdb}
{rank=same; redis; svc; events}
{rank=same; lb; regb}
```

A request from one of the clients first meets the CDN / WAF edge of Chapter 15, which applies coarse per-IP limits in each point of presence, sheds floods and routes the client to its nearest region. There the load balancer hands it to one of the API gateways, which has authenticated the API key and knows the plan. The limiter library matches the request against its in-memory rules and sends one `EVALSHA` per identity, API key and client IP, to the shard of the Redis counters that consistent hashing picks; each script refills, decides and decrements atomically. If every rule allows, the gateway adds the headers and forwards the request to the backend services, which keep concurrency limits of their own; otherwise it answers 429 itself, at the cost of one Redis call.

Operators change rules through the rules service, which validates them, stores a new version in the rules DB and pushes the snapshot to the gateways of every region, the propagation problem of Chapter 49. The gateways also write, asynchronously, to the decision log, which a usage and alerts job turns into dashboards, shadow-rule reports and pages when denials spike. Region B runs the same stack, and the cross-region usage sync worker moves the counts of global rules between the regions' counters every second.

### Deep Dives

#### Choosing the algorithm: windows versus buckets

The simplest limiter is a fixed window: one counter per client per minute, bumped by `INCR` and discarded when the minute turns. It fails at the boundary. A client that sends 100 requests in the last second of one minute and 100 in the first second of the next passes 200 in two seconds, twice the limit, and throttled clients all retry at the top of the next minute.

```text
limit: 100 requests per minute
              window 12:00                          window 12:01
 ├─────────────────────────────────────┼─────────────────────────────────────┤
                         100 requests ▲ ▲ 100 requests
                               12:00:59 12:01:00
 fixed window      each window counts 100, so 200 pass within two seconds  ✗
 sliding counter   at 12:01:00   100 × 60/60 + 0 = 100: the second burst waits
                   at 12:01:30   100 × 30/60 + 0 = 50: 50 more may pass
```

The sliding log of #138 is exact: a sorted set of admitted request times, trimmed to the window and counted. Its memory grows with traffic, 144 GB for one hourly rule, so it suits only small limits that must be exact, such as five login attempts per account per fifteen minutes. The sliding window counter gets most of that accuracy from two integers, weighting the previous window's count by the share of it still inside the sliding window. It assumes that window's requests were spread evenly, which the burst in the sketch violates, yet on real traffic Cloudflare found only 0.003% of 400 million requests wrongly allowed or limited. More buckets per window, the ring of the hit counter (#45), tighten it further.

The token bucket states what API contracts usually say, a steady rate plus a tolerated burst, in two numbers refilled lazily; over any `T` seconds it admits at most `burst + rate × T`, and AWS API Gateway and Stripe both describe their limits this way. The leaky bucket of NGINX's `limit_req` queues requests and releases them at a fixed rate, smoothing traffic by delaying it, which suits calls to a fragile downstream and suits an interactive API poorly. This design uses token buckets for request rates, sliding window counters for hourly quotas, logs for small security limits and fixed windows only for coarse daily quotas.

#### One atomic decision in Redis

The naive implementation reads the counter, compares in the gateway and writes back. Between the read and the write other gateways read the same value, so two that both read 99 against a limit of 100 both admit, and a hot key overshoots further with every gateway. `INCR` closes this race by incrementing and returning the new value in one step; increment first, compare afterwards, and exactly `limit` callers see a value within the limit. Setting the expiry with a separate `EXPIRE` after the first increment opens a second race, which Redis's documentation describes: a gateway that dies between the two leaves a counter with no TTL that never resets, locking the client out for good. `MULTI`/`EXEC` or a script closes it.

A token bucket's read-modify-write of two fields must also be one step, and a Lua script makes it one: Redis runs a script atomically, with no other command executing meanwhile. The gateway loads the script once and calls it by its SHA-1 digest with `EVALSHA`, one round trip per decision.

```text
-- KEYS[1] = rl:{k_9f2}:free-search       ARGV = rate per second, burst, cost
local rate, burst = tonumber(ARGV[1]), tonumber(ARGV[2])
local cost = tonumber(ARGV[3])
local t = redis.call('TIME')                     -- the shard's clock, not ours
local b = redis.call('HMGET', KEYS[1], 'tokens', 'ts')
local now = tonumber(t[1]) + tonumber(t[2]) / 1e6
local tokens = tonumber(b[1]) or burst           -- no key: a full bucket
local last = tonumber(b[2]) or now
now = math.max(now, last)                        -- time never runs backwards
tokens = math.min(burst, tokens + (now - last) * rate)    -- lazy, capped
local ok = tokens >= cost
if ok then tokens = tokens - cost end
redis.call('HSET', KEYS[1], 'tokens', tokens, 'ts', now)
redis.call('EXPIRE', KEYS[1], math.ceil(burst / rate))
local wait = ok and 0 or (cost - tokens) / rate
return {ok and 1 or 0, math.floor(tokens), math.ceil(wait)}
```

The script reads the time from the shard, so gateways with skewed clocks cannot mint tokens, and never moves a timestamp backwards, so a replica whose clock lags after a failover can neither drain buckets nor overfill them later. It returns the tokens left and the wait for the next one, which become the headers. For a client with several rules, the production script takes all their keys and decrements only if every rule allows; Redis Cluster requires a script's declared keys to share a hash slot, which the `{k_9f2}` tag guarantees. A script blocks its shard while it runs, so it must do constant work, as the bucket and the window counter do.

#### One budget across gateways and regions

Within a region, the shared counter makes 200 gateways behave as one limiter. Giving each gateway `limit / 200` instead fails, because a load balancer that spreads connections rather than requests sends a client with one long-lived HTTP/2 connection to a single gateway, which throttles it at a two-hundredth of its limit. One global Redis for all regions fails the other way, putting a 100 ms round trip in front of every request and turning a network partition into a limiter outage everywhere.

So each region enforces against its own counters, and global rules use one of two mechanisms. The first shares counts asynchronously: every second the usage sync worker copies each global key's regional count into the other regions, and the script adds the remote counts to the local one before deciding. The overshoot is at most what the other regions admitted during one interval. A client sending 50 requests a second to each of two regions against 6,000 a minute overshoots by at most about 50, under 1%, but one that bursts its whole budget into several regions within a second can get the limit in each.

The second splits the budget: the worker divides each global limit into regional shares in proportion to recent traffic, rewrites them every few seconds, and each region enforces its share locally. The limit is never exceeded, but a client whose traffic shifts between regions is under-admitted until the shares catch up; Google's Doorman applies the idea to internal clients, which lease capacity from a server and fall back to a configured safe capacity when it is unreachable. Geographic routing keeps most clients in one region, so shared counts serve most global rules, and split budgets are kept for caps where an overshoot is expensive, such as a partner API's contractual limit.

### Scaling and Bottlenecks

A Redis shard breaks first, because it runs scripts on one thread and every decision is a write. Shards scale out, and consistent hashing (#139) on the client part of the key means a seventeenth shard moves only about a seventeenth of the clients, whose counters simply restart as full buckets; `hash mod n` would reset nearly every counter in the region at once. Redis Cluster's 16,384 hash slots do the same job on the server side and migrate keys instead of dropping them; Chapter 4 covers what moves on a resize.

A hot key breaks a shard sooner: an enterprise key at 50,000 requests a second is one shard's whole planned capacity. The fix is token leasing, in which a gateway that sees heavy traffic for a key takes about 100 ms of that traffic in tokens per call and spends them from memory. With 200 gateways each seeing 250 of those requests a second, each leases 25 tokens ten times a second, so the shard sees 2,000 calls a second instead of 50,000 and the client loses at most the tokens outstanding, a tenth of a second of traffic. Refused clients are cached on the gateway until their `Retry-After` passes, as in Envoy's reference rate-limit service, so an abuser costs no Redis calls; the cache is an LRU map (#44) that a flood of distinct IPs cannot grow without bound.

### Failure Modes

When a shard is slow or down, the gateway abandons the call after a few milliseconds and applies the rule's `on_error`. Ordinary API limits fail open, since refusing everything would turn a limiter outage into an API outage, which is also Stripe's published advice. Security limits fail closed, because unlimited login attempts or SMS sends cost more than a minute of refusals. Open need not mean unbounded: the gateway falls back to local buckets at each client's full limit, and a circuit breaker spares the recovering shard.

Redis replicates asynchronously, so a promoted replica may lack the last few writes and some buckets roll back a few tokens, which the requirements accept; its script cache may be empty too, so the gateway reloads the script on `NOSCRIPT`. If the rules service fails, gateways keep their last snapshot. The most dangerous failure is a bad rule, such as a limit of zero on a busy route, so rules are validated, run in shadow mode first, reach one region before the rest and roll back in seconds. Clients that ignore `Retry-After` amplify load just as it is being shed, so the SDKs back off exponentially with jitter. A region outage gives its clients fresh buckets elsewhere, a one-time burst of at most one bucket each.

### Trade-offs and Alternatives

The limiter can live in three places. As a library in the gateway, as here, it adds no hop and keeps leases and caches local, but every gateway must embed it. As a separate gRPC service, the model of Envoy's global rate limiting, whose reference implementation from Lyft keeps fixed-window counters in Redis, it serves every proxy and language for one more hop. Cloudflare's published design counts per point of presence in a memcache cluster, with asynchronous increments and block decisions cached on each server, giving up exact global counts for almost no added latency, a fit for stopping abuse rather than metering customers.

Limits also belong outside the gateway. Clients should throttle themselves: SDKs honour `Retry-After`, and Google's SRE book describes adaptive throttling, in which a client tracks its requests and the backend's accepts over two minutes and rejects locally with probability `max(0, (requests - K × accepts) / (requests + 1))`, typically with K = 2. Services need their own load shedding, because the sum of all quotas can exceed capacity, and they answer 503, not 429, when the server rather than the client is over its limit.

### What Interviewers Probe

Expect six questions. Which algorithm? Token buckets for rates with bursts and sliding window counters for quotas, knowing why fixed windows and logs fall short. How do gateways avoid racing on one counter? Increment-then-check or a Lua script, never a separate read and write. What if Redis is down? Fail open to local buckets for API limits, closed for security limits. A global limit across regions? Never synchronous: shared counts with a bounded overshoot, or split budgets. What does the client see? A 429 with `Retry-After` and allowance headers, a 503 for overload. A hot key? Token leasing and a cache of refused clients.

Strong candidates raise four more points unprompted: shadow mode for new rules; the weakness of per-IP limits, since carrier-grade NAT puts many users behind one IPv4 address while an IPv6 client can rotate through its whole /64, which is therefore the unit to limit; whether refused requests count, which a login limit wants and an API quota does not; and request cost, so that an expensive export cannot hide among cheap lookups. Interviewers care less about the algorithm you name than about a check that stays atomic, local and cheap at a million requests a second.

*Algorithms:* #138 Rate Limiter · #45 Design Hit Counter · #139 Consistent Hashing · #44 LRU Cache
