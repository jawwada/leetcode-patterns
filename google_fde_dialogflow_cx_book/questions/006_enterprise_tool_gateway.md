# Q006. Design a CX tool gateway for enterprise APIs

## Scope and success

Expose customer systems through a small set of approved capabilities. Assume different authentication schemes, inconsistent errors, and independent API rate limits. The gateway must preserve user authority, translate stable contracts, and make failures understandable to CX.

## Architecture and request path

CX calls authenticated webhooks or configured playbook tools. The gateway validates a registered operation, resolves the trusted user and tenant, checks policy, applies rate limits, and invokes a vendor adapter. It normalizes the result into a canonical schema. Each operation declares whether it is read-only, idempotent, or requires a proposal.

If the customer exposes MCP, an adapter can translate approved capabilities to that protocol. Keep protocol translation separate from authorization. An unrestricted pass-through tool would make it difficult to control destinations, arguments, and side effects.

## Data and contracts

The registry stores operation name, schema version, endpoint binding, required scopes, timeout, result schema, and side-effect class. Store credential references in a protected vault. Pass minimal data; a lookupOrder result should not include every CRM note or payment field.

## Failure, security, and scale

Use allowlisted egress, request size limits, argument validation, and per-adapter circuit breakers. Customer identity must not be replaced by the gateway's broad service identity. Apply concurrency caps to protect legacy APIs. Mutating calls use durable operation IDs and explicit recovery states.

## Trade-off and validation

A gateway creates a shared dependency but centralizes policy and observability. Start with clear module boundaries and split deployments when isolation warrants it. Contract-test adapters, evaluate tool selection, and inject timeout, unauthorized, malformed, and empty responses.

## Interview follow-up answered

**A tool schema changes during active conversations.** Version the operation and keep the old contract available during the session drain period. Register compatible schemas in the release manifest. Reject unsupported calls with a recoverable status; do not reinterpret old arguments under a new meaning.
