# Q019. Design an inference gateway with fallback

## Scope and success

Provide a controlled interface to approved model configurations for CX backends. Establish region, quota, latency, schema, and budget requirements. Success is an evaluated response within policy, or a clear bounded failure that the conversation can recover from.

## Architecture and request path

CX calls a webhook or tool, which requests a named generation task. The gateway authenticates the service and user context, applies policy and admission control, resolves a model/prompt configuration, invokes inference, validates output, and returns a canonical result. It can select an evaluated fallback configuration for eligible transient failures.

Keep generation separate from side-effect execution. A model-generated action remains a proposal requiring domain authorization. Use end-to-end deadlines instead of independent unlimited retries at each layer.

## Data and contracts

Requests contain task type, permitted context, configuration version, deadline, and correlation ID. Responses contain status, output, usage, model/configuration, and validation result. Store prompt references and lineage under retention policy. Track quota state and circuit health without logging secrets.

## Failure, security, and scale

Throttle by tenant and task, with reserved capacity for essential paths. Bound tokens, queue wait, retry count, and fallback duration. A fallback must satisfy residency and quality requirements. Invalid structured output can trigger one bounded repair where evaluated, then an explicit failure.

## Trade-off and validation

A gateway centralizes governance but becomes a critical dependency. Deploy stateless instances with resilient configuration access and conservative cached policy. Test quota exhaustion, delayed inference, incompatible schemas, health oscillation, and region restrictions. Compare success, latency, and total cost including failed calls.

## Interview follow-up answered

**All approved models are unavailable.** Return a typed generation-unavailable result. CX can use a deterministic answer, source link, pending task, or handoff according to the journey. Sending data to an unapproved model or region is not an acceptable automatic availability strategy.
