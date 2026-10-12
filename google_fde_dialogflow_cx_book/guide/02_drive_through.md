# 2. Drive-through voice ordering: a complete CX design

## Customer journey and system boundary

A customer arrives at a lane, speaks an order, corrects items, hears a final summary, and submits the order to the restaurant's point-of-sale system. The assistant needs to handle background engines, accents, interruptions, incomplete orders, and unavailable items. The objective is an accurate confirmed order with a fast path to a staff member when automation cannot resolve the conversation.

The lane is the source of location and hardware context. A restaurant configuration service supplies store ID, menu revision, supported languages, and availability. The ordering service owns carts, prices, taxes, modifiers, and POS submission. CX owns conversational progress. In this design the customer pays using the restaurant's existing payment channel after ordering; payment-card collection is outside this voice conversation.

:::diagram drive_arch

## The concrete CX objects

| Concept | Concrete object in this case | Equivalent in another system |
| --- | --- | --- |
| Flow | `Order`, `MenuHelp`, `StaffHandoff` | Ordering subgraph, knowledge task, transfer workflow |
| Page | `CollectItem`, `ClarifyItem`, `CollectOptions`, `ReviewCart`, `SubmitOrder`, `OrderStatus` | Dialogue states or wizard steps |
| Intent | `order.add`, `order.remove`, `order.change`, `order.finish`, `confirm.yes`, `confirm.no`, `help.staff` | Semantic commands dispatched by an intent router |
| Entity | `menu_item`, `portion_size`, `modifier`, `drink_type`; a numeric quantity type | Enums, canonical catalog vocabulary, typed slots |
| Parameter | `item_id`, `quantity`, `size`, `cart_id`, `cart_revision`, `proposal_id` | Extracted fields plus state variables |
| Form | Item, quantity, and applicable options on `CollectOptions` | Required-input collection step |
| Route | Finish intent to review; confirmed valid proposal to submit | Guarded transitions in a state graph |
| Webhook | Tags `cart.add`, `cart.quote`, `order.commit`, `order.status` | RPC/tool adapter to ordering services |
| Fulfillment | Read back item, ask size, announce backend order status | Response/action handler |
| Event | No-input, no-match, webhook error | Timeout, classification failure, exception branch |
| Playbook | Optional `MenuExplainer` for nontransactional questions | Instruction recipe or knowledge subagent |
| Generator | Optional short reformulation of an approved description | Bounded prompt/model call |
| Session | Current lane conversation and selected cart reference | Ephemeral dialogue context |

Names in backticks are suggested configuration labels, not built-in CX objects. A playbook is optional: the ordering journey can be implemented with flows alone. It should be included only if the menu-help experience benefits from generative language.

## Flow: a bounded task area

The `Order` flow contains the order-building states. Its start page can welcome the customer and route an `order.add` intent to item collection. Flow-level reusable routes handle staff requests and selected interruptions. The `MenuHelp` flow can answer a question and return control to ordering. A flow has its own conversational structure; it is not a durable POS transaction.

In a general graph framework, the `Order` flow would be a subgraph with an entry point, nodes, edges, and inputs/outputs. In a backend workflow engine, order submission might be an activity inside a durable workflow. That durable workflow is a separate layer: CX's flow contains dialogue behavior, while the order service records business execution. [Flows](https://docs.cloud.google.com/dialogflow/cx/docs/concept/flow).

## Page: what the conversation is doing now

`CollectItem` means the agent is trying to identify an item. `CollectOptions` means an item has been selected but its required configuration may be incomplete. `ReviewCart` means the customer can inspect and change the current cart. `SubmitOrder` means an approved proposal is being committed or reconciled.

A page is like a dialogue-state node. It can define entry fulfillment, form parameters, routes, and event handlers. It is not a browser page, database row, or generic LLM prompt. The page should be named after its conversational responsibility. A customer can be in `ReviewCart` while the durable cart is still an editable draft. [Pages](https://docs.cloud.google.com/dialogflow/cx/docs/concept/page).

:::diagram drive_states

## Intent: the purpose of the utterance

For `order.add`, training phrases might include "add a cheeseburger," "can I get two fries," and "one medium cola." Annotate the appropriate spans with entity types. For `order.change`, examples include "make that large" and "no onions on the first burger." For `order.finish`, use utterances such as "that's everything" and "I'm ready to order."

Intent classification tells you the kind of request. It does not fully determine which line the customer means. "Make that large" needs current conversational context; "remove one" may require a clarification. The corresponding general-system component is a semantic command classifier. A model's function-call selection can serve a similar role, but it still needs schema validation and context resolution. [Intents](https://docs.cloud.google.com/dialogflow/cx/docs/concept/intent).

## Entity: normalized meaning, not an authoritative catalog

The `menu_item` entity can normalize "cheese burger" and a store-approved alias to `CHEESEBURGER`. A `portion_size` entity can normalize "regular" to the appropriate canonical value only if that meaning is unambiguous for the store. System numeric entities can help extract quantity. Do not train one enormous free-form phrase to encode every combination of item, size, and modifier.

An entity resembles a typed slot or controlled vocabulary. The ordering backend still validates that the canonical item exists in the current store's menu and supports the requested size or modifier. An extracted `LARGE` value is a candidate, not proof that a large version is available. Session-specific vocabulary can help with local names, but store configuration and prices remain server-owned. [Entities](https://docs.cloud.google.com/dialogflow/cx/docs/concept/entity).

## Parameters and forms: collecting a valid line item

Suppose the customer says "one cola." CX can identify a drink and quantity while the size is absent. On `CollectOptions`, a required `size` form parameter prompts "What size cola?" A completed form can trigger a route using `$page.params.status = "FINAL"`. The webhook then validates the requested line and updates the cart.

The key distinction is between **conversation variables** and **cart state**. `selected_item_id` is a conversational selection. The cart service records a line ID, normalized item ID, modifiers, quantity, pricing revision, and line revision. After adding a line, clear the selected-item parameters that should not carry into the next item. Same-named session parameters may fill form fields, so stale values can silently skip a question if you fail to reset them. [Parameters](https://docs.cloud.google.com/dialogflow/cx/docs/concept/parameter).

For modifiers, the backend returns applicable constraints: a burger may allow removal of onions, while a bottled drink has no size selection. CX uses those results to choose the next conversational step. In another framework this is schema-driven slot filling followed by a validation node.

## Routes: explicit choices and guards

On `ReviewCart`, an `order.change` route returns to an editing state. An `order.finish` route runs `cart.quote` and presents the authoritative summary. A `confirm.yes` route may transition to `SubmitOrder` only when the current proposal is valid. An unqualified "yes" elsewhere should not be interpreted as approval to submit an old proposal.

An illustrative condition for a proposal guard is:

```text
$session.params.proposal_id != null
AND $session.params.proposal_ready = true
```

The backend must enforce proposal revision, owner/lane binding, expiry, and allowed state again at commit. The condition is a conversational convenience, not a security boundary. In a state-machine library it corresponds to a guarded edge. In a web router, the route usually selects an HTTP handler by URL; CX's route selects conversational behavior by intent and/or condition.

## Fulfillment and webhook: connecting the conversation to the order

`cart.add` receives a cart reference and candidate item fields, resolves the current restaurant catalog, and returns the updated summary. `cart.quote` returns a proposal ID, cart revision, total, expiry, and human-readable readback. `order.commit` submits that same proposal. `order.status` reconciles uncertain submission outcomes.

A fulfillment can send a static prompt, assign parameters, and invoke a webhook. The FastAPI webhook endpoint dispatches the tag to these domain functions. An MCP server could expose `add_cart_item` and `submit_order` to an agent host, but CX would not thereby speak MCP. Both adapters can call the same cart service.

The durable commit contract should include `operation_id`, `proposal_id`, expected cart revision, and lane/cart binding. Never use an NLU confidence score as a substitute for proposal validation. Never compute a total by asking a language model to add menu text.

## Worked conversation and state trace

| Turn | Conversation | CX interpretation/state | Backend result |
| --- | --- | --- | --- |
| 1 | Customer: "Two cheeseburgers, no onions, and a cola." | `order.add`; item candidates and modifier extracted | Cart draft created; supported modifiers validated |
| 2 | Agent: "Two cheeseburgers without onions. What size cola?" | `CollectOptions`; required size missing | Cart stores burgers; drink candidate remains pending |
| 3 | Customer: "Medium. Actually make one burger plain." | Size collected; correction detected | Clarify what "plain" removes under the store's definition |
| 4 | Agent: "For one burger, remove all toppings and sauces?" | `ClarifyItem` with selected line | No change committed yet |
| 5 | Customer: "Yes, just meat, cheese, and bun." | Confirm line edit, then return to collection | Specific line updated; cart revision increases |
| 6 | Customer: "That's all." | `order.finish` to `ReviewCart` | Quote proposal for current revision |
| 7 | Agent: "Two cheeseburgers, one without onions and one with meat, cheese, and bun, plus a medium cola. Total $12.40. Place this order?" | Await scoped confirmation | Synthetic quote remains valid until expiry/change |
| 8 | Customer: "Yes." | `confirm.yes` with active proposal | Commit recorded once under operation ID |
| 9 | Agent: "Order 184 is accepted. Please continue to the next window." | Terminal success page | POS acceptance and order number verified |

Multiple extracted items require an application-level representation of line candidates; do not assume one scalar form parameter represents a complete cart. A list/composite representation and iterative clarification are design choices to verify with your CX configuration.

## Corrections invalidate prior confirmation

If the customer says "make the cola large" after the readback, the cart changes. The backend increments the cart revision, invalidates the proposal, and produces a new quote. CX clears its approval-related parameters and asks for confirmation again. A late `confirm.yes` associated with the old quote cannot submit the changed cart.

The state invariant is: **the exact cart revision the user reviewed must be the revision the service commits**. This is optimistic concurrency plus consent binding. It translates directly to a workflow-engine guard, a transaction precondition, or an agent tool policy, regardless of dialogue platform.

## Voice-specific behavior

End-of-utterance detection controls when the agent starts answering. Too aggressive an endpoint cuts off "a burger ... without onions"; too slow an endpoint makes every turn feel delayed. Barge-in allows the customer to interrupt playback, but an interruption must cancel obsolete audio and prevent the agent from acting on a stale confirmation context. Test with the actual microphone, speaker, acoustic echo, lane noise, and integration.

No-input handlers can first repeat a short prompt, then offer staff assistance. No-match handlers should ask a specific clarification such as "Was that a medium or large cola?" A staff-request intent should be reachable from important pages. CX handoff metadata can signal a transfer, but the lane/channel integration must execute it. [Advanced speech](https://docs.cloud.google.com/dialogflow/cx/docs/concept/advanced-speech), [Fulfillment and handoff](https://docs.cloud.google.com/dialogflow/cx/docs/concept/fulfillment).

An illustrative latency budget from the end of speech to first audible response is 250 ms endpointing, 200 ms recognition/NLU, 200 ms backend work, and 150 ms initial speech delivery: 800 ms total. These are planning assumptions, not CX guarantees. Measure the actual critical path and p95 by store and network condition. A brief acknowledgement can help for slower calls, but repeated filler does not repair slow business processing.

## Optional playbook: menu explanation

`MenuExplainer` can explain differences between items from approved menu content and return a selected item candidate. Instructions should require a clarification for unsupported substitutions, avoid inventing prices, and direct ordering actions to the flow. Suggested tools are `get_menu_item` and `list_available_options`, both read-only.

The equivalent skill might package "explain this restaurant's menu" instructions and catalog references. The playbook is the running task behavior; the skill is reusable guidance. Neither should authorize submitting an order. Allergy questions should use the restaurant's maintained information and staff escalation when that information is inadequate; fluent guesses would be a direct failure of the requested service.

## Timeout, duplicate request, and staff handoff

CX can automatically retry a webhook for transient failures. If POS accepted an order and the response was lost, a repeat must retrieve the same operation's outcome. Persist an operation before submission, reuse the operation reference, and reconcile with the POS using its supported lookup/idempotency behavior. If acceptance cannot be established, report "I'm checking whether the order was accepted" and hand the unresolved operation to staff. Do not say "failed" and immediately create a second order. [Webhook retries](https://docs.cloud.google.com/dialogflow/cx/docs/concept/webhook).

Staff handoff context should contain the current cart, unresolved line or operation, last question, and reason. Transfer the lane controls and stop agent playback so two speakers do not compete. The assistant should preserve the customer's work even when automation ends.

## Evaluation and delivery plan

Start with one store and a constrained menu. Replay conversations with substitutions, unavailable items, multi-item utterances, interruptions, repeated confirmations, and POS timeouts. Measure exact cart accuracy, correction success, false submission, duplicate submission, p95 response latency, and staff escalation with reason. Word error rate is a diagnostic; an accurately transcribed order can still be mapped to the wrong item.

Run shadow evaluation before allowing order commits, then a small supervised lane rollout. Compare submitted POS lines with reviewed proposals and staff corrections. Retain menu revision and agent version with each evaluation. Stop expanding the menu until the core correction and recovery paths work. In an interview, explain that adoption depends on reliable ordering and staff integration as much as language understanding.

## A concise interview answer

"I would model order capture and review in CX flows and pages, use intents and entities to interpret items and corrections, and collect missing options with page forms. Webhook fulfillment would call a FastAPI adapter to a server-owned cart and POS integration. The cart service would validate store-specific availability, prices, and revisions. A scoped confirmation would bind to a versioned proposal; submission would use a durable operation ID and reconciliation. I would test the voice integration under lane noise and interruptions, and measure exact cart correctness, duplicate submissions, latency, and staff handoff."
