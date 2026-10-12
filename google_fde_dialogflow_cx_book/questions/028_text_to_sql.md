# Q028. Design a CX text-to-SQL analyst

## Scope and success

Let verified business users ask questions over approved analytics data. Clarify metric definitions, row/column access, freshness, and query budgets. Success means the query answers the intended business question and the user is authorized for its data.

## Architecture and request path

CX collects ambiguous dimensions and time ranges. A backend resolves permitted semantic models and schemas, generates a query, parses it, validates allowed tables/functions and policy, then executes under a restricted identity with time/resource limits. A summarizer explains the result and explicit assumptions.

Use curated views and metric definitions to reduce ambiguity. Parameterize values rather than concatenating user input. If generation cannot produce a valid bounded query, CX asks for clarification or provides a supported alternative.

## Data and contracts

Store metric catalog version, authorized datasets, query AST or normalized SQL, parameter values, execution ID, result summary, and data timestamp. The response distinguishes empty results, denied access, query failure, and incomplete execution. Preserve query lineage for reproducibility.

## Failure, security, and scale

Read-only execution prevents modifications but does not prevent disclosure or expensive scans. Enforce row and column policy independently, deny unrestricted exports, limit result size, and estimate or cap cost. Treat schemas and result text as data. Avoid exposing sensitive values in prompts or logs.

## Trade-off and validation

Free-form SQL offers flexibility; a semantic layer with approved query templates offers stronger correctness and predictable cost. Evaluate against expected business results, not merely syntax. Test ambiguous revenue, time zones, joins, tenant isolation, and misleading nulls.

## Interview follow-up answered

**The query runs but uses the wrong revenue definition.** SQL validity did not establish semantic correctness. Ask for clarification or resolve through the approved metric catalog, regenerate, and show the selected definition. Add a regression case comparing gross, net, recognized, and refunded revenue.
