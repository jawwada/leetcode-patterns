# Q008. Design conversation and tool-call tracing

## Scope and success

Explain why a customer's task failed without exposing unnecessary private content. Trace CX, webhooks, retrieval, model calls, workers, and customer APIs. Success means an operator can locate the failed stage, affected release, and durable business outcome.

## Architecture and request path

The channel assigns a conversation correlation ID. Each turn connects to CX response identifiers and backend spans. The webhook adds tool, retrieval, and domain-service spans. Background workers link to the originating operation rather than pretending they remain inside a synchronous request.

An event pipeline stores structured telemetry and publishes service metrics. A query interface lets authorized operators move from conversation to turn, stage, source version, and operation. Keep a stable release manifest reference on every event.

## Data and contracts

Events include tenant, pseudonymous conversation ID, turn, component, start/end time, status, version, operation ID, and safe error category. Store model and source metadata without assuming every prompt must be retained. Distinguish domain failure, authorization denial, timeout, and invalid model output.

## Failure, security, and scale

Telemetry should not block customer transactions. Buffer or drop optional traces under pressure while retaining critical audit events durably. Redact before export, restrict operator access, and set retention by data class. Use sampling for ordinary successful traces and targeted capture for failures, subject to policy.

## Trade-off and validation

Full capture simplifies reproduction but increases privacy exposure and cost. Metadata plus controlled content sampling is often sufficient. Validate trace completeness with synthetic journeys, test redaction, and monitor missing spans and pipeline lag. Avoid high-cardinality customer identifiers as metric labels.

## Interview follow-up answered

**The webhook succeeds but the customer hears a failure.** Inspect the full chain: response serialization, CX route transition, channel delivery, and audio playback. A backend success span alone is incomplete. Join the authoritative operation state to channel outcome before deciding whether to retry or repair presentation.
