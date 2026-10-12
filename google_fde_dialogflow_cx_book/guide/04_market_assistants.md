# 4. Kalshi and Polymarket: conversational market assistants

## Use case and scope

The assistant helps a user discover a market, understand its resolution criteria, inspect a timestamped quote or order book, and check their own order status. An optional trading extension prepares a specific user-requested order for review and submission through an authorized execution service. The conversational model should explain data and clarify requests; it should not invent current prices, promise outcomes, or treat an ambiguous utterance as an order.

Kalshi and Polymarket are separate integrations. They use different market identifiers, authentication schemes, trading representations, and lifecycle rules. This chapter discusses the event-contract APIs documented by Kalshi and the Polymarket international documentation at `docs.polymarket.com`. Polymarket US has separate documentation and should be implemented as a distinct provider if it is the intended product. Eligibility and product availability must be checked against the provider's current requirements, rather than inferred from access to public data. [Kalshi documentation](https://docs.kalshi.com/welcome), [Polymarket documentation](https://docs.polymarket.com/).

:::diagram market_arch

## Every CX concept in the two integrations

| Concept | Kalshi example | Polymarket example |
| --- | --- | --- |
| Flow | `KalshiDiscovery`, `KalshiOrderReview`, `KalshiOrderTracking` | `PolyDiscovery`, `PolyOrderReview`, `PolyOrderTracking` |
| Page | `ChooseEvent`, `ChooseMarket`, `ShowQuote`, `ConfirmOrder` | `ChooseEvent`, `ChooseOutcome`, `ShowBook`, `ConfirmOrder` |
| Intent | Discover event, read rules, get quote, prepare order, check order | Discover event, select outcome, get book, prepare order, check order |
| Entity | Topic/date/outcome vocabulary; ticker resolved by backend | Topic/date/outcome vocabulary; token/asset ID resolved by backend |
| Parameter | Provider, market ticker, requested outcome, quantity, limit price, proposal ID | Provider, event/market reference, outcome asset ID, quantity, limit price, proposal ID |
| Form | Missing market, side/outcome, quantity, order constraints | Missing outcome, quantity, price, order constraints |
| Route | Valid market to quote; approved current proposal to execution | Valid asset to book; approved current proposal to signing/execution |
| Webhook | Tags dispatched to Kalshi metadata, quote, order, status adapters | Tags dispatched to Gamma/CLOB and order-status adapters |
| Playbook | Optional read-only market explorer and rules explainer | Optional read-only event explorer and rules explainer |
| Fulfillment | Present title, rules, timestamped quote, verified order state | Present outcome, timestamped book, verified order state |
| Event | Stale feed, no-match, unavailable API, uncertain submission | Disconnected stream, changed tick size, failed signing, uncertain submission |
| Session | Current selected market and proposal reference | Current selected outcome and proposal reference |

In both implementations, a flow is a provider-specific task subgraph, a page is a dialogue node, an entity is a typed extraction vocabulary, and a route is a guarded transition. The webhook is a provider adapter. A playbook resembles a market-exploration skill or agent recipe, but the execution service remains responsible for authorization and order correctness.

## Market discovery and resolution criteria

The user says "Show the temperature market for this Friday." Topic and date extraction are insufficient: the city, exact date/time zone, market threshold, and provider may be missing. Ask for those missing details and present exact titles and identifiers. Do not choose a vaguely similar market because its name appears first in search.

Maintain a mapping from user-facing choices to provider identifiers. Preserve the specific market rules and the version/time observed. A generative explanation can summarize the rules with a source reference, but the provider's published resolution criteria control the contract. Event similarity across providers does not establish identical payout conditions.

A playbook can perform discovery, compare descriptions, and ask clarifying questions. A flow can then collect exact order inputs. In another agent system, the discovery recipe would call read tools such as `search_markets` and `get_market_rules`; an explicit approval node would precede an execution tool.

## Kalshi adapter: isolate the API representation

Kalshi documents public market-data access, authenticated account operations, and streaming APIs. Its current key guide supports Ed25519 and RSA-PSS signing. Requests use the key ID, timestamp, and signature headers; the documented pre-sign text combines timestamp, HTTP method, and path without query parameters. Keep signing in a protected service, not in CX parameters or browser chat messages. [Market-data quick start](https://docs.kalshi.com/getting_started/quick_start_market_data), [API keys](https://docs.kalshi.com/getting_started/api_keys).

The current V2 event-order endpoint is `/trade-api/v2/portfolio/events/orders`, with a single-book bid/ask representation and fixed-point values. The adapter should translate a validated domain request into the currently supported provider representation. Do not reuse legacy YES/NO order payloads without checking the migration rules. Retain the application operation ID and provider client-order/order references for reconciliation. [Create Order V2](https://docs.kalshi.com/api-reference/orders/create-order-v2), [Order direction](https://docs.kalshi.com/getting_started/order_direction), [Fixed-point representation](https://docs.kalshi.com/getting_started/fixed_point_migration).

Quote normalization must reflect the provider's documented order-book shape. The book's binary-outcome representation differs from a generic two-column stock book; derive any complementary values only under the documented contract mechanics. Use decimal/fixed-point arithmetic and explicit units. [Order-book responses](https://docs.kalshi.com/getting_started/orderbook_responses).

## Polymarket adapter: separate discovery, quotes, and signing

Use the market-discovery API for event/market metadata and the CLOB interfaces for order-book and trading operations. Keep the selected outcome's exact asset identifier through the entire path. A display title is insufficient to sign or place an order. Use the current official SDK/API documentation for account and protocol selection. [Market data](https://docs.polymarket.com/market-data/overview).

Polymarket documents wallet ownership signing for L1 authentication and L2 credentials for private requests. An order also needs the appropriate authorized signature; possessing request credentials does not replace the order-signing requirement. Wallet type and signing domain matter. Keep private keys outside conversational state and model context. A user-controlled wallet flow can return a signing result through a dedicated application channel rather than through chat. [Wallets and authentication](https://docs.polymarket.com/trading/wallets-auth).

Before preparing an order, read current market constraints such as tick size and minimum size. The documented book/protocol version determines the signing domain; it should not be guessed from an old code sample. Use the official library or a carefully versioned adapter to validate rounding and amounts. [Place orders](https://docs.polymarket.com/trading/place-orders).

## Prices, probability language, and executable quotes

A market price can be described as an implied probability under the contract's mechanics; it is not a guaranteed real-world probability. The displayed price, last trade, best bid, best ask, and price available for a requested size are different values. Label which one is being reported.

For a synthetic book with a best bid of $0.41 and best ask of $0.45, the midpoint is $0.43. A request to buy may consume offers starting at $0.45 and could reach higher levels for a larger quantity. The assistant should not promise execution at the midpoint. Polymarket's price documentation explicitly distinguishes displayed prices from executable bid/ask values. [Prices and order book](https://docs.polymarket.com/concepts/prices-orderbook).

A normalized quote record can contain provider, market/outcome ID, bid, ask, depth summary, source timestamp, received timestamp, currency/unit, and freshness state. Keep price interpretation provider-specific. Avoid comparing two markets until their event definition, time horizon, and resolution criteria have been matched.

## A worked read-only conversation

| Turn | User/assistant | CX behavior | Backend behavior |
| --- | --- | --- | --- |
| 1 | User: "What's the price on that weather market?" | Missing provider/location/date; clarification page | No guessed lookup |
| 2 | Agent: "Which provider, city, and date?" | Collect required discovery inputs | None |
| 3 | User supplies the details | Discovery intent and entities | Search provider metadata |
| 4 | Agent presents exact candidate titles | `ChooseMarket` / `ChooseOutcome` | Preserve result-set-to-ID mapping |
| 5 | User selects a candidate | Route to quote page | Read current book and rules |
| 6 | Agent: "The synthetic best ask is $0.45, observed at 10:02:03 UTC. The resolution rule is shown below." | Fulfillment formats verified fields | Return timestamp and source reference |

If the feed is stale, say that the displayed value is stale and refresh or decline to quote. A fluent response without a freshness check is not a real-time market assistant.

## Optional user-approved order path

Collect the exact provider, market/outcome, requested direction, quantity, limit constraint, time-in-force, and account context. The domain service validates eligibility, funds/positions, provider rules, and current trading state. It generates a proposal showing the exact requested action and relevant cost/fee information from authoritative sources. The user reviews that proposal and explicitly approves it.

Execution binds to a proposal ID, input hash, expiry, and stable operation ID. A changed price constraint, outcome, quantity, or account invalidates approval. An expired proposal returns to review. The signing/execution service verifies the same inputs and records provider references. An HTTP success may establish order acceptance; it does not necessarily establish a complete fill.

The assistant distinguishes `SUBMITTING`, `ACCEPTED`, `PARTIALLY_FILLED`, `FILLED`, `CANCELED`, `REJECTED`, and `UNKNOWN` as application states, mapping provider semantics carefully. If a request times out after acceptance, reconcile using provider-supported identifiers and queries before attempting another placement. Repeated "yes" or webhook retries must not create distinct operations.

## Streaming and evaluation

Maintain market connections in provider-specific services, not one long-lived connection inside every webhook. Rebuild state on reconnect according to the provider's snapshot/delta or current stream semantics, detect sequence gaps where available, and mark data stale until recovery succeeds. Track provider rate limits centrally. [Kalshi WebSockets](https://docs.kalshi.com/getting_started/quick_start_websockets), [Polymarket real-time data](https://docs.polymarket.com/market-data/realtime-data).

Test ambiguous market names, wrong outcome mappings, stale quotes, changed constraints, rejected signatures, partial fills, repeated confirmation, and timeouts after provider acceptance. Measure identifier correctness, quote freshness, unauthorized operations blocked, duplicate placements, and truthful order-state reporting. First validate with fixtures and provider-supported test environments; do not use live money to test basic dialogue routing.

## What this case teaches

Market assistants make the difference between language and authority visible. CX understands and guides the user; provider adapters understand protocol details; domain services enforce exact actions and reconcile outcomes. The same division works when CX is replaced by a graph router, when webhooks are replaced by MCP tools, or when a playbook's guidance is packaged as a skill.
