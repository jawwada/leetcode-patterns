# Q002. Design a customer support agent connected to CRM and order APIs

## Scope and success

Serve order status, policy questions, and case creation through chat. Existing CRM and order systems remain authoritative. Define which journeys require login, the allowed actions, response deadlines, and human support availability. Measure resolved tasks and accepted cases rather than conversation length alone.

## Architecture and request path

CX routes to Orders, Knowledge, Case Creation, or Escalation flows. The authenticated channel creates a server-side identity binding. A Cloud Run webhook maps allowlisted fulfillment tags to domain adapters. Order lookup checks ownership; policy questions use approved retrieval; case creation receives an explicit summary and confirmed contact preference.

Keep adapters separate from conversational wording. A CRM vendor change should affect the integration contract rather than every CX page. Return canonical results such as FOUND, ACTION_RECORDED, NEEDS_AUTHENTICATION, and TEMPORARILY_UNAVAILABLE.

## Data and contracts

Store conversation identity bindings, case operations, source-system references, and release metadata. A create-case operation has a stable operation ID and unique deduplication rule. CRM free text is untrusted evidence; do not let it select arbitrary backend tools. Minimize fields sent to the model.

## Failure, security, and scale

Put deadlines and concurrency limits on each adapter. If orders are unavailable, case creation can still record a request with an explicit verification-pending state. If CRM accepts a case but the response disappears, reconcile using the operation reference. Preserve customer authorization in both lookup and mutation paths.

## Trade-off and validation

Direct API integration is simple but exposes vendor instability. An adapter layer adds code while providing consistent errors, auditability, and contract tests. Test customer corrections, denied orders, duplicate case creation, and human transfer. Compare automated resolution with repeat-contact rates to detect superficially successful conversations.

## Interview follow-up answered

**The CRM only exposes a slow legacy interface. What changes?** Record the request durably, enqueue integration work, return a pending reference, and provide status through the channel. Avoid holding a synchronous CX webhook until the legacy task finishes.
