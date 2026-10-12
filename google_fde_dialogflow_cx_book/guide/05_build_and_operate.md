# 5. Building, testing, and operating the conversational layer

## Start with a workflow inventory

For each of the cases, list the user goal, required inputs, source of truth, expected response, allowed mutation, confirmation rule, and recovery behavior. The resulting inventory should be small enough to review with a product/domain expert. A drive-through order requires store-specific cart validation; Noctal submission requires ready media and durable job creation; a market order requires an exact provider contract and authorized execution.

Use the inventory to decide where a flow is sufficient and where a playbook adds useful flexibility. Do not add generative components simply to make a state machine look more "agentic." Conversely, do not enumerate every possible procedural question as a transaction route when grounded retrieval can answer it safely.

## A practical CX build sequence

1. Create the agent in the intended region and configure the primary language. Choose locations for backend, storage, logs, and generative dependencies deliberately.
2. Define canonical entity types for the domain values you actually need. Keep dynamic object authorization in the backend.
3. Create a small intent set with varied training phrases. Separate questions, selections, corrections, confirmations, and requests to act.
4. Create task flows and conversational pages. Assign page forms only where required inputs are missing.
5. Add scoped routes and conditions. Review handler precedence so global convenience routes do not bypass a review page.
6. Add fulfillment tags and a protected webhook endpoint. Keep tag dispatch explicit and input validation action-specific.
7. Add no-input, no-match, webhook-error, cancellation, and handoff paths as applicable to the case.
8. Add optional playbooks/data stores for exploratory questions. Give them narrow tools and examples covering empty/error results.
9. Run simulator conversations and backend contract checks. Verify both state transitions and business records.
10. Deploy a tested agent version/configuration with compatible webhook services and explicit rollback behavior.

Region and integration choices affect feature availability. They also constrain where data is processed, including dependencies outside CX. Agent location alone does not establish end-to-end residency. [Regions](https://docs.cloud.google.com/dialogflow/cx/docs/concept/region).

## Playbook tools, generators, and fallback are different

A playbook tool exposes a capability to generative task behavior. A generator is a configured model call in fulfillment. Generative fallback can help recover from unhandled input under its configured behavior. A data store supports grounded information retrieval. None replaces a transaction service, and none makes an external system's facts automatically fresh.

CX supports several playbook tool types with distinct execution paths. Function tools can require the calling client to execute a returned tool call and send back the result, while other configured tools use their own invocation mechanisms. Confirm the integration path instead of assuming all tools execute in the same place. [Playbook tools](https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook/tool), [Generators](https://docs.cloud.google.com/dialogflow/cx/docs/concept/generators), [Generative fallback](https://docs.cloud.google.com/dialogflow/cx/docs/concept/generative-fallback).

For these cases, let generative components explain approved menu information, Noctal submission instructions, or market rules. Return structured selections to explicit flows. Validate tool outputs, cap response size, and define behavior when an API returns empty data. Some generative features are excluded from the CX SLA; verify the feature's current documentation when setting production expectations.

## Security: two identities and two checks

The CX-to-webhook caller identity proves that the configured service can call FastAPI. It does not prove that the chat user owns an asset, a job, a cart, or a trading account. The server-bound session resolves the user context; domain services enforce object access and action permission.

For authenticated Noctal or market users, keep the BFF's session binding keyed by the full CX session resource and configured environment, with expiry and tenant/user association. Avoid accepting arbitrary session IDs from an unauthenticated browser. For the drive-through lane, bind the lane hardware/store context to the cart rather than trusting a spoken store ID.

Do not store credentials, wallet keys, unrestricted signed URLs, or access tokens in dialogue parameters, prompts, or logs. Retrieval and search must filter permitted content before presentation. Tool responses and uploaded media are untrusted data even when they contain instructions. [CX access control](https://docs.cloud.google.com/dialogflow/cx/docs/concept/access-control).

## Durable state and consent

| State | Store | Why |
| --- | --- | --- |
| Active page and temporary extracted fields | CX session | Conversation continuity |
| Authenticated user/lane binding | Application session service | Trusted context |
| Cart, selected asset version, job inputs | Domain database | Durable business record |
| Proposal and approval record | Operation/proposal store | Exact reviewed action and expiry |
| Worker stage and output references | Job/workflow store | Recovery and progress |
| Provider/POS submission reference | Operation store | Duplicate prevention and reconciliation |

CX sessions have bounded lifetimes. The application should resume from durable business records and rebuild conversational context when needed. Reconstructing a page and parameters does not imply that all prior runtime state is restored. [Sessions](https://docs.cloud.google.com/dialogflow/cx/docs/concept/session).

An approval should bind the actor, action type, target, input version/hash, limits, and expiry. Store it where the execution service can verify it. The conversational phrase "yes" is evidence only in context. Cancellation and changes require explicit transitions; they should not leave an old approval usable.

## Retry handling and the unknown outcome

The central failure pattern is "the service performed work, but the caller did not receive the answer." The order was accepted, the media job was enqueued, or the market order was placed. A retry must use the same durable operation reference.

Record an operation before the external boundary. Use the provider's idempotency contract if one exists. After an ambiguous timeout, query the same operation/provider reference and reconcile. If the external system cannot provide reliable reconciliation, surface `UNKNOWN` and an operator path. A database transaction cannot atomically commit your database and an arbitrary remote API unless a supported protocol covers both.

Keep read retries bounded and back off. Keep mutation retries tied to durable state. Deduplicate at the domain service even if a particular channel usually retries only once; users, browsers, workers, and proxies can also repeat requests.

## A regression set based on the named cases

| Case | Conversation variation | Required outcome |
| --- | --- | --- |
| Drive-through | "Make one burger plain" after a multi-item order | Clarify/select correct line; do not change both |
| Drive-through | Add item after final readback | Invalidate old quote and ask for new confirmation |
| Drive-through | POS accepts, webhook response times out | Reconcile same operation; no second order |
| Noctal | "How do I submit?" | Explain; create no job |
| Noctal | "The second video" after search results | Resolve against presented result-set version |
| Noctal | Upload incomplete | Reject job start until finalized/ready |
| Noctal | Another user's job ID | Nondisclosing denial; no metadata leak |
| Noctal | Decline follow-up questions | End/review without automatic follow-up work |
| Market assistant | Similar title, different resolution rule | Ask/confirm exact market rather than substitute |
| Market assistant | Stale quote or changed tick size | Refresh/revalidate before proposal/execution |
| Market assistant | Accepted but partially filled order | Report partial fill truthfully |

Built-in CX test cases can check dialogue expectations, but supplement them with backend assertions. A correct page transition with two duplicate business records is a failed test. Use separate checks for conversation, authorization, domain invariants, and quality of generated explanations. [Test cases](https://docs.cloud.google.com/dialogflow/cx/docs/concept/test-case).

## Observability and release

Trace the end-to-end path with channel request ID, CX response ID, session reference, fulfillment tag, domain operation ID, and backend/provider status. Limit sensitive content in telemetry and apply redaction independently to channel, CX, FastAPI, worker, and provider-adapter logs. CX security settings do not automatically redact every application log. [Security settings](https://docs.cloud.google.com/dialogflow/cx/docs/concept/security-settings).

Version the agent/configuration, webhook contract, domain schemas, menu/docs/index revisions, and optional model/prompt configuration in a release manifest. Use environment-specific webhooks and compatibility rules. Plan for active sessions during releases: incompatible page/parameter changes can require a controlled restart or migration. Rollback must include the backend contract, not only the conversational graph. [Versions and environments](https://docs.cloud.google.com/dialogflow/cx/docs/concept/version).

Monitor business success and incorrect action rates before aggregate containment. Track p95 latency, stale-data rate, webhook errors, no-match/no-input, unknown operations, duplicate attempts, and handoff reasons. Price planning should use current usage categories and model/region choices; do not hardcode a universal cost per conversation. [Quotas](https://docs.cloud.google.com/dialogflow/quotas), [Pricing](https://cloud.google.com/products/conversational-agents/pricing).

## Interview explanation framework

Begin with one user journey and its invariant. Draw the channel, CX, webhook adapter, domain services, and durable store. Walk through one utterance: intent, entities, form, route, fulfillment, and backend result. Explain the optional playbook and why its authority is bounded. Then walk through a correction and an ambiguous timeout. Finish with the evaluation method and evidence you would use to decide whether to deploy.

For Noctal, keep the boundary clear: the supplied project establishes CX and FastAPI in the conversational layer. For unverified internals, describe the design you would propose. That distinction lets you answer deeply without inventing experience.
